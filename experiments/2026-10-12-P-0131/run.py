#!/usr/bin/env python3
"""P-0131: does API-Football's /injuries answer on the Free plan, and what does a round cost against 100 a day?

Spends at most six requests: /status, /injuries by date (today, tomorrow), by league+season (current, which the
Free plan is known to refuse for other endpoints), and by one fixture id from today's or tomorrow's list.
Writes result.json beside this script. Run with /Users/triton/PROTEUS/.venv/bin/python3.
"""
import json
import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, "/Users/triton/PROTEUS/pitch")
import apisports as A

HERE = os.path.dirname(os.path.abspath(__file__))
h = A.headers()
out = {"calls": []}


def call(path, **params):
    err, resp, left = A.get(path, h, **params)
    row = {"path": path, "params": params, "errors": err, "n": len(resp) if isinstance(resp, list) else 1, "left": left,
           "sample": (resp[:2] if isinstance(resp, list) else resp)}
    out["calls"].append(row)
    print(path, params, "errors", err, "n", row["n"], "left", left)
    return err, resp


today = datetime.now(timezone.utc).date()
call("/status")
for day in (today, today + timedelta(days=1)):
    call("/injuries", date=day.isoformat())
call("/injuries", league=39, season=2026)
err, fx = call("/fixtures", date=(today + timedelta(days=1)).isoformat())
fid = next((f["fixture"]["id"] for f in fx if f["league"]["id"] in A.LEAGUE_DIV), None) or (fx[0]["fixture"]["id"] if fx else None)
out["fixture_used"] = fid
if fid:
    call("/injuries", fixture=fid)
json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=str)
