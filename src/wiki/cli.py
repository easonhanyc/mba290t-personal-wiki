"""`wiki` command line: parses the command, calls the harness, prints the result, maps errors to messages."""

from __future__ import annotations

import argparse
import json
import sys
import textwrap

from . import __version__, config, serve, ui
from .llm import ModelError, ModelUnavailable

OVERVIEW = """\
Personal wiki CLI: your own notes + a local Gemma model, fully offline by default.

commands:
  ingest [PATH...]    read sources, write/update wiki notes with local Gemma, rebuild index.md and the search index
  search "words"      show matching ORIGINAL passages and their paths (no model, no generated answer)
  ask "question"      one neutral, cited answer from retrieved evidence, or "Insufficient evidence"
  chat                talk to Wren, your assistant; remembers the conversation, looks up notes only when needed
  serve start|stop|status   run the local model servers (Gemma on :8080, EmbeddingGemma on :8081)
  check               lint the vault: file names, headings, links, source references, index coverage
  rename OLD NEW      rename a note and update every link, the catalog and the index
  merge KEEP REMOVE   fold a duplicate note into another (facts, sources, links, catalog)
  status              show configuration, models, servers and index size
  help [COMMAND]      this overview, or details for one command

execution setting:
  --mode local        (default) llama.cpp on 127.0.0.1 with the Gemma file named in config/settings.toml
  --mode online       optional: hosted Gemma via the Gemini API; needs $GEMINI_API_KEY; never used as a fallback

configuration and inputs:
  config/settings.toml   model files, endpoints, context size, retrieval and prompt budgets
  config/sources.toml    where each original came from (repo + commit or URL)
  instructions/          persona.md (chat), research-rules.md (ask), ingest-rules.md (note writing)
  vault/raw/             original sources, never modified (.md .txt .html)
  vault/wiki/            generated notes in topic folders; vault/index.md is the landing page
  data/ runs/            machine files: catalog, passages, vectors, and a JSON record of every ask/chat/ingest

typical session:
  wiki serve start
  wiki ingest vault/raw
  wiki search "row level security"
  wiki ask "What share of the final grade is attendance?"
  wiki chat
"""


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="wiki", description=OVERVIEW, formatter_class=argparse.RawDescriptionHelpFormatter,
                                usage="wiki [-h] [--version] COMMAND ...")
    p.add_argument("--version", action="version", version=f"wiki {__version__}")
    sub = p.add_subparsers(dest="command", metavar="COMMAND")

    s = sub.add_parser("ingest", help="read sources and update the wiki", description=textwrap.dedent("""\
        Read local sources, have local Gemma write or update one wiki note per subject, then rebuild
        vault/index.md, vault/Source Catalog.md and the retrieval index. Unchanged files (same sha256)
        are skipped, so re-running never creates duplicate notes. Files outside vault/raw are copied
        into vault/raw/<--into> byte-for-byte first."""), formatter_class=argparse.RawDescriptionHelpFormatter)
    s.add_argument("paths", nargs="*", help="files or folders (default: vault/raw)")
    s.add_argument("--force", action="store_true", help="re-read sources even if unchanged (same note paths are reused)")
    s.add_argument("--overwrite-reviewed", action="store_true", help="allow regenerating notes marked reviewed")
    s.add_argument("--dry-run", action="store_true", help="show what would happen without calling the model")
    s.add_argument("--into", default="imported", help="subfolder of vault/raw for files copied from elsewhere")

    s = sub.add_parser("search", help="show original passages (no model)", description=
                       "Retrieval only: BM25 + EmbeddingGemma vectors fused by rank. Prints passages and source "
                       "locations; never generates an answer. Works with the Gemma server stopped.")
    s.add_argument("query")
    s.add_argument("-k", type=int, default=None, help="number of passages (default from settings)")
    s.add_argument("--kind", choices=["all", "source", "wiki"], default="all", help="originals, notes, or both")
    s.add_argument("--json", action="store_true")

    s = sub.add_parser("ask", help="cited factual answer from the sources", description=
                       "Standalone factual question: retrieve passages, apply instructions/research-rules.md, call "
                       "Gemma, check citations. Uses no chat history and no persona. Saved to runs/ask-*.json.")
    s.add_argument("question")
    s.add_argument("--mode", choices=["local", "online"], default="local")
    s.add_argument("-k", type=int, default=None)
    s.add_argument("--json", action="store_true")

    s = sub.add_parser("chat", help="talk to your assistant", description=
                       "Personal assistant with conversation memory. Retrieves wiki notes only when a turn needs "
                       "them; /help inside chat lists commands. Each turn is saved to runs/chat-*.jsonl.")
    s.add_argument("--mode", choices=["local", "online"], default="local")
    s.add_argument("--script", help="read user turns from a file, one per line (for reproducible checks)")

    s = sub.add_parser("serve", help="start/stop/status of local model servers")
    s.add_argument("action", choices=["start", "stop", "status"])
    s.add_argument("--only", choices=["gemma", "embed"], help="act on one server")

    sub.add_parser("check", help="lint the vault")
    s = sub.add_parser("merge", help="merge two notes about the same subject")
    s.add_argument("keep")
    s.add_argument("remove")
    s.add_argument("--drop-facts", action="store_true",
                   help="discard the removed note's facts (use when they only repeat the kept, reviewed note)")
    s = sub.add_parser("rename", help="rename a note and update links")
    s.add_argument("old")
    s.add_argument("new")
    sub.add_parser("status", help="configuration, models, servers, index")
    s = sub.add_parser("help", help="show help")
    s.add_argument("topic", nargs="?")
    return p


