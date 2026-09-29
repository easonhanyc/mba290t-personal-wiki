"""Ingestion: original sources -> wiki notes, source catalog, index page and retrieval index.

Per source file (skipped when its sha256 is unchanged):
  1. parse it into sections (textparse)
  2. small source: local Gemma reads it whole; large source: Gemma extracts facts part by part
  3. Gemma writes the note as JSON (title, folder, summary, facts with section, concepts, related)
  4. the harness validates it: facts whose numbers are not in the source are dropped, sections are
     matched to real headings, the title is cleaned and checked against the naming rules
  5. the note is merged into an existing note on the same subject, or created at a readable path
Then: concept notes for ideas shared by 2+ sources, a link pass, index.md, Source Catalog.md, and
the retrieval index. Structured drafts live in data/notes.json; the vault holds only Markdown.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import re
import shutil
import time
from datetime import datetime
from pathlib import Path

from . import config, retrieval, vault
from .llm import ModelError, get_model, parse_json
from .textparse import SUPPORTED, Document, Section, parse_file, render

FACT = {"type": "object", "properties": {"fact": {"type": "string"}, "section": {"type": "string"}},
        "required": ["fact", "section"]}
LINKED = {"type": "object", "properties": {"title": {"type": "string"}, "why": {"type": "string"}},
          "required": ["title", "why"]}
SCHEMA_FACTS = {"type": "object", "required": ["facts"],
                "properties": {"facts": {"type": "array", "items": FACT, "maxItems": 8}}}
SCHEMA_NOTE = {
    "type": "object",
    "required": ["title", "folder", "summary", "key_facts", "concepts", "related"],
    "properties": {
        "title": {"type": "string"},
        "folder": {"type": "string", "enum": vault.FOLDERS},
        "summary": {"type": "string"},
        "key_facts": {"type": "array", "items": FACT, "maxItems": 12},
        "concepts": {"type": "array", "maxItems": 4, "items": {
            "type": "object", "properties": {"name": {"type": "string"}, "why": {"type": "string"}},
            "required": ["name", "why"]}},
        "related": {"type": "array", "items": LINKED, "maxItems": 5},
    },
}
SCHEMA_CONCEPT = {
    "type": "object", "required": ["summary", "key_facts"],
    "properties": {
        "summary": {"type": "string"},
        "key_facts": {"type": "array", "maxItems": 8, "items": {
            "type": "object", "properties": {"fact": {"type": "string"}, "passage": {"type": "string"}},
            "required": ["fact", "passage"]}},
    },
}
SCHEMA_LINKS = {"type": "object", "required": ["related"],
                "properties": {"related": {"type": "array", "items": LINKED, "maxItems": 5}}}


# --------------------------------------------------------------------------- stores

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_id(rel: str, sha: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", rel.removeprefix("raw/").rsplit(".", 1)[0].lower()).strip("-")
    return f"{slug}-{sha[:8]}"


def origin_for(settings: config.Settings, rel: str) -> dict:
    for o in settings.origins():
        if rel.startswith(o["prefix"]):
            out = {k: v for k, v in o.items() if k != "prefix"}
            if o.get("repo") and o.get("commit"):
                sub = rel[len(o["prefix"]):] if o["prefix"].endswith("/") else Path(rel).name
                out["url"] = f"{o['repo']}/blob/{o['commit']}/{o.get('repo_dir', '')}{sub}"
            return out
    return {"collection": "Imported local file"}


class Store:
    """data/catalog.json (sources -> notes) and data/notes.json (structured note drafts)."""

    def __init__(self, settings: config.Settings):
        self.dir = settings.path("data")
        self.dir.mkdir(parents=True, exist_ok=True)
        self.catalog = self._load("catalog.json", {"sources": {}, "notes": {}})
        self.notes = self._load("notes.json", {})

    def _load(self, name: str, default):
        p = self.dir / name
        return json.loads(p.read_text()) if p.exists() else default

    def save(self) -> None:
        (self.dir / "catalog.json").write_text(json.dumps(self.catalog, indent=2, ensure_ascii=False))
        (self.dir / "notes.json").write_text(json.dumps(self.notes, indent=2, ensure_ascii=False))


# --------------------------------------------------------------------------- helpers

_NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")


def numbers_in(text: str) -> set[str]:
    return {n.replace(",", "").rstrip(".") for n in _NUM.findall(text)}


def match_section(name: str, doc: Document) -> Section | None:
    wanted = name.strip().lstrip("#").strip().lower()
    by_label = {s.label.lower(): s for s in doc.sections}
    by_head = {s.heading.lower(): s for s in doc.sections if s.heading}
    if wanted in by_label:
        return by_label[wanted]
    if wanted in by_head:
        return by_head[wanted]
    last = wanted.split(" › ")[-1]
    if last in by_head:
        return by_head[last]
    close = difflib.get_close_matches(wanted, list(by_label) + list(by_head), n=1, cutoff=0.75)
    if close:
        return by_label.get(close[0]) or by_head.get(close[0])
    return None


def parts_of(doc: Document, part_words: int) -> list[list[Section]]:
    parts, cur, words = [], [], 0
    for s in doc.sections:
        if cur and words + s.words > part_words:
            parts.append(cur)
            cur, words = [], 0
        if s.words > part_words:  # one huge section: split its blocks
            chunk, w = Section(path=s.path, kind=s.kind), 0
            for b in s.blocks:
                if chunk.blocks and w + len(b.text.split()) > part_words:
                    parts.append([chunk])
                    chunk, w = Section(path=s.path, kind=s.kind), 0
                chunk.blocks.append(b)
                w += len(b.text.split())
            if chunk.blocks:
                cur, words = [chunk], w
            continue
        cur.append(s)
        words += s.words
    if cur:
        parts.append(cur)
    return parts


def discover(paths: list[str] | None, into: str, settings: config.Settings, log) -> list[Path]:
    raw = settings.path("raw")
    targets = [Path(p).expanduser() for p in paths] if paths else [raw]
    files: list[Path] = []
    for t in targets:
        t = t if t.is_absolute() else (Path.cwd() / t)
        if not t.exists():
            raise FileNotFoundError(f"No such file or folder: {t}")
        found = [p for p in sorted(t.rglob("*"))] if t.is_dir() else [t]
        for p in found:
            if not p.is_file() or p.name.startswith(".") or p.suffix.lower() not in SUPPORTED:
                continue
            p = p.resolve()
            if raw.resolve() not in p.parents:
                dest = raw / into / p.name
                if dest.exists() and sha256_file(dest) != sha256_file(p):
                    raise FileExistsError(f"{dest} already exists with different content; not overwriting an original.")
                if not dest.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(p, dest)
                    log(f"  copied {p.name} -> {config.rel(dest)} (byte-for-byte; sha256 {sha256_file(dest)[:12]})")
                else:
                    log(f"  {p.name} is already in {config.rel(dest)} (identical)")
                p = dest.resolve()
            files.append(p)
    return files


# --------------------------------------------------------------------------- the ingester

class Ingester:
    def __init__(self, model=None, log=print, dry_run: bool = False):
        self.settings = config.load()
        self.vault = self.settings.vault
        self.model = model or get_model("local")
        self.log = log
        self.dry_run = dry_run
        self.store = Store(self.settings)
        self.rules = (self.settings.path("instructions") / "ingest-rules.md").read_text()
        self.cfg = self.settings.section("ingest")
        self.calls: list[dict] = []
        self.changed: set[str] = set()
        self.dropped: list[dict] = []
        self.failures: list[dict] = []

    # ---- model calls
    def _call(self, stage: str, user: str, schema: dict, max_tokens: int, source: str) -> dict:
        messages = [{"role": "system", "content": self.rules}, {"role": "user", "content": user}]
        budget = max_tokens
        for attempt in (1, 2):
            reply = self.model.chat(messages, max_tokens=budget, temperature=0.1, schema=schema)
            t = reply.timings
            self.calls.append({"stage": stage, "source": source, "seconds": round(reply.seconds, 1),
                               "prompt_tokens": t.get("prompt_n"), "output_tokens": t.get("predicted_n"),
                               "finish": reply.finish_reason, "attempt": attempt})
            try:
                return parse_json(reply.text)
            except ModelError as e:
                cut = reply.finish_reason == "length"
                self.log(f"    ! {stage}: {'output hit the token limit' if cut else 'invalid JSON'} "
                         f"(attempt {attempt}): {str(e)[:120]}")
                if cut:
                    budget = int(budget * 1.7)  # retry with room to finish the object
        raise ModelError(f"{stage} for {source}: model output was not valid JSON twice")

    def existing_titles(self) -> list[str]:
        out = []
        for rel, d in sorted(self.store.notes.items()):
            out.append(f"- {d['title']} — {d.get('summary', '')[:140]}")
        return out

    # ---- per source
    def read_source(self, path: Path, rel: str, doc: Document) -> dict:
        existing = "\n".join(self.existing_titles()) or "(none yet)"
        if doc.words <= self.cfg["direct_word_limit"]:
            material = f"SOURCE TEXT:\n{render(doc, short=True)}"
        else:
            parts = parts_of(doc, self.cfg["part_words"])
            facts = []
            for i, part in enumerate(parts, 1):
                self.log(f"    part {i}/{len(parts)} ({sum(s.words for s in part)} words)")
                try:
                    out = self._call("facts", (
                        f"SOURCE FILE: {rel}\nSOURCE TITLE: {doc.title}\nPART {i} of {len(parts)}\n\n"
                        f"{render(doc, part, short=True)}\n\nExtract up to {self.cfg['max_facts_per_part']} of the most "
                        "important facts in this part. Each fact is one self-contained sentence; `section` is the exact "
                        "`## ` heading it came from. Return compact JSON {\"facts\": [...]}."), SCHEMA_FACTS, 1000, rel)
                    facts.extend(out.get("facts", []))
                except ModelError as e:
                    self.failures.append({"source": rel, "stage": f"facts part {i}", "error": str(e)[:300]})
                    self.log(f"    ! skipped part {i}: {e}")
            material = "FACTS EXTRACTED FROM THE SOURCE, WITH THEIR SECTION:\n" + "\n".join(
                f"- [{f.get('section', '')}] {f.get('fact', '')}" for f in facts[:48])
        user = (f"SOURCE FILE: {rel}\nSOURCE TITLE: {doc.title}\n\n"
                f"{material}\n\nEXISTING NOTES (the only allowed targets for `related`):\n{existing}\n\n"
                f"Write the wiki note for this source's main subject. Return JSON with: title (2–6 word subject "
                f"name), folder, summary (2–3 sentences), key_facts (up to {self.cfg['max_note_facts']}, each "
                "with the exact section heading), concepts (up to 4 general techniques/ideas discussed in "
                "substance), related (up to 5, only from EXISTING NOTES, each with a one-line reason).")
        return self._call("note", user, SCHEMA_NOTE, 1500, rel)

    def validate_facts(self, facts: list[dict], doc: Document, rel: str) -> list[dict]:
        source_numbers = numbers_in("\n".join(b.text for s in doc.sections for b in s.blocks))
        kept = []
        for f in facts:
            text = str(f.get("fact", "")).strip()
            if not text:
                continue
            missing = numbers_in(text) - source_numbers
            if missing:
                self.dropped.append({"source": rel, "fact": text, "reason": f"numbers not in source: {sorted(missing)}"})
                continue
            section = match_section(str(f.get("section", "")), doc)
            anchor = section.heading if section and section.kind == "body" else None
            kept.append({"fact": text, "source": rel, "section": section.label if section else None,
                         "heading": anchor})
        return kept

    def choose_title(self, proposed: str, doc: Document) -> str:
        for candidate in (proposed, doc.title, " ".join(doc.title.split()[:5])):
            t = vault.clean_title(candidate)
            if t and not vault.naming_problems(t):
                return t
        return vault.clean_title(Path(doc.path).stem.replace("-", " "))

    def place(self, rel: str, plan: dict, doc: Document) -> str:
        """Return the vault-relative note path this source's subject belongs to."""
        mapped = self.store.catalog["sources"].get(rel, {}).get("notes", [])
        if mapped and mapped[0] in self.store.notes:
            return mapped[0]  # re-ingest: same note, same readable name
        title = self.choose_title(plan.get("title", ""), doc)
        for note_rel, d in self.store.notes.items():
            if vault.similar(d["title"], title):
                self.log(f"    same subject as existing note '{d['title']}' -> merging")
                return note_rel
        folder = plan.get("folder") if plan.get("folder") in vault.FOLDERS else "Concepts"
        # A note named like an original file ("TikTok" vs raw/.../tiktok.md) makes [[TikTok]] ambiguous in
        # Obsidian. Fall back to Gemma's fuller subject name, or add the folder as a qualifier.
        raw_stems = {p.stem.lower() for p in self.settings.path("raw").rglob("*") if p.is_file()}
        if title.lower() in raw_stems:
            fuller = re.sub(r"\s+", " ", vault._BAD_CHARS.sub(" ", str(plan.get("title", "")))).strip()
            title = fuller if fuller and fuller.lower() not in raw_stems and not vault.naming_problems(fuller) \
                else f"{title} - {folder}"
        path = f"wiki/{folder}/{title}.md"
        if (self.vault / path).exists() or path in self.store.notes:
            path = f"wiki/{folder}/{title} - {folder}.md"
        return path

    def ingest_source(self, path: Path, force: bool, overwrite_reviewed: bool) -> str:
        rel = path.relative_to(self.vault).as_posix()
        sha = sha256_file(path)
        entry = self.store.catalog["sources"].get(rel)
        known = lambda n: (self.vault / n).exists() or n in self.store.notes  # noqa: E731
        if entry and entry["sha256"] == sha and not force and all(known(n) for n in entry.get("notes", [])):
            self.log(f"= {rel}: unchanged (sha256 {sha[:12]}), notes up to date: {', '.join(Path(n).stem for n in entry['notes'])}")
            return "unchanged"
        doc = parse_file(path)
        self.log(f"+ {rel}: {doc.words} words, {len(doc.sections)} sections")
        if self.dry_run:
            mapped = entry.get("notes") if entry else None
            self.log(f"    dry run: would {'update ' + ', '.join(mapped) if mapped else 'create or merge a note'}")
            return "dry-run"
        start = time.perf_counter()
        plan = self.read_source(path, rel, doc)
        facts = self.validate_facts(plan.get("key_facts", []), doc, rel)
        note_rel = self.place(rel, plan, doc)
        existing = self.store.notes.get(note_rel)
        reviewed = (self.vault / note_rel).exists() and vault.read_note(self.vault / note_rel).meta.get("reviewed")
        if reviewed and not overwrite_reviewed:
            self.log(f"    {note_rel} is reviewed: new facts appended for review, reviewed text left as is")
            self.append_to_reviewed(note_rel, rel, facts, doc)
        else:
            d = existing or {"title": Path(note_rel).stem, "folder": Path(note_rel).parent.name,
                             "summary": plan.get("summary", "").strip(), "facts": [], "related": [],
                             "concepts": [], "sources": []}
            d["facts"] = [f for f in d["facts"] if f["source"] != rel] + facts
            if rel not in d["sources"]:
                d["sources"].append(rel)
            if not existing or not d.get("summary"):
                d["summary"] = plan.get("summary", "").strip()
            d["concepts"] = [c for c in d["concepts"] if c.get("source") != rel] + [
                {"name": c.get("name", ""), "why": c.get("why", ""), "source": rel} for c in plan.get("concepts", [])]
            d["related"] = merge_related(d["related"], plan.get("related", []), self.store.notes, d["title"])
            d["property_related"] = sorted(set(d.get("property_related", [])) | set(doc.properties.get("related") or []))
            self.store.notes[note_rel] = d
        self.changed.add(note_rel)
        self.store.catalog["sources"][rel] = {
            "source_id": source_id(rel, sha), "sha256": sha, "bytes": path.stat().st_size, "title": doc.title,
            "origin": origin_for(self.settings, rel), "notes": [note_rel],
            "ingested_at": datetime.now().isoformat(timespec="seconds"), "model": self.model.model_id}
        self.store.catalog["notes"].setdefault(note_rel, {})["title"] = Path(note_rel).stem
        self.log(f"    -> {note_rel} ({len(facts)} facts) in {time.perf_counter() - start:.0f}s")
        return "ingested"

    def append_to_reviewed(self, note_rel: str, rel: str, facts: list[dict], doc: Document) -> None:
        note = vault.read_note(self.vault / note_rel)
        if any(s.get("path") == rel for s in note.meta.get("sources", [])):
            block_re = re.compile(rf"\n### From {re.escape(rel.removeprefix('raw/'))}\n.*?(?=\n### |\n## )", re.S)
            note.body = block_re.sub("", note.body)
        lines = [f"\n### From {rel.removeprefix('raw/')}"] + [render_fact(f) for f in facts]
        note.body = re.sub(r"\n## Related notes", "\n".join(lines) + "\n\n## Related notes", note.body, count=1)
        if not any(s.get("path") == rel for s in note.meta.get("sources", [])):
            note.meta.setdefault("sources", []).append(self.source_meta(rel))
            note.body = note.body.rstrip() + "\n" + self.source_line(rel) + "\n"
        note.meta["needs_review"] = True
        vault.write_note(note)

    # ---- concepts and links
    def concept_pass(self) -> None:
        groups: list[dict] = []
        for note_rel, d in self.store.notes.items():
            for c in d.get("concepts", []):
                name = vault.clean_title(c.get("name", ""))
                if not name or vault.naming_problems(name):
                    continue
                g = next((g for g in groups if vault.similar(g["name"], name)), None)
                if g is None:
                    g = {"name": name, "mentions": []}
                    groups.append(g)
                g["mentions"].append({"note": note_rel, "why": c.get("why", ""), "source": c.get("source")})
        existing_titles = {d["title"] for d in self.store.notes.values()}
        # Subjects that were merged away or renamed must never come back as new notes.
        retired = set(self.store.catalog.get("redirects", {}))
        for rel in self.store.notes:
            p = self.vault / rel
            if p.exists():
                retired |= set(vault.read_note(p).meta.get("previous_names") or [])
        idx = None
        for g in sorted(groups, key=lambda g: -len({m["note"] for m in g["mentions"]})):
            notes_mentioning = {m["note"] for m in g["mentions"]}
            if len(notes_mentioning) < 2:
                continue
            if any(vault.similar(g["name"], old) for old in retired):
                self.log(f"  concept '{g['name']}' was merged away or renamed earlier; not re-created")
                continue
            match = next((t for t in existing_titles if vault.similar(t, g["name"])), None)
            if match:
                target_rel = next(r for r, d in self.store.notes.items() if d["title"] == match)
            else:
                idx = idx or self._fresh_index()
                target_rel = self.write_concept(g["name"], idx)
                if not target_rel:
                    continue
                existing_titles.add(g["name"])
            target = self.store.notes[target_rel]
            for m in g["mentions"]:
                if m["note"] == target_rel or m["note"] not in self.store.notes:
                    continue
                src = self.store.notes[m["note"]]
                why = m["why"].strip() or f"{src['title']} applies this idea."
                add_related(src, target["title"], why)
                add_related(target, src["title"], why)
                self.changed.update({m["note"], target_rel})

    def _fresh_index(self) -> retrieval.Index:
        retrieval.build_index(self.settings, log=self.log)
        return retrieval.Index(self.settings)

    def write_concept(self, name: str, idx: retrieval.Index, query: str | None = None) -> str | None:
        hits = idx.search(query or name, k=6, kinds=("source",))
        if not hits:
            return None
        self.log(f"+ concept '{name}' from {len(hits)} passages")
        passages = "\n\n".join(f"[P{i}] ({h.chunk.path} › {h.chunk.section})\n{h.chunk.text}" for i, h in enumerate(hits, 1))
        try:
            out = self._call("concept", (
                f"CONCEPT: {name}\n\nPASSAGES FROM THE SOURCES:\n{passages}\n\nWrite a concept note about {name} "
                "using only these passages: a 2–3 sentence summary of what it is and how it shows up in these "
                "sources, and up to 8 key facts, each naming the passage id (P1, P2, ...) it comes from. "
                "Return JSON {\"summary\": ..., \"key_facts\": [{\"fact\": ..., \"passage\": ...}]}."),
                SCHEMA_CONCEPT, 1200, f"concept:{name}")
        except ModelError as e:
            self.failures.append({"source": f"concept:{name}", "stage": "concept", "error": str(e)[:300]})
            return None
        facts = []
        for f in out.get("key_facts", []):
            m = re.search(r"\d+", str(f.get("passage", "")))
            if not m or not (1 <= int(m.group()) <= len(hits)):
                continue
            h = hits[int(m.group()) - 1]
            # Gemma sometimes echoes the passage id into the sentence ("... (P5)"); it is not part of the fact.
            text = re.sub(r"\s*\(?\[?P\d+(?:\s*[,/]\s*P\d+)*\]?\)?(?=[.\s]*$)", "", str(f.get("fact", ""))).strip()
            text = re.sub(r"\s*\((?:P\d+[,\s]*)+\)", "", text).strip()
            missing = numbers_in(text) - numbers_in(h.chunk.text)
            if missing:
                self.dropped.append({"source": h.chunk.path, "fact": text, "reason": f"numbers not in passage: {sorted(missing)}"})
                continue
            heading = h.chunk.section.split(" › ")[-1] if h.chunk.section not in ("Properties", "(introduction)") else None
            facts.append({"fact": text, "source": h.chunk.path, "section": h.chunk.section, "heading": heading})
        if not facts:
            return None
        rel = f"wiki/Concepts/{name}.md"
        self.store.notes[rel] = {"title": name, "folder": "Concepts", "summary": out.get("summary", "").strip(),
                                 "facts": facts, "related": [], "concepts": [],
                                 "sources": sorted({f["source"] for f in facts})}
        self.store.catalog["notes"].setdefault(rel, {})["title"] = name
        for s in self.store.notes[rel]["sources"]:
            src = self.store.catalog["sources"].get(s)
            if src and rel not in src["notes"]:
                src["notes"].append(rel)
        self.changed.add(rel)
        return rel

    def link_pass(self) -> None:
        by_title = {d["title"]: r for r, d in self.store.notes.items()}
        for note_rel in sorted(self.changed):
            d = self.store.notes.get(note_rel)
            if d is None or self.is_reviewed(note_rel):
                continue
            # Related work named in the source's own properties (website "related" slugs).
            for slug in d.get("property_related", []):
                target = self.note_for_raw(f"raw/website/projects/{slug}.md")
                if target and target != note_rel:
                    d.setdefault("_suggested", []).append(self.store.notes[target]["title"])
            candidates = [f"- {o['title']} — {o.get('summary', '')[:120]}" for r, o in sorted(self.store.notes.items())
                          if r != note_rel]
            if not candidates:
                continue
            suggested = d.pop("_suggested", [])
            facts = "\n".join(f"- {f['fact']}" for f in d["facts"][:8])
            hint = f"\nThe source itself lists these as related: {', '.join(suggested)}." if suggested else ""
            try:
                out = self._call("links", (
                    f"NOTE: {d['title']}\nSUMMARY: {d.get('summary', '')}\nKEY FACTS:\n{facts}{hint}\n\n"
                    f"OTHER NOTES:\n" + "\n".join(candidates) + "\n\nChoose up to 5 OTHER NOTES that are genuinely "
                    "related to this note (shared technique, same project, same employer or course, one built on the "
                    "other). For each, give a one-line reason that says what they share. Return JSON {\"related\": [...]}; "
                    "an empty list is fine."), SCHEMA_LINKS, 700, note_rel)
            except ModelError as e:
                self.failures.append({"source": note_rel, "stage": "links", "error": str(e)[:300]})
                out = {"related": []}
            d["related"] = merge_related(d["related"], out.get("related", []), self.store.notes, d["title"])
            for t in suggested:
                if t not in {r["title"] for r in d["related"]}:
                    d["related"].append({"title": t, "why": "Listed as related work in this subject's source."})

    def note_for_raw(self, rel: str) -> str | None:
        notes = self.store.catalog["sources"].get(rel, {}).get("notes", [])
        return notes[0] if notes and notes[0] in self.store.notes else None

    def is_reviewed(self, note_rel: str) -> bool:
        p = self.vault / note_rel
        return p.exists() and bool(vault.read_note(p).meta.get("reviewed"))

    # ---- rendering
    def source_meta(self, rel: str) -> dict:
        src = self.store.catalog["sources"].get(rel, {})
        return {"path": rel, "source_id": src.get("source_id"), "sha256": src.get("sha256")}

    def source_line(self, rel: str) -> str:
        src = self.store.catalog["sources"].get(rel, {})
        origin = src.get("origin") or origin_for(self.settings, rel)
        label = f"{origin.get('collection', 'Source')}: {src.get('title') or Path(rel).name}"
        url = origin.get("url")
        return f"- {vault.raw_link(rel, None, label)}" + (f" — [origin]({url})" if url else "")

    def render(self, note_rel: str) -> None:
        d = self.store.notes[note_rel]
        path = self.vault / note_rel
        old = vault.read_note(path) if path.exists() else None
        if old and old.meta.get("reviewed"):
            return
        lines = [f"# {d['title']}", "", d.get("summary", "").strip(), "", "## Key facts"]
        sources = d["sources"]
        for rel in sources:
            facts = [f for f in d["facts"] if f["source"] == rel]
            if not facts:
                continue
            if len(sources) > 1:
                lines.append(f"\n### From {rel.removeprefix('raw/')}")
            lines.extend(render_fact(f) for f in facts)
        lines += ["", "## Related notes"]
        rel_lines = [f"- [[{r['title']}]] — {r['why'].strip()}" for r in d.get("related", [])
                     if any(o["title"] == r["title"] for o in self.store.notes.values())]
        lines += rel_lines or ["- (none yet)"]
        lines += ["", "## Sources"] + [self.source_line(rel) for rel in sources]
        summary = d.get("summary", "").strip()
        first = vault.first_sentence(summary)
        meta = {
            "title": d["title"], "type": d["folder"].lower().rstrip("s"), "summary": first,
            "sources": [self.source_meta(rel) for rel in sources],
            "generated_by": f"{self.model.model_id} ({self.model.mode}, {self.settings.local['runtime']})",
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "reviewed": False,
        }
        vault.write_note(vault.Note(path=path, meta=meta, body="\n".join(lines)))

    # ---- entry point
    def run(self, paths: list[str] | None, force=False, overwrite_reviewed=False, into="imported") -> dict:
        t0 = time.perf_counter()
        files = discover(paths, into, self.settings, self.log)
        if not files:
            raise FileNotFoundError("No supported source files found (.md, .txt, .html).")
        results = {}
        if not self.dry_run:
            self.model.require()
        for f in files:
            rel = f.relative_to(self.vault).as_posix()
            try:
                results[rel] = self.ingest_source(f, force, overwrite_reviewed)
            except ModelError as e:  # one bad source must not lose the rest of the run
                results[rel] = "failed"
                self.failures.append({"source": rel, "stage": "note", "error": str(e)[:300]})
                self.log(f"  ! {rel}: FAILED ({e}); re-run `wiki ingest {rel}` to retry")
            if not self.dry_run:
                self.store.save()  # progress survives an interrupted run
        if self.dry_run:
            return {"files": results}
        if self.changed:
            self.concept_pass()
            self.store.save()
            self.link_pass()
        written = []   # notes whose file actually changed (the concept pass re-renders notes it only re-checked)
        for note_rel in sorted(self.store.notes):
            path = self.vault / note_rel
            if note_rel in self.changed or not path.exists():
                before = path.read_bytes() if path.exists() else None
                self.render(note_rel)
                if path.read_bytes() != before:
                    written.append(note_rel)
        self.store.save()
        vault.render_index(self.settings)
        vault.render_catalog(self.store.catalog, self.settings)
        stats = retrieval.build_index(self.settings, log=self.log)
        summary = {"time": datetime.now().isoformat(timespec="seconds"), "files": results,
                   "notes_changed": written, "model": self.model.model_id, "mode": self.model.mode,
                   "model_calls": len(self.calls), "seconds": round(time.perf_counter() - t0, 1),
                   "dropped_facts": self.dropped, "failures": self.failures, "calls": self.calls, "index": stats}
        runs = self.settings.path("runs")
        runs.mkdir(parents=True, exist_ok=True)
        # Millisecond stamp: two ingests in the same second must not overwrite each other's record (fix 12).
        record = runs / f"ingest-{datetime.now().strftime('%Y%m%d-%H%M%S-%f')[:-3]}.json"
        record.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
        return summary


