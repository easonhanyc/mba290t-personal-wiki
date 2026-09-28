"""The harness: everything around the model and the retrieval tool.

  ask   question -> retrieve -> research rules + numbered passages + question -> Gemma
        -> citation check -> answer + sources (no persona, no chat history)
  chat  persona + recent conversation (+ wiki notes only when the router says the turn needs them)
        -> Gemma -> reply, with [N#] tags checked against the notes that were supplied
  search is not here: it is the retrieval tool on its own (retrieval.Index.search), no model at all.

Every ask and chat turn is saved under runs/ with the exact messages sent to the model.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from . import config, retrieval, vault
from .llm import get_model

INSUFFICIENT = "insufficient evidence"


def tokens_estimate(text: str) -> int:
    return int(len(text) / 3.6) + 1  # English prose and Markdown average ~3.6-4 characters per Gemma token


def instructions(name: str) -> str:
    return (config.load().path("instructions") / name).read_text(encoding="utf-8")


def _runs() -> Path:
    d = config.load().path("runs")
    d.mkdir(parents=True, exist_ok=True)
    return d


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S-%f")[:-3]


def select_within(hits: list[retrieval.Hit], budget: int) -> list[retrieval.Hit]:
    chosen, used = [], 0
    for h in hits:
        cost = tokens_estimate(h.chunk.text) + 25
        if chosen and used + cost > budget:
            break
        chosen.append(h)
        used += cost
    return chosen


def passage_block(hits: list[retrieval.Hit], tag: str) -> str:
    out = []
    for i, h in enumerate(hits, 1):
        c = h.chunk
        kind = "original source" if c.kind == "source" else "wiki note (reviewed summary)"
        out.append(f"[{tag}{i}] {c.path} lines {c.line_start}-{c.line_end} | {c.section} | {kind}\n{c.text}")
    return "\n\n".join(out)


def check_citations(answer: str, hits: list[retrieval.Hit], tag: str = "S") -> dict:
    """Mechanical checks a reader would do first. Not proof of support: the evidence card says so."""
    cited = [int(n) for n in re.findall(rf"{tag}(\d+)", " ".join(re.findall(r"\[([^\]]+)\]", answer)))]
    unknown = sorted({n for n in cited if not 1 <= n <= len(hits)})
    insufficient = answer.strip().lower().startswith(INSUFFICIENT)
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", answer) if len(s.strip()) > 25]
    uncited = [s for s in sentences if not re.search(rf"\[{tag}\d+", s) and not s.lower().startswith(INSUFFICIENT)]
    unsupported_numbers = []
    for s in sentences:
        ids = [int(n) for n in re.findall(rf"{tag}(\d+)", s) if 1 <= int(n) <= len(hits)]
        if not ids:
            continue
        evidence = " ".join(hits[i - 1].chunk.text for i in ids).replace(",", "")
        clean = re.sub(rf"\[[^\]]*\]", "", s)
        for num in re.findall(r"\d[\d,]*(?:\.\d+)?%?", clean):
            if num.replace(",", "").rstrip("%") not in evidence:
                unsupported_numbers.append({"sentence": s, "number": num})
    if insufficient:
        status = "insufficient-evidence"
    elif not cited:
        status = "no-citations"
    elif unknown or unsupported_numbers:
        status = "citation-problems"
    elif uncited:
        status = "some-sentences-uncited"
    else:
        status = "ok"
    return {"status": status, "cited": sorted(set(cited)), "unknown_ids": unknown,
            "uncited_sentences": uncited, "numbers_not_in_cited_passages": unsupported_numbers,
            "insufficient_evidence": insufficient}


# --------------------------------------------------------------------------- ask

@dataclass
class AskResult:
    question: str
    answer: str
    mode: str
    model: str
    passages: list[retrieval.Hit]
    method: str
    checks: dict
    timings: dict
    messages: list[dict]
    run_file: str = ""
    model_called: bool = True


def ask(question: str, mode: str = "local", model=None, index: retrieval.Index | None = None,
        k: int | None = None, save: bool = True) -> AskResult:
    """Standalone factual answer. Deliberately takes no history argument: ask cannot see chat."""
    settings = config.load()
    cfg = settings.section("ask")
    model = model or get_model(mode)
    model.require()
    index = index or retrieval.Index(settings)
    t0 = time.perf_counter()
    hits = index.search(question, k=k)
    t_retrieval = time.perf_counter() - t0
    passages = select_within(hits, cfg["evidence_token_budget"])
    messages = [
        {"role": "system", "content": instructions("research-rules.md")},
        {"role": "user", "content": f"EVIDENCE PASSAGES:\n\n{passage_block(passages, 'S')}\n\nQUESTION: {question}"},
    ]
    if not passages:
        answer = "Insufficient evidence: the retrieval tool found no passages related to this question."
        result = AskResult(question, answer, model.mode, model.model_id, [], index.last_method,
                           check_citations(answer, []), {"retrieval_s": round(t_retrieval, 2), "total_s": round(t_retrieval, 2)},
                           messages, model_called=False)
    else:
        reply = model.chat(messages, max_tokens=cfg["max_answer_tokens"], temperature=cfg["temperature"])
        timings = {"retrieval_s": round(t_retrieval, 2), "model_s": round(reply.seconds, 2),
                   "total_s": round(time.perf_counter() - t0, 2), **{f"llama_{k}": v for k, v in reply.timings.items()}}
        result = AskResult(question, reply.text, reply.mode, reply.model, passages, index.last_method,
                           check_citations(reply.text, passages, "S"), timings, messages)
    if save:
        result.run_file = config.rel(save_ask(result))
    return result


def hit_record(h: retrieval.Hit, tag: str) -> dict:
    c = h.chunk
    return {"id": tag, "kind": c.kind, "path": c.path, "lines": [c.line_start, c.line_end], "section": c.section,
            "fused_score": round(h.score, 5), "bm25_rank": h.bm25_rank, "vector_rank": h.vector_rank,
            "cosine": None if h.cosine is None else round(h.cosine, 4), "text": c.text}


def save_ask(r: AskResult) -> Path:
    path = _runs() / f"ask-{_stamp()}.json"
    path.write_text(json.dumps({
        "command": "ask", "time": datetime.now().isoformat(timespec="seconds"), "execution": r.mode,
        "model": r.model, "question": r.question, "retrieval_method": r.method,
        "passages": [hit_record(h, f"S{i}") for i, h in enumerate(r.passages, 1)],
        "messages_sent_to_model": r.messages, "model_called": r.model_called,
        "answer": r.answer, "citation_check": r.checks, "timings": r.timings,
    }, indent=2, ensure_ascii=False))
    return path


# --------------------------------------------------------------------------- chat

CAPABILITIES = """- Talk things through with you: brainstorm, plan, draft and rewrite. I remember the recent turns of
  this conversation only; it resets when you quit or type /reset.
