#!/usr/bin/env bash
# The systems book's daily step, run by launchd (com.proteus.systems, systems/com.proteus.systems.plist),
# Monday to Friday at 22:30 local, once loaded (it waits for CHARTER-v3.1-DIFF.md section 6, 27 Nov 2026). Luke cut the nightly to Wednesday and Saturday
# that day (WF-0518) and asked for lightweight Python tracking of systems book 2 (IBS) to continue.
# Book 1 rides along: systems.py logs both from one fetch.
#
# What it does: the kill switch, then systems.py update and score, then one LOCAL commit of the
# three systems CSVs by named path. It does not push: a git push from launchd blocks on the
# osxkeychain credential helper (found 9 Oct 2026, prelisting tracker). The next nightly's
# preregister.py pre pushes these commits. Until then the proof of timing is the local commit and
# each row's logged_utc, which is weaker than a pushed commit, and systems/RULES.md says so.
#
# One line goes to state/runs/YYYY-MM-DD.md. No Claude session is involved. Switch off with
#   launchctl bootout gui/$(id -u)/com.proteus.systems
set -u
ROOT="/Users/triton/PROTEUS"
PY="$ROOT/.venv/bin/python3"
DAY="$(date '+%Y-%m-%d')"
RUNLOG="$ROOT/state/runs/$DAY.md"
OUT="$ROOT/systems/log/daily-$DAY.txt"
mkdir -p "$ROOT/state/runs" "$ROOT/systems/log"

if [ -e "$ROOT/HALT" ] || ! /usr/bin/env python3 "$ROOT/bin/halt-check.py" > "$OUT" 2>&1; then
  printf -- '- Systems daily %s: skipped, kill switch (see %s)\n' "$(date '+%H:%M')" "systems/log/daily-$DAY.txt" >> "$RUNLOG"
  exit 0
fi

"$PY" "$ROOT/systems/systems.py" update >> "$OUT" 2>&1
UPD=$?
"$PY" "$ROOT/systems/systems.py" score >> "$OUT" 2>&1
NEWDAYS="$(grep -c ' [1-9][0-9]* new day' "$OUT")"
FAILED="$(grep -c 'fetch failed' "$OUT")"
SCORE="$(grep -m1 '^Systems book 2' "$OUT" | cut -c1-200)"

FILES=(systems/SIGNALS.csv systems/SIGNALS_IBS.csv systems/EVENTS.csv)
if git -C "$ROOT" status --porcelain -- "${FILES[@]}" | grep -q .; then
  git -C "$ROOT" add -- "${FILES[@]}" >> "$OUT" 2>&1
  if git -C "$ROOT" commit -q -m "systems daily $DAY: signals (launchd, local commit, the next nightly pushes)" -- "${FILES[@]}" >> "$OUT" 2>&1; then
    COMMIT="committed $(git -C "$ROOT" rev-parse --short HEAD) locally"
  else
    COMMIT="commit FAILED (see systems/log/daily-$DAY.txt)"
  fi
else
  COMMIT="nothing to commit"
fi

printf -- '- Systems daily %s: update exit %s, %s market(s) with new days, %s fetch failure(s); %s. %s\n' \
  "$(date '+%H:%M')" "$UPD" "$NEWDAYS" "$FAILED" "$COMMIT" "$SCORE" >> "$RUNLOG"
exit 0
