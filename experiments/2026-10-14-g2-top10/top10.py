#!/usr/bin/env python3
"""G2 top ten: which trades carry the book's edge, and does anything known at entry mark them out?

Counted rule as in bin/killcheck.py: latency <= 120 s, liq >= $50k, block_t >= 3 Oct 12:00Z, primary exit P present.
Writes result.json beside this script. Read-only.
"""
import json, statistics as st, datetime as dt
from pathlib import Path
HERE = Path(__file__).parent
G2_FROM = dt.datetime(2026, 10, 3, 12, tzinfo=dt.timezone.utc).timestamp()
rows = []
for line in open("/Users/triton/PROTEUS/grinder/graduates/closed.jsonl"):
    try: r = json.loads(line)
    except Exception: continue
    if r.get("latency_s") is not None and r["latency_s"] <= 120 and (r.get("liq") or 0) >= 50000 \
       and r["block_t"] >= G2_FROM and r.get("P") is not None:
        rows.append(r)
rows.sort(key=lambda r: -r["P"])
top, rest = rows[:10], rows[10:]
def med(xs): return round(st.median(xs), 2) if xs else None
def hour(r): return dt.datetime.fromtimestamp(r["block_t"], dt.timezone.utc).strftime("%a %H:%M")
out = {"counted": len(rows), "expectancy": round(sum(r["P"] for r in rows) / len(rows), 2),
       "expectancy_without_top10": round(sum(r["P"] for r in rest) / len(rest), 2),
       "top10_share_of_total_pnl": round(sum(r["P"] for r in top) / sum(r["P"] for r in rows), 2) if sum(r["P"] for r in rows) else None,
       "top": [{"mint": r["mint"], "P": r["P"], "max_move_pct": round(r["max"] / r["entry"] * 100 - 100, 0),
                "liq_usd": round(r["liq"]), "latency_s": r["latency_s"], "entered": hour(r), "n_samples": r["n_samples"]} for r in top],
       "medians": {"top10": {"liq": med([r["liq"] for r in top]), "latency": med([r["latency_s"] for r in top])},
                   "rest": {"liq": med([r["liq"] for r in rest]), "latency": med([r["latency_s"] for r in rest])}},
       "winners_over_plus50": sum(1 for r in rows if r["P"] >= 50), "losers_under_minus50": sum(1 for r in rows if r["P"] <= -50),
       "liq_buckets": {}}
for lo, hi in ((50000, 75000), (75000, 100000), (100000, 150000), (150000, 10**9)):
    b = [r for r in rows if lo <= r["liq"] < hi]
    if b: out["liq_buckets"][f"{lo//1000}k-{hi//1000}k"] = {"n": len(b), "expectancy": round(sum(r["P"] for r in b) / len(b), 2), "top10_in": sum(1 for r in top if lo <= r["liq"] < hi)}
hours = {}
for r in rows:
    h = dt.datetime.fromtimestamp(r["block_t"], dt.timezone.utc).hour // 4 * 4
    hours.setdefault(f"{h:02d}-{h+4:02d}Z", []).append(r["P"])
out["utc_4h_buckets"] = {k: {"n": len(v), "expectancy": round(sum(v) / len(v), 2)} for k, v in sorted(hours.items())}
(HERE / "result.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
