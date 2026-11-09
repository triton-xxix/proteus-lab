#!/usr/bin/env python3
"""Sleep until a UTC clock time today, in pieces a foreground Bash call can hold.

Usage: python3 /Users/triton/PROTEUS/bin/wait-until.py HH:MM [--max-minutes 9]

Prints READY once the time has passed, or WAIT and how far off it still is after sleeping at most
--max-minutes, so a run calls it again. Written 9 Nov 2026 for the Lichess morning job (F-0076): the
slot fires at 07:55 and the bots' daily caps reset about 08:03 to 08:20 UTC. Python's sleep, because a
foreground shell sleep is blocked and the slot time is scheduler config.
"""
import argparse
import datetime as dt
import time

ap = argparse.ArgumentParser()
ap.add_argument("hhmm")
ap.add_argument("--max-minutes", type=float, default=9)
a = ap.parse_args()

hour, minute = (int(x) for x in a.hhmm.split(":"))
now = dt.datetime.now(dt.timezone.utc)
target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
gap = (target - now).total_seconds()
if gap <= 0:
    print("READY %s UTC already passed (now %s)" % (a.hhmm, now.strftime("%H:%M:%S")))
else:
    time.sleep(min(gap, a.max_minutes * 60))
    now = dt.datetime.now(dt.timezone.utc)
    left = (target - now).total_seconds()
    if left <= 0:
        print("READY %s UTC reached (now %s)" % (a.hhmm, now.strftime("%H:%M:%S")))
    else:
        print("WAIT %.1f min to %s UTC, call again" % (left / 60, a.hhmm))
