"""P-0256: configured think (GAMES.csv think_s) against the think measured from Lichess clocks (P-0255
results.json), per game, and the one loss.

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 experiments/2026-10-29-P-0256/configured_v_measured.py
"""
import csv, json
from collections import defaultdict
import numpy as np

OUT = "/Users/triton/PROTEUS/experiments/2026-10-29-P-0256/results.json"
meas = {r["id"]: r for r in json.load(open("/Users/triton/PROTEUS/experiments/2026-10-29-P-0255/results.json"))["rows"]}
log = list(csv.DictReader(open("/Users/triton/PROTEUS/games/lichess/GAMES.csv")))
groups = defaultdict(list)
rows = []
for r in log:
    m = meas.get(r["game_id"])
    if not m:
        continue
    k = r["think_s"] or "blank"
    groups[k].append(m["median_think_s"])
    rows.append({"id": r["game_id"], "finished": r["finished_utc"], "think_s": k, "result": r["result"],
                 "measured_median_s": m["median_think_s"], "measured_mean_s": m["mean_think_s"], "max_s": m["max_think_s"]})
out = {"by_think_s": {k: {"games": len(v), "median_of_medians_s": round(float(np.median(v)), 3),
                          "min": round(float(min(v)), 3), "max": round(float(max(v)), 3),
                          "first": min(x["finished"] for x in rows if x["think_s"] == k),
                          "last": max(x["finished"] for x in rows if x["think_s"] == k)}
                      for k, v in sorted(groups.items())},
       "loss": [x for x in rows if x["result"] == "loss"], "rows": rows}
json.dump(out, open(OUT, "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1))
