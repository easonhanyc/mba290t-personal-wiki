"""Regenerate the measured tables inside README.md from the evidence files.

Each table sits between <!-- BEGIN:name --> and <!-- END:name --> markers; only those blocks are
replaced, so the prose around them is untouched. No number in these tables is typed by hand.

    python scripts/build_readme_tables.py --eval-label offline --metrics-label local
"""

from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from pathlib import Path

import yaml

from wiki import config, vault


def block(readme: str, name: str, body: str) -> str:
    pattern = re.compile(rf"(<!-- BEGIN:{name} -->\n).*?(<!-- END:{name} -->)", re.S)
    if not pattern.search(readme):
        print(f"  (no {name} markers in README; skipped)")
        return readme
    return pattern.sub(lambda m: m.group(1) + body.strip() + "\n" + m.group(2), readme)


def eval_table(root: Path, label: str) -> str:
    p = root / "evidence" / label / "results.json"
    if not p.exists():
        return f"_No evaluation run `{label}` yet._"
    data = json.loads(p.read_text())
    assess = (yaml.safe_load((root / "evidence" / "assessments.yaml").read_text()) or {}).get(label, {}) \
        if (root / "evidence" / "assessments.yaml").exists() else {}
    meta = data["meta"]
    where = (f"(file sha256 matches Hugging Face: {meta['model']['sha256_match']})" if meta.get("execution", "local") == "local"
             else f"(hosted: {meta['model']['runtime']})")
    rows = [f"Run `{label}` at {meta['time']}; internet **{meta['network']['internet']}**; model `{meta['model']['id']}` "
            f"{where}; {meta['passages_indexed']} passages indexed.", "",
            "| Test | Question | Expected evidence retrieved | Answer (first sentence) | Citation check | Time | Assessment |",
            "|---|---|---|---|---|---|---|"]
    for r in data["ask"]:
        t = r["test"]
        found = "; ".join(f"{e['id']} {'yes (' + e['found_as'] + ')' if e['found_as'] else 'no'}" for e in r["expected_found"]) or "n/a"
        first = vault.first_sentence(r["answer"]).replace("|", "\\|")
        verdict = (assess.get(t["id"]) or "pending review").split(".")[0]
        rows.append(f"| [{t['id']}](evidence/{label}/ask/{t['id']}.md) | {t['question']} | {found} | {first} | "
                    f"{r['checks']['status']} | {r['timings'].get('total_s')} s | {verdict} |")
    if not data["mode_checks"]:
        return "\n".join(rows)
    rows += ["", "| Check | Result | Assessment |", "|---|---|---|"]
    for m in data["mode_checks"]:
        c = m["check"]
        if c["id"] in ("M1", "M2", "M5"):
            res = "; ".join(f"\"{t['user'][:40]}\" → {'notes looked up' if t['route']['retrieve'] else 'no lookup'}"
                            + (f" (tags: {t['checks'].get('status')}"
                               + (", notes listed by the harness" if t["checks"].get("notes_listed_by_harness") else "") + ")"
                               if t["notes"] else "") for t in m["turns"])
        elif c["id"] == "M3":
            res = f"{len(m['passages'])} original passages, 0 model calls, Gemma running: {m['gemma_server_running_during_search']}"
        else:
            res = f"ask: \"{m['ask_answer'][:60]}…\"; chat claim in ask prompt: {m['chat_claim_in_ask_prompt']}"
        verdict = (assess.get(c["id"]) or "pending review").split(".")[0]
        rows.append(f"| [{c['id']} {c['name']}](evidence/{label}/mode_checks.md) | {res.replace('|', '/')} | {verdict} |")
    return "\n".join(rows)


