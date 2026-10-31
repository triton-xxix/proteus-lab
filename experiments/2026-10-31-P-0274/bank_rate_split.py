"""P-0274: the systems book's RSI(5) simple rule, next-open fills, split by whether the signal day
falls in the 5 trading days before a Bank of England Bank Rate change (BoE series IUDBEDR, daily, from
2 Jan 2009, pulled keyless on 31 Oct 2026 to sandbox/boe-bank-rate.csv). Same backtest and control
as P-0243 (vix_split.py): random signal days drawn from the same bucket's pool of days with close above
the 200-day average, next-open entry, hold drawn from the bucket's real trades, 2000 draws.

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 experiments/2026-10-31-P-0274/bank_rate_split.py
"""
import csv, json, sys
from datetime import datetime
import numpy as np

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/p0082")
sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-10-07-P-0083")
from p0082 import load, sma  # noqa: E402
from basket_backtest import rsi5_next_open_rp, BASKET  # noqa: E402

OUT = "/Users/triton/PROTEUS/experiments/2026-10-31-P-0274/results.json"
WINDOW = 5

# rate-change dates: the first day the daily series shows a new value
rows = [r for r in csv.reader(open("/Users/triton/PROTEUS/sandbox/boe-bank-rate.csv")) if len(r) == 2 and r[0] != "DATE"]
series = [(np.datetime64(datetime.strptime(r[0], "%d %b %Y").date()), float(r[1])) for r in rows]
changes = [d for (d, v), (_, pv) in zip(series[1:], series[:-1]) if v != pv]
print("bank rate rows", len(series), "changes since 2009:", len(changes), "last", str(changes[-1]), series[-1][1], flush=True)

rng = np.random.default_rng(20261031)


def run(symbols, label):
    trades = {"pre": [], "rest": []}
    pool = {"pre": [], "rest": []}
    opens = {}
    for s in symbols:
        df = load(s)
        o, c = df["open"].to_numpy(), df["close"].to_numpy()
        idx = df.index.values
        opens[s] = o
        start = int(np.searchsorted(idx, np.datetime64("2009-01-01")))
        # position of each change date on this symbol's calendar (the next trading day on or after it)
        cpos = np.unique(np.searchsorted(idx, np.array(changes), side="left"))
        cpos = cpos[cpos < len(idx)]
        pre = np.zeros(len(idx), dtype=bool)
        for p in cpos:
            pre[max(0, p - WINDOW):p] = True      # the WINDOW trading days before the change day
        rets, tid = rsi5_next_open_rp(o, c, 1)
        ks = np.unique(tid[start:][tid[start:] > 0])
        for k in ks:
            w = np.where(tid == k)[0]
            e, x = w[0], w[-1]
            if x == len(c) - 1 and rets[x] == np.log(c[x]) - np.log(c[x - 1]):
                continue
            b = "pre" if pre[e - 1] else "rest"
            trades[b].append((float(np.expm1(rets[w].sum())), int(x - e)))
        m200 = sma(c, 200)
        for i in range(start, len(o) - 60):
            if c[i] > m200[i]:
                pool["pre" if pre[i] else "rest"].append((s, i))
    out = {}
    for b in ("pre", "rest"):
        a = np.array([r for r, _ in trades[b]])
        holds = np.array([h for _, h in trades[b]])
        n = a.size
        P = pool[b]
        if n < 2 or not P:
            out[b] = {"trades": int(n), "note": "too few"}
            print(label, b, out[b], flush=True)
            continue
        sims = np.empty(2000)
        for j in range(2000):
            pick = rng.integers(0, len(P), n)
            hh = holds[rng.integers(0, n, n)]
            sims[j] = np.mean([opens[P[q][0]][P[q][1] + 1 + h] / opens[P[q][0]][P[q][1] + 1] - 1 for q, h in zip(pick, hh)])
        out[b] = {
            "trades": int(n), "mean_pct": round(a.mean() * 100, 3), "win_pct": round((a > 0).mean() * 100, 1),
            "t": round(float(a.mean() / (a.std(ddof=1) / np.sqrt(n))), 2) if n > 1 else None,
            "mean_hold_days": round(float(holds.mean()), 2),
            "control_mean_pct": round(float(sims.mean()) * 100, 3), "excess_pct": round((a.mean() - sims.mean()) * 100, 3),
            "p": round(float((sims >= a.mean()).mean()), 4), "pool_days": len(P)}
        print(label, b, out[b], flush=True)
    return out


res = {"window_trading_days_before_change": WINDOW, "bank_rate_changes_since_2009": len(changes),
       "change_dates": [str(d) for d in changes], "n_draws": 2000,
       "EWU": run(["EWU"], "EWU"), "SPY": run(["SPY"], "SPY"), "all_nine": run(BASKET, "all nine")}
json.dump(res, open(OUT, "w"), indent=1)
