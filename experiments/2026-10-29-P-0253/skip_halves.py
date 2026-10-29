"""P-0253: deepen P-0252. The RSI(5) book (next-open fills, 9 ETFs) with and without a skip when
VIX/VIX3M on the signal day is at or above 1, in two halves by entry date (2009-17, 2018-26), after a
0.1% round trip per trade. Also the skip book's trades per year, since skipping costs exposure.

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 experiments/2026-10-29-P-0253/skip_halves.py
"""
import csv, json, sys
import numpy as np

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/p0082")
sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-10-07-P-0083")
from p0082 import load  # noqa: E402
from basket_backtest import rsi5_next_open_rp, BASKET  # noqa: E402

OUT = "/Users/triton/PROTEUS/experiments/2026-10-29-P-0253/results.json"
COST = 0.001


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
    i = np.searchsorted(rdates, d, side="right") - 1
    return rvals[i] if i >= 0 else np.nan


rows = []   # (entry date, net return, backwardation flag)
for s in BASKET:
    df = load(s)
    o, c = df["open"].to_numpy(), df["close"].to_numpy()
    idx = df.index.values
    start = int(np.searchsorted(idx, np.datetime64("2009-01-01")))
    rets, tid = rsi5_next_open_rp(o, c, 1)
    for k in np.unique(tid[start:][tid[start:] > 0]):
        w = np.where(tid == k)[0]
        e, x = w[0], w[-1]
        if x == len(c) - 1 and rets[x] == np.log(c[x]) - np.log(c[x - 1]):
            continue
        rows.append((idx[e], float(np.expm1(rets[w].sum())) - COST, ratio_on(idx[e - 1]) >= 1))

cut = np.datetime64("2018-01-01")
res = {"cost_round_trip": COST, "halves": {}}
for name, lo, hi in (("2009-17", np.datetime64("2009-01-01"), cut), ("2018-26", cut, np.datetime64("2027-01-01"))):
    sub = [r for r in rows if lo <= r[0] < hi]
    full = np.array([r[1] for r in sub])
    skip = np.array([r[1] for r in sub if not r[2]])
    back = np.array([r[1] for r in sub if r[2]])
    years = (min(hi, np.datetime64("2026-10-29")) - lo).astype("timedelta64[D]").astype(int) / 365.25
    res["halves"][name] = {
        "full_trades": int(full.size), "full_mean_pct": round(full.mean() * 100, 3),
        "skip_trades": int(skip.size), "skip_mean_pct": round(skip.mean() * 100, 3),
        "skipped_trades": int(back.size), "skipped_mean_pct": round(back.mean() * 100, 3) if back.size else None,
        "skip_minus_full_pts": round((skip.mean() - full.mean()) * 100, 3),
        "full_sum_pct": round(full.sum() * 100, 1), "skip_sum_pct": round(skip.sum() * 100, 1),
        "skip_trades_per_year": round(skip.size / years, 1)}
    print(name, res["halves"][name], flush=True)
json.dump(res, open(OUT, "w"), indent=1)
