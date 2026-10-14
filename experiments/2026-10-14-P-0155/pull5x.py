"""P-0155: pull-at-5x against holding, on the graduation watcher's closed trades.

The watcher samples each graduation every 15 s for 30 minutes (grinder/graduates/RULES.md), so
"hold to 24 h" is not in the data; the hold here is B (sell at 30 min). Raw moves, before costs.
Pull rule: if the sampled max reaches 5x entry, sell at exactly 5x (+400%), else take B's move.
That flatters the pull (a 15 s sampler fills at the sample, not the level, and the max may be a
single print), so it is an upper bound.
"""
import json
import statistics
import sys
from pathlib import Path

rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
out = Path(sys.argv[2])
res = {}
for label, keep in (
    ("counted (latency <= 120 s, liq >= 5k)", lambda r: r["latency_s"] <= 120 and r["liq"] >= 5000),
    ("liq >= 50k (G2 line)", lambda r: r["latency_s"] <= 120 and r["liq"] >= 50000),
):
    sel = [r for r in rows if keep(r) and r.get("entry") and r.get("B_move") is not None]
    hit = [r for r in sel if r["max"] / r["entry"] >= 5]
    hold = [r["B_move"] for r in sel]
    pull = [4.0 if r["max"] / r["entry"] >= 5 else r["B_move"] for r in sel]
    hit_first_sample = [r for r in hit if r["n_samples"] <= 2]
    res[label] = {
        "n": len(sel), "reached_5x": len(hit), "share_pct": round(100 * len(hit) / len(sel), 3),
        "reached_2x": sum(r["max"] / r["entry"] >= 2 for r in sel),
        "hold_B_mean_pct": round(100 * statistics.mean(hold), 2),
        "pull_mean_pct": round(100 * statistics.mean(pull), 2),
        "diff_pct_points": round(100 * (statistics.mean(pull) - statistics.mean(hold)), 2),
        "hit_B_moves_pct": sorted(round(100 * r["B_move"], 1) for r in hit)[:40],
        "hit_liq_median": round(statistics.median([r["liq"] for r in hit]), 0) if hit else None,
    }
(out / "results.json").write_text(json.dumps(res, indent=1))
for k, v in res.items():
    print(k, {x: y for x, y in v.items() if x != "hit_B_moves_pct"})
