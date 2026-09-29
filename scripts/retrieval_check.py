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

from wiki import config, harness, retrieval


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
    ap.add_argument("--no-openings", action="store_true",
                    help="top-k only, without adding section openings (how retrieval worked before fix 14)")
    args = ap.parse_args()
    settings = config.load()
    tests = yaml.safe_load((settings.root / "tests" / "questions.yaml").read_text())["ask_tests"]
    idx = retrieval.Index(settings)
    k = settings.retrieval["top_k"]
    out = {"label": args.label, "time": datetime.now().isoformat(timespec="seconds"), "top_k": k,
           "passages_indexed": len(idx.chunks), "tests": []}
    md = [f"# Retrieval check: {args.label}", "",
          f"Run {out['time']}. {len(idx.chunks)} passages indexed; top-{k}"
          + ("" if args.no_openings else " plus the opening passage of each retrieved section, within the evidence budget")
          + " (what ask mode passes to Gemma). No language model is called.", ""]
    budget = settings.section("ask")["evidence_token_budget"]
    for t in tests:
        hits = idx.search(t["question"], k=k, use=args.use)
        if not args.no_openings:
            hits = harness.select_within(idx.add_section_openings(hits), budget)
        rows, found = [], {}
        for n, h in enumerate(hits, 1):
            tags = [f"E{j + 1}" for j, e in enumerate(t["expected_evidence"]) if matches(h.chunk, e)]
            for tag in tags:
                found.setdefault(tag, n)
            rows.append({"rank": n, "location": h.chunk.location, "kind": h.chunk.kind, "section": h.chunk.section,
                         "bm25_rank": h.bm25_rank, "vector_rank": h.vector_rank, "expected": tags,
                         "opens_section_of": h.opens_section_of,
                         "text": h.chunk.text})
        expected = [{"id": f"E{j + 1}", **e, "found_at_rank": found.get(f"E{j + 1}")}
                    for j, e in enumerate(t["expected_evidence"])]
        out["tests"].append({"id": t["id"], "question": t["question"], "method": idx.last_method,
                             "expected": expected, "results": rows})
        md += [f"## {t['id']}: {t['question']}", "", f"Method: {idx.last_method}", ""]
        if expected:
            md.append("| Expected evidence | Position in what Gemma receives |")
            md.append("|---|---|")
            for e in expected:
                md.append(f"| {e['id']}: `{e['path']}` › {e['section']} (must contain {', '.join(e['must_contain'])}) "
                          f"| {e['found_at_rank'] or 'not retrieved'} |")
        else:
            md.append("No supporting passage exists (unsupported question); these are the distractors retrieved.")
        md += ["", "| Rank | Passage | Section | BM25 rank | Vector rank | Matches |", "|---|---|---|---|---|---|"]
        for r in rows:
            ranks = (f"{r['bm25_rank'] or '-'} | {r['vector_rank'] or '-'}" if not r["opens_section_of"] else
                     f"added: opens the section of `{r['opens_section_of']}` | added")
            md.append(f"| {r['rank']} | `{r['location']}` | {r['section']} | {ranks} | {', '.join(r['expected'])} |")
        md.append("")
    dest = settings.root / "evidence" / "retrieval"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f"{args.label}.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    (dest / f"{args.label}.md").write_text("\n".join(md))
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