def render_fact(f: dict) -> str:
    rel = f["source"]
    where = f.get("heading") or ("front matter" if f.get("section") == "Properties" else None)
    label = rel.removeprefix("raw/") + (f" › {where}" if where else "")
    return f"- {f['fact']} ({vault.raw_link(rel, f.get('heading'), label)})"


def add_related(d: dict, title: str, why: str) -> None:
    if title != d["title"] and title not in {r["title"] for r in d.setdefault("related", [])}:
        d["related"].append({"title": title, "why": why})


def merge_related(current: list[dict], proposed: list[dict], notes: dict, self_title: str) -> list[dict]:
    titles = {d["title"] for d in notes.values()}
    out = list(current)
    for r in proposed:
        t = str(r.get("title", "")).strip()
        exact = t if t in titles else next((x for x in titles if vault.similar(x, t)), None)
        why = str(r.get("why", "")).strip()
        if exact and exact != self_title and why and exact not in {o["title"] for o in out}:
            out.append({"title": exact, "why": why})
    return out[:8]


def ingest(paths=None, force=False, overwrite_reviewed=False, dry_run=False, into="imported", log=print, model=None) -> dict:
    return Ingester(model=model, log=log, dry_run=dry_run).run(paths, force, overwrite_reviewed, into)


def merge_notes(keep_title: str, remove_title: str, drop_facts: bool = False, log=print) -> list[str]:
    """Merge two notes about the same subject: facts, sources, links and catalog entries move to `keep`.

    Every [[remove]] link in the vault is redirected to [[keep]], the removed file is deleted, and a
    redirect is recorded in data/catalog.json so a later ingest can never re-create the removed subject.
    If `keep` is already reviewed its text is left alone, so the removed note's facts must be duplicates
    (drop_facts=True) - otherwise review the facts by hand.
    """
    ing = Ingester(model=get_model("local"), log=log)
    notes = ing.store.notes
    by_title = {d["title"]: r for r, d in notes.items()}
    if keep_title not in by_title or remove_title not in by_title:
        raise ValueError(f"both notes must exist; known titles: {', '.join(sorted(by_title))}")
    k, r = by_title[keep_title], by_title[remove_title]
    if ing.is_reviewed(r):
        raise ValueError(f"{r} is already reviewed; edit it by hand instead of merging it away")
    if ing.is_reviewed(k) and not drop_facts:
        raise ValueError(f"{k} is reviewed; pass --drop-facts if {remove_title!r} only repeats it, or edit by hand")
    keep, rem = notes[k], notes[r]
    ing.store.catalog.setdefault("redirects", {})[remove_title] = keep_title
    seen = {f["fact"] for f in keep["facts"]}
    if not drop_facts:
        keep["facts"] += [f for f in rem["facts"] if f["fact"] not in seen]
    keep["sources"] += [s for s in rem["sources"] if s not in keep["sources"]]
    keep["concepts"] = keep.get("concepts", []) + rem.get("concepts", [])
    keep["property_related"] = sorted(set(keep.get("property_related", [])) | set(rem.get("property_related", [])))
    keep["merged_from"] = sorted(set(keep.get("merged_from", [])) | {remove_title})
    for rel_ in rem.get("related", []):
        if rel_["title"] not in (keep_title, remove_title):
            add_related(keep, rel_["title"], rel_["why"])
    keep["related"] = [x for x in keep["related"] if x["title"] != remove_title]
    for d in notes.values():
        for x in d.get("related", []):
            if x["title"] == remove_title:
                x["title"] = keep_title
        uniq, titles = [], set()
        for x in d.get("related", []):
            if x["title"] not in titles and x["title"] != d["title"]:
                uniq.append(x)
                titles.add(x["title"])
        d["related"] = uniq
    del notes[r]
    for src in ing.store.catalog["sources"].values():
        src["notes"] = list(dict.fromkeys(k if n == r else n for n in src.get("notes", [])))
    ing.store.catalog["notes"].pop(r, None)
    (ing.vault / r).unlink(missing_ok=True)
    changed = [k]
    pattern = re.compile(r"\[\[" + re.escape(remove_title) + r"(#[^\]|]*)?(\|[^\]]*)?\]\]")
    for p in ing.vault.rglob("*.md"):
        if "raw" in p.relative_to(ing.vault).parts:
            continue
        text = p.read_text(encoding="utf-8")
        new = pattern.sub(lambda m: f"[[{keep_title}{m.group(1) or ''}{m.group(2) or ''}]]", text)
        if new != text:
            p.write_text(new, encoding="utf-8")
            changed.append(p.relative_to(ing.vault).as_posix())
    for rel in notes:
        if not ing.is_reviewed(rel):
            ing.render(rel)
    ing.store.save()
    vault.render_index(ing.settings)
    vault.render_catalog(ing.store.catalog, ing.settings)
    retrieval.build_index(ing.settings, log=log)
    return changed


def regenerate_concept(title: str, query: str, log=print) -> str:
    """Rewrite one (unreviewed) concept note from passages found with a more specific query.

    Used when the concept's own name retrieves the wrong material (e.g. "Agentic AI" pulling the
    course syllabus). Related links are kept; facts and summary come from Gemma again.
    """
    ing = Ingester(model=get_model("local"), log=log)
    rel = next((r for r, d in ing.store.notes.items() if d["title"] == title and d["folder"] == "Concepts"), None)
    if rel is None:
        raise ValueError(f"no concept note titled {title!r}")
    if ing.is_reviewed(rel):
        raise ValueError(f"{rel} is reviewed; edit it by hand")
    related = ing.store.notes[rel].get("related", [])
    del ing.store.notes[rel]
    idx = retrieval.Index(ing.settings)
    new_rel = ing.write_concept(title, idx, query=query)
    if not new_rel:
        raise ModelError(f"could not regenerate {title!r}")
    ing.store.notes[new_rel]["related"] = related
    ing.render(new_rel)
    ing.store.save()
    vault.render_index(ing.settings)
    vault.render_catalog(ing.store.catalog, ing.settings)
    return new_rel
