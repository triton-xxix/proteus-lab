"""P-0086: the Darvas box breakout on SPY, as Quantified Strategies state it (TRADING-IDEAS.md A-01,
video b8Usenu2QIY), replicated, luck-tested, nulled and run on the nine-ETF basket.

Rule, as stated, fixed before the run:
  signal day: close above the highest high of the PREVIOUS 12 sessions, by no more than 0.75% of
  that level, and volume above its 15-day average. Buy at the next open.
  exit: when the close is above the previous day's high, sell at the next open. No stop.
Unstated and declared here: whether the 15-day volume average includes the signal day. Both are
run ("vol_incl", "vol_excl"); the one nearer their 279 trades is the headline, the other is reported.
Claimed: 279 trades, 74.2% winners, avg +0.34%, PF 3.08 (1993-2026); era PFs 2.70 / 2.78 / 3.94
(1993-2004, 2005-2015, 2016-2026); lookback sweep 11d 2.75, 13d 2.97, 16d 2.84, 18d 2.71, 20d 2.80.

Nulls, declared before the run:
  plain12   the same entry with no chase cap and no volume filter.
  random    random entry days, same count as the rule, same exit; 500 draws; where the real PF sits.
Luck test: neurotrader888 bar permutation (P-0082 port) with volume permuted alongside the bars
(same index permutation as the high/low/close), 1000 shuffles full sample and from 2009.
Data: Yahoo daily, as traded, not dividend-adjusted (what the channel uses, P-0082). One position
at a time, no costs.

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 /Users/triton/PROTEUS/experiments/2026-10-07-P-0086/p0086.py
"""
import json, os, sys, time
import numpy as np
import pandas as pd
from numba import njit

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/p0082")
sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-10-07-P-0085")
from p0082 import pf, stats, trades_from_rp  # noqa: E402
from p0085 import run  # noqa: E402  (entry next open, exit close > yesterday's high -> next open)

OUT = "/Users/triton/PROTEUS/experiments/2026-10-07-P-0086"
DATA = "/Users/triton/PROTEUS/sandbox/p0082/data"
BASKET = ["SPY", "QQQ", "DIA", "IWM", "EFA", "EEM", "EWU", "EWJ", "EWG"]
N_PERM = int(os.environ.get("N_PERM", "1000"))
N_PERM_BASKET = int(os.environ.get("N_PERM_BASKET", "300"))
N_RANDOM = 500
LOOKBACK, CAP, VOL_N = 12, 0.0075, 15


def load_v(sym):
    df = pd.read_csv(os.path.join(DATA, sym + ".csv"), parse_dates=["date"]).set_index("date")
    return df[["open", "high", "low", "close", "volume"]].astype(float)


@njit(cache=True)
def box_signal(h, c, v, lookback, cap, vol_n, vol_incl, use_cap, use_vol):
    n = c.size
    s = np.zeros(n, dtype=np.bool_)
    for t in range(max(lookback, vol_n), n):
        hh = h[t - lookback:t].max()          # previous `lookback` sessions, today excluded
        if c[t] <= hh:
            continue
        if use_cap and c[t] > hh * (1.0 + cap):
            continue
        if use_vol:
            if vol_incl:
                va = v[t - vol_n + 1:t + 1].mean()
            else:
                va = v[t - vol_n:t].mean()
            if not v[t] > va:
                continue
        s[t] = True
    return s


@njit(cache=True)
def permute_v(o, h, l, c, v, start, seed):
    """P-0082's permute with volume carried on the same bar permutation as high/low/close."""
    np.random.seed(seed)
    lo, lh, ll, lc = np.log(o), np.log(h), np.log(l), np.log(c)
    n = c.size
    m = n - start - 1
    r_o = np.empty(m); r_h = np.empty(m); r_l = np.empty(m); r_c = np.empty(m); r_v = np.empty(m)
    for k in range(m):
        i = start + 1 + k
        r_o[k] = lo[i] - lc[i - 1]
        r_h[k] = lh[i] - lo[i]
        r_l[k] = ll[i] - lo[i]
        r_c[k] = lc[i] - lo[i]
        r_v[k] = v[i]
    p1 = np.random.permutation(m)
    p2 = np.random.permutation(m)
    po, ph, pl, pc, pv = lo.copy(), lh.copy(), ll.copy(), lc.copy(), v.copy()
    for k in range(m):
        i = start + 1 + k
        po[i] = pc[i - 1] + r_o[p2[k]]
        ph[i] = po[i] + r_h[p1[k]]
        pl[i] = po[i] + r_l[p1[k]]
        pc[i] = po[i] + r_c[p1[k]]
        pv[i] = r_v[p1[k]]
    return np.exp(po), np.exp(ph), np.exp(pl), np.exp(pc), pv


