"""Experiment (not used by the harness): two-level retrieval, the improvement first proposed in the README.

Level 1 ranks wiki notes only and keeps the top N notes; level 2 ranks only the originals those notes cite
(plus the notes). The table compares where each expected passage lands: global search as ask uses it,
level 2 alone, and the two rankings fused. No language model is called.

    python scripts/retrieval_two_level.py        # writes evidence/retrieval/two-level-notes-first.md
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import yaml

from wiki import config, retrieval, vault

sys.path.insert(0, str(Path(__file__).parent))
from retrieval_check import matches  # noqa: E402


def ranked(idx: retrieval.Index, query: str, mask: np.ndarray) -> list[int]:
    r = idx.settings.retrieval
    bm = idx.bm25.scores(retrieval.tokenize(query))
    bm_order = [i for i in np.argsort(-bm) if bm[i] > 0 and mask[i]][: r["candidates"]]
    cos = idx.vectors @ idx.embedder.embed_query(query)
    vec_order = [i for i in np.argsort(-cos) if mask[i]][: r["candidates"]]
    fused: dict[int, float] = {}
    for order in (bm_order, vec_order):
        for n, i in enumerate(order, 1):
            fused[i] = fused.get(i, 0.0) + 1.0 / (r["rrf_k"] + n)
    return sorted(fused, key=lambda i: -fused[i])


def main() -> int:
    settings = config.load()
    idx = retrieval.Index(settings)
    if idx.vectors is None or not idx.embedder.available():
        print("Needs the embedding server: wiki serve start --only embed")
        return 1
    tests = yaml.safe_load((settings.root / "tests" / "questions.yaml").read_text())["ask_tests"]
    notes = {n.title: n for n in vault.all_notes(settings)}
    everything = np.ones(len(idx.chunks), bool)
    wiki_only = np.array([c.kind == "wiki" for c in idx.chunks])

    def position(order, expected):
        return next((n for n, i in enumerate(order, 1) if matches(idx.chunks[i], expected)), None)

    md = ["# Retrieval experiment: two-level (notes first, then their sources)", "",
          f"Run {datetime.now().isoformat(timespec='seconds')}, {len(idx.chunks)} passages. Ask gives Gemma the top 6, so "
          "a position above 6 means Gemma never sees the passage. Script: `scripts/retrieval_two_level.py`.", "",
          "| Notes kept | Test | Notes chosen at level 1 | Passages searched at level 2 | Expected evidence: global / level 2 only / fused |",
          "|---|---|---|---|---|"]
    for keep in (1, 2, 3):
        for t in tests:
            top: list[str] = []
            for i in ranked(idx, t["question"], wiki_only):
                if idx.chunks[i].path not in top:
                    top.append(idx.chunks[i].path)
                if len(top) == keep:
                    break
            sources = set(top)
            for path in top:
                note = notes.get(Path(path).stem)
                sources |= {s["path"] for s in (note.meta.get("sources", []) if note else [])}
            scoped = np.array([c.path in sources for c in idx.chunks])
            glob, level2 = ranked(idx, t["question"], everything), ranked(idx, t["question"], scoped)
            fused: dict[int, float] = {}
            for order in (glob, level2):
                for n, i in enumerate(order, 1):
                    fused[i] = fused.get(i, 0.0) + 1.0 / (60 + n)
            both = sorted(fused, key=lambda i: -fused[i])
            cells = "; ".join(f"E{j}: {position(glob, e) or '—'} / {position(level2, e) or '—'} / {position(both, e) or '—'}"
                              for j, e in enumerate(t["expected_evidence"], 1)) or "n/a (unsupported)"
            md.append(f"| {keep} | {t['id']} | {', '.join(Path(p).stem for p in top)} | {int(scoped.sum())} | {cells} |")
    md += ["", "— = not found among the ranked candidates.", ""]
    dest = settings.root / "evidence" / "retrieval" / "two-level-notes-first.md"
    dest.write_text("\n".join(md))
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