def details_block(root: Path, label: str) -> str:
    """Per test, collapsed: retrieved passages with paths, the verbatim answer, and the manual assessment."""
    p = root / "evidence" / label / "results.json"
    if not p.exists():
        return f"_No evaluation run `{label}` yet._"
    data = json.loads(p.read_text())
    assess = (yaml.safe_load((root / "evidence" / "assessments.yaml").read_text()) or {}).get(label, {})
    out = []
    for r in data["ask"]:
        t = r["test"]
        ids = {f"{x['path']}:{x['lines'][0]}-{x['lines'][1]}": x["id"] for x in r["passages"]}
        out += [f"<details><summary><b>{t['id']}</b> ({t['kind']}): {t['question']}</summary>", "",
                f"Expected: {t['expected_answer']}", "",
                "| Id | Passage given to Gemma | Section | How it was retrieved | Expected evidence |", "|---|---|---|---|---|"]
        for x in r["passages"]:
            how = (f"added: opening of the section of {ids.get(x['opens_section_of'], x['opens_section_of'])}"
                   if x.get("opens_section_of") else f"BM25 #{x['bm25_rank'] or '-'} · vector #{x['vector_rank'] or '-'}")
            out.append(f"| {x['id']} | `{x['path']}:{x['lines'][0]}-{x['lines'][1]}` | {x['section'].replace('|', '/')} | "
                       f"{how} | {', '.join(x['expected'])} |")
        answer = "\n".join("> " + line if line else ">" for line in r["answer"].splitlines())
        out += ["", "Gemma's answer, verbatim (citation check: **" + r["checks"]["status"] + "**):", "", answer, "",
                "**Do the cited passages support it?** " + (assess.get(t["id"]) or "pending review"), "",
                f"Full card with every passage's text: [{t['id']}](evidence/{label}/ask/{t['id']}.md)", "", "</details>", ""]
    return "\n".join(out)


INGEST_NOTES = {
    "20260926-231200": "trial on one small source before the full run (that note was discarded and rebuilt)",
    "concepts": "4 concept notes regenerated after fix #2 in evidence/changes.md",
    "20260928-2106": "**second offline demonstration, Wi-Fi off**: the held-back `prioritization-framework.md` (the note itself took 42 s)",
}


