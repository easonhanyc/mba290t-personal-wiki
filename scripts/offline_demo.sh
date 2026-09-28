#!/bin/bash
# Offline demonstration. Run it yourself with Wi-Fi OFF (Claude cannot operate offline):
#   1. Turn Wi-Fi off (and unplug Ethernet). Optionally start a screen recording: Cmd+Shift+5.
#   2. In Terminal:  cd <project folder> && ./scripts/offline_demo.sh
# Everything printed is also saved to evidence/offline/transcript-<time>.txt by macOS `script`.
set -u
cd "$(dirname "$0")/.."
mkdir -p evidence/offline
STAMP=$(date +%Y%m%d-%H%M%S)
OUT="evidence/offline/transcript-$STAMP.txt"
echo "Recording transcript to $OUT"
script -q "$OUT" bash scripts/offline_steps.sh
echo
echo "Done. Transcript: $OUT"
echo "Evidence cards: evidence/offline/ (summary.md, ask/T1-T4.md, mode_checks.md)"
echo "Reconnect Wi-Fi and tell Claude the run is finished."
