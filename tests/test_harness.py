import inspect
import json

from conftest import FakeModel

from wiki import harness, retrieval


def _hit(text, path="raw/a.md"):
    return retrieval.Hit(chunk=retrieval.Chunk(id="x", kind="source", path=path, title="A", section="S",
                                               line_start=1, line_end=2, text=text), score=1.0, bm25_rank=1, vector_rank=None)


def test_citation_check_statuses():
    hits = [_hit("Attendance is worth 20% of the grade."), _hit("One absence has no penalty.")]
    ok = harness.check_citations("Attendance is 20% of the grade [S1]. One absence is allowed [S2].", hits)
    assert ok["status"] == "ok" and ok["cited"] == [1, 2]
    bad_num = harness.check_citations("Attendance is 25% of the grade [S1].", hits)
    assert bad_num["status"] == "citation-problems" and bad_num["numbers_not_in_cited_passages"][0]["number"] == "25%"
    unknown = harness.check_citations("Attendance matters a great deal here [S7].", hits)
    assert unknown["unknown_ids"] == [7]
    assert harness.check_citations("Insufficient evidence: the sources do not state a grade.", hits)["status"] == "insufficient-evidence"
    assert harness.check_citations("Attendance is important for the course overall.", hits)["status"] == "no-citations"


def _small_index(project):
    raw = project / "vault" / "raw"
    (raw / "syllabus.md").write_text("# Syllabus\n\n## Attendance\n\nAttendance is required and is worth 20% of your grade.\n")
    (raw / "pacman.md").write_text("# Pac-Man\n\n## Results\n\nThe trained agent scored 906 against a 492 baseline.\n")
    retrieval.build_index()
    return retrieval.Index()


def test_ask_has_no_history_parameter_and_sends_only_rules_and_evidence(project):
    assert set(inspect.signature(harness.ask).parameters) == {"question", "mode", "model", "index", "k", "save"}
    model = FakeModel(lambda m, s: "Attendance is worth 20% of the grade [S1].")
    r = harness.ask("How much is attendance worth?", model=model, index=_small_index(project))
    sent = model.calls[0]["messages"]
    assert [m["role"] for m in sent] == ["system", "user"]
    assert "Research rules" in sent[0]["content"] and "Wren" not in sent[0]["content"]
    assert r.checks["status"] == "ok"
    saved = json.loads((project / r.run_file).read_text())
    assert saved["messages_sent_to_model"] == sent and saved["execution"] == "local"


def test_persona_states_where_the_model_runs(project):
    local = harness.ChatSession(model=FakeModel(), index=_small_index(project)).system
    online_model = FakeModel()
    online_model.mode = "online"
    online = harness.ChatSession(model=online_model, index=_small_index(project)).system
    assert "on his laptop" in local and "Google" not in local
    assert "sent to Google" in online and "on his laptop" not in online
    assert "{runtime}" not in local + online


def test_chat_claim_does_not_reach_ask(project):
    idx = _small_index(project)
    chat_model = FakeModel(lambda m, s: "Noted!" if s is None else {"needs_notes": False, "query": ""})
    session = harness.ChatSession(model=chat_model, index=idx)
    session.turn("By the way, my favorite programming language is Rust.")
    ask_model = FakeModel(lambda m, s: "Insufficient evidence: the sources do not name a favorite language.")
    r = harness.ask("What is my favorite programming language?", model=ask_model, index=idx)
    # Whether or not a passage matched, the prompt ask builds (and saves) never contains chat text.
    assert "Rust" not in json.dumps(r.messages)
    assert "Rust" not in (project / r.run_file).read_text()
    assert r.checks["insufficient_evidence"]


def test_chat_router_casual_personal_and_followup(project):
    idx = _small_index(project)
    model = FakeModel(lambda m, s: {"needs_notes": False, "query": ""} if s else "Here is a plan.")
    session = harness.ChatSession(model=model, index=idx)
    assert not session.route("what can you help me with?").retrieve
    assert not session.route("make that shorter").retrieve
    assert not session.route("Draft a short plan for my week: I need to finish Assignment 4.").retrieve
    assert session.route("What did my Pac-Man agent score?").retrieve
    t1 = session.turn("Draft a three-step plan for tomorrow.")
    assert not t1.route.retrieve
    session.turn("make that shorter")
    last_messages = model.calls[-1]["messages"]
    assert any(m["role"] == "assistant" and m["content"] == "Here is a plan." for m in last_messages)
    assert last_messages[-1]["content"] == "make that shorter"


def test_chat_retrieval_attaches_notes_but_history_keeps_plain_message(project):
    idx = _small_index(project)
    model = FakeModel(lambda m, s: "It scored 906 [N1].")
    session = harness.ChatSession(model=model, index=idx)
    turn = session.turn("What did my Pac-Man agent score?")
    assert turn.route.retrieve and turn.notes
    assert "NOTES FROM THE WIKI" in model.calls[-1]["messages"][-1]["content"]
    assert session.history[0]["content"] == "What did my Pac-Man agent score?"
    assert turn.checks["status"] == "ok" and "Notes used" not in turn.reply


def test_chat_lists_notes_when_reply_tags_none(project):
    """Fix 11: a draft built from notes but with no [N#] tags still shows which notes it used."""
    idx = _small_index(project)
    session = harness.ChatSession(model=FakeModel(lambda m, s: "Here is a post about the agent."), index=idx)
    turn = session.turn("What did my Pac-Man agent score?")
    assert turn.notes and turn.checks["status"] == "no-citations" and turn.checks["notes_listed_by_harness"]
    assert "Notes used (not tagged claim by claim): [N1]" in turn.reply
    assert session.history[-1]["content"] == "Here is a post about the agent."   # history keeps the model's text


def test_generic_title_words_do_not_trigger_lookup(project):
    """Regression (dry run 2026-09-27): 'PM internship applications' matched the note 'TikTok Internship'."""
    idx = _small_index(project)
    note = project / "vault" / "wiki" / "Experience" / "TikTok Internship.md"
    note.parent.mkdir(parents=True, exist_ok=True)
    note.write_text("---\ntitle: TikTok Internship\n---\n\n# TikTok Internship\n")
    session = harness.ChatSession(model=FakeModel(lambda m, s: {"needs_notes": False, "query": ""}), index=idx)
    assert not session.route("Draft a short plan for my week: I need to prep for PM internship applications.").retrieve
    assert session.route("How did the internship at TikTok go?").retrieve


def test_note_tags_without_notes_are_removed(project):
    """Fix 16 (offline-2 M1): a capability answer ended with "[N1]" although no notes were supplied."""
    idx = _small_index(project)
    session = harness.ChatSession(model=FakeModel(lambda m, s: "I can check your notes [N1]. Or [N2, N3] too."), index=idx)
    turn = session.turn("what can you help me with?")
    assert not turn.notes and turn.reply == "I can check your notes. Or too."
    assert turn.checks["stray_tags_removed"] == ["[N1]", "[N2, N3]"]
