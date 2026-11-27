"""P-0583: does the 5 Nov Yahoo feed hole change the stock scan's ladder? Offline, over P-0573 leg1.
Runs scan.py's stock rules twice: as-is (stock days under 70 bars dropped, so 5 Nov goes) and with the
floor at 60 (5 Nov stays with its 16-bar hole). Compares rung counts and W1, W2, W3 totals."""
import json
import os
import sys
from datetime import datetime, timezone

SCAN = "/Users/triton/PROTEUS/edges/scan/scan.py"
LEG1 = "/Users/triton/PROTEUS/experiments/2026-11-26-P-0573/leg1/"
HERE = "/Users/triton/PROTEUS/experiments/2026-11-27-P-0583/"

src = open(SCAN).read()
assert src.count("b - a < 70") == 1
sys.path.insert(0, os.path.dirname(SCAN))


def load_ns(floor):
    ns = {"__name__": "scan_copy", "__file__": SCAN}
    exec(compile(src.replace("b - a < 70", "b - a < %d" % floor), SCAN, "exec"), ns)
    ns["PERMS"] = 2  # p-values are not compared here; totals and rungs do not use them
    return ns


def rows_from_file(sym):
    r = json.load(open(LEG1 + sym + ".json"))["chart"]["result"][0]
    q, off = r["indicators"]["quote"][0], r["meta"].get("gmtoffset", 0)
    rows = []
    for i, ts in enumerate(r["timestamp"]):
        vals = [q[k][i] for k in ("open", "high", "low", "close", "volume")]
        if None in vals:
            continue
        local = datetime.fromtimestamp(ts + off, tz=timezone.utc)
        rows.append((ts, local.date().isoformat(), local.hour * 60 + local.minute) + tuple(float(v) for v in vals))
    return rows


def run(floor):
    ns = load_ns(floor)
    days = {s: ns["prepare"](rows_from_file(s), "stock") for s in ns["STOCKS"]}
    bl = ns["blocks"]({D["date"] for s in ns["STOCKS"] for D in days[s]}, 5)
    n5 = {s: next((D["n"] for D in days[s] if D["date"] == "2026-11-05"), None) for s in ns["STOCKS"]}
    out = {}
    for kind, name, fn in ns["RULES"]:
        if kind != "stock":
            continue
        per = [[] for _ in bl]
        for s in ns["STOCKS"]:
            for D in days[s]:
                bi = next((i for i, b in enumerate(bl) if D["date"] in b), None)
                if bi is None:
                    continue
                for e, side, j, en, ex in fn(D):
                    per[bi].append(side * (ex / en - 1) - ns["COST"]["stock"])
        tot = [round(sum(t) * 100, 3) for t in per[:3]]
        rungs = 0
        for i in range(3):
            if per[i] and tot[i] > 0:
                rungs += 1
            else:
                break
        out[name] = {"W1": tot[0], "W2": tot[1], "W3": tot[2], "n": [len(p) for p in per[:3]], "rungs": rungs}
    return out, [sorted(b) for b in bl[:3]], n5


drop, drop_blocks, n5_drop = run(70)
keep, keep_blocks, n5_keep = run(50)  # 60 still dropped it: SPY 5 Nov is 78 bars with 19 null rows, 59 left
changed_rungs = [k for k in drop if drop[k]["rungs"] != keep[k]["rungs"]]
moved = {w: [k for k in drop if abs(drop[k][w] - keep[k][w]) > 1.0] for w in ("W1", "W2", "W3")}
res = {
    "stock_rules": len(drop),
    "blocks_drop": drop_blocks, "blocks_keep": keep_blocks,
    "bars_on_5_nov_kept": n5_keep,
    "changed_rungs": {k: [drop[k]["rungs"], keep[k]["rungs"]] for k in changed_rungs},
    "moved_over_1pt": {w: len(v) for w, v in moved.items()},
    "moved_rules": moved,
    "rung3_drop": sorted(k for k in drop if drop[k]["rungs"] == 3),
    "rung3_keep": sorted(k for k in keep if keep[k]["rungs"] == 3),
    "drop": drop, "keep": keep,
}
json.dump(res, open(HERE + "results.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k not in ("drop", "keep")}, indent=1))