def cmd_search(args) -> int:
    from .retrieval import Index
    idx = Index()
    kinds = ("source", "wiki") if args.kind == "all" else (args.kind,)
    hits = idx.search(args.query, k=args.k, kinds=kinds)
    if args.json:
        from .harness import hit_record
        print(json.dumps({"query": args.query, "method": idx.last_method,
                          "passages": [hit_record(h, str(i)) for i, h in enumerate(hits, 1)]}, indent=2, ensure_ascii=False))
        return 0
    print(ui.header("search", f"{idx.last_method} · no language model"))
    if not hits:
        print("No matching passages.")
    for i, h in enumerate(hits, 1):
        c = h.chunk
        ranks = f"BM25 #{h.bm25_rank or '-'} · vector #{h.vector_rank or '-'}"
        print(f"\n{ui.bold(f'[{i}] {c.location}')}  ({'original' if c.kind == 'source' else 'wiki note'}; {ranks})")
        print(ui.dim(f"    {c.section}"))
        print(textwrap.indent(c.text, "    "))
    print(ui.dim(f"\n{len(hits)} passages from {len(idx.chunks)} indexed. No answer generated; open the paths above to read more."))
    return 0


def cmd_ask(args) -> int:
    from .harness import ask
    r = ask(args.question, mode=args.mode, k=args.k)
    if args.json:
        print(json.dumps({"answer": r.answer, "checks": r.checks, "run": r.run_file}, indent=2, ensure_ascii=False))
        return 0
    label = f"{r.model} · {r.mode}" + (" (llama.cpp, this machine)" if r.mode == "local" else " (HOSTED: prompt and passages sent to Google)")
    print(ui.header("ask", label))
    print(f"\n{r.answer}\n")
    print(ui.bold("Sources"))
    for i, h in enumerate(r.passages, 1):
        mark = "*" if i in r.checks.get("cited", []) else " "
        print(f" {mark}[S{i}] {h.chunk.location} › {h.chunk.section}" + ("" if h.chunk.kind == "source" else "  (wiki note)")
              + ("  (opening of this section, added)" if h.opens_section_of else ""))
    print(ui.dim("  * = cited in the answer"))
    c = r.checks
    detail = []
    if c.get("unknown_ids"):
        detail.append(f"unknown ids {c['unknown_ids']}")
    if c.get("numbers_not_in_cited_passages"):
        detail.append(f"{len(c['numbers_not_in_cited_passages'])} number(s) not found in the cited passage")
    if c.get("uncited_sentences"):
        detail.append(f"{len(c['uncited_sentences'])} sentence(s) without a citation")
    print(f"\nCitation check: {c['status']}" + (f" ({'; '.join(detail)})" if detail else ""))
    t = r.timings
    print(ui.dim(f"Retrieval: {r.method}. Time: {t.get('total_s', 0):.1f}s (retrieval {t.get('retrieval_s', 0):.2f}s). Saved: {r.run_file}"))
    return 0


