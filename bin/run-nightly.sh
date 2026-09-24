#!/usr/bin/env bash
# Proteus nightly preflight. Called by the proteus-nightly scheduled task as its first Bash step.
# Exits 0 with "OK" when the run may proceed, 0 with "HALTED" when it must not (the SKILL then stops).
# Absolute paths only; no cd; safe under the unattended hook.
#
# The kill switch is bin/halt-check.py: the local HALT file, a HALT file on origin/main, or an open
# HALT issue by an allowed login. Any non-zero exit from the check, including the check itself
# breaking, is a halt. The check writes its own line to the run log.
set -u
ROOT="/Users/triton/PROTEUS"
DAY="$(date '+%Y-%m-%d')"
mkdir -p "$ROOT/state/runs"
if ! /usr/bin/env python3 "$ROOT/bin/halt-check.py"; then
  printf '%s run skipped: kill switch (see the HALT line above)\n' "$(date '+%H:%M')" >> "$ROOT/state/runs/$DAY.md"
  echo "HALTED"
  exit 0
fi
# The check fetched origin/main. If a remote halt was set and cleared, main is two commits ahead of
# us; take them now so tonight's push is a fast-forward. A refusal is logged, not fatal.
if ! git -C "$ROOT" merge --ff-only --quiet origin/main 2>/dev/null; then
  printf '%s origin/main not fast-forwardable into local main; push may be rejected\n' "$(date '+%H:%M')" >> "$ROOT/state/runs/$DAY.md"
fi
printf '\n## Nightly run %s %s\n' "$DAY" "$(date '+%H:%M')" >> "$ROOT/state/runs/$DAY.md"
echo "OK"
