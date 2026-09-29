"""Run the four ask-mode tests and the chat/search mode checks; write evidence cards.

    python scripts/run_evals.py --label local-dryrun          # run everything, write evidence/<label>/
    python scripts/run_evals.py --label offline --cards-only  # re-render cards from saved results + assessments

Uses the same harness functions the CLI calls (harness.ask, harness.ChatSession, retrieval.Index).
Nothing here edits a model answer: cards print the saved text verbatim. Manual assessments live in
evidence/assessments.yaml and are merged into the cards when present.
"""

from __future__ import annotations

import argparse
import json
import platform
import socket
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import yaml

from wiki import config, harness, retrieval, serve
from wiki.llm import get_model

sys.path.insert(0, str(Path(__file__).parent))
from retrieval_check import matches  # noqa: E402


def network_status() -> dict:
    """Internet = a real HTTPS request succeeds (route + DNS + valid certificate).

    A raw TCP connect to 1.1.1.1:53 is recorded for information only: on this Mac the Cisco AnyConnect
    socket filter answers it locally even with Wi-Fi off, so it cannot prove the machine is online.
    """
    import ssl
    import urllib.error
    import urllib.request
    out = {}
    for url in ("https://1.1.1.1", "https://huggingface.co"):
        try:
            urllib.request.urlopen(url, timeout=5, context=ssl.create_default_context())
            out[url] = "reachable"
        except urllib.error.HTTPError as e:  # a real server answered with an HTTP status: online
            out[url] = f"reachable (HTTP {e.code})"
        except Exception as e:  # noqa: BLE001
            out[url] = f"unreachable ({e.__class__.__name__})"
    try:
        with socket.create_connection(("1.1.1.1", 53), timeout=2):
            out["tcp 1.1.1.1:53 (informational)"] = "answered"
    except OSError as e:
        out["tcp 1.1.1.1:53 (informational)"] = f"no answer ({e.__class__.__name__})"
    https = [v for k, v in out.items() if k.startswith("https")]
    out["internet"] = "offline" if all(v.startswith("unreachable") for v in https) else "ONLINE"
    return out


def device() -> dict:
    def sh(cmd):
        try:
            return subprocess.run(cmd, capture_output=True, text=True, timeout=20).stdout.strip()
        except Exception as e:  # noqa: BLE001
            return f"unavailable: {e}"
    return {"os": f"macOS {platform.mac_ver()[0]} ({platform.machine()})",
            "chip": sh(["sysctl", "-n", "machdep.cpu.brand_string"]),
            "memory_gb": round(int(sh(["sysctl", "-n", "hw.memsize"]) or 0) / 2**30, 1),
            "llama_server": sh(["llama-server", "--version"]).splitlines()[-2:] if sh(["which", "llama-server"]) else "missing"}


def model_identity(settings) -> dict:
    lock = json.loads((settings.root / "config" / "models.lock.json").read_text())
    gen = lock["models"][0]
    path = Path(settings.local["model_file"]).expanduser()
    actual = subprocess.run(["shasum", "-a", "256", str(path)], capture_output=True, text=True).stdout.split()[0]
    return {"id": gen["id"], "file": gen["file"], "hf_repo": gen["hf_repo"], "sha256_expected": gen["sha256"],
            "sha256_actual": actual, "sha256_match": actual == gen["sha256"], "runtime": lock["runtime"]["version"],
            "embedding_model": lock["models"][1]["id"]}


# --------------------------------------------------------------------------- run

def run_ask_tests(tests, index, model) -> list[dict]:
    out = []
    for t in tests:
        print(f"[ask] {t['id']}: {t['question']}")
        r = harness.ask(t["question"], model=model, index=index)
        passages = []
        for i, h in enumerate(r.passages, 1):
            rec = harness.hit_record(h, f"S{i}")
            rec["expected"] = [f"E{j + 1}" for j, e in enumerate(t["expected_evidence"]) if matches(h.chunk, e)]
            passages.append(rec)
        expected = []
        for j, e in enumerate(t["expected_evidence"]):
            ranks = [p["id"] for p in passages if f"E{j + 1}" in p["expected"]]
            expected.append({"id": f"E{j + 1}", **e, "found_as": ranks[0] if ranks else None})
        out.append({"test": t, "answer": r.answer, "mode": r.mode, "model": r.model, "method": r.method,
                    "passages": passages, "expected_found": expected, "checks": r.checks, "timings": r.timings,
                    "run_file": r.run_file, "model_called": r.model_called})
        print(f"      -> {r.checks['status']} in {r.timings.get('total_s')}s")
    return out