def metrics_table(root: Path, label: str) -> str:
    p = root / "evidence" / "metrics" / f"{label}.json"
    if not p.exists():
        return "_Not measured yet._"
    m = json.loads(p.read_text())
    b = m.get("llama_cpp_breakdown", {})
    act, proj = b.get("actual_at_shutdown", {}), b.get("projected_at_load", {})
    gpu, host = act.get("gpu", {}), act.get("host", {})
    s = m["ask_summary"]
    peak = m.get("during_asks_peak", {})
    rows = [f"Measured {m['time']} with `scripts/measure.py` ([raw](evidence/metrics/{label}.json), "
            f"[llama.cpp log](evidence/metrics/measure-gemma-server.log)). Other apps were open, as on a normal day.", "",
            "| Memory | Value | Source |", "|---|---|---|",
            f"| **Gemma server, resident memory** | **{m['after_load']['gemma']['rss_mb']:,.0f} MB after load, "
            f"{peak.get('gemma', {}).get('rss_mb', 0):,.0f} MB peak while answering** | `ps` RSS, sampled every second |",
            f"| of which: model file, memory-mapped | {gpu.get('model_mib', 0):,} MiB (GPU view of the whole 4.9 GB file; the "
            f"{host.get('model_mib', 0):,} MiB of per-layer embedding tables read on the CPU are pages of the same file, not extra memory) "
            f"| llama.cpp buffer accounting |",
            f"| of which: KV cache for the 8,192-token context | {gpu.get('context_mib', 0)} MiB | llama.cpp |",
            f"| of which: compute buffers | {gpu.get('compute_mib', 0)} MiB GPU + {host.get('compute_mib', 0)} MiB CPU | llama.cpp |",
            f"| llama.cpp's fit projection at load | {proj.get('gpu', {}).get('self_mib', 0):,} MiB GPU + "
            f"{proj.get('host', {}).get('self_mib', 0):,} MiB host = {proj.get('gpu', {}).get('self_mib', 0) + proj.get('host', {}).get('self_mib', 0):,} MiB "
            f"(of the ~12 GB macOS lets the M2 GPU use) | llama.cpp |",
            f"| EmbeddingGemma server, resident memory | {peak.get('embed', {}).get('rss_mb', 0):,.0f} MB peak | `ps` RSS |",
            f"| `wiki` CLI process (a search) | {m['cli_search_process']['peak_rss_mb']} MB peak | `/usr/bin/time -l` |",
            f"| System memory in use, before → after loading both servers | {m['system_before']['used_gb']} → "
            f"{m['after_load']['system_used_gb']} GB, with {m['system_before']['swap_used_mb'] / 1024:.1f} GB swap already in use | `vm_stat`, `sysctl vm.swapusage` |",
            f"| Layers on the GPU | {b.get('layers_on_gpu', '?')} | llama.cpp |", "",
            "| Response time | Value |", "|---|---|",
            f"| Ask mode, end to end ({s['runs']} runs: 4 test questions × {s['runs'] // 4}, prompt cache off) | median **{s['median_total_s']:.1f} s**, "
            f"range {s['min_total_s']:.1f}–{s['max_total_s']:.1f} s |",
            f"| of which retrieval (BM25 + EmbeddingGemma query) | median {s['median_retrieval_s']:.2f} s |",
            f"| Prompt reading / answer writing speed | {s['median_prompt_tok_s']:.0f} / {s['median_gen_tok_s']:.1f} tokens per second |",
            "| Per question (median) | " + ", ".join(f"{k} {v:.1f} s" for k, v in s["per_test_median_s"].items()) + " |",
            f"| Gemma server start | {m.get('gemma_first_start_seconds', '?')} s the first time (file read from disk, Metal setup; "
            f"[log](evidence/metrics/first-start-gemma-server.log)); {m['gemma_load_seconds']} s on restart with the file cached |"]
    sys.path.insert(0, str(root / "scripts"))
    from measure import ingest_timings
    ingests = ingest_timings(config.load())
    if ingests:
        rows += ["", "| Ingestion run | Sources read | Model calls | Wall time | Tokens in / out | Note |", "|---|---|---|---|---|---|"]
        for r in ingests:
            note = next((v for k, v in INGEST_NOTES.items() if k in r["record"]), "")
            rows.append(f"| [{r['time']}]({r['record']}) | {r['files_ingested']} (+{r['files_unchanged']} unchanged) | "
                        f"{r['model_calls']} | {r['wall_seconds'] / 60:.1f} min | {r['prompt_tokens']:,} / {r['output_tokens']:,} | {note} |")
    # The offline ingest's own run record was overwritten by the re-ingest in the same second (fix 12);
    # its timing is taken from the offline transcript instead.
    for t in sorted((root / "evidence" / "offline").glob("transcript-*.txt")):
        text = t.read_text(errors="replace")
        note_s = re.search(r"-> wiki/\S+ .*?\((\d+) facts\) in (\d+)s", text)
        for m in re.finditer(r"Ingest finished in (\d+)s with (\S+) \((\w+)\): (\d+) ingested", text):
            rows.append(f"| [offline transcript]({t.relative_to(root).as_posix()}) | {m.group(4)} | (record overwritten, fix 12) | "
                        f"{int(m.group(1)) / 60:.1f} min | — | **first offline demonstration, Wi-Fi off**: the held-back Kickstarter "
                        f"source; the note itself took {note_s.group(2) if note_s else '?'} s, the rest was the concept and link passes |")
    return "\n".join(rows)


def vault_table(root: Path) -> str:
    notes = vault.all_notes()
    lint = vault.lint()
    by_folder = {}
    for n in notes:
        by_folder.setdefault(n.folder, []).append(n.title)
    from wiki.textparse import SUPPORTED
    raw = [p for p in (root / "vault" / "raw").rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED]
    rows = [f"{len(raw)} originals in `vault/raw/`, {len(notes)} notes in `vault/wiki/`. "
            f"`wiki check`: {lint['links']} links, {lint['broken_or_ambiguous']} broken or ambiguous, "
            f"{len(lint['errors'])} errors, {len(lint['warnings'])} warnings.", "",
            "| Folder | Notes |", "|---|---|"]
    for folder in vault.FOLDERS:
        titles = sorted(by_folder.get(folder, []))
        rows.append(f"| {folder} ({len(titles)}) | " + ", ".join(titles) + " |")
    return "\n".join(rows)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval-label", default="offline")
    ap.add_argument("--metrics-label", default="local")
    args = ap.parse_args()
    root = config.load().root
    readme_path = root / "README.md"
    text = readme_path.read_text()
    text = block(text, "eval", eval_table(root, args.eval_label))
    text = block(text, "online", eval_table(root, "online"))
    text = block(text, "details", details_block(root, args.eval_label))
    text = block(text, "metrics", metrics_table(root, args.metrics_label))
    text = block(text, "vault", vault_table(root))
    readme_path.write_text(text)
    print("README tables regenerated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
