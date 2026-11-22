"""P-0537: share of graduated pump.fun tokens (PumpSwap pairs) with 99%+ LP locked or burned.

Reads tonight's rows of grinder/SNAPSHOTS.csv (rugcheck's lp_locked_pct per token) and compares
PumpSwap pairs (where pump.fun graduates land) with every other dex in the same snapshot.
"""
import csv, json, statistics, sys
from collections import defaultdict
from pathlib import Path

SNAP = Path("/Users/triton/PROTEUS/grinder/SNAPSHOTS.csv")
OUT = Path(__file__).with_name("results.json")
day = sys.argv[1] if len(sys.argv) > 1 else "2026-11-22"

rows = [r for r in csv.DictReader(open(SNAP)) if r["ts"].startswith(day)]
latest = max(r["ts"][:13] for r in rows)
rows = [r for r in rows if r["ts"][:13] == latest]
seen, uniq = set(), []
for r in rows:
    if r["mint"] not in seen:
        seen.add(r["mint"])
        uniq.append(r)


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


by = defaultdict(list)
for r in uniq:
    by[r["dex"] or "?"].append(r)

res = {"snapshot_hour": latest, "tokens": len(uniq), "by_dex": {}}
for dex, rs in sorted(by.items(), key=lambda kv: -len(kv[1])):
    vals = [num(r["lp_locked_pct"]) for r in rs]
    known = [v for v in vals if v is not None]
    res["by_dex"][dex] = {
        "n": len(rs),
        "lp_known": len(known),
        "lp_99_plus": sum(1 for v in known if v >= 99),
        "lp_under_50": sum(1 for v in known if v < 50),
        "median_lp": round(statistics.median(known), 2) if known else None,
        "median_age_h": round(statistics.median([num(r["age_h"]) for r in rs if num(r["age_h"]) is not None]), 1),
    }
pump = [r for r in uniq if r["dex"].lower().startswith("pump")]
recent = sorted(pump, key=lambda r: num(r["age_h"]) or 1e9)[:30]
rk = [num(r["lp_locked_pct"]) for r in recent if num(r["lp_locked_pct"]) is not None]
res["youngest_30_pump"] = {
    "n": len(recent), "lp_known": len(rk), "lp_99_plus": sum(1 for v in rk if v >= 99),
    "values": sorted(rk),
}
OUT.write_text(json.dumps(res, indent=2))
print(json.dumps(res, indent=2))
