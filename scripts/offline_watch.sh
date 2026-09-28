#!/bin/bash
# Waits (while online) until the internet connection drops, then runs the offline demonstration unattended.
# Started by Claude before you turn Wi-Fi off, because Claude itself cannot act while the machine is offline.
#   ./scripts/offline_watch.sh          # then turn Wi-Fi off; a notification appears when the demo is done
set -u
cd "$(dirname "$0")/.."
source .venv/bin/activate
online() { curl -sS -m 5 -o /dev/null https://1.1.1.1 2>/dev/null || curl -sS -m 5 -o /dev/null https://huggingface.co 2>/dev/null; }
notify() { osascript -e "display notification \"$2\" with title \"$1\" sound name \"Glass\"" 2>/dev/null; }
echo "$(date '+%H:%M:%S') waiting for the internet connection to drop (turn Wi-Fi off)..."
for i in $(seq 1 1800); do           # up to 60 minutes
  if ! online; then break; fi
  sleep 2
done
if online; then echo "Still online after 60 minutes; not starting the offline demo."; notify "Offline demo not started" "The connection never dropped. Ask Claude to restart the watcher."; exit 1; fi
sleep 3                              # let the interface settle
if online; then echo "Connection came back; not starting."; exit 1; fi
mkdir -p evidence/offline
OUT="evidence/offline/transcript-$(date +%Y%m%d-%H%M%S).txt"
echo "$(date '+%H:%M:%S') offline detected; running scripts/offline_steps.sh -> $OUT"
notify "Offline demo started" "Keep Wi-Fi off for about 20 minutes, until 'Offline demo finished' appears."
{
  echo "Offline demonstration, started automatically by scripts/offline_watch.sh when the connection dropped."
  echo "Wi-Fi was turned off by Eason; every command below ran on this machine with no internet."
  UNATTENDED=1 bash scripts/offline_steps.sh
} 2>&1 | tee "$OUT"
echo "$(date '+%H:%M:%S') finished: $OUT"
osascript -e 'display notification "You can turn Wi-Fi back on and tell Claude." with title "Offline demo finished" sound name "Glass"' 2>/dev/null
