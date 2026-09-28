"""Score retrieval alone (no language model) for the ask tests in tests/questions.yaml.

For each test: which passages come back, from which ranker, and whether each expected evidence
item appears in the top-k passages that ask mode would hand to Gemma.

    python scripts/retrieval_check.py --label baseline-sources-only
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import yaml

from wiki import config, retrieval


def matches(chunk: retrieval.Chunk, expected: dict) -> bool:
    if chunk.path != expected["path"].removeprefix("vault/"):
        return False
    section = expected.get("section", "any")
    if section != "any" and section.lower() not in chunk.section.lower():
        return False
    return all(s.lower() in chunk.text.lower() for s in expected["must_contain"])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--use", choices=["hybrid", "bm25", "vector"], default="hybrid")
    args = ap.parse_args()
    settings = config.load()
    tests = yaml.safe_load((settings.root / "tests" / "questions.yaml").read_text())["ask_tests"]
    idx = retrieval.Index(settings)
    k = settings.retrieval["top_k"]
    out = {"label": args.label, "time": datetime.now().isoformat(timespec="seconds"), "top_k": k,
           "passages_indexed": len(idx.chunks), "tests": []}
    md = [f"# Retrieval check: {args.label}", "",
          f"Run {out['time']}. {len(idx.chunks)} passages indexed; top-{k} shown (what ask mode passes to Gemma). "
          "No language model is called.", ""]
    for t in tests:
        hits = idx.search(t["question"], k=k, use=args.use)
        rows, found = [], {}
        for n, h in enumerate(hits, 1):
            tags = [f"E{j + 1}" for j, e in enumerate(t["expected_evidence"]) if matches(h.chunk, e)]
            for tag in tags:
                found.setdefault(tag, n)
            rows.append({"rank": n, "location": h.chunk.location, "kind": h.chunk.kind, "section": h.chunk.section,
                         "bm25_rank": h.bm25_rank, "vector_rank": h.vector_rank, "expected": tags,
                         "text": h.chunk.text})
        expected = [{"id": f"E{j + 1}", **e, "found_at_rank": found.get(f"E{j + 1}")}
                    for j, e in enumerate(t["expected_evidence"])]
        out["tests"].append({"id": t["id"], "question": t["question"], "method": idx.last_method,
                             "expected": expected, "results": rows})
        md += [f"## {t['id']}: {t['question']}", "", f"Method: {idx.last_method}", ""]
        if expected:
            md.append("| Expected evidence | Found at rank |")
            md.append("|---|---|")
            for e in expected:
                md.append(f"| {e['id']}: `{e['path']}` › {e['section']} (must contain {', '.join(e['must_contain'])}) "
                          f"| {e['found_at_rank'] or f'not in top {k}'} |")
        else:
            md.append("No supporting passage exists (unsupported question); these are the distractors retrieved.")
        md += ["", "| Rank | Passage | Section | BM25 rank | Vector rank | Matches |", "|---|---|---|---|---|---|"]
        for r in rows:
            md.append(f"| {r['rank']} | `{r['location']}` | {r['section']} | {r['bm25_rank'] or '-'} | "
                      f"{r['vector_rank'] or '-'} | {', '.join(r['expected'])} |")
        md.append("")
    dest = settings.root / "evidence" / "retrieval"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f"{args.label}.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    (dest / f"{args.label}.md").write_text("\n".join(md))
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
