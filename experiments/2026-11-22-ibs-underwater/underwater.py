"""Improve (systems book), 22 Nov 2026: how deep and how long did gated-IBS trades sit under water in
the 2009-26 backtest? A yardstick for book 2's nine open trades, all under water on 21 Nov.

Uses P-0091's own engine (books(), gate on, the nine ETFs from 2009) unchanged. Per closed trade:
length in sessions, worst close-to-entry return while open (max adverse excursion), sessions closed
under water, and the final result. Reports the distribution and the win rate by how deep a trade went.
Report only; nothing in the book or its rules changes on it.

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 experiments/2026-11-22-ibs-underwater/underwater.py
"""
import json, os, sys
import numpy as np

sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-10-07-P-0091")
sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/p0082")
import p0091  # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))
import pandas as pd  # noqa: E402

data = {s: p0091.load(s, adjusted=False) for s in p0091.BASKET}  # as P-0091's main()
common = pd.DatetimeIndex(sorted(set.intersection(*[set(d.index) for d in data.values()])))
start = int(np.searchsorted(common.values, np.datetime64(p0091.FROM)))
rows = []
for sym in p0091.BASKET:
    o, h, l, c = (data[sym].loc[common, x].to_numpy(dtype=float) for x in ("open", "high", "low", "close"))
    _, _, ir, it = p0091.books(o, h, l, c, True)
    for k in np.unique(it[it > 0]):
        idx = np.where(it == k)[0]
        if idx[0] < start:
            continue
        path = np.cumsum(ir[idx])
        rows.append({"sym": sym, "len": int(idx.size), "mae": float(np.exp(path.min()) - 1),
                     "under": int((path < 0).sum()), "final": float(np.exp(path[-1]) - 1)})

mae = np.array([r["mae"] for r in rows]); fin = np.array([r["final"] for r in rows])
ln = np.array([r["len"] for r in rows]); und = np.array([r["under"] for r in rows])
bands = [(0, -0.01), (-0.01, -0.02), (-0.02, -0.04), (-0.04, -1.0)]
by = []
for hi, lo in bands:
    sel = (mae <= hi) & (mae > lo)
    by.append({"mae_band": f"{hi:.0%} to {lo:.0%}", "n": int(sel.sum()),
               "won": round(float((fin[sel] > 0).mean()), 3) if sel.any() else None,
               "mean_final": round(float(fin[sel].mean()), 4) if sel.any() else None})
res = {"trades": len(rows),
       "len_sessions": {"median": float(np.median(ln)), "p90": float(np.percentile(ln, 90)), "max": int(ln.max())},
       "mae": {"median": round(float(np.median(mae)), 4), "p10": round(float(np.percentile(mae, 10)), 4),
               "p1": round(float(np.percentile(mae, 1)), 4)},
       "ever_under_water": round(float((und > 0).mean()), 3),
       "under_3plus_sessions": round(float((und >= 3).mean()), 3),
       "won_after_3plus_under": round(float((fin[und >= 3] > 0).mean()), 3) if (und >= 3).any() else None,
       "by_depth": by}
json.dump(res, open(os.path.join(OUT, "results.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
