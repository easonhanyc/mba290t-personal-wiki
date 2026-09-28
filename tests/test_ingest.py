from conftest import FakeModel

from wiki import ingest, vault

SOURCE = """---
title: "Demo Tracker — A Very Long Marketing Subtitle Here"
---
# Demo Tracker

## Results
The tracker served 120 users in its first week.

## Security
Row level security keeps each list private.
"""


def _plan(messages, schema):
    props = schema["properties"] if schema else {}
    if "folder" in props:
        return {"title": "demo-tracker-export-task-3f9a2c1d", "folder": "Projects",
                "summary": "A tracker. It served 120 users.",
                "key_facts": [{"fact": "The tracker served 120 users in its first week.", "section": "Results"},
                              {"fact": "The tracker served 999 users.", "section": "Results"},
                              {"fact": "Row level security keeps each list private.", "section": "Security"}],
                "concepts": [], "related": []}
    if "related" in props:
        return {"related": []}
    return {"facts": []}


def test_ingest_twice_no_duplicates_and_readable_name(project):
    raw = project / "vault" / "raw" / "projects"
    raw.mkdir(parents=True)
    (raw / "demo.md").write_text(SOURCE)
    model = FakeModel(_plan)
    s1 = ingest.ingest(model=model, log=lambda *_: None)
    notes = sorted(p.relative_to(project / "vault").as_posix() for p in (project / "vault" / "wiki").rglob("*.md"))
    # The machine-style proposal is rejected and the source title (minus subtitle) is used instead.
    assert notes == ["wiki/Projects/Demo Tracker.md"]
    note = vault.read_note(project / "vault" / notes[0])
    assert note.h1 == "Demo Tracker" and note.meta["sources"][0]["path"] == "raw/projects/demo.md"
    assert "999" not in note.body and any("999" in d["fact"] for d in s1["dropped_facts"])
    assert "[[raw/projects/demo#Security|" in note.body
    calls_after_first = len(model.calls)
    s2 = ingest.ingest(model=model, log=lambda *_: None)
    assert s2["files"] == {"raw/projects/demo.md": "unchanged"}
    assert len(model.calls) == calls_after_first
    again = sorted(p.relative_to(project / "vault").as_posix() for p in (project / "vault" / "wiki").rglob("*.md"))
    assert again == notes
    index = (project / "vault" / "index.md").read_text()
    assert "[[Demo Tracker]]" in index


def test_forced_reingest_keeps_path_and_protects_reviewed(project):
    raw = project / "vault" / "raw"
    (raw / "demo.md").write_text(SOURCE)
    model = FakeModel(_plan)
    ingest.ingest(model=model, log=lambda *_: None)
    path = project / "vault" / "wiki" / "Projects" / "Demo Tracker.md"
    note = vault.read_note(path)
    note.meta["reviewed"] = True
    note.body = note.body.replace("A tracker.", "A tracker (checked by hand).")
    vault.write_note(note)
    ingest.ingest(force=True, model=model, log=lambda *_: None)
    files = list((project / "vault" / "wiki").rglob("*.md"))
    assert files == [path]
    assert "checked by hand" in path.read_text()


def test_external_file_is_copied_unchanged(project, tmp_path):
    outside = tmp_path / "elsewhere"
    outside.mkdir()
    src = outside / "note.md"
    src.write_text(SOURCE)
    model = FakeModel(_plan)
    ingest.ingest([str(src)], into="imported", model=model, log=lambda *_: None)
    copied = project / "vault" / "raw" / "imported" / "note.md"
    assert copied.read_bytes() == src.read_bytes()


def test_merge_notes_moves_facts_links_and_catalog(project, monkeypatch):
    raw = project / "vault" / "raw"
    (raw / "a.md").write_text("# Alpha Tool\n\n## Results\nThe tool served 120 users.\n")
    (raw / "b.md").write_text("# Alpha Tool Notes\n\n## Method\nIt was built in Python.\n")
    titles = iter(["Alpha Tool", "Zeta Method Study"])

    def plan(messages, schema):
        props = schema["properties"] if schema else {}
        if "folder" in props:
            text = messages[-1]["content"]
            fact = ("The tool served 120 users.", "Results") if "120" in text else ("It was built in Python.", "Method")
            return {"title": next(titles), "folder": "Projects", "summary": "S.", "key_facts": [{"fact": fact[0], "section": fact[1]}],
                    "concepts": [], "related": []}
        return {"related": []}

    ingest.ingest(model=FakeModel(plan), log=lambda *_: None)
    assert len(list((project / "vault" / "wiki").rglob("*.md"))) == 2
    monkeypatch.setattr(ingest, "get_model", lambda mode="local": FakeModel(plan))
    ingest.merge_notes("Alpha Tool", "Zeta Method", log=lambda *_: None)
    files = [p.name for p in (project / "vault" / "wiki").rglob("*.md")]
    assert files == ["Alpha Tool.md"]
    body = (project / "vault" / "wiki" / "Projects" / "Alpha Tool.md").read_text()
    assert "120 users" in body and "built in Python" in body
    import json
    cat = json.loads((project / "data" / "catalog.json").read_text())
    assert cat["sources"]["raw/b.md"]["notes"] == ["wiki/Projects/Alpha Tool.md"]


def test_merged_subject_is_not_recreated_by_a_later_ingest(project, monkeypatch):
    """Regression (offline run 2026-09-28): a later ingest re-created the merged-away 'Agentic AI' note."""
    raw = project / "vault" / "raw"
    for name in ("a", "b", "c"):
        (raw / f"{name}.md").write_text(f"# Tool {name.upper()}\n\n## Notes\nTool {name} uses agents.\n")
    titles = iter(["Tool Alpha", "Tool Beta", "Tool Gamma"])

    def plan(messages, schema):
        props = schema["properties"] if schema else {}
        if "folder" in props:
            return {"title": next(titles), "folder": "Projects", "summary": "S.",
                    "key_facts": [{"fact": "It uses agents.", "section": "Notes"}],
                    "concepts": [{"name": "Agent Systems", "why": "uses agents"}], "related": []}
        if "key_facts" in props:  # concept note
            return {"summary": "Agents.", "key_facts": [{"fact": "Tool a uses agents.", "passage": "P1"}]}
        return {"related": []}

    model = FakeModel(plan)
    monkeypatch.setattr(ingest, "get_model", lambda mode="local": model)
    ingest.ingest([str(raw / "a.md"), str(raw / "b.md")], model=model, log=lambda *_: None)
    concept = project / "vault" / "wiki" / "Concepts" / "Agent Systems.md"
    assert concept.exists()
    ingest.merge_notes("Tool Alpha", "Agent Systems", log=lambda *_: None)
    assert not concept.exists()
    ingest.ingest([str(raw / "c.md")], model=model, log=lambda *_: None)   # a new source triggers the concept pass
    assert not concept.exists()
    import json
    assert json.loads((project / "data" / "catalog.json").read_text())["redirects"]["Agent Systems"] == "Tool Alpha"