def cmd_ingest(args) -> int:
    from .ingest import ingest
    from .llm import get_model
    model = None if args.dry_run else get_model("local")
    s = ingest(args.paths or None, force=args.force, overwrite_reviewed=args.overwrite_reviewed,
               dry_run=args.dry_run, into=args.into, model=model)
    if args.dry_run:
        return 0
    counts = {}
    for v in s["files"].values():
        counts[v] = counts.get(v, 0) + 1
    print(f"\nIngest finished in {s['seconds']:.0f}s with {s['model']} ({s['mode']}): "
          + ", ".join(f"{n} {k}" for k, n in counts.items()))
    if s["notes_changed"]:
        print("Notes written or updated:\n" + "\n".join(f"  vault/{n}" for n in s["notes_changed"]))
    if s["dropped_facts"]:
        print(f"{len(s['dropped_facts'])} generated fact(s) dropped because their numbers are not in the source (see runs/).")
    ix = s["index"]
    print(f"Index: {ix['passages']} passages ({ix['sources']} sources, {ix['wiki_notes']} reviewed notes); "
          f"{ix['embedded_new']} newly embedded. index.md and Source Catalog.md rebuilt.")
    return 0


def cmd_check(_args) -> int:
    from .vault import lint
    r = lint()
    print(ui.header("check", "vault lint"))
    for e in r["errors"]:
        print(f"  ERROR  {e}")
    for w in r["warnings"]:
        print(ui.dim(f"  warn   {w}"))
    print(f"\n{r['notes']} notes, {r['links']} links checked, {r['broken_or_ambiguous']} broken/ambiguous, "
          f"{len(r['errors'])} errors, {len(r['warnings'])} warnings.")
    return 1 if r["errors"] else 0


def cmd_status(_args) -> int:
    from pathlib import Path
    s = config.load()
    st = serve.status()
    print(ui.header("status", str(s.root)))
    print(f"  local model   {s.local['model_id']}  file {Path(s.local['model_file']).expanduser()}"
          f"  ({'present' if Path(s.local['model_file']).expanduser().exists() else 'MISSING'})")
    print(f"  embeddings    {s.local['embed_model_id']}  ({'present' if Path(s.local['embed_model_file']).expanduser().exists() else 'MISSING'})")
    for name, info in st.items():
        print(f"  {name:12}  {'running' if info['healthy'] else 'stopped'} at {info['url']}")
    print(f"  online model  {s.online['model_id']} via {s.online['provider']} (only with --mode online)")
    notes = list(s.path("wiki").rglob("*.md"))
    from .textparse import SUPPORTED
    raw = [p for p in s.path("raw").rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED]
    chunks = s.path("data") / "chunks.jsonl"
    n = sum(1 for _ in open(chunks)) if chunks.exists() else 0
    print(f"  vault         {len(raw)} originals in vault/raw, {len(notes)} notes in vault/wiki, {n} indexed passages")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    if args.command in (None, "help"):
        topic = getattr(args, "topic", None)
        if topic:
            parser.parse_args([topic, "--help"])
        parser.print_help()
        return 0
    try:
        if args.command == "search":
            return cmd_search(args)
        if args.command == "ask":
            return cmd_ask(args)
        if args.command == "chat":
            from .chat import run
            return run(mode=args.mode, script=args.script)
        if args.command == "ingest":
            return cmd_ingest(args)
        if args.command == "serve":
            names = (args.only,) if args.only else ("gemma", "embed")
            if args.action == "start":
                return 0 if serve.start(names) else 1
            if args.action == "stop":
                serve.stop(names)
                return 0
            for name, info in serve.status().items():
                print(f"{name}: {'running' if info['healthy'] else 'stopped'} ({info['url']}, pid {info['pid']})")
            return 0
        if args.command == "check":
            return cmd_check(args)
        if args.command == "merge":
            from .ingest import merge_notes
            changed = merge_notes(args.keep, args.remove, drop_facts=args.drop_facts)
            print(f"Merged '{args.remove}' into '{args.keep}'. Files updated:\n" + "\n".join(f"  vault/{c}" for c in changed))
            return 0
        if args.command == "rename":
            from .vault import render_index, rename_note
            changed = rename_note(args.old, args.new)
            render_index()
            print("Renamed. Files updated:\n" + "\n".join(f"  vault/{c}" for c in changed))
            print("Run `wiki ingest` to refresh the retrieval index, then re-run your question tests.")
            return 0
        if args.command == "status":
            return cmd_status(args)
    except ModelUnavailable as e:
        print(f"error: {e}", file=sys.stderr)
        return 3
    except (ModelError, FileNotFoundError, FileExistsError, ValueError, config.ConfigError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
