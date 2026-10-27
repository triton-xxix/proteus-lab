"""P-0239: turn of the month on the nine systems-book ETFs (Quantpedia's free page, refill 37).

Rule: buy at the close of the day before the month's last trading day, sell at the close of the
new month's third trading day. That holds four sessions (last day plus days 1 to 3).
Control: four-session holds starting on random days that are not turn-of-month entries, same
count per market, 2,000 draws. Dividend-adjusted closes, because ex-dates cluster near month
ends and unadjusted prices would bias this one. Windows: 2009-26 and the last 12 months.
"""
import json, sys
import numpy as np
import pandas as pd

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/p0082")
from p0082 import load  # noqa: E402

OUT = "/Users/triton/PROTEUS/experiments/2026-10-27-P-0239/results.json"
BASKET = ["SPY", "QQQ", "DIA", "IWM", "EFA", "EEM", "EWU", "EWJ", "EWG"]
HOLD = 4
COST = 0.0005


def entries(idx):
    """Positions of entry closes: two sessions before each month's first session."""
    month = idx.to_period("M")
    first = np.flatnonzero(month[1:] != month[:-1]) + 1  # first session of each new month
    return [f - 2 for f in first if f - 2 >= 0 and f + 2 < len(idx)]


def window(c, idx, start, end, rng):
    pos = [e for e in entries(idx) if start <= idx[e] < end]
    rets = np.array([c[e + HOLD] / c[e] - 1 for e in pos])
    ok = np.array([i for i in range(len(c) - HOLD) if start <= idx[i] < end and i not in set(pos)])
    ctrl = np.array([(c[d + HOLD] / c[d] - 1).mean() for d in (rng.choice(ok, len(pos)) for _ in range(2000))])
    return rets, ctrl


res = {"markets": {}, "pooled": {}}
rng = np.random.default_rng(239)
wins = {"2009-26": (pd.Timestamp("2009-01-01"), pd.Timestamp("2100-01-01")),
        "last_12m": (pd.Timestamp("2025-10-27"), pd.Timestamp("2100-01-01"))}
pool = {w: {"rets": [], "ctrl": []} for w in wins}
for s in BASKET:
    d = load(s, adjusted=True)
    c, idx = d["close"].to_numpy(), pd.DatetimeIndex(d.index)
    res["markets"][s] = {}
    for w, (a, b) in wins.items():
        r, ctrl = window(c, idx, a, b, rng)
        p = float((ctrl >= r.mean()).mean())
        res["markets"][s][w] = {"n": int(r.size), "mean_pct": round(float(r.mean() * 100), 3),
                                "win_pct": round(float((r > 0).mean() * 100), 1),
                                "control_mean_pct": round(float(ctrl.mean() * 100), 3), "p": round(p, 4)}
        pool[w]["rets"] += list(r)
        pool[w]["ctrl"].append(ctrl)
for w in wins:
    r = np.array(pool[w]["rets"])
    ctrl = np.mean(np.vstack(pool[w]["ctrl"]), axis=0)  # equal-weight market mean per draw
    res["pooled"][w] = {"n": int(r.size), "mean_pct": round(float(r.mean() * 100), 3),
                        "net_mean_pct": round(float((r.mean() - COST) * 100), 3),
                        "win_pct": round(float((r > 0).mean() * 100), 1),
                        "control_mean_pct": round(float(ctrl.mean() * 100), 3),
                        "p": round(float((ctrl >= r.mean()).mean()), 4)}
json.dump(res, open(OUT, "w"), indent=1)
for w, st in res["pooled"].items():
    print("pooled", w, st)
for s in BASKET:
    m = res["markets"][s]["2009-26"]
    print("%-4s n %d mean %+.3f control %+.3f p %.3f | last 12m %+.3f (n %d)" % (
        s, m["n"], m["mean_pct"], m["control_mean_pct"], m["p"],
        res["markets"][s]["last_12m"]["mean_pct"], res["markets"][s]["last_12m"]["n"]))
