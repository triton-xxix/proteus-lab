"""Re-walk the rows that ended in a transient error, and the 2021 rows the wall cut off.

The 6-thread run hit rate limits: the error pages load fine when asked again (errors.py). 2026 comes from
the 5 Nov 17:18 walk on the same 100 starts by the same rule. Writes final.json after each date.
Usage: python3 finish.py WALL_SECONDS
"""
import json
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-11-05-P-0332")
import ringdate

HERE = "/Users/triton/PROTEUS/experiments/2026-11-05-P-0332/"
wall = float(sys.argv[1])
t0 = time.time()
res = json.load(open(HERE + "results.json"))
base = json.load(open(ringdate.ROOT))
sample = [r["start"] for r in base["rows"]]
final = {"source": "results.json with errors and missing rows re-walked at 3 threads", "dates": {}}

for d in ["2011-07-01", "2014-07-01", "2016-07-01", "2018-07-01", "2021-07-01"]:
    have = {r["start"]: r for r in res["dates"][d]["rows"] if r["outcome"] != "error"}
    todo = [s for s in sample if s not in have]
    cache = {}

    def one(s):
        if time.time() - t0 > wall:
            return None
        outcome, path = ringdate.walk(s, d, cache)
        return {"start": s, "outcome": outcome, "hops": len(path) - 1, "path": path}

    with ThreadPoolExecutor(3) as pool:
        for g in pool.map(one, todo):
            if g:
                have[g["start"]] = g
    rows = [have[s] for s in sample if s in have]
    c = Counter(r["outcome"] for r in rows)
    rings = Counter(" > ".join(sorted(ringdate.ring_of(r["path"]))) for r in rows if r["outcome"] == "loop")
    final["dates"][d] = {"counts": dict(c), "walked": len(rows), "rings": rings.most_common(4), "rows": rows}
    print(d, "walked", len(rows), dict(c), "top ring", rings.most_common(1), "secs", round(time.time() - t0), flush=True)
    final["calls"] = ringdate.calls
    with open(HERE + "final.json", "w") as fh:
        json.dump(final, fh, indent=1)

rows = base["rows"]
c = Counter(r["outcome"] for r in rows)
print("2026-11-05 walked", len(rows), dict(c), "(from the 17:18 walk)", flush=True)
final["dates"]["2026-11-05"] = {"counts": dict(c), "walked": len(rows), "from": "experiments/2026-11-05-philosophy/walks.json"}
with open(HERE + "final.json", "w") as fh:
    json.dump(final, fh, indent=1)
print("done, calls", ringdate.calls, flush=True)