def rp_for(o, h, c, v, lookback=LOOKBACK, vol_incl=True, use_cap=True, use_vol=True):
    sig = box_signal(h, c, v, lookback, CAP, VOL_N, vol_incl, use_cap, use_vol)
    return run(o, h, c, sig, False, 0, 0)


def luck(o, h, l, c, v, start, n_perm, seed0, **kw):
    real = pf(rp_for(o, h, c, v, **kw)[0], start)
    better, vals = 1, []
    for k in range(n_perm):
        po, ph, pl, pc, pv = permute_v(o, h, l, c, v, start, seed0 + k)
        x = pf(rp_for(po, ph, pc, pv, **kw)[0], start)
        vals.append(x)
        better += x >= real
    return {"real_bar_pf": round(float(real), 3), "p": round(better / (n_perm + 1), 4),
            "perm_median_pf": round(float(np.median(vals)), 3), "n": n_perm}


def random_entry_control(o, h, c, n_trades, idx, start, draws, seed=7):
    """Same exit, random entry days (uniform over sessions after `start`), same trade count."""
    rng = np.random.default_rng(seed)
    pfs, avgs = [], []
    n = c.size
    for _ in range(draws):
        sig = np.zeros(n, dtype=np.bool_)
        sig[rng.choice(np.arange(start + 20, n - 2), size=n_trades, replace=False)] = True
        rp = run(o, h, c, sig, False, 0, 0)
        st = stats(rp, idx, start)
        pfs.append(st["trade_pf"] or 0.0)
        avgs.append(st["avg_trade_pct"] or 0.0)
    return np.array(pfs), np.array(avgs)


def era_pf(rp, idx):
    out = {}
    for name, a, b in (("1993-2004", "1993-01-01", "2004-12-31"), ("2005-2015", "2005-01-01", "2015-12-31"), ("2016-2026", "2016-01-01", "2026-12-31")):
        tr = [t for t in trades_from_rp(rp, idx) if pd.Timestamp(a) <= t[0] <= pd.Timestamp(b)]
        s = np.array([np.expm1(t[2]) for t in tr])
        w, l_ = s[s > 0].sum(), -s[s < 0].sum()
        out[name] = {"trades": int(s.size), "pf": round(float(w / l_), 2) if l_ > 0 else None,
                     "avg_pct": round(float(s.mean() * 100), 2) if s.size else None}
    return out


