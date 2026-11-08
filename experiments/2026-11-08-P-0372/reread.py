"""P-0372 part two. Part one's 60 rows repeat pools and are all under three minutes old, so:
(a) dedupe them, reporting how far repeat rows of one pool disagree;
(b) measure vol_h1 on tonight's rows of grinder/SNAPSHOTS.csv, which is what the gate actually sees.
Reads only. No rule is changed.
"""
import collections
import csv
import json
import pathlib
import statistics

HERE = pathlib.Path(__file__).parent
SNAP = "/Users/triton/PROTEUS/grinder/SNAPSHOTS.csv"
LINE = 10_000.0
rows = json.loads((HERE / "results.json").read_text())["rows"]


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


by_pool = collections.defaultdict(list)
for r in rows:
    by_pool[r["pool"]].append(r)
repeats = {p: [x["vol_h1"] for x in v] for p, v in by_pool.items() if len(v) > 1}
last = [v[-1] for v in by_pool.values()]
top = [max(x["vol_h1"] for x in v) for v in by_pool.values()]

with open(SNAP, newline="") as f:
    snap = list(csv.DictReader(f))
ts_field = next(k for k in snap[0] if k in ("snapshot_at", "ts", "at", "scanned_at", "time", "taken_at"))
latest_day = max(r[ts_field][:10] for r in snap)
tonight = [r for r in snap if r[ts_field][:10] == latest_day]
aged = [r for r in tonight if (num(r.get("age_h")) is not None and 1.0 <= num(r["age_h"]) <= 48.0)]
vols = sorted(v for v in (num(r.get("vol_h1")) for r in aged) if v is not None)

out = {
    "feed": {
        "rows": len(rows), "distinct_pools": len(by_pool), "pools_seen_twice_or_more": len(repeats),
        "worst_repeat_ratio": round(max((max(v) / max(min(v), 1) for v in repeats.values()), default=0), 2),
        "clear_line_taking_max_of_repeats": sum(v >= LINE for v in top),
        "clear_line_taking_last_row": sum(r["vol_h1"] >= LINE for r in last),
        "median_vol_h1_distinct_last_row": round(statistics.median(r["vol_h1"] for r in last), 2),
    },
    "snapshot": {
        "ts_field": ts_field, "day": latest_day, "rows_that_day": len(tonight),
        "rows_in_1_to_48h": len(aged), "with_vol_h1": len(vols),
        "clear_line": sum(v >= LINE for v in vols),
        "within_half_below_line": sum(LINE / 2 <= v < LINE for v in vols),
        "median": round(statistics.median(vols), 2) if vols else None,
        "p90": round(vols[int(len(vols) * 0.9)], 2) if vols else None,
        "max": round(vols[-1], 2) if vols else None,
    },
}
(HERE / "reread.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
