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
WEEK="$(date '+%G-W%V')"
SUBJECT="Proteus Field Notes $WEEK"
if "$PY" "$SENDER" "$TO" "$SUBJECT" "$BODY" --html-report; then
  printf '%s sent Field Notes %s\n' "$(date '+%Y-%m-%d %H:%M')" "$WEEK" >> "$ROOT/state/sends.log"
  exit 0
fi
echo "send failed" >&2
exit 1
