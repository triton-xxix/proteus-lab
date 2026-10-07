"""P-0083 baseline: the P-0082 survivor (RSI(5) dip-buying inside an uptrend) on a basket fixed
before this was run, 2009 onwards, with neurotrader's permutation test. Two fills:
  close      the rule as tested: signal and fill at the same close (a market-on-close order)
  next_open  signal at the close, fill at the next open (what an order placed after the close gets)

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 experiments/2026-10-07-P-0083/basket_backtest.py
"""
import json, os, sys
import numpy as np
from numba import njit

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/p0082")
from p0082 import load, rsi_wilder, sma, rsi5_rets, rsi5_rp, stats, mcpt, pf, trades_from_rp  # noqa: E402

OUT = "/Users/triton/PROTEUS/experiments/2026-10-07-P-0083/basket_backtest.json"
BASKET = ["SPY", "QQQ", "DIA", "IWM", "EFA", "EEM", "EWU", "EWJ", "EWG"]


@njit(cache=True)
def rsi5_next_open_rp(o, c, variant):
    r = rsi_wilder(c, 5)
    m = sma(c, 200)
    rets = np.zeros(c.size)
    tid = np.zeros(c.size, dtype=np.int64)
    state = 0  # 0 flat, 1 buy at next open, 2 long, 3 sell at next open
    k = 0
    for t in range(1, c.size):
        if state == 1:
            rets[t] = np.log(c[t]) - np.log(o[t])
            state = 2
            k += 1
            tid[t] = k
        elif state == 2:
            rets[t] = np.log(c[t]) - np.log(c[t - 1])
            tid[t] = k
        elif state == 3:
            rets[t] = np.log(o[t]) - np.log(c[t - 1])
            tid[t] = k
            state = 0
        if state == 2:
            if r[t] > 50:
                state = 3
        elif state == 0 and t >= 3 and not np.isnan(m[t]) and not np.isnan(r[t - 3]):
            ok = c[t] > m[t] and r[t] < 30
            if variant >= 2:
                ok = ok and r[t] < r[t - 1] and r[t - 1] < r[t - 2] and r[t - 2] < r[t - 3]
            if variant >= 3:
                ok = ok and r[t - 3] < 60
            if ok:
                state = 1
    return rets, tid


@njit(cache=True)
def rsi5_rets_next_open(o, c, variant):
    return rsi5_next_open_rp(o, c, variant)[0]


def main():
    res = {"basket": BASKET, "from": "2009-01-01", "n_perm": 1000, "markets": {}}
    pooled = {k: [] for k in ("simple_close", "simple_next_open", "triple_close", "triple_next_open")}
    for s in BASKET:
        df = load(s)
        o, h, l, c = (df[x].to_numpy() for x in ("open", "high", "low", "close"))
        start = int(np.searchsorted(df.index.values, np.datetime64("2009-01-01")))
        row = {}
        for v, vn in ((1, "simple"), (3, "triple")):
            for fill, fn, rp in (("close", lambda o, h, l, c, v=v: rsi5_rets(c, v), lambda v=v: rsi5_rp(c, v)),
                                 ("next_open", lambda o, h, l, c, v=v: rsi5_rets_next_open(o, c, v), lambda v=v: rsi5_next_open_rp(o, c, v))):
                key = vn + "_" + fill
                st = stats(rp(), df.index, start)
                real, p, med = mcpt(lambda o, h, l, c, fn=fn: pf(fn(o, h, l, c), start), o, h, l, c, start, 1000, seed0=9001)
                st["p"] = round(p, 4)
                row[key] = st
                rets, tid = rp()
                pooled[key] += [float(np.expm1(t[2])) for t in trades_from_rp((rets[start:], tid[start:]), df.index[start:])]
        res["markets"][s] = row
        print(s, " | ".join("%s %d tr avg %.2f%% win %.0f%% p %.3f" % (k, r["trades"], r["avg_trade_pct"], r["win_rate"], r["p"])
                             for k, r in row.items()), flush=True)
    years = 17.76
    res["pooled"] = {}
    for k, tr in pooled.items():
        a = np.array(tr)
        t = a.mean() / (a.std(ddof=1) / np.sqrt(a.size))
        res["pooled"][k] = {"trades": int(a.size), "per_year": round(a.size / years, 1), "avg_trade_pct": round(a.mean() * 100, 3),
                            "sd_trade_pct": round(a.std(ddof=1) * 100, 3), "win_rate": round((a > 0).mean() * 100, 1), "t_stat": round(float(t), 2)}
        print("pooled", k, res["pooled"][k])
    json.dump(res, open(OUT, "w"), indent=1)


if __name__ == "__main__":
    main()