def chat_turns(session, turns) -> list[dict]:
    rows = []
    for text in turns:
        print(f"[chat] {text}")
        t = session.turn(text)
        rows.append({"user": text, "reply": t.reply, "route": t.route.__dict__,
                     "notes": [harness.hit_record(h, f"N{i}") for i, h in enumerate(t.notes, 1)],
                     "checks": t.checks, "timings": t.timings})
    return rows


def run_mode_checks(checks, index, model) -> list[dict]:
    out = []
    by_id = {c["id"]: c for c in checks}
    s = harness.ChatSession(model=model, index=index)
    out.append({"check": by_id["M1"], "turns": chat_turns(s, by_id["M1"]["turns"]), "log": config.rel(s.log_path)})
    s = harness.ChatSession(model=model, index=index)
    out.append({"check": by_id["M2"], "turns": chat_turns(s, by_id["M2"]["turns"]), "log": config.rel(s.log_path)})

    m3 = by_id["M3"]
    # Search must not need the language model: stop Gemma, search, then bring it back.
    serve.stop(("gemma",), log=lambda *_: None)
    gemma_up = serve.status()["gemma"]["healthy"]
    t0 = time.perf_counter()
    hits = index.search(m3["query"])
    search_s = round(time.perf_counter() - t0, 3)
    print(f"[search] {m3['query']} (Gemma running: {gemma_up}) -> {len(hits)} passages")
    serve.start(("gemma",), log=lambda *_: None)
    out.append({"check": m3, "gemma_server_running_during_search": gemma_up, "method": index.last_method,
                "seconds": search_s, "model_calls": 0,
                "passages": [harness.hit_record(h, str(i)) for i, h in enumerate(hits, 1)]})

    m4 = by_id["M4"]
    s = harness.ChatSession(model=model, index=index)
    turns = chat_turns(s, m4["chat_turns"])
    print(f"[ask] {m4['ask']}")
    r = harness.ask(m4["ask"], model=model, index=index)
    sent = json.dumps(r.messages)
    out.append({"check": m4, "turns": turns, "log": config.rel(s.log_path), "ask_answer": r.answer,
                "ask_checks": r.checks, "ask_run_file": r.run_file,
                "chat_claim_in_ask_prompt": any(x in sent for x in ("Rust", "favorite programming language is")),
                "ask_passages": [harness.hit_record(h, f"S{i}") for i, h in enumerate(r.passages, 1)]})
    return out


# --------------------------------------------------------------------------- cards

def quote(text: str) -> str:
    return "\n".join("> " + line if line else ">" for line in text.splitlines())


