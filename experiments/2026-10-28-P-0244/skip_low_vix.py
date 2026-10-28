"""P-0244: the RSI(5) book with a skip when the signal-day VIX close is under a walk-forward cut.

Cut for year Y = lower tercile (33.3rd percentile) of VIXCLS closes from 1990 to the end of Y-1.
Same rule, basket and fills as P-0243; 0.05% a side (0.10% round trip) on every trade.
Growth: each ETF a 1/9 sleeve compounding its own trades; book growth = mean of sleeve multiples.
Control on kept trades: random filtered days with VIX at or above the cut, holds drawn from kept trades.

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 experiments/2026-10-28-P-0244/skip_low_vix.py
"""
import csv, json, sys
import numpy as np

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/p0082")
sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-10-07-P-0083")
from p0082 import load, sma  # noqa: E402
from basket_backtest import rsi5_next_open_rp, BASKET  # noqa: E402

OUT = "/Users/triton/PROTEUS/experiments/2026-10-28-P-0244/results.json"
COST = 0.001
vd, vv = [], []
for r in list(csv.reader(open("/Users/triton/PROTEUS/sandbox/fred/VIXCLS.csv")))[1:]:
    if r[1] not in ("", "."):
        vd.append(np.datetime64(r[0]))
        vv.append(float(r[1]))
vd, vv = np.array(vd), np.array(vv)
cut = {y: float(np.percentile(vv[vd < np.datetime64("%d-01-01" % y)], 100 / 3)) for y in range(2009, 2027)}


def vix_on(d):
    i = np.searchsorted(vd, d, side="right") - 1
    return vv[i]


def year(d):
    return int(str(d)[:4])


rng = np.random.default_rng(20261028)
allt, kept, pool, opens, sleeves_all, sleeves_kept = [], [], [], {}, [], []
for s in BASKET:
    df = load(s)
    o, c = df["open"].to_numpy(), df["close"].to_numpy()
    idx = df.index.values
    opens[s] = o
    start = int(np.searchsorted(idx, np.datetime64("2009-01-01")))
    rets, tid = rsi5_next_open_rp(o, c, 1)
    ga = gk = 1.0
    for k in np.unique(tid[start:][tid[start:] > 0]):
        w = np.where(tid == k)[0]
        e, x = w[0], w[-1]
        if x == len(c) - 1:
            continue
        sig = idx[e - 1]
        r = float(np.expm1(rets[w].sum())) - COST
        allt.append(r)
        ga *= 1 + r
        if vix_on(sig) >= cut[year(sig)]:
            kept.append((r, int(x - e)))
            gk *= 1 + r
    sleeves_all.append(ga)
    sleeves_kept.append(gk)
    m200 = sma(c, 200)
    for i in range(start, len(o) - 60):
        if c[i] > m200[i] and vix_on(idx[i]) >= cut[year(idx[i])]:
            pool.append((s, i))

a = np.array(allt)
kr = np.array([r for r, _ in kept])
holds = np.array([h for _, h in kept])
sims = np.empty(2000)
for j in range(2000):
    pick = rng.integers(0, len(pool), kr.size)
    hh = holds[rng.integers(0, kr.size, kr.size)]
    sims[j] = np.mean([opens[pool[q][0]][pool[q][1] + 1 + h] / opens[pool[q][0]][pool[q][1] + 1] - 1 - COST for q, h in zip(pick, hh)])
res = {"cuts_by_year": {y: round(v, 2) for y, v in cut.items()}, "cost_round_trip": COST,
       "book": {"trades": int(a.size), "net_mean_pct": round(a.mean() * 100, 3), "growth_x": round(float(np.mean(sleeves_all)), 3)},
       "skip": {"trades": int(kr.size), "dropped_pct": round(100 * (1 - kr.size / a.size), 1),
                "net_mean_pct": round(kr.mean() * 100, 3), "growth_x": round(float(np.mean(sleeves_kept)), 3),
                "control_net_mean_pct": round(float(sims.mean()) * 100, 3), "p": round(float((sims >= kr.mean()).mean()), 4)}}
json.dump(res, open(OUT, "w"), indent=1)
print(json.dumps(res))