- Look things up in your wiki (your projects, work, school and MBA 290T) when a question needs your notes,
  and tag those claims [N1], [N2]. Type /notes <topic> to force a lookup.
- Chat commands: /notes <topic>, /sources (show the notes behind my last reply), /save (write my last reply
  to drafts/), /reset, /help, /exit.
- Other commands, run from the terminal: `wiki ask "question"` gives a neutral, cited factual answer from
  the sources; `wiki search "words"` shows the original passages; `wiki ingest <path>` adds a source;
  `wiki check` checks the vault's links and names.
- I cannot browse the internet, read files that were never ingested, remember earlier chat sessions, send
  messages or take actions outside this terminal, or know facts about you that are not in the notes or
  this conversation."""

_CASUAL = re.compile(
    r"^\s*(hi|hello|hey|thanks|thank you|ok|okay|cool|great|good (morning|afternoon|evening))\b"
    r"|what can (you|we|i) do|what can you help|help me with\?|who are you|what are you|how do(es)? (this|you) work"
    r"|\b(make|keep) (it|that|this) (shorter|longer|simpler|punchier|more \w+)|\bshorter\b|\bshorten\b"
    r"|\b(rephrase|rewrite|reword|simplify|condense|summari[sz]e) (it|that|this)\b|\bturn (it|that|this) into\b",
    re.I)
_DRAFT = re.compile(r"^\s*(please\s+)?(help me\s+)?(draft|write|plan|brainstorm|outline|suggest|give me|list|create|make)\b", re.I)
_PERSONAL = re.compile(
    r"\b(my|mine|i|i've|i'm|me)\b.*\b(did|do|was|were|built|build|made|worked|work|score|scored|result|results|role|"
    r"title|job|project|projects|course|class|assignment|assignments|deadline|due|grade|learn|learned|use|used|chose|choose)\b"
    r"|\b(my notes|my wiki|according to|in my|from my|what did i|when did i|where did i|which of my)\b", re.I)
_FOLLOWUP = re.compile(r"\b(it|that|this|those|they|them|its|their)\b", re.I)

ROUTER_PROMPT = """Decide whether the user's latest message needs facts from their personal wiki (their projects,
jobs, school, courses, results, dates). Casual talk, opinions, general knowledge, drafting or editing text
that is already in the conversation do NOT need the wiki. Return JSON {"needs_notes": true|false,
"query": "search words if needed, else empty"}."""
ROUTER_SCHEMA = {"type": "object", "required": ["needs_notes", "query"],
                 "properties": {"needs_notes": {"type": "boolean"}, "query": {"type": "string"}}}


@dataclass
class Route:
    retrieve: bool
    query: str
    reason: str
    model_used: bool = False


@dataclass
class ChatTurn:
    user: str
    reply: str
    route: Route
    notes: list[retrieval.Hit] = field(default_factory=list)
    checks: dict = field(default_factory=dict)
    timings: dict = field(default_factory=dict)


class ChatSession:
    def __init__(self, mode: str = "local", model=None, index: retrieval.Index | None = None):
        self.settings = config.load()
        self.cfg = self.settings.section("chat")
        self.model = model or get_model(mode)
        self.index = index
        self.history: list[dict] = []
        self.last: ChatTurn | None = None
        self.system = instructions("persona.md").replace("{capabilities}", CAPABILITIES)
        self.titles = [n.title for n in vault.all_notes(self.settings)]
        self.log_path = _runs() / f"chat-{_stamp()}.jsonl"
        self.turns = 0

    def _index(self) -> retrieval.Index:
        if self.index is None:
            self.index = retrieval.Index(self.settings)
        return self.index

    # Title words too common to mean the user named that note ("internship" is not "TikTok Internship").
    GENERIC = {"project", "learning", "course", "notes", "internship", "program", "automation", "setting", "target",
               "adoption", "analysis", "trends", "racing", "screening", "network", "series", "access", "board", "rides",
               "tracker", "secure", "networking", "search", "agent", "custom", "services", "capital", "university",
               "syllabus", "sustainability", "hazardous", "action", "data", "deep", "time", "amazon", "web", "with"}

    def mentions_wiki_subject(self, text: str) -> str | None:
        low = text.lower()
        for t in self.titles:
            if t.lower() in low:
                return t
            words = [w for w in re.findall(r"[a-z0-9][a-z0-9.-]+", t.lower()) if len(w) >= 5 and w not in self.GENERIC]
            if any(re.search(rf"\b{re.escape(w)}\b", low) for w in words):
                return t
        return None

    def route(self, message: str) -> Route:
        subject = self.mentions_wiki_subject(message)
        if _CASUAL.search(message) and not subject:
            return Route(False, "", "casual, capability or edit request: answered from the conversation")
        if _DRAFT.search(message) and not subject and not _PERSONAL.search(message.split(":")[0]):
            return Route(False, "", "drafting/planning from what you said: no personal facts needed")
        if subject or _PERSONAL.search(message):
            query = message
            if _FOLLOWUP.search(message) and len(message.split()) < 12 and self.history:
                prev = next((m["content"] for m in reversed(self.history) if m["role"] == "user"), "")
                query = f"{prev} {message}"
            why = f"mentions wiki subject '{subject}'" if subject else "asks about your own facts"
            return Route(True, query, why)
        # Ambiguous: ask the model to classify (cheap, JSON only).
        convo = "\n".join(f"{m['role']}: {m['content'][:300]}" for m in self.history[-4:])
        reply = self.model.chat([{"role": "system", "content": ROUTER_PROMPT},
                                 {"role": "user", "content": f"CONVERSATION SO FAR:\n{convo or '(none)'}\n\nLATEST MESSAGE: {message}"}],
                                max_tokens=60, temperature=0.0, schema=ROUTER_SCHEMA)
        try:
            data = json.loads(reply.text)
            needs, query = bool(data.get("needs_notes")), str(data.get("query") or message)
        except (json.JSONDecodeError, AttributeError):
            needs, query = False, ""
        return Route(needs, query if needs else "", "model router decided " + ("notes needed" if needs else "no notes needed"), True)

    def trimmed_history(self) -> list[dict]:
        budget, out, used = self.cfg["history_token_budget"], [], 0
        for m in reversed(self.history):
            cost = tokens_estimate(m["content"]) + 4
            if out and used + cost > budget:
                break
            out.append(m)
            used += cost
        return list(reversed(out))

    def turn(self, message: str, force_query: str | None = None) -> ChatTurn:
        self.model.require()
        t0 = time.perf_counter()
        route = Route(True, force_query, "forced by /notes") if force_query else self.route(message)
        notes: list[retrieval.Hit] = []
        user_content = message
        if route.retrieve:
            hits = self._index().search(route.query, k=self.cfg["notes_top_k"])
            notes = select_within(hits, self.cfg["notes_token_budget"])
            if notes:
                user_content = (f"{message}\n\n---\nNOTES FROM THE WIKI (retrieved by the harness for this turn; tag "
                                f"claims that use them as [N1], [N2]...):\n\n{passage_block(notes, 'N')}")
        messages = [{"role": "system", "content": self.system}, *self.trimmed_history(),
                    {"role": "user", "content": user_content}]
        reply = self.model.chat(messages, max_tokens=self.cfg["max_answer_tokens"], temperature=self.cfg["temperature"])
        checks = check_citations(reply.text, notes, "N") if notes else {"status": "no notes used"}
        # History keeps what was said, not the retrieved notes, so old evidence does not crowd the context.
        self.history += [{"role": "user", "content": message}, {"role": "assistant", "content": reply.text}]
        self.turns += 1
        turn = ChatTurn(message, reply.text, route, notes, checks,
                        {"total_s": round(time.perf_counter() - t0, 2), "model_s": round(reply.seconds, 2),
                         **{f"llama_{k}": v for k, v in reply.timings.items()}})
        self.last = turn
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"command": "chat", "turn": self.turns, "time": datetime.now().isoformat(timespec="seconds"),
                                "execution": reply.mode, "model": reply.model, "user": message,
                                "route": route.__dict__, "notes": [hit_record(h, f"N{i}") for i, h in enumerate(notes, 1)],
                                "messages_sent_to_model": messages, "reply": reply.text, "citation_check": checks,
                                "timings": turn.timings}, ensure_ascii=False) + "\n")
        return turn

    def reset(self) -> None:
        self.history.clear()
        self.last = None

    def save_last(self) -> Path | None:
        """Explicit save: drafts are generated text, kept apart from the evidence in vault/raw."""
        if not self.last:
            return None
        drafts = self.settings.path("drafts")
        drafts.mkdir(parents=True, exist_ok=True)
        slug = re.sub(r"[^a-z0-9]+", "-", self.last.user.lower())[:40].strip("-") or "draft"
        path = drafts / f"{datetime.now():%Y-%m-%d-%H%M} {slug}.md"
        path.write_text(f"---\ntype: draft (generated by chat, not a source)\nprompt: {json.dumps(self.last.user)}\n"
                        f"model: {self.model.model_id} ({self.model.mode})\n---\n\n{self.last.reply}\n", encoding="utf-8")
        return path
