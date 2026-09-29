#!/bin/bash
# Submission-checklist item 2: follow the README's setup and launch steps once more, from a fresh clone of the
# public repository (signed out), and record the CLI's error messages. Needs the internet for the clone and
# pip install; uses the model files already in ~/models/gemma and the local servers if they are running.
#   ./scripts/setup_check.sh      -> evidence/setup-check-<time>.txt
set -u
cd "$(dirname "$0")/.."
OUT="$PWD/evidence/setup-check-$(date +%Y%m%d-%H%M%S).txt"
WORK="$(mktemp -d)"
run() { echo; echo "\$ $*"; "$@"; echo "[exit code $?]"; }
{
  echo "Setup check from a fresh clone, $(date)"
  cd "$WORK"
  run env GIT_TERMINAL_PROMPT=0 git -c credential.helper= clone -q https://github.com/easonhanyc/mba290t-personal-wiki.git
  cd mba290t-personal-wiki
  run git log --oneline -1
  run python3 -m venv .venv
  source .venv/bin/activate
  run pip install -q -e ".[test]"
  run pytest -q
  run shasum -a 256 "$HOME/models/gemma/gemma-4-E4B_q4_0-it.gguf" "$HOME/models/gemma/embeddinggemma-300m-qat-Q8_0.gguf"
  run wiki serve status
  run wiki status
  run wiki check
  run wiki ingest vault/raw
  run wiki search "row level security" -k 2
  run wiki ask "What share of the final grade is attendance?"
  echo; echo "-- errors: a missing file, and online mode without a key (no request is sent) --"
  run wiki ingest notes/does-not-exist.md
  run env -u GEMINI_API_KEY wiki ask "What share of the final grade is attendance?" --mode online
  run wiki help ask
} > "$OUT" 2>&1
rm -rf "$WORK"
echo "written: ${OUT#$PWD/}"
