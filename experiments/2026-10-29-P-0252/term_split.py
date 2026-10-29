"""P-0252: the systems book's RSI(5) simple rule, next-open fills, 9 ETFs, 2009 on, split by VIX/VIX3M
on the signal day (FRED VIXCLS over VXVCLS). Backwardation = ratio >= 1, contango = ratio < 1.

Control as P-0243: random signal days from that symbol's days in the same bucket (2009 on, close above
its 200-day average), next-open entry, hold drawn from that bucket's real trades, exit at the open.
2000 draws of n trades each; p = share of draws whose mean >= the real mean.

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 experiments/2026-10-29-P-0252/term_split.py
"""
import csv, json, sys
import numpy as np

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/p0082")
sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-10-07-P-0083")
from p0082 import load, sma  # noqa: E402
from basket_backtest import rsi5_next_open_rp, BASKET  # noqa: E402

OUT = "/Users/triton/PROTEUS/experiments/2026-10-29-P-0252/results.json"


def series(path):
    d = {}
    for r in list(csv.reader(open(path)))[1:]:
        if r[1] not in ("", "."):
            d[np.datetime64(r[0])] = float(r[1])
    return d


vix = series("/Users/triton/PROTEUS/sandbox/fred/VIXCLS.csv")
v3m = series("/Users/triton/PROTEUS/sandbox/fred/VXVCLS.csv")
rdates = np.array(sorted(set(vix) & set(v3m)))
rvals = np.array([vix[d] / v3m[d] for d in rdates])


def ratio_on(d):
    i = np.searchsorted(rdates, d, side="right") - 1  # that day's close, or the last before it
    return rvals[i] if i >= 0 else np.nan


def bucket(r):
    return 1 if r >= 1 else 0


since = rdates >= np.datetime64("2009-01-01")
rng = np.random.default_rng(20261029)
trades = {0: [], 1: []}
pool = {0: [], 1: []}
opens = {}
for s in BASKET:
    df = load(s)
    o, c = df["open"].to_numpy(), df["close"].to_numpy()
    idx = df.index.values
    opens[s] = o
    start = int(np.searchsorted(idx, np.datetime64("2009-01-01")))
    rets, tid = rsi5_next_open_rp(o, c, 1)
    ks = np.unique(tid[start:][tid[start:] > 0])
    for k in ks:
        w = np.where(tid == k)[0]
        e, x = w[0], w[-1]
        if x == len(c) - 1 and rets[x] == np.log(c[x]) - np.log(c[x - 1]):
            continue                     # still open at the end
        b = bucket(ratio_on(idx[e - 1]))
        trades[b].append((float(np.expm1(rets[w].sum())), int(x - e)))
    tb = np.array([bucket(ratio_on(d)) for d in idx])
    m200 = sma(c, 200)
    for i in range(start, len(o) - 60):
        if c[i] > m200[i]:
            pool[tb[i]].append((s, i))

res = {"n_draws": 2000, "days_2009_on": int(since.sum()),
       "backwardation_day_share_pct": round(float((rvals[since] >= 1).mean()) * 100, 2), "by_bucket": {}}
print("days", res["days_2009_on"], "backwardation share", res["backwardation_day_share_pct"], flush=True)
for b, name in ((0, "contango ratio < 1"), (1, "backwardation ratio >= 1")):
    a = np.array([r for r, _ in trades[b]])
    holds = np.array([h for _, h in trades[b]])
    n = a.size
    P = pool[b]
    sims = np.empty(2000)
    for j in range(2000):
        pick = rng.integers(0, len(P), n)
        hh = holds[rng.integers(0, n, n)]
        sims[j] = np.mean([opens[P[q][0]][P[q][1] + 1 + h] / opens[P[q][0]][P[q][1] + 1] - 1 for q, h in zip(pick, hh)])
    res["by_bucket"][name] = {
        "trades": int(n), "mean_pct": round(a.mean() * 100, 3), "win_pct": round((a > 0).mean() * 100, 1),
        "t": round(float(a.mean() / (a.std(ddof=1) / np.sqrt(n))), 2), "mean_hold_days": round(float(holds.mean()), 2),
        "control_mean_pct": round(float(sims.mean()) * 100, 3), "excess_pct": round((a.mean() - sims.mean()) * 100, 3),
        "p": round(float((sims >= a.mean()).mean()), 4), "pool_days": len(P)}
    print(name, res["by_bucket"][name], flush=True)
json.dump(res, open(OUT, "w"), indent=1)
