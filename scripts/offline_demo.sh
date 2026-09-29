#!/bin/bash
# Offline demonstration. Run it yourself with Wi-Fi OFF (Claude cannot operate offline):
#   1. Turn Wi-Fi off (and unplug Ethernet). Make the Terminal window full screen-sized.
#   2. In Terminal:  cd <project folder> && ./scripts/offline_demo.sh
#   3. When the script shows a SCREENSHOT prompt, press Cmd+Shift+3, then Enter.
# Everything printed is also saved to evidence/<label>/transcript-<time>.txt by macOS `script`.
# LABEL (default offline-2) names the evidence folder; the first offline run is kept in evidence/offline/.
# REHEARSAL=1 runs the same steps with the internet on (no network gate, no pauses, no live chat).
set -u
cd "$(dirname "$0")/.."
export LABEL="${LABEL:-offline-2}"
mkdir -p "evidence/$LABEL"
STAMP=$(date +%Y%m%d-%H%M%S)
OUT="evidence/$LABEL/transcript-$STAMP.txt"
echo "Recording transcript to $OUT"
script -q "$OUT" bash scripts/offline_steps.sh
echo
echo "Done. Transcript: $OUT"
echo "Evidence cards: evidence/$LABEL/ (summary.md, ask/T1-T4.md, mode_checks.md)"
echo "Reconnect Wi-Fi and tell Claude the run is finished."
