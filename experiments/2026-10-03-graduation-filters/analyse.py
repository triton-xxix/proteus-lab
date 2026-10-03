"""Would a different filter have saved the graduation book?

Honest version: search every filter on the FIRST half of counted trades (by time), pick the best,
then score that one filter on the SECOND half, which the search never saw. Filters available are
only what the watcher recorded: entry liquidity, latency, hour of day (UTC), entry price, and the
four exits (P, A, B, D).
"""
import json
import statistics
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).parent
rows = [json.loads(l) for l in open("/Users/triton/PROTEUS/grinder/graduates/closed.jsonl")]
rows = [r for r in rows if r.get("latency_s") is not None and r["latency_s"] <= 120 and (r.get("liq") or 0) >= 5000]
rows.sort(key=lambda r: r["block_t"])
for r in rows:
    r["hour"] = datetime.fromtimestamp(r["block_t"], timezone.utc).hour
half = len(rows) // 2
first, second = rows[:half], rows[half:]


def stats(rs, exit_):
    xs = [r[exit_] for r in rs if r.get(exit_) is not None]
    if not xs:
        return None
    s = sorted(xs)
    return {"n": len(xs), "exp": round(statistics.mean(xs), 2),
            "exp_less_best10": round(statistics.mean(s[:-10]), 2) if len(s) > 20 else None,
            "win": round(sum(x > 0 for x in xs) / len(xs), 3),
            "le_minus50": round(sum(x <= -50 for x in xs) / len(xs), 3)}


filters = {"all": lambda r: True}
for lo, hi in [(5e3, 1e4), (1e4, 2e4), (2e4, 5e4), (5e4, 1e5), (1e5, 1e12), (2e4, 1e12), (5e4, 1e12)]:
    filters[f"liq {int(lo)}-{'inf' if hi > 1e11 else int(hi)}"] = lambda r, lo=lo, hi=hi: lo <= r["liq"] < hi
for lo, hi in [(0, 2), (2, 5), (5, 30), (30, 121)]:
    filters[f"latency {lo}-{hi}s"] = lambda r, lo=lo, hi=hi: lo <= r["latency_s"] < hi
for lo, hi in [(0, 6), (6, 12), (12, 18), (18, 24)]:
    filters[f"hour {lo}-{hi} UTC"] = lambda r, lo=lo, hi=hi: lo <= r["hour"] < hi

results = []
for name, f in filters.items():
    for ex in ("P", "A", "B", "D"):
        a = stats([r for r in first if f(r)], ex)
        if a and a["n"] >= 100:
            results.append({"filter": name, "exit": ex, "first": a})
results.sort(key=lambda x: -x["first"]["exp"])
best = results[0]
f = filters[best["filter"]]
best["second"] = stats([r for r in second if f(r)], best["exit"])
top5 = results[:5]
for t in top5:
    t["second"] = stats([r for r in second if filters[t["filter"]](r)], t["exit"])
out = {"counted": len(rows), "first_half": len(first), "second_half": len(second),
       "first_span": [first[0]["block_t"], first[-1]["block_t"]],
       "baseline_P_all": stats(rows, "P"), "combos_searched": len(results),
       "best_on_first_half": best, "top5_with_second_half": top5,
       "share_of_combos_positive_on_first_half": round(sum(x["first"]["exp"] > 0 for x in results) / len(results), 3)}
(OUT / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps({k: v for k, v in out.items() if k != "first_span"}, indent=1))
