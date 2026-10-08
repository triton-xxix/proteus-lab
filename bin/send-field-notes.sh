#!/usr/bin/env bash
# Send the week's Field Notes to Luke through the ONE existing send path (no second SMTP identity).
# usage: send-field-notes.sh <body-file>
# HALT-checked. Recipient fixed. Sender is the estate's Triton identity; the subject carries the
# Proteus name. Exits 0 on deliberate skip, 1 on failure, 2 on usage error.
set -u
ROOT="/Users/triton/PROTEUS"
TO="lukewboyd@gmail.com"
SENDER="/Users/triton/OBSIDIAN/TRITON-CORE/Ventures/Amazon-FBA/60-day-seller-programme/pipeline/send_email.py"
BODY="${1:-}"
if [ -z "$BODY" ] || [ ! -f "$BODY" ]; then
  echo "usage: send-field-notes.sh <body-file>" >&2
  exit 2
fi
# Kill switch: local file, HALT file on origin/main, or an open HALT issue by an allowed login.
# Any non-zero exit, including the check breaking, means not sent. The check logs its own line.
if ! /usr/bin/env python3 "$ROOT/bin/halt-check.py"; then
  echo "HALTED: Field Notes not sent." >&2
  exit 0
fi
PY="$(command -v python3 || true)"
[ -z "$PY" ] && for c in /usr/local/bin/python3 /opt/homebrew/bin/python3; do [ -x "$c" ] && PY="$c" && break; done
[ -z "$PY" ] && { echo "python3 not found" >&2; exit 1; }
# The week comes from the note's own filename (field-notes/2026-W40.md), not the clock: on 5 Oct a
# resend of W40 would have gone out labelled W41. The clock is the fallback for an unnamed body.
WEEK="$(basename "$BODY" | grep -oE '^[0-9]{4}-W[0-9]{2}' || true)"
[ -z "$WEEK" ] && WEEK="$(date '+%G-W%V')"
SUBJECT="Proteus Field Notes $WEEK"
# The emailed copy, and only the emailed copy, carries the private dashboard's link and passphrase
# (field-notes/staging/ is gitignored; the committed note stays clean).
STAGED="$ROOT/field-notes/staging/$WEEK-email.md"
if "$PY" "$ROOT/bin/dash.py" --email-body "$BODY" "$STAGED" >/dev/null 2>&1 && [ -s "$STAGED" ]; then
  BODY="$STAGED"
fi
if "$PY" "$SENDER" "$TO" "$SUBJECT" "$BODY" --html-report; then
  printf '%s sent Field Notes %s\n' "$(date '+%Y-%m-%d %H:%M')" "$WEEK" >> "$ROOT/state/sends.log"
  exit 0
fi
echo "send failed" >&2
exit 1
