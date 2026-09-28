#!/bin/bash
# Optional online-mode check (the extension). Run it yourself, with the internet ON:
#   export GEMINI_API_KEY=...   # create a key at https://aistudio.google.com/apikey — never commit it
#   ./scripts/online_check.sh
# Sends the research rules, the retrieved passages and each test question to hosted Gemma 4 26B A4B.
# Retrieval, embeddings and the vault stay on this machine. Results go to evidence/online/.
set -u
cd "$(dirname "$0")/.."
source .venv/bin/activate
if [ -z "${GEMINI_API_KEY:-}" ]; then echo "Set GEMINI_API_KEY first (see the comment at the top of this file)."; exit 1; fi
wiki serve start --only embed
wiki ask "What share of the final grade is attendance, and how many classes can be missed without penalty?" --mode online
python scripts/run_evals.py --label online --mode online
echo "Done: evidence/online/summary.md"
