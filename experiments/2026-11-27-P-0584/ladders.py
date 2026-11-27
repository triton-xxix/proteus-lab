"""P-0584: which committed scan runs had a stock week that held 4 Nov because 5 Nov was dropped,
and where the four ORB rules P-0583 flipped sat in those runs."""
import json
import os
from datetime import date, timedelta

SCAN = "/Users/triton/PROTEUS/edges/scan/"
HERE = "/Users/triton/PROTEUS/experiments/2026-11-27-P-0584/"
ORB4 = ["ORB 15m, target 2R", "ORB 15m, target close", "ORB 30m, target 1R", "ORB 30m, target 2R"]
US_HOLIDAYS = {"2026-11-26"}


def weekdays(a, b):
    d, e, out = date.fromisoformat(a), date.fromisoformat(b), []
    while d <= e:
        if d.weekday() < 5 and d.isoformat() not in US_HOLIDAYS:
            out.append(d.isoformat())
        d += timedelta(days=1)
    return out


rows = []
for name in sorted(os.listdir(SCAN)):
    p = os.path.join(SCAN, name, "results.json")
    if not os.path.isfile(p):
        continue
    j = json.load(open(p))
    weeks = j["span"]["stock_weeks"]
    hit = None
    for wi, w in enumerate(weeks):
        a, b = w.split(" to ")
        days = weekdays(a, b)
        if "2026-11-04" in days and "2026-11-05" in days and len(days) > 5:
            hit = "W%d %s" % (wi + 1, w)
        elif "2026-11-05" in days and len(days) == 5:
            hit = hit or None
    rules = {r["rule"]: r for r in j["rules"] if r["kind"] == "stock"}
    orb = {k: rules[k]["rungs"] for k in ORB4 if k in rules}
    rows.append({"run": name, "weeks": weeks, "dropped_5nov_week": hit, "orb4_rungs": orb})

held = [r for r in rows if r["dropped_5nov_week"]]
res = {"runs": len(rows), "runs_with_5nov_dropped_in_W1_W3": len(held),
       "orb4_at_rung2plus_in_those": [(r["run"], k, v) for r in held for k, v in r["orb4_rungs"].items() if v >= 2],
       "rows": rows}
json.dump(res, open(HERE + "results.json", "w"), indent=1)
for r in rows:
    print(r["run"], r["dropped_5nov_week"] or "-", r["orb4_rungs"])
print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1))
