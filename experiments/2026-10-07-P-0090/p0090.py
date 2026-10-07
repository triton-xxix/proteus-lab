"""P-0090: two monthly or weekly timing models, replicated on free ETF data, luck-tested, scored
against 60/40 and SPY. Fixed before the run.

GEM (Antonacci, A-13): at each month end, 12-month total returns of SPY, EFA and BIL. If SPY has
  not beaten BIL, hold AGG next month; else hold the better of SPY and EFA. ETF proxies: SPY, EFA,
  AGG, BIL (T-bills; BIL starts 2007-05-30, so the first decision is 2008-05-30 and the record runs
  June 2008 to October 2026, about 220 months). Claimed (third-party paper, 1971-2026): 15.2% a
  year v 11.3% S&P, max drawdown 21.7% v 50.9%, about 1.5 switches a year; since 2010 about 9.5%
  against over 14% for the S&P.
Fabian (A-12): weekly closes. Long SPY when ^GSPC, ^DJI and ^DJU are all above their 39-week
  average; sell when at least two of the three are below it; cash earns BIL's return (zero before
  BIL exists). Record 1993 (SPY start) to 2026. No figures claimed.
Luck tests: joint shuffles of the period returns across every series the model reads (same order
for all, so correlations survive and the trends die), 1,000 draws, fitness Sharpe. GEM's bills are
left unshuffled. Benchmarks on the same months or weeks: SPY, 60/40 (SPY/IEF, rebalanced each
period; IEF from 2002-07).

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 /Users/triton/PROTEUS/experiments/2026-10-07-P-0090/p0090.py
"""
import json, os, sys, time
import numpy as np
import pandas as pd

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/p0082")
from p0082 import load  # noqa: E402

OUT = "/Users/triton/PROTEUS/experiments/2026-10-07-P-0090"
N_PERM = int(os.environ.get("N_PERM", "1000"))


def tr_close(sym):
    return load(sym, adjusted=True)["close"]


def summarise(r, per_year):
    r = pd.Series(r).dropna()
    eq = (1 + r).cumprod()
    yrs = len(r) / per_year
    dd = 1 - eq / eq.cummax()
    return {"cagr_pct": round(float(eq.iloc[-1] ** (1 / yrs) - 1) * 100, 2), "vol_pct": round(float(r.std() * np.sqrt(per_year) * 100), 2),
            "sharpe": round(float(r.mean() / r.std() * np.sqrt(per_year)), 3), "max_dd_pct": round(float(dd.max() * 100), 2),
            "growth_x": round(float(eq.iloc[-1]), 2), "periods": int(len(r))}


def sharpe(r, per_year):
    r = np.asarray(r)
    return float(r.mean() / r.std() * np.sqrt(per_year))


# ---------------------------------------------------------------- GEM
def gem_returns(mr, start):
    """mr: DataFrame of monthly simple returns SPY, EFA, AGG, BIL. Decision at month end t uses the
    trailing 12 months ending t; return earned in month t+1."""
    g12 = (1 + mr).rolling(12).apply(np.prod, raw=True) - 1
    pos = []
    out = []
    for t in range(start, len(mr) - 1):
        r = g12.iloc[t]
        if r["SPY"] <= r["BIL"]:
            p = "AGG"
        else:
            p = "SPY" if r["SPY"] >= r["EFA"] else "EFA"
        pos.append(p)
        out.append(mr.iloc[t + 1][p])
    return np.array(out), pos


def gem():
    px = pd.concat({s: tr_close(s) for s in ("SPY", "EFA", "AGG", "BIL", "IEF")}, axis=1).dropna()
    mp = px.resample("ME").last()
    mr = mp.pct_change().dropna()
    start = 12  # first decision with a full 12 months
    real, pos = gem_returns(mr, start)
    months = mr.index[start + 1:]
    spy = mr["SPY"].to_numpy()[start + 1:]
    sixty = (0.6 * mr["SPY"] + 0.4 * mr["IEF"]).to_numpy()[start + 1:]
    switches = sum(1 for a, b in zip(pos[:-1], pos[1:]) if a != b)
    res = {"from": str(months[0].date()), "to": str(months[-1].date()), "gem": summarise(real, 12), "spy": summarise(spy, 12),
           "sixty_forty": summarise(sixty, 12), "switches_per_year": round(switches / (len(pos) / 12), 2),
           "months_in": {k: pos.count(k) for k in ("SPY", "EFA", "AGG")}}
    m10 = months >= pd.Timestamp("2010-01-01")
    res["since_2010"] = {"gem": summarise(real[m10], 12), "spy": summarise(spy[m10], 12), "sixty_forty": summarise(sixty[m10], 12)}
    # down years of SPY
    yr = pd.Series(spy, index=months).groupby(months.year).apply(lambda x: (1 + x).prod() - 1)
    yg = pd.Series(real, index=months).groupby(months.year).apply(lambda x: (1 + x).prod() - 1)
    down = yr[yr < 0].index
    res["spy_down_years"] = {int(y): {"spy": round(float(yr[y] * 100), 1), "gem": round(float(yg[y] * 100), 1)} for y in down}
    # luck: shuffle months jointly for SPY, EFA, AGG, IEF; bills kept
    rng = np.random.default_rng(90)
    rs = sharpe(real, 12)
    better, vals = 1, []
    risky = mr[["SPY", "EFA", "AGG", "IEF"]].to_numpy()
    for k in range(N_PERM):
        order = rng.permutation(len(mr))
        pm = mr.copy()
        pm[["SPY", "EFA", "AGG", "IEF"]] = risky[order]
        pr, _ = gem_returns(pm, start)
        v = sharpe(pr, 12)
        vals.append(v); better += v >= rs
    res["mcpt"] = {"n": N_PERM, "real_sharpe": round(rs, 3), "p": round(better / (N_PERM + 1), 4), "perm_median": round(float(np.median(vals)), 3),
                   "perm_95th": round(float(np.percentile(vals, 95)), 3)}
    return res