def ask_card(res: dict, meta: dict, assessment: str | None) -> str:
    t = res["test"]
    mid = meta["model"]
    lines = [f"# {t['id']}: {t['kind']}", "",
             "| | |", "|---|---|",
             f"| Question | {t['question']} |",
             f"| Command | `wiki ask \"{t['question']}\"` (same code path: `harness.ask`) |",
             (f"| Execution | **{res['mode']}** — llama.cpp `llama-server` on 127.0.0.1; internet: **{meta['network']['internet']}** |"
              if res["mode"] == "local" else
              f"| Execution | **ONLINE (optional extension)** — hosted Gemma via the Gemini API; prompt and passages sent to Google |"),
             (f"| Model | `{res['model']}` · file `{mid['file']}` · sha256 `{mid['sha256_actual'][:16]}…` "
              f"({'matches' if mid['sha256_match'] else 'DOES NOT MATCH'} the Hugging Face checksum) · {mid['runtime']} |"
              if res["mode"] == "local" else f"| Model | `{res['model']}` · {mid['runtime']} |"),
             f"| Run | label `{meta['label']}`, {meta['time']} |",
             f"| Expected behavior | {t['expected_behavior']} |",
             f"| Expected answer | {t['expected_answer']} |", ""]
    lines += ["## 1. Retrieval (checked before the answer)", "", f"Method: {res['method']}.", ""]
    if res["expected_found"]:
        lines += ["| Expected evidence | Retrieved? |", "|---|---|"]
        for e in res["expected_found"]:
            lines.append(f"| {e['id']}: `{e['path']}` › {e['section']} — must contain {', '.join(repr(s) for s in e['must_contain'])} "
                         f"| {'yes, as ' + e['found_as'] if e['found_as'] else '**no** (not among the passages given to Gemma)'} |")
    else:
        lines.append("No source contains the answer (by design). The passages below are what the retriever offered instead.")
    lines += ["", "| Id | Passage | Section | BM25 rank | Vector rank | Expected? |", "|---|---|---|---|---|---|"]
    for p in res["passages"]:
        lines.append(f"| {p['id']} | `{p['path']}:{p['lines'][0]}-{p['lines'][1]}` | {p['section']} | "
                     f"{p['bm25_rank'] or '-'} | {p['vector_rank'] or '-'} | {', '.join(p['expected']) or ''} |")
    lines += ["", "<details><summary>Full text of the passages given to Gemma</summary>", ""]
    for p in res["passages"]:
        lines += [f"**[{p['id']}] `{p['path']}:{p['lines'][0]}-{p['lines'][1]}` — {p['section']}**", "", quote(p["text"]), ""]
    lines += ["</details>", "", "## 2. Gemma's answer (verbatim)", "", quote(res["answer"]), ""]
    c = res["checks"]
    lines += ["## 3. Citations", "", "| Cited | Points to |", "|---|---|"]
    for n in c.get("cited", []):
        p = res["passages"][n - 1] if 1 <= n <= len(res["passages"]) else None
        lines.append(f"| [S{n}] | " + (f"`{p['path']}:{p['lines'][0]}-{p['lines'][1]}` › {p['section']} |" if p else "**no such passage** |"))
    if not c.get("cited"):
        lines.append("| — | no citations |")
    lines += ["", f"Automated check: **{c['status']}**. Unknown ids: {c.get('unknown_ids') or 'none'}. "
              f"Numbers not found in the cited passage: {[x['number'] for x in c.get('numbers_not_in_cited_passages', [])] or 'none'}. "
              f"Sentences without a citation: {len(c.get('uncited_sentences', []))}.", "",
              "The automated check only confirms that citations point at supplied passages and that numbers appear in "
              "them. Whether each claim is actually supported is judged by reading the passages (below).", "",
              "## 4. Assessment (manual, after reading the cited passages)", "",
              assessment or "_Pending manual review._", "",
              "## 5. Timing", ""]
    tm = res["timings"]
    total = f"Total {tm.get('total_s')} s = retrieval {tm.get('retrieval_s')} s + model {tm.get('model_s', 0)} s"
    if "llama_prompt_n" in tm:
        lines.append(total + f" (prompt {tm['llama_prompt_n']} tokens at {round(tm['llama_prompt_per_second'], 1)} tok/s; "
                     f"answer {tm['llama_predicted_n']} tokens at {round(tm['llama_predicted_per_second'], 1)} tok/s).")
    else:
        lines.append(total + " (hosted model: includes the network round trip; no token timings reported).")
    lines += ["", f"Full record including the exact messages sent to the model: [`{res['run_file']}`](../../../{res['run_file']})", ""]
    return "\n".join(lines)


def mode_card(results: list[dict], meta: dict, assessments: dict) -> str:
    lines = ["# Mode-boundary checks", "",
             f"Label `{meta['label']}`, {meta['time']}. Execution: local (llama.cpp on 127.0.0.1), model "
             f"`{meta['model']['id']}`; internet: **{meta['network']['internet']}**.", ""]
    for r in results:
        c = r["check"]
        lines += [f"## {c['id']}: {c['name']}", "", f"Expected: {c['expected']}.", ""]
        if "turns" in r:
            for t in r["turns"]:
                route = t["route"]
                lines += [f"**you ›** {t['user']}", "",
                          f"_Harness routing: {'looked up notes' if route['retrieve'] else 'no notes lookup'} — {route['reason']}"
                          + (f"; {len(t['notes'])} passages" if t['notes'] else "") + f"; {t['timings']['total_s']} s._", "",
                          "**Wren ›**", "", quote(t["reply"]), ""]
                for n in t["notes"]:
                    lines.append(f"- [{n['id']}] `{n['path']}:{n['lines'][0]}-{n['lines'][1]}` › {n['section']}")
                if t["notes"]:
                    lines += ["", f"Citation check on [N#] tags: {t['checks'].get('status')}", ""]
            lines.append(f"Chat log with exact messages: `{r['log']}`")
            lines.append("")
        if c["id"] == "M3":
            lines += [f"Gemma server running during this search: **{r['gemma_server_running_during_search']}**. "
                      f"Model calls: **0**. Method: {r['method']}. Time: {r['seconds']} s.", "",
                      "| # | Passage | Section |", "|---|---|---|"]
            for p in r["passages"]:
                lines.append(f"| {p['id']} | `{p['path']}:{p['lines'][0]}-{p['lines'][1]}` | {p['section']} |")
            lines += ["", "First passage, verbatim:", "", quote(r["passages"][0]["text"]) if r["passages"] else "(none)", ""]
        if c["id"] == "M4":
            lines += [f"Then, separately: `wiki ask \"{c['ask']}\"`", "", quote(r["ask_answer"]), "",
                      f"Citation check: {r['ask_checks']['status']}. Chat claim present in the ask prompt: "
                      f"**{r['chat_claim_in_ask_prompt']}** (record: `{r['ask_run_file']}`).", ""]
        a = assessments.get(c["id"])
        lines += ["Assessment: " + (a or "_pending manual review_"), ""]
    return "\n".join(lines)


