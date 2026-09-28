"""Print each generated note fact next to the source section it cites, for the manual review pass.

    python scripts/review_notes.py                 # every unreviewed note
    python scripts/review_notes.py "Action Hub"    # one note

For each fact: the words it shares with the cited section (a low overlap is a prompt to read closely,
not a verdict). The reviewer then fixes the note text and records the change in evidence/wiki_review.md.
"""

from __future__ import annotations

import re
import sys

from wiki import config, vault
from wiki.retrieval import tokenize
from wiki.textparse import parse_file

LINK = re.compile(r"\(\[\[(raw/[^\]|#]+)(#[^\]|]*)?\|[^\]]*\]\]\)\s*$")


def section_text(rel_raw: str, heading: str | None) -> str:
    vault_dir = config.load().vault
    path = vault_dir / rel_raw
    if not path.exists():
        path = vault_dir / f"{rel_raw}.md"
    doc = parse_file(path)
    if heading:
        for s in doc.sections:
            if s.heading.lower() == heading.lower():
                return " ".join(b.text for b in s.blocks)
    return " ".join(b.text for s in doc.sections for b in s.blocks)


def main() -> int:
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for note in vault.all_notes():
        if only and note.title != only:
            continue
        if not only and note.meta.get("reviewed"):
            continue
        print(f"\n######## {note.rel(config.load().vault)}\nSUMMARY: {note.meta.get('summary', '')}")
        for line in note.body.splitlines():
            m = LINK.search(line)
            if not line.startswith("- ") or not m:
                continue
            fact = LINK.sub("", line[2:]).strip()
            heading = m.group(2)[1:] if m.group(2) else None
            src = section_text(m.group(1), heading)
            ft, st = set(tokenize(fact)), set(tokenize(src))
            overlap = len(ft & st) / max(1, len(ft))
            print(f"\n- FACT ({overlap:.0%} word overlap): {fact}\n  CITES: {m.group(1)} › {heading or '(whole file)'}")
            print(f"  SOURCE: {src[:700]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
