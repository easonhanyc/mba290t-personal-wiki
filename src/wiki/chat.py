"""Interactive chat loop (the terminal side of harness.ChatSession)."""

from __future__ import annotations

import sys
from pathlib import Path

from . import ui
from .harness import ChatSession

HELP = """Chat commands:
  /notes <topic>   look this up in the wiki and answer with it
  /sources         show the notes behind my last reply
  /save            save my last reply to drafts/ (drafts are never treated as sources)
  /reset           forget this conversation
  /help            this list
  /exit            quit (Ctrl-D also works)"""


def show_turn(turn) -> None:
    r = turn.route
    if r.retrieve:
        print(ui.dim(f"  (looked up notes: {r.reason}; query \"{r.query[:70]}\" -> {len(turn.notes)} passages)"))
    else:
        print(ui.dim(f"  (no notes lookup: {r.reason})"))
    print(f"\n{ui.bold('Wren ›')} {turn.reply}\n")
    if turn.checks.get("stray_tags_removed"):
        print(ui.dim(f"  (removed {' '.join(turn.checks['stray_tags_removed'])}: no notes were used for this reply)"))
    if turn.notes:
        for i, h in enumerate(turn.notes, 1):
            print(ui.dim(f"  [N{i}] {h.chunk.location} › {h.chunk.section}"))
        status = turn.checks.get("status")
        if status not in ("ok", None):
            print(ui.dim(f"  citation check: {status}"))
        print()
    print(ui.dim(f"  {turn.timings['total_s']:.1f}s"))


def run(mode: str = "local", script: str | None = None) -> int:
    session = ChatSession(mode=mode)
    session.model.require()
    print(ui.header("chat", session.model.describe()))
    print("Wren here, your chief of staff. Ask me anything, or type /help. /exit to quit.\n")
    lines = None
    if script:
        lines = [l.rstrip("\n") for l in Path(script).read_text(encoding="utf-8").splitlines() if l.strip()]
    while True:
        if lines is not None:
            if not lines:
                break
            message = lines.pop(0)
            print(f"{ui.bold('you ›')} {message}")
        else:
            try:
                message = input(ui.bold("you › ")).strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
        if not message:
            continue
        if message in ("/exit", "/quit"):
            break
        if message == "/help":
            print(HELP)
            continue
        if message == "/reset":
            session.reset()
            print(ui.dim("  (conversation cleared)"))
            continue
        if message == "/sources":
            if session.last and session.last.notes:
                for i, h in enumerate(session.last.notes, 1):
                    print(f"[N{i}] {h.chunk.location} › {h.chunk.section}\n{h.chunk.text}\n")
            else:
                print(ui.dim("  (my last reply did not use any notes)"))
            continue
        if message == "/save":
            path = session.save_last()
            print(ui.dim(f"  saved to {path}" if path else "  (nothing to save yet)"))
            continue
        force = None
        if message.startswith("/notes"):
            force = message[len("/notes"):].strip()
            if not force:
                print("usage: /notes <topic>")
                continue
            message = f"What do my notes say about {force}?"
        show_turn(session.turn(message, force_query=force))
    print(ui.dim(f"  chat log: {session.log_path}"))
    return 0


if __name__ == "__main__":
    sys.exit(run())