def write_cards(label: str) -> None:
    settings = config.load()
    base = settings.root / "evidence" / label
    data = json.loads((base / "results.json").read_text())
    all_assess = {}
    ap = settings.root / "evidence" / "assessments.yaml"
    if ap.exists():
        all_assess = (yaml.safe_load(ap.read_text()) or {}).get(label, {}) or {}
    (base / "ask").mkdir(parents=True, exist_ok=True)
    for res in data["ask"]:
        (base / "ask" / f"{res['test']['id']}.md").write_text(ask_card(res, data["meta"], all_assess.get(res["test"]["id"])))
    if data["mode_checks"]:
        (base / "mode_checks.md").write_text(mode_card(data["mode_checks"], data["meta"], all_assess))
    rows = ["| Test | Expected evidence retrieved | Citation check | Time (s) | Manual assessment |", "|---|---|---|---|---|"]
    for res in data["ask"]:
        found = ", ".join(f"{e['id']}:{'yes' if e['found_as'] else 'no'}" for e in res["expected_found"]) or "n/a (unsupported)"
        verdict = (all_assess.get(res["test"]["id"]) or "pending").split(".")[0]
        rows.append(f"| [{res['test']['id']}](ask/{res['test']['id']}.md) | {found} | {res['checks']['status']} | "
                    f"{res['timings'].get('total_s')} | {verdict} |")
    meta = data["meta"]
    summary = [f"# Evaluation run `{label}`", "",
               f"{meta['time']} · internet **{meta['network']['internet']}** · {meta['device']['os']} · {meta['device']['chip']} · "
               f"{meta['device']['memory_gb']} GB · model `{meta['model']['id']}` "
               f"{'(sha256 match: ' + str(meta['model']['sha256_match']) + ')' if meta.get('execution', 'local') == 'local' else '(hosted)'} · "
               f"{meta['model']['runtime']}", "", *rows, ""]
    if data["mode_checks"]:
        summary += ["Mode checks: [mode_checks.md](mode_checks.md)", ""]
    elif (base / "chat_checks.md").exists():
        summary += ["Chat checks (run separately, assessed by hand): [chat_checks.md](chat_checks.md)", ""]
    (base / "summary.md").write_text("\n".join(summary))
    print(f"cards written to {config.rel(base)}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--cards-only", action="store_true")
    ap.add_argument("--mode", choices=["local", "online"], default="local",
                    help="online: hosted Gemma via the Gemini API (needs $GEMINI_API_KEY); runs the four ask tests only")
    args = ap.parse_args()
    settings = config.load()
    if args.cards_only:
        write_cards(args.label)
        return 0
    spec = yaml.safe_load((settings.root / "tests" / "questions.yaml").read_text())
    model = get_model(args.mode)
    model.require()
    index = retrieval.Index(settings)
    identity = model_identity(settings) if args.mode == "local" else {
        "id": model.model_id, "file": "(hosted)", "sha256_actual": "n/a", "sha256_match": None,
        "runtime": f"{settings.online['provider']} — retrieval and embeddings still local"}
    meta = {"label": args.label, "time": datetime.now().isoformat(timespec="seconds"), "execution": args.mode,
            "network": network_status(), "device": device(), "model": identity, "passages_indexed": len(index.chunks)}
    print(f"network: {meta['network']}")
    results = {"meta": meta, "ask": run_ask_tests(spec["ask_tests"], index, model),
               "mode_checks": run_mode_checks(spec["mode_checks"], index, model) if args.mode == "local" else []}
    base = settings.root / "evidence" / args.label
    base.mkdir(parents=True, exist_ok=True)
    (base / "results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False))
    write_cards(args.label)
    return 0


if __name__ == "__main__":
    sys.exit(main())
