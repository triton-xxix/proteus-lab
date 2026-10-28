"""P-0243: the systems book's RSI(5) simple rule, next-open fills, 9 ETFs, 2009 on, split by the
VIX close on the signal day. Terciles fixed in the probe title (15.2 and 20.7, full 1990-2026 history).

Control per tercile: random signal days drawn from that symbol's days in the same tercile (2009 on),
next-open entry, held for a hold length drawn from that tercile's real trades, exit at the open.
2000 draws of n trades each; p = share of draws whose mean >= the real mean.

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 experiments/2026-10-28-P-0243/vix_split.py
"""
import csv, json, sys
import numpy as np

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/p0082")
sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-10-07-P-0083")
from p0082 import load, sma  # noqa: E402
from basket_backtest import rsi5_next_open_rp, BASKET  # noqa: E402

OUT = "/Users/triton/PROTEUS/experiments/2026-10-28-P-0243/results.json"
LO, HI = 15.2, 20.7
vix = {}
for r in list(csv.reader(open("/Users/triton/PROTEUS/sandbox/fred/VIXCLS.csv")))[1:]:
    if r[1] not in ("", "."):
        vix[np.datetime64(r[0])] = float(r[1])
vdates = np.array(sorted(vix))
vvals = np.array([vix[d] for d in vdates])


def vix_on(d):
    i = np.searchsorted(vdates, d, side="right") - 1  # that day's close, or the last before it
    return vvals[i] if i >= 0 else np.nan


def terc(v):
    return 0 if v < LO else (1 if v < HI else 2)


rng = np.random.default_rng(20261028)
trades = {0: [], 1: [], 2: []}      # (ret, hold)
pool = {0: [], 1: [], 2: []}        # (symbol open array, signal index)
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
        e, x = w[0], w[-1]               # entry day (filled at its open), exit day (sold at its open)
        if x == len(c) - 1 and rets[x] == np.log(c[x]) - np.log(c[x - 1]):
            continue                     # still open at the end
        sig = idx[e - 1]
        t = terc(vix_on(sig))
        trades[t].append((float(np.expm1(rets[w].sum())), int(x - e)))
    tv = np.array([terc(vix_on(d)) for d in idx])
    m200 = sma(c, 200)
    for i in range(start, len(o) - 60):
        if c[i] > m200[i]:               # same filter as the rule: close above its 200-day average
            pool[tv[i]].append((s, i))

res = {"terciles": [LO, HI], "n_draws": 2000, "by_tercile": {}}
for t, name in ((0, "low VIX < 15.2"), (1, "mid"), (2, "high VIX >= 20.7")):
    a = np.array([r for r, _ in trades[t]])
    holds = np.array([h for _, h in trades[t]])
    n = a.size
    P = pool[t]
    sims = np.empty(2000)
    for j in range(2000):
        pick = rng.integers(0, len(P), n)
        hh = holds[rng.integers(0, n, n)]
        sims[j] = np.mean([opens[P[q][0]][P[q][1] + 1 + h] / opens[P[q][0]][P[q][1] + 1] - 1 for q, h in zip(pick, hh)])
    res["by_tercile"][name] = {
        "trades": int(n), "mean_pct": round(a.mean() * 100, 3), "win_pct": round((a > 0).mean() * 100, 1),
        "t": round(float(a.mean() / (a.std(ddof=1) / np.sqrt(n))), 2), "mean_hold_days": round(float(holds.mean()), 2),
        "control_mean_pct": round(float(sims.mean()) * 100, 3), "excess_pct": round((a.mean() - sims.mean()) * 100, 3),
        "p": round(float((sims >= a.mean()).mean()), 4), "pool_days": len(P)}
    print(name, res["by_tercile"][name], flush=True)
json.dump(res, open(OUT, "w"), indent=1)
