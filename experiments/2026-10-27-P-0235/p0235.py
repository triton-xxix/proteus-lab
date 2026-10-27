"""P-0235: IBS with close fills against next-open fills, on the same signals.

Rule as P-0091, ungated: IBS below 0.2 at a close is the buy signal; a close above yesterday's
high is the sell signal. Four fill variants of that one signal set, per market, 2009 on:
  open/open    buy next open, sell next open        (systems book 2, before its gate)
  close/close  buy at the signal close, sell at the signal close  (the videos' version)
  close/open   buy at the close, sell next open
  open/close   buy next open, sell at the signal close
Trade returns before costs; the book's 0.05% round trip is shown alongside.

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 experiments/2026-10-27-P-0235/p0235.py
"""
import json, sys
import numpy as np
import pandas as pd

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/p0082")
from p0082 import load  # noqa: E402

OUT = "/Users/triton/PROTEUS/experiments/2026-10-27-P-0235/results.json"
BASKET = ["SPY", "QQQ", "DIA", "IWM", "EFA", "EEM", "EWU", "EWJ", "EWG"]
FROM = "2009-01-01"
COST = 0.0005


def signals(o, h, l, c, start):
    """(entry signal day, exit signal day) pairs; one position at a time, entries from start."""
    pairs, t, n = [], max(start, 1), len(c)
    while t < n - 1:
        rng = h[t] - l[t]
        if rng > 0 and (c[t] - l[t]) / rng < 0.2:
            e = t
            x = None
            for u in range(e + 1, n - 1):
                if c[u] > h[u - 1]:
                    x = u
                    break
            if x is None:
                break
            pairs.append((e, x))
            t = x + 1  # next open fill frees the slot; same for all variants so signals match
        else:
            t += 1
    return pairs


def stats(a):
    a = np.asarray(a)
    return {"trades": int(a.size), "mean_pct": round(float(a.mean() * 100), 3),
            "net_mean_pct": round(float((a.mean() - COST) * 100), 3),
            "win_pct": round(float((a > 0).mean() * 100), 1),
            "t": round(float(a.mean() / (a.std(ddof=1) / np.sqrt(a.size))), 2)}


res = {"from": FROM, "markets": {}, "pooled": {}}
pool = {k: [] for k in ("open_open", "close_close", "close_open", "open_close")}
for s in BASKET:
    d = load(s, adjusted=False)
    o, h, l, c = (d[x].to_numpy() for x in ("open", "high", "low", "close"))
    start = int(np.searchsorted(d.index.values, np.datetime64(FROM)))
    pairs = signals(o, h, l, c, start)
    v = {
        "open_open": [o[x + 1] / o[e + 1] - 1 for e, x in pairs],
        "close_close": [c[x] / c[e] - 1 for e, x in pairs],
        "close_open": [o[x + 1] / c[e] - 1 for e, x in pairs],
        "open_close": [c[x] / o[e + 1] - 1 for e, x in pairs],
    }
    res["markets"][s] = {k: stats(a) for k, a in v.items()}
    for k, a in v.items():
        pool[k] += a
    # the overnight gap after an IBS signal: close to next open
    res["markets"][s]["entry_gap_mean_pct"] = round(float(np.mean([o[e + 1] / c[e] - 1 for e, _ in pairs]) * 100), 3)
res["pooled"] = {k: stats(a) for k, a in pool.items()}
json.dump(res, open(OUT, "w"), indent=1)
for k, st in res["pooled"].items():
    print("pooled %-12s %s" % (k, st))
for s in BASKET:
    m = res["markets"][s]
    print("%-4s open/open %+.3f  close/close %+.3f  gap after signal %+.3f  n %d" % (
        s, m["open_open"]["mean_pct"], m["close_close"]["mean_pct"], m["entry_gap_mean_pct"], m["open_open"]["trades"]))
