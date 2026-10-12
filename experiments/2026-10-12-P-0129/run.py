#!/usr/bin/env python3
"""P-0129, first leg: re-pull API-Football odds for today's Pitch fixtures and set them beside the commit-time
line in pitch/cache/apisports.json (fetched by the nightly). One request per fixture.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/experiments/2026-10-12-P-0129/run.py [label]

Appends a snapshot to snapshots.json beside this script, so later legs (about 2 h before kickoff) add to it.
"""
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, "/Users/triton/PROTEUS/pitch")
import apisports as A

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "snapshots.json")
cache = json.load(open(A.CACHE))
h = A.headers()
now = datetime.now(timezone.utc)
snap = {"label": sys.argv[1] if len(sys.argv) > 1 else "snap", "at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "commit_line_fetched": cache["fetched"], "rows": [], "left": None}
for r in cache["rows"]:
    ko = datetime.strptime(r["kickoff_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    if ko <= now:
        continue
    err, od, left = A.get("/odds", h, fixture=r["fixture_id"])
    snap["left"] = left
    o = A.avg_odds(od)
    moves = {}
    for k in ("AvgH", "AvgD", "AvgA"):
        if r.get(k) and o.get(k):
            moves[k] = round(o[k] / r[k] - 1, 4)
    row = {"match": "%s v %s" % (r["HomeTeam"], r["AwayTeam"]), "Div": r["Div"], "kickoff_utc": r["kickoff_utc"],
           "hours_to_ko": round((ko - now).total_seconds() / 3600, 2), "commit": {k: r.get(k) for k in ("AvgH", "AvgD", "AvgA", "bookmakers")},
           "now": {k: o.get(k) for k in ("AvgH", "AvgD", "AvgA", "bookmakers")}, "move": moves, "errors": err}
    snap["rows"].append(row)
    print(row["match"], row["hours_to_ko"], "h to ko", row["commit"], "->", row["now"], row["move"])
hist = json.load(open(OUT)) if os.path.exists(OUT) else []
hist.append(snap)
json.dump(hist, open(OUT, "w"), indent=1)
moved = [abs(v) for r in snap["rows"] for v in r["move"].values()]
print("prices", len(moved), "mean abs move %.4f" % (sum(moved) / len(moved)) if moved else "", "max %.4f" % max(moved) if moved else "", "left", snap["left"])
