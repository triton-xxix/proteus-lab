"""P-0542: PumpSwap curve graduates across seven nights of Grinder snapshots.

grinder/SNAPSHOTS.csv, nightly snapshots 16 to 22 Nov 2026 (the 23:xx UTC hour each night). Curve
mints = dex pumpswap and a mint ending in "pump" (pump.fun's vanity suffix). Per night: count and share
at 99%+ lp_locked_pct; across nights: mints seen on two or more nights whose LP share ever fell below
99 after reading 99+, and the non-curve tokens on PumpSwap.
"""
import csv, json
from collections import defaultdict
from pathlib import Path

SNAP = Path("/Users/triton/PROTEUS/grinder/SNAPSHOTS.csv")
OUT = Path(__file__).with_name("results.json")
DAYS = [f"2026-11-{d}" for d in range(16, 23)]


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


rows = [r for r in csv.DictReader(open(SNAP)) if r["ts"][:10] in DAYS and r["dex"] == "pumpswap"]
by_night = defaultdict(dict)
for r in rows:
    night = r["ts"][:10]
    by_night[night][r["mint"]] = r  # last row of the night wins

nights, track, noncurve = [], defaultdict(list), {}
for n in DAYS:
    toks = by_night.get(n, {})
    curve = {m: r for m, r in toks.items() if m.endswith("pump")}
    for m, r in toks.items():
        if not m.endswith("pump"):
            noncurve[m] = (r["symbol"], num(r["lp_locked_pct"]))
    lp = [num(r["lp_locked_pct"]) for r in curve.values()]
    known = [x for x in lp if x is not None]
    nights.append({"night": n, "pumpswap": len(toks), "curve": len(curve), "lp_known": len(known),
                   "lp_99_plus": sum(1 for x in known if x >= 99),
                   "under_99": sorted((r["symbol"], num(r["lp_locked_pct"])) for r in curve.values()
                                      if num(r["lp_locked_pct"]) is not None and num(r["lp_locked_pct"]) < 99)})
    for m, r in curve.items():
        track[m].append((n, num(r["lp_locked_pct"]), r["symbol"]))

multi = {m: s for m, s in track.items() if len(s) >= 2}
fell = {m: s for m, s in multi.items()
        if any(a[1] is not None and a[1] >= 99 and b[1] is not None and b[1] < 99 for a, b in zip(s, s[1:]))}
res = {"nights": nights, "distinct_curve_mints": len(track), "seen_2plus_nights": len(multi),
       "fell_below_99_after_99": {m: s for m, s in fell.items()},
       "non_curve_on_pumpswap": noncurve,
       "all_curve_rows": sum(x["lp_known"] for x in nights),
       "all_curve_99_plus": sum(x["lp_99_plus"] for x in nights)}
OUT.write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
