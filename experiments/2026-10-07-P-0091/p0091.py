"""P-0091: IBS as a second systems book, with a rule a trader could actually follow.

Fixed before the first run (this file is committed before results.json):
  RSI(5) book  exactly the systems book's scored rule: close above its 200-day average and RSI(5)
               below 30 at the close, buy next open; RSI(5) above 50 at a close, sell next open.
  gated IBS    IBS = (close - low) / (high - low) below 0.2 at the close, AND the RSI(5) book flat
               after that close's decisions (no position, no buy or sell pending); buy next open;
               sell the next open after a close above yesterday's high. One IBS position at a time.
               Once in, the IBS trade runs to its own exit even if RSI(5) buys meanwhile.
  markets      the nine-ETF basket, as traded (not dividend-adjusted, like the live book), scored
               from 2009-01-01, on the dates all nine share.
  luck test    neurotrader888's bar permutation, the same shuffle for all nine markets (dates
               aligned), so dips still arrive together; 1,000 shuffles. Fitness: profit factor of
               the pooled daily strategy returns. Also run per market (1,000 each).
  pass mark    a candidate second book only if all three hold: pooled p < 0.05, mean trade > 0,
               and a positive mean trade in at least 5 of the 9 markets.
  portfolio    each market gets 1/9 of capital; in "both", RSI(5) and IBS each get half of that
               slice. Compared on growth, drawdown and time in the market.

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 experiments/2026-10-07-P-0091/p0091.py
"""
import json, os, sys
import numpy as np
import pandas as pd
from numba import njit

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/p0082")
from p0082 import load, sma, rsi_wilder, permute  # noqa: E402

OUT = "/Users/triton/PROTEUS/experiments/2026-10-07-P-0091"
BASKET = ["SPY", "QQQ", "DIA", "IWM", "EFA", "EEM", "EWU", "EWJ", "EWG"]
IBS_MAX = 0.2
FROM = "2009-01-01"
N_PERM = int(os.environ.get("N_PERM", "1000"))


@njit(cache=True)
def books(o, h, l, c, gate_on):
    """Both books in one pass. Returns rsi rets, rsi trade ids, ibs rets, ibs trade ids."""
    n = c.size
    r = rsi_wilder(c, 5)
    m = sma(c, 200)
    rr = np.zeros(n)
    rt = np.zeros(n, dtype=np.int64)
    ir = np.zeros(n)
    it = np.zeros(n, dtype=np.int64)
    rs = 0   # RSI(5): 0 flat, 1 buy next open, 2 long, 3 sell next open
    ist = 0  # IBS: same states
    rk = 0
    ik = 0
    for t in range(1, n):
        # opens and holding, RSI(5)
        if rs == 1:
            rr[t] = np.log(c[t]) - np.log(o[t])
            rs = 2
            rk += 1
            rt[t] = rk
        elif rs == 2:
            rr[t] = np.log(c[t]) - np.log(c[t - 1])
            rt[t] = rk
        elif rs == 3:
            rr[t] = np.log(o[t]) - np.log(c[t - 1])
            rt[t] = rk
            rs = 0
        # opens and holding, IBS
        if ist == 1:
            ir[t] = np.log(c[t]) - np.log(o[t])
            ist = 2
            ik += 1
            it[t] = ik
        elif ist == 2:
            ir[t] = np.log(c[t]) - np.log(c[t - 1])
            it[t] = ik
        elif ist == 3:
            ir[t] = np.log(o[t]) - np.log(c[t - 1])
            it[t] = ik
            ist = 0
        # the close: RSI(5) decides first
        if rs == 2:
            if r[t] > 50:
                rs = 3
        elif rs == 0 and t >= 3 and not np.isnan(m[t]) and not np.isnan(r[t - 3]):
            if c[t] > m[t] and r[t] < 30:
                rs = 1
        # then IBS, gated on the RSI(5) book being flat after its decision
        if ist == 2:
            if c[t] > h[t - 1]:
                ist = 3
        elif ist == 0 and h[t] > l[t]:
            if (c[t] - l[t]) / (h[t] - l[t]) < IBS_MAX and (rs == 0 or not gate_on):
                ist = 1
    return rr, rt, ir, it


def trades(rets, tid, start):
    out = {}
    for i in range(start, len(tid)):
        k = int(tid[i])
        if k:
            out[k] = out.get(k, 0.0) + rets[i]
    return np.expm1(np.array(list(out.values()))) if out else np.array([])


def tstats(a):
    if a.size < 2:
        return {"trades": int(a.size)}
    return {"trades": int(a.size), "mean_pct": round(float(a.mean() * 100), 3), "win_pct": round(float((a > 0).mean() * 100), 1),
            "t": round(float(a.mean() / (a.std(ddof=1) / np.sqrt(a.size))), 2)}


def pf_pooled(rets_list, start):
    gp = gl = 0.0
    for r in rets_list:
        x = r[start:]
        gp += x[x > 0].sum()
        gl += -x[x < 0].sum()
    return gp / gl if gl > 0 else 0.0


def eq_stats(r, idx):
    eq = np.cumprod(1 + r)
    yrs = (idx[-1] - idx[0]).days / 365.25
    dd = 1 - eq / np.maximum.accumulate(eq)
    return {"growth_x": round(float(eq[-1]), 3), "cagr_pct": round(float((eq[-1] ** (1 / yrs) - 1) * 100), 2),
            "max_dd_pct": round(float(dd.max() * 100), 2), "vol_pct": round(float(r.std() * np.sqrt(252) * 100), 2),
            "sharpe": round(float(r.mean() / r.std() * np.sqrt(252)), 3) if r.std() > 0 else None}


