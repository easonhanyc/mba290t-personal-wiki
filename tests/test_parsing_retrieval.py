from pathlib import Path

from wiki import retrieval
from wiki.textparse import parse_file

MD = """---
title: "Demo Project"
role: "Builder"
order: 3
---
Intro line.

## Results
<figure><svg viewBox="0 0 10 10">
<title id="t">Score rose from 492 to 906</title>
<rect/>
</svg></figure>

Mean score rose from **492 to 906**.

## Limits
- first
- second
"""


def test_markdown_front_matter_svg_and_line_numbers(tmp_path):
    p = tmp_path / "demo.md"
    p.write_text(MD)
    doc = parse_file(p)
    assert doc.title == "Demo Project"
    props = doc.sections[0]
    assert props.kind == "properties" and "role: Builder" in props.blocks[0].text and "order" not in props.blocks[0].text
    results = next(s for s in doc.sections if s.heading == "Results")
    text = "\n".join(b.text for b in results.blocks)
    assert "[Figure: Score rose from 492 to 906]" in text and "<rect" not in text
    # The figure spans source lines 9-12; the sentence after it must still report its true line, 14.
    assert any(b.line == 14 and b.text.startswith("Mean score") for b in results.blocks)
    limits = next(s for s in doc.sections if s.heading == "Limits")
    assert limits.blocks[0].text == "- first\n- second" and limits.blocks[0].line == 17


def test_html_sections_follow_headings(tmp_path):
    p = tmp_path / "page.html"
    p.write_text("<html><title>Syl</title><nav>Home Menu</nav><h2>Attendance</h2><p>Worth 20%.</p>"
                 "<h2>Grading</h2><table><tr><td>Attendance</td><td>20%</td></tr></table></html>")
    doc = parse_file(p)
    labels = [s.label for s in doc.sections]
    assert labels == ["Attendance", "Grading"]
    assert "Home Menu" not in " ".join(b.text for s in doc.sections for b in s.blocks)


def test_long_table_is_split_under_char_cap():
    rows = "\n".join(f"| {i} | {i * 1.2345:.4f} | {i * 2.5:.4f} | {i * 3.75:.4f} |" for i in range(200))
    parts = retrieval._split_long(rows, 300)
    assert len(parts) > 1 and all(len(p) <= retrieval.MAX_CHARS for p in parts)


def test_tokenizer_keeps_numbers_and_strips_possessives():
    toks = retrieval.tokenize("Someone else's list: 20% at 0.0001 policies")
    assert "else" in toks and "20%" in toks and "0.0001" in toks and "polici" in toks


def test_bm25_prefers_matching_passage():
    docs = [retrieval.tokenize(t) for t in ["attendance is worth 20% of the grade", "the agent scored 906", "unrelated text"]]
    scores = retrieval.BM25(docs).scores(retrieval.tokenize("how much is attendance worth"))
    assert scores.argmax() == 0


def test_index_search_bm25_only_without_embedder(project):
    raw = project / "vault" / "raw"
    (raw / "a.md").write_text("# Alpha\n\nAttendance is worth 20% of the grade.\n")
    (raw / "b.md").write_text("# Beta\n\nThe agent scored 906 points.\n")
    stats = retrieval.build_index()
    assert stats["passages"] == 2 and stats["vectors"] is False
    idx = retrieval.Index()
    hits = idx.search("attendance grade share")
    assert hits[0].chunk.path == "raw/a.md" and "BM25 only" in idx.last_method
