#!/bin/bash
# The steps of the offline demonstration (called by offline_demo.sh inside `script`).
set -u
source .venv/bin/activate
export NO_COLOR=1
LABEL="${LABEL:-offline-2}"
REHEARSAL="${REHEARSAL:-0}"
NEW_SOURCE="incoming/prioritization-framework.md"   # held back from the wiki until this run
NEW_SOURCE_DIR="website/artifacts"
T1="What share of the final grade is attendance, and how many classes can be missed without penalty?"
T2="In the app I built to track people I meet, what stops one user from seeing someone else's list?"
T3="What was my job title at Amazon Web Services, and by how much did the Action Hub cut sellers' time-to-insight?"
T4="What grade did I receive on the Pac-Man assignment?"
START=$(date +%s)
SHOT=0

step() { echo; echo "================================================================"; echo "== $*"; echo "================================================================"; }
run()  { echo; echo "\$ $*"; "$@"; echo "[exit code $?]"; }
# Pause so the screen (menu bar with the Wi-Fi icon + this Terminal) can be captured.
shot() {
  SHOT=$((SHOT + 1))
  if [ "$REHEARSAL" = "1" ] || [ "${UNATTENDED:-0}" = "1" ]; then return; fi
  echo; echo "################################################################"
  echo "##  SCREENSHOT $SHOT of 5: $*"
  echo "##  Press Cmd+Shift+3 now, then press Enter here to continue."
  echo "################################################################"
  read -r _ < /dev/tty
}

step "0. When and where"
run date
run sw_vers
run sysctl -n machdep.cpu.brand_string
echo "RAM: $(( $(sysctl -n hw.memsize) / 1073741824 )) GB unified memory"
run df -h /

step "1. Proof the internet is disconnected"
# Internet test = real HTTPS requests (need a route, DNS and a valid TLS certificate).
# A raw TCP connect to 1.1.1.1:53 is NOT used as the test: on this Mac the Cisco AnyConnect socket
# filter answers it locally even with Wi-Fi off (see evidence/changes.md, fix 9).
internet() { curl -sS -m 5 -o /dev/null https://1.1.1.1 2>/dev/null || curl -sS -m 5 -o /dev/null https://huggingface.co 2>/dev/null; }
run networksetup -getairportpower en0
run route -n get default
run curl -sS -m 5 -o /dev/null https://huggingface.co
run curl -sS -m 5 -o /dev/null https://1.1.1.1
echo "(for information: a raw TCP connect to 1.1.1.1:53 can be answered locally by a network extension)"
run python -c "import socket; socket.create_connection(('1.1.1.1', 53), timeout=3); print('TCP 1.1.1.1:53 answered (locally or remotely)')"
if [ "$REHEARSAL" = "1" ]; then
  echo "REHEARSAL: the internet is ON on purpose; this run only checks that the steps work. Not offline evidence."
elif internet; then
  echo "!! An HTTPS request succeeded, so the internet is reachable. Turn Wi-Fi off and run again."; exit 1
else
  echo "OK: no HTTPS request can leave this machine (no route, no DNS). Everything below runs locally."
fi

step "2. Restart the local model servers and the CLI (fresh processes, local mode)"
run wiki serve stop
run wiki serve start
run wiki status
shot "Wi-Fi off, HTTPS failing, local servers restarted"
run wiki --help

step "3. Useful error when the local model is unavailable (no cloud fallback)"
run wiki serve stop --only gemma
run wiki ask "$T1"
echo "-- search still works: it is retrieval only, no language model --"
run wiki search "row level security" -k 3
run wiki serve start --only gemma

step "4. Ingest a new local source offline, then ingest it again (no duplicates)"
NOTES_BEFORE=$(find vault/wiki -name '*.md' | wc -l | tr -d ' ')
echo "Notes before: $NOTES_BEFORE"
run wiki ingest "$NEW_SOURCE" --into "$NEW_SOURCE_DIR"
NOTES_AFTER1=$(find vault/wiki -name '*.md' | wc -l | tr -d ' ')
echo "Notes after first ingest: $NOTES_AFTER1"
run wiki ingest "$NEW_SOURCE" --into "$NEW_SOURCE_DIR"
run wiki ingest vault/raw
NOTES_AFTER2=$(find vault/wiki -name '*.md' | wc -l | tr -d ' ')
echo "Notes after re-ingesting everything: $NOTES_AFTER2 (same as after the first ingest: no duplicates)"
run wiki check
echo "-- the newest notes (readable names, no hashes) --"
ls -t vault/wiki/*/ | head -20
shot "the new source ingested offline, and re-ingest with no duplicates"

step "5. The four ask-mode tests (standalone, cited, local Gemma)"
run wiki ask "$T1"
run wiki ask "$T2"
run wiki ask "$T3"
run wiki ask "$T4"
shot "the ask answers with their sources (scroll up to show T2 if you can)"

step "6. Chat and search mode checks"
run wiki chat --script tests/chat_scripts/M1_capabilities.txt
run wiki chat --script tests/chat_scripts/M2_followup.txt
run wiki search "row level security" -k 3
run wiki chat --script tests/chat_scripts/M4_claim.txt
run wiki ask "What is my favorite programming language?"
run wiki chat --script tests/chat_scripts/M5_draft_from_notes.txt
shot "the chat and search checks"

step "7. Evidence cards for the same checks (scripts/run_evals.py, same harness code)"
run python scripts/run_evals.py --label "$LABEL"

if [ "$REHEARSAL" = "1" ] || [ "${UNATTENDED:-0}" = "1" ]; then
  step "8. Live chat skipped (rehearsal or unattended run); scripted chat checks are in step 6"
else
  step "8. Your turn: a short live chat (type a few messages, then /exit)"
  echo "Suggested: 'what can you help me with?', then ask it to draft something about one of your projects,"
  echo "then 'make that shorter', then /exit."
  wiki chat
  shot "your live chat (before this prompt scrolls away)"
fi

step "9. Still offline at the end?"
run curl -sS -m 5 -o /dev/null https://1.1.1.1
run curl -sS -m 5 -o /dev/null https://huggingface.co
echo "Total time: $(( $(date +%s) - START )) s"
