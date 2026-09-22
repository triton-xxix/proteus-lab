#!/usr/bin/env bash
# Proteus nightly preflight. Called by the proteus-nightly scheduled task as its first Bash step.
# Exits 0 with "OK" when the run may proceed, 0 with "HALTED" when it must not (the SKILL then stops).
# Absolute paths only; no cd; safe under the unattended hook.
set -u
ROOT="/Users/triton/PROTEUS"
DAY="$(date '+%Y-%m-%d')"
mkdir -p "$ROOT/state/runs"
if [ -f "$ROOT/HALT" ]; then
  printf '%s HALT set, run skipped\n' "$(date '+%H:%M')" >> "$ROOT/state/runs/$DAY.md"
  echo "HALTED"
  exit 0
fi
printf '\n## Nightly run %s %s\n' "$DAY" "$(date '+%H:%M')" >> "$ROOT/state/runs/$DAY.md"
echo "OK"
