from wiki import vault


def test_clean_title_drops_subtitles_and_generic_tails():
    assert vault.clean_title("Action Hub — Ranked Alerts with Next Actions") == "Action Hub"
    assert vault.clean_title("Amazon Web Services Experience") == "Amazon Web Services"
    assert vault.clean_title("row level security") == "Row Level Security"


def test_machine_style_names_are_rejected():
    bad = "class4-gpu-parallel-training-visual--task-1-gpu-parallel-training-slide-visual--c8d92e24fd"
    assert vault.naming_problems(bad)
    assert vault.naming_problems("How does the app keep users apart?")
    assert vault.naming_problems("Notes 2026-09-26")
    assert vault.naming_problems("GPU Parallel Training") == []
    assert vault.naming_problems("Memory - Computers") == []


def test_similar_titles_merge_but_different_subjects_do_not():
    assert vault.similar("Ms. Pac-Man DQN", "Ms. Pac-Man DQN Agent")
    assert vault.similar("Pac-Man DQN Methodology Study", "Ms. Pac-Man DQN Implementation")
    assert not vault.similar("Row Level Security", "Secure Networking Tracker")
    assert not vault.similar("GenAI Target Setting", "GenAI Adoption Program")


def _note(project, folder, title, body_links, source="raw/s.md", reviewed=True):
    note = vault.Note(path=project / "vault" / "wiki" / folder / f"{title}.md",
                      meta={"title": title, "summary": f"About {title}.", "reviewed": reviewed},
                      body=f"# {title}\n\nText.\n\n## Key facts\n- Fact ([[{source[:-3]}|s]])\n\n## Related notes\n{body_links}\n")
    vault.write_note(note)
    return note


def test_lint_finds_broken_links_and_passes_clean_vault(project):
    (project / "vault" / "raw" / "s.md").write_text("# S\n\nx\n")
    _note(project, "Concepts", "Alpha Topic", "- [[Beta Topic]] — shares data.")
    _note(project, "Concepts", "Beta Topic", "- [[Alpha Topic]] — shares data.")
    vault.render_index()
    vault.render_catalog({"sources": {}})
    report = vault.lint()
    assert report["errors"] == [], report["errors"]
    _note(project, "Concepts", "Gamma Topic", "- [[Missing Topic]] — nope.")
    vault.render_index()
    report = vault.lint()
    assert any("broken link [[Missing Topic]]" in e for e in report["errors"])


def test_rename_updates_incoming_links_and_heading(project):
    (project / "vault" / "raw" / "s.md").write_text("# S\n\nx\n")
    _note(project, "Concepts", "Old Name", "- [[Beta Topic]] — x.")
    _note(project, "Concepts", "Beta Topic", "- [[Old Name]] — why. Also [[Old Name|alias]].")
    vault.rename_note("Old Name", "New Name")
    beta = (project / "vault" / "wiki" / "Concepts" / "Beta Topic.md").read_text()
    assert "[[New Name]]" in beta and "[[New Name|alias]]" in beta and "Old Name" not in beta
    new = vault.read_note(project / "vault" / "wiki" / "Concepts" / "New Name.md")
    assert new.h1 == "New Name" and new.meta["previous_names"] == ["Old Name"]
    assert not (project / "vault" / "wiki" / "Concepts" / "Old Name.md").exists()