def main():
    data = {s: load(s, adjusted=False) for s in BASKET}
    common = sorted(set.intersection(*[set(d.index) for d in data.values()]))
    idx = pd.DatetimeIndex(common)
    arr = {s: tuple(data[s].loc[idx, x].to_numpy() for x in ("open", "high", "low", "close")) for s in BASKET}
    start = int(np.searchsorted(idx.values, np.datetime64(FROM)))
    res = {"from": FROM, "to": str(idx[-1].date()), "common_days": len(idx), "ibs_max": IBS_MAX, "markets": {}}
    out = {s: books(*arr[s], True) for s in BASKET}
    ungated = {s: books(*arr[s], False) for s in BASKET}
    pooled = {"rsi5": [], "ibs_gated": [], "ibs_ungated": []}
    pos_markets = 0
    for s in BASKET:
        rr, rt, ir, it = out[s]
        _, _, ur, ut = ungated[s]
        a_r, a_i, a_u = trades(rr, rt, start), trades(ir, it, start), trades(ur, ut, start)
        pooled["rsi5"] += list(a_r)
        pooled["ibs_gated"] += list(a_i)
        pooled["ibs_ungated"] += list(a_u)
        pos_markets += a_i.size > 0 and a_i.mean() > 0
        res["markets"][s] = {"rsi5": tstats(a_r), "ibs_gated": tstats(a_i), "ibs_ungated": tstats(a_u)}
    years = (idx[-1] - idx[start]).days / 365.25
    res["pooled"] = {k: dict(tstats(np.array(v)), per_year=round(len(v) / years, 1)) for k, v in pooled.items()}
    res["markets_positive_ibs_gated"] = int(pos_markets)
    # per-market luck tests on gated IBS
    for s in BASKET:
        o, h, l, c = arr[s]
        real = pf_pooled([out[s][2]], start)
        better = 1
        for k in range(N_PERM):
            po, ph, pl, pc = permute(o, h, l, c, start, 7001 + k)
            better += pf_pooled([books(po, ph, pl, pc, True)[2]], start) >= real
        res["markets"][s]["ibs_gated"]["p"] = round(better / (N_PERM + 1), 4)
        print(s, res["markets"][s]["ibs_gated"], flush=True)
    # pooled luck test: one shuffle for all nine (same seed, same length -> same day order)
    real = {"ibs_gated": pf_pooled([out[s][2] for s in BASKET], start), "rsi5": pf_pooled([out[s][0] for s in BASKET], start),
            "ibs_ungated": pf_pooled([ungated[s][2] for s in BASKET], start)}
    better = {k: 1 for k in real}
    for k in range(N_PERM):
        perm = {s: permute(*arr[s], start, 11001 + k) for s in BASKET}
        g = {s: books(*perm[s], True) for s in BASKET}
        u = {s: books(*perm[s], False) for s in BASKET}
        better["ibs_gated"] += pf_pooled([g[s][2] for s in BASKET], start) >= real["ibs_gated"]
        better["rsi5"] += pf_pooled([g[s][0] for s in BASKET], start) >= real["rsi5"]
        better["ibs_ungated"] += pf_pooled([u[s][2] for s in BASKET], start) >= real["ibs_ungated"]
    res["pooled_luck"] = {k: {"real_bar_pf": round(float(real[k]), 3), "p": round(better[k] / (N_PERM + 1), 4), "n": N_PERM} for k in real}
    # portfolio: 1/9 a market; "both" splits each slice half and half
    E = idx[start:]
    sim = lambda x: np.expm1(x[start:])
    rsi_port = np.mean([sim(out[s][0]) for s in BASKET], axis=0)
    ibs_port = np.mean([sim(out[s][2]) for s in BASKET], axis=0)
    both_port = 0.5 * rsi_port + 0.5 * ibs_port
    spy = np.concatenate([[0.0], arr["SPY"][3][start + 1:] / arr["SPY"][3][start:-1] - 1])
    res["portfolio"] = {"rsi5_alone": eq_stats(rsi_port, E), "ibs_gated_alone": eq_stats(ibs_port, E), "both": eq_stats(both_port, E),
                        "spy_price_only": eq_stats(spy, E),
                        "time_in_market_pct": {
                            "rsi5": round(float(np.mean([(out[s][1][start:] != 0).mean() for s in BASKET]) * 100), 1),
                            "ibs_gated": round(float(np.mean([(out[s][3][start:] != 0).mean() for s in BASKET]) * 100), 1)},
                        "daily_corr_rsi5_ibs": round(float(np.corrcoef(rsi_port, ibs_port)[0, 1]), 3)}
    pl = res["pooled"]["ibs_gated"]
    res["pass_mark"] = {"pooled_p_lt_05": res["pooled_luck"]["ibs_gated"]["p"] < 0.05, "mean_gt_0": pl.get("mean_pct", 0) > 0,
                        "five_of_nine_positive": pos_markets >= 5}
    res["pass_mark"]["passes"] = all(res["pass_mark"].values())
    json.dump(res, open(os.path.join(OUT, "results.json"), "w"), indent=1, default=str)
    print("pooled", res["pooled"])
    print("luck", res["pooled_luck"])
    print("portfolio", res["portfolio"])
    print("pass", res["pass_mark"])


if __name__ == "__main__":
    main()
