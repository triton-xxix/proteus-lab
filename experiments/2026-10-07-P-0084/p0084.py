"""P-0084: trend following the way the funds run it, one portfolio across 28 ETFs.

Everything below was fixed and committed before the first run (the commit before results.json is
the proof). No parameter is searched, so there is no sweep for the luck test to pay for.

Universe (28, all trading from April 2007):
  equities    SPY QQQ IWM EFA EEM EWJ EWU EWG EWZ FXI VNQ
  bonds       TLT IEF LQD HYG TIP
  commodities GLD SLV USO UNG DBA DBC
  currencies  FXE FXY FXB FXA FXC UUP
Data: Yahoo daily closes scaled to total return (sandbox/p0082/data, fetch_prices.py).

Rules:
  signal A (primary)   12-month time-series momentum: long if the last 252 days' return is
                       positive, short if negative (Moskowitz, Ooi and Pedersen 2012).
  signal B (secondary) 100-day breakout: long on a close at a 100-day high, short at a 100-day low,
                       otherwise keep the last position.
  sizing               each market scaled to 40% annualised volatility on its last 60 days of
                       returns, divided by 28; gross exposure capped at 3x.
  timing               decided at the close, held from the next day; rebalanced every 5 trading
                       days. Costs 5 basis points per unit of weight traded.
  benchmarks           60/40 (SPY/IEF, rebalanced daily), SPY alone, and a 50/50 blend of 60/40
                       with signal A.
Luck test: the 28 markets' daily returns are shuffled together, the same day order for every
market, so their correlations survive and every trend is destroyed. 1,000 shuffles. Fitness is the
portfolio's Sharpe ratio. Adapted from neurotrader888/mcpt for a close-only strategy.

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 experiments/2026-10-07-P-0084/p0084.py
"""
import json, os, sys
import numpy as np
import pandas as pd

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/p0082")
from p0082 import load  # noqa: E402

OUT = "/Users/triton/PROTEUS/experiments/2026-10-07-P-0084"
UNIVERSE = {
    "equities": ["SPY", "QQQ", "IWM", "EFA", "EEM", "EWJ", "EWU", "EWG", "EWZ", "FXI", "VNQ"],
    "bonds": ["TLT", "IEF", "LQD", "HYG", "TIP"],
    "commodities": ["GLD", "SLV", "USO", "UNG", "DBA", "DBC"],
    "currencies": ["FXE", "FXY", "FXB", "FXA", "FXC", "UUP"],
}
SYMS = [s for g in UNIVERSE.values() for s in g]
LOOKBACK, BREAKOUT, VOL_N, VOL_TARGET, GROSS_CAP, REBAL, COST = 252, 100, 60, 0.40, 3.0, 5, 0.0005
EVAL_FROM = "2008-05-01"
N_PERM = int(os.environ.get("N_PERM", "1000"))


def closes():
    df = pd.concat({s: load(s)["close"] for s in SYMS}, axis=1).dropna()
    return df


def signal_tsmom(logp):
    return np.sign(logp - np.roll(logp, LOOKBACK, axis=0)) * (np.arange(len(logp))[:, None] >= LOOKBACK)


def signal_breakout(logp):
    p = pd.DataFrame(logp)
    hi = p.rolling(BREAKOUT).max().shift(1)
    lo = p.rolling(BREAKOUT).min().shift(1)
    s = pd.DataFrame(np.nan, index=p.index, columns=p.columns)
    s[p >= hi] = 1.0
    s[p <= lo] = -1.0
    return s.ffill().fillna(0.0).to_numpy()


def portfolio(rets, sig):
    """rets: T x N simple daily returns. sig: T x N signals at each close. Returns daily portfolio
    returns (index t = return over day t, from weights set at close t-1) and the weight matrix."""
    T, N = rets.shape
    lr = np.log1p(rets)
    c1 = np.cumsum(np.vstack([np.zeros((1, N)), lr]), axis=0)
    c2 = np.cumsum(np.vstack([np.zeros((1, N)), lr ** 2]), axis=0)
    vol = np.full((T, N), np.nan)
    m = (c1[VOL_N:] - c1[:-VOL_N]) / VOL_N
    v = (c2[VOL_N:] - c2[:-VOL_N]) / VOL_N - m ** 2
    vol[VOL_N - 1:] = np.sqrt(np.maximum(v, 1e-12) * 252)
    raw = sig * (VOL_TARGET / vol) / N
    raw = np.nan_to_num(raw)
    gross = np.abs(raw).sum(axis=1, keepdims=True)
    raw = raw * np.minimum(1.0, GROSS_CAP / np.maximum(gross, 1e-12))
    w = np.zeros_like(raw)
    cur = np.zeros(N)
    for t in range(T):
        if t % REBAL == 0:
            cur = raw[t]
        w[t] = cur
    held = np.vstack([np.zeros((1, N)), w[:-1]])
    turn = np.abs(np.diff(np.vstack([np.zeros((1, N)), w]), axis=0)).sum(axis=1)
    cost = np.concatenate([[0.0], turn[:-1]]) * COST
    return (held * rets).sum(axis=1) - cost, w


def summarise(r, idx):
    r = pd.Series(r, index=idx)
    eq = (1 + r).cumprod()
    yrs = (idx[-1] - idx[0]).days / 365.25
    dd = 1 - eq / eq.cummax()
    by_year = (1 + r).groupby(idx.year).prod() - 1
    return {
        "cagr_pct": round(float((eq.iloc[-1] ** (1 / yrs) - 1) * 100), 2),
        "vol_pct": round(float(r.std() * np.sqrt(252) * 100), 2),
        "sharpe": round(float(r.mean() / r.std() * np.sqrt(252)), 3),
        "max_dd_pct": round(float(dd.max() * 100), 2),
        "growth_x": round(float(eq.iloc[-1]), 2),
        "by_year_pct": {int(k): round(float(v * 100), 1) for k, v in by_year.items()},
    }