def main():
    t0 = time.time()
    res = {"rule": "12-day-high breakout, chase cap 0.75%, volume > 15-day avg, buy next open, exit next open after close > prior high",
           "data": "as traded, not dividend-adjusted", "spy": {}, "nulls": {}, "sweep": {}, "basket_2009_on": {}, "pooled_2009_on": {}}
    d = load_v("SPY")
    O, H, L, C, V = (d[x].to_numpy() for x in ("open", "high", "low", "close", "volume"))
    idx = d.index
    s09 = int(np.searchsorted(idx.values, np.datetime64("2009-01-01")))
    res["spy_span"] = [str(idx[0].date()), str(idx[-1].date()), int(len(idx))]

    for name, incl in (("vol_incl", True), ("vol_excl", False)):
        rp = rp_for(O, H, C, V, vol_incl=incl)
        res["spy"][name] = {"full": stats(rp, idx), "since_2009": stats(rp, idx, s09), "eras": era_pf(rp, idx)}
        print("SPY", name, res["spy"][name]["full"], flush=True)
    head = min(("vol_incl", "vol_excl"), key=lambda k: abs(res["spy"][k]["full"]["trades"] - 279))
    res["headline_variant"] = head
    incl = head == "vol_incl"
    rp = rp_for(O, H, C, V, vol_incl=incl)
    res["spy"][head]["luck_full"] = luck(O, H, L, C, V, 0, N_PERM, 1, vol_incl=incl)
    res["spy"][head]["luck_2009_on"] = luck(O, H, L, C, V, s09, N_PERM, 5001, vol_incl=incl)
    print("luck", res["spy"][head]["luck_full"], res["spy"][head]["luck_2009_on"], round(time.time() - t0), "s", flush=True)

    # nulls
    rp_plain = rp_for(O, H, C, V, use_cap=False, use_vol=False)
    res["nulls"]["plain12"] = {"full": stats(rp_plain, idx), "since_2009": stats(rp_plain, idx, s09),
                               "luck_full": luck(O, H, L, C, V, 0, N_PERM, 1, use_cap=False, use_vol=False)}
    rp_nocap = rp_for(O, H, C, V, use_cap=False, vol_incl=incl)
    res["nulls"]["no_cap"] = {"full": stats(rp_nocap, idx)}
    rp_novol = rp_for(O, H, C, V, use_vol=False)
    res["nulls"]["no_vol"] = {"full": stats(rp_novol, idx)}
    n_tr = res["spy"][head]["full"]["trades"]
    pfs, avgs = random_entry_control(O, H, C, n_tr, idx, 0, N_RANDOM)
    real_pf = res["spy"][head]["full"]["trade_pf"]
    real_avg = res["spy"][head]["full"]["avg_trade_pct"]
    res["nulls"]["random_entry_same_exit"] = {
        "draws": N_RANDOM, "trades_each": n_tr, "pf_median": round(float(np.median(pfs)), 2),
        "pf_p90": round(float(np.percentile(pfs, 90)), 2), "pf_max": round(float(pfs.max()), 2),
        "share_pf_at_or_above_real": round(float((pfs >= real_pf).mean()), 3),
        "avg_median_pct": round(float(np.median(avgs)), 3), "share_avg_at_or_above_real": round(float((avgs >= real_avg).mean()), 3)}
    print("nulls", {k: (v.get("full") or v) for k, v in res["nulls"].items()}, round(time.time() - t0), "s", flush=True)

    for lb in (11, 12, 13, 16, 18, 20):
        st = stats(rp_for(O, H, C, V, lookback=lb, vol_incl=incl), idx)
        res["sweep"][str(lb)] = {"trades": st["trades"], "trade_pf": st["trade_pf"], "avg_trade_pct": st["avg_trade_pct"]}
    print("sweep", res["sweep"], flush=True)

    pooled = []
    for sym in BASKET:
        b = load_v(sym)
        o, h, l, c, v = (b[x].to_numpy() for x in ("open", "high", "low", "close", "volume"))
        st_ = int(np.searchsorted(b.index.values, np.datetime64("2009-01-01")))
        rpb = rp_for(o, h, c, v, vol_incl=incl)
        res["basket_2009_on"][sym] = {"stats": stats(rpb, b.index, st_), "luck": luck(o, h, l, c, v, st_, N_PERM_BASKET, 9001, vol_incl=incl)}
        rets, tid = rpb
        pooled += [float(np.expm1(t[2])) for t in trades_from_rp((rets[st_:], tid[st_:]), b.index[st_:])]
        print("basket", sym, res["basket_2009_on"][sym]["stats"]["trades"], res["basket_2009_on"][sym]["stats"]["avg_trade_pct"], "p", res["basket_2009_on"][sym]["luck"]["p"], round(time.time() - t0), "s", flush=True)
    a = np.array(pooled)
    res["pooled_2009_on"] = {"trades": int(a.size), "mean_pct": round(float(a.mean() * 100), 3), "win_pct": round(float((a > 0).mean() * 100), 1),
                             "t": round(float(a.mean() / (a.std(ddof=1) / np.sqrt(a.size))), 2),
                             "markets_p_lt_05": int(sum(res["basket_2009_on"][s]["luck"]["p"] < 0.05 for s in BASKET)),
                             "markets_positive": int(sum((res["basket_2009_on"][s]["stats"]["avg_trade_pct"] or 0) > 0 for s in BASKET))}
    print("pooled", res["pooled_2009_on"])
    res["runtime_s"] = round(time.time() - t0)
    json.dump(res, open(os.path.join(OUT, "results.json"), "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