# ---------------------------------------------------------------- Fabian
def fabian_returns(wr_spy, wr_cash, above):
    """above: T x 3 booleans at each week's close. Position for week t+1 decided at close t."""
    pos = np.zeros(len(wr_spy), dtype=bool)
    cur = False
    for t in range(len(wr_spy) - 1):
        n_above = above[t].sum()
        if n_above == 3:
            cur = True
        elif n_above <= 1:
            cur = False
        pos[t + 1] = cur
    return np.where(pos, wr_spy, wr_cash), pos


def fabian():
    idx = {s: load(s.replace("^", ""), adjusted=False)["close"] for s in ("^GSPC", "^DJI", "^DJU")}
    spy = tr_close("SPY")
    bil = tr_close("BIL")
    ief = tr_close("IEF")
    wk = pd.concat({**idx, "SPY": spy}, axis=1).resample("W-FRI").last().dropna()
    wk_bil = bil.resample("W-FRI").last().reindex(wk.index)
    wk_ief = ief.resample("W-FRI").last().reindex(wk.index)
    ma = wk[["^GSPC", "^DJI", "^DJU"]].rolling(39).mean()
    above = (wk[["^GSPC", "^DJI", "^DJU"]] > ma).to_numpy()
    ok = ~ma.isna().any(axis=1).to_numpy()
    wr_spy = wk["SPY"].pct_change().fillna(0.0).to_numpy()
    wr_cash = wk_bil.pct_change().fillna(0.0).to_numpy()
    wr_ief = wk_ief.pct_change().fillna(0.0).to_numpy()
    first = int(np.argmax(ok))
    real, pos = fabian_returns(wr_spy, wr_cash, above)
    sl = slice(first + 1, None)
    weeks = wk.index[sl]
    res = {"from": str(weeks[0].date()), "to": str(weeks[-1].date()), "fabian": summarise(real[sl], 52), "spy": summarise(wr_spy[sl], 52),
           "weeks_in_market_pct": round(float(pos[sl].mean() * 100), 1),
           "round_trips": int(np.sum(np.diff(pos[sl].astype(int)) == 1))}
    has_ief = ~np.isnan(wk_ief.to_numpy())
    m = has_ief & (np.arange(len(wk)) >= first + 1)
    sixty = 0.6 * wr_spy + 0.4 * wr_ief
    res["since_ief_2002"] = {"fabian": summarise(real[m], 52), "spy": summarise(wr_spy[m], 52), "sixty_forty": summarise(sixty[m], 52),
                            "from": str(wk.index[m][0].date())}
    rng = np.random.default_rng(91)
    rs = sharpe(real[sl], 52)
    better, vals = 1, []
    lr = np.log(wk[["^GSPC", "^DJI", "^DJU", "SPY"]]).diff().fillna(0.0).to_numpy()
    for k in range(N_PERM):
        order = np.concatenate([np.arange(first + 1), first + 1 + rng.permutation(len(wk) - first - 1)])
        plr = lr[order]
        plog = np.log(wk[["^GSPC", "^DJI", "^DJU", "SPY"]].iloc[0].to_numpy()) + np.cumsum(plr, axis=0)
        pwk = pd.DataFrame(np.exp(plog), index=wk.index, columns=["^GSPC", "^DJI", "^DJU", "SPY"])
        pma = pwk[["^GSPC", "^DJI", "^DJU"]].rolling(39).mean()
        pabove = (pwk[["^GSPC", "^DJI", "^DJU"]] > pma).to_numpy()
        pr, _ = fabian_returns(np.expm1(plr[:, 3]), wr_cash, pabove)
        v = sharpe(pr[sl], 52)
        vals.append(v); better += v >= rs
    res["mcpt"] = {"n": N_PERM, "real_sharpe": round(rs, 3), "p": round(better / (N_PERM + 1), 4), "perm_median": round(float(np.median(vals)), 3),
                   "perm_95th": round(float(np.percentile(vals, 95)), 3)}
    return res


def main():
    t0 = time.time()
    res = {"gem": gem()}
    print("GEM", {k: res["gem"][k] for k in ("gem", "spy", "sixty_forty", "switches_per_year", "months_in", "mcpt")}, round(time.time() - t0), "s", flush=True)
    print("GEM since 2010", res["gem"]["since_2010"], "down years", res["gem"]["spy_down_years"], flush=True)
    res["fabian"] = fabian()
    print("FABIAN", {k: res["fabian"][k] for k in ("fabian", "spy", "weeks_in_market_pct", "round_trips", "mcpt")}, round(time.time() - t0), "s", flush=True)
    print("FABIAN since 2002", res["fabian"]["since_ief_2002"])
    res["runtime_s"] = round(time.time() - t0)
    json.dump(res, open(os.path.join(OUT, "results.json"), "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