def sharpe(r):
    return float(r.mean() / r.std() * np.sqrt(252))


def main():
    px = closes()
    idx = px.index
    rets = px.pct_change().fillna(0.0).to_numpy()
    logp = np.log(px.to_numpy())
    ev = idx >= pd.Timestamp(EVAL_FROM)
    res = {"universe": UNIVERSE, "from": str(idx[0].date()), "eval_from": EVAL_FROM, "to": str(idx[-1].date()),
           "params": {"lookback": LOOKBACK, "breakout": BREAKOUT, "vol_n": VOL_N, "vol_target": VOL_TARGET,
                      "gross_cap": GROSS_CAP, "rebalance_days": REBAL, "cost_per_unit": COST}}
    ra, wa = portfolio(rets, signal_tsmom(logp))
    rb, wb = portfolio(rets, signal_breakout(logp))
    spy = rets[:, SYMS.index("SPY")]
    sixty = 0.6 * spy + 0.4 * rets[:, SYMS.index("IEF")]
    blend = 0.5 * sixty + 0.5 * ra
    E = idx[ev]
    res["tsmom_12m"] = summarise(ra[ev], E)
    res["breakout_100d"] = summarise(rb[ev], E)
    res["sixty_forty"] = summarise(sixty[ev], E)
    res["spy"] = summarise(spy[ev], E)
    res["blend_6040_plus_tsmom"] = summarise(blend[ev], E)
    res["corr_tsmom_vs_6040"] = round(float(np.corrcoef(ra[ev], sixty[ev])[0, 1]), 3)
    res["corr_breakout_vs_6040"] = round(float(np.corrcoef(rb[ev], sixty[ev])[0, 1]), 3)
    res["avg_gross_tsmom"] = round(float(np.abs(wa[ev]).sum(axis=1).mean()), 2)
    # by asset class: the primary signal run on each class alone (same sizing, N = class size)
    res["tsmom_by_class_sharpe"] = {}
    for g, ss in UNIVERSE.items():
        cols = [SYMS.index(s) for s in ss]
        rg, _ = portfolio(rets[:, cols], signal_tsmom(logp[:, cols]))
        res["tsmom_by_class_sharpe"][g] = round(sharpe(rg[ev]), 3)
    # sub-periods
    for lab, a, b in (("2008_2016", "2008-05-01", "2016-12-31"), ("2017_2026", "2017-01-01", "2026-12-31")):
        m = (idx >= pd.Timestamp(a)) & (idx <= pd.Timestamp(b))
        res["tsmom_" + lab] = {"sharpe": round(sharpe(ra[m]), 3), "cagr_pct": summarise(ra[m], idx[m])["cagr_pct"],
                               "sixty_forty_sharpe": round(sharpe(sixty[m]), 3)}
    # luck test: shuffle whole days across all markets together
    rng = np.random.default_rng(84)
    real_a, real_b = sharpe(ra[ev]), sharpe(rb[ev])
    ba = bb = 1
    perm_a, perm_b = [], []
    # Keep the warm-up real and shuffle the rest. Fixed before the first run: the data starts only
    # 260 days before EVAL_FROM, so this offset was negative and broke the index; clamp to 0, which
    # shuffles the whole series (neurotrader's start_index=0).
    first = max(0, np.where(ev)[0][0] - LOOKBACK - VOL_N)
    for k in range(N_PERM):
        order = np.concatenate([np.arange(first), first + rng.permutation(len(rets) - first)])
        pr = rets[order]
        plogp = np.vstack([logp[:1], logp[0] + np.cumsum(np.log1p(pr[1:]), axis=0)])
        pa, _ = portfolio(pr, signal_tsmom(plogp))
        pb, _ = portfolio(pr, signal_breakout(plogp))
        sa, sb = sharpe(pa[ev]), sharpe(pb[ev])
        perm_a.append(sa)
        perm_b.append(sb)
        ba += sa >= real_a
        bb += sb >= real_b
    res["mcpt"] = {"n": N_PERM,
                   "tsmom_12m": {"real_sharpe": round(real_a, 3), "p": round(ba / (N_PERM + 1), 4),
                                 "perm_median": round(float(np.median(perm_a)), 3), "perm_95th": round(float(np.percentile(perm_a, 95)), 3)},
                   "breakout_100d": {"real_sharpe": round(real_b, 3), "p": round(bb / (N_PERM + 1), 4),
                                     "perm_median": round(float(np.median(perm_b)), 3), "perm_95th": round(float(np.percentile(perm_b, 95)), 3)}}
    json.dump(res, open(os.path.join(OUT, "results.json"), "w"), indent=1)
    for k in ("tsmom_12m", "breakout_100d", "sixty_forty", "spy", "blend_6040_plus_tsmom"):
        print(k, {x: res[k][x] for x in ("cagr_pct", "vol_pct", "sharpe", "max_dd_pct", "growth_x")})
    print("corr", res["corr_tsmom_vs_6040"], res["corr_breakout_vs_6040"], "gross", res["avg_gross_tsmom"])
    print("by class", res["tsmom_by_class_sharpe"])
    print("sub", res["tsmom_2008_2016"], res["tsmom_2017_2026"])
    print("mcpt", res["mcpt"])


if __name__ == "__main__":
    main()
