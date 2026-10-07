"""P-0085: the dip-buying family. Five rules from Quantified Strategies videos (TRADING-IDEAS.md),
replicated on SPY, luck-tested, run on the nine-ETF basket, and measured against the RSI(5) book.

Rules as the videos state them (reader A's notes, state/agents/2026-10-07/yt-ideas-A-*.json):
  wr7     Williams %R(7) below -95 at the close, buy next open; exit next open after a close above
          the previous day's high. Claimed: 288 trades, PF 2.61, avg 0.82%, 76.4% win.
  stoch   slow stochastic (7, 3-bar smoothing) below 25; same exit. Claimed next-open: 394 trades,
          73.6% win, PF 2.47, avg 0.65%. Close fills: 394, 77.7%, PF 2.58, avg 0.68%.
  ibs     internal bar strength below a threshold the video does not give; I fix 0.2 here, before
          running. Same exit. Claimed: 631 trades, PF 2.12.
  dip5    SPY down 5% or more over 5 days, buy next open, sell at the close of the 5th session.
          Claimed: 81 cases, average +1.24% against +0.20% for any 5-day stretch.
  low3    three lower closes in a row, buy next open, sell at the close of the 3rd session.
          Claimed: 459 cases, average +0.23% against +0.12%.
No trend filter in any of them (the videos use none). Added after the smoke run and before the
full run, so declared here before any luck-test result: each rule again with RSI(5)'s filter (close
above its 200-day average at entry), the "_trend" rows, to see whether the filter is what makes
RSI(5) the stronger of the family. Also after the smoke run: no re-entry on the bar of an exit at
the close (the videos give the same 394 trades for both stochastic fills, which needs this rule). Data as traded, not dividend-adjusted,
which is what Quantified Strategies uses (P-0082). One position at a time, no costs, as in the
videos. The luck test is neurotrader888's bar permutation (P-0082's numba port).

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 experiments/2026-10-07-P-0085/p0085.py
"""
import json, os, sys, time
import numpy as np
from numba import njit

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/p0082")
sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-10-07-P-0083")
from p0082 import load, sma, permute, pf, stats, trades_from_rp  # noqa: E402
from basket_backtest import rsi5_next_open_rp  # noqa: E402

OUT = "/Users/triton/PROTEUS/experiments/2026-10-07-P-0085"
BASKET = ["SPY", "QQQ", "DIA", "IWM", "EFA", "EEM", "EWU", "EWJ", "EWG"]
IBS_MAX = 0.2
N_PERM = int(os.environ.get("N_PERM", "1000"))
N_PERM_BASKET = int(os.environ.get("N_PERM_BASKET", "500"))
RULES = ["wr7", "stoch", "ibs", "dip5", "low3"]


@njit(cache=True)
def roll_max(x, n):
    out = np.full(x.size, np.nan)
    for i in range(n - 1, x.size):
        out[i] = x[i - n + 1:i + 1].max()
    return out


@njit(cache=True)
def roll_min(x, n):
    out = np.full(x.size, np.nan)
    for i in range(n - 1, x.size):
        out[i] = x[i - n + 1:i + 1].min()
    return out


@njit(cache=True)
def signal(rule, h, l, c):
    n = c.size
    s = np.zeros(n, dtype=np.bool_)
    if rule == 0 or rule == 1:
        hh = roll_max(h, 7)
        ll = roll_min(l, 7)
        k = np.full(n, np.nan)
        for t in range(n):
            if not np.isnan(hh[t]) and hh[t] > ll[t]:
                k[t] = 100.0 * (c[t] - ll[t]) / (hh[t] - ll[t])
        if rule == 0:
            for t in range(n):
                s[t] = (not np.isnan(k[t])) and (k[t] - 100.0) < -95.0   # %R = %K - 100
        else:
            sk = sma(np.where(np.isnan(k), 0.0, k), 3)
            for t in range(8, n):
                s[t] = sk[t] < 25.0
    elif rule == 2:
        for t in range(n):
            if h[t] > l[t]:
                s[t] = (c[t] - l[t]) / (h[t] - l[t]) < IBS_MAX
    elif rule == 3:
        for t in range(5, n):
            s[t] = c[t] / c[t - 5] - 1.0 <= -0.05
    else:
        for t in range(3, n):
            s[t] = c[t] < c[t - 1] and c[t - 1] < c[t - 2] and c[t - 2] < c[t - 3]
    return s


@njit(cache=True)
def run(o, h, c, sig, entry_at_close, exit_kind, hold_n):
    """exit_kind 0: close above yesterday's high, filled next open. 1: same, filled at that close.
    2: hold hold_n sessions, out at the close of the last. Returns (log returns per bar, trade ids)."""
    n = c.size
    rets = np.zeros(n)
    tid = np.zeros(n, dtype=np.int64)
    state = 0   # 0 flat, 1 buy at next open, 2 long, 3 sell at next open
    k = 0
    held = 0
    for t in range(1, n):
        out_at_close = False
        if state == 1:
            rets[t] = np.log(c[t]) - np.log(o[t])
            state = 2
            k += 1
            held = 1
            tid[t] = k
        elif state == 2:
            rets[t] = np.log(c[t]) - np.log(c[t - 1])
            held += 1
            tid[t] = k
        elif state == 3:
            rets[t] = np.log(o[t]) - np.log(c[t - 1])
            tid[t] = k
            state = 0
        if state == 2:
            if exit_kind == 2:
                if held >= hold_n:
                    state = 0
                    out_at_close = True
            elif c[t] > h[t - 1]:
                if exit_kind == 0:
                    state = 3
                else:
                    state = 0
                    out_at_close = True
        if state == 0 and sig[t] and not out_at_close:
            if entry_at_close:
                state = 2
                k += 1
                held = 0
            else:
                state = 1
    return rets, tid


SPEC = {  # rule -> (rule id, entry at close, exit kind, hold)
    "wr7": (0, False, 0, 0),
    "stoch": (1, False, 0, 0),
    "stoch_close": (1, True, 1, 0),
    "ibs": (2, False, 0, 0),
    "dip5": (3, False, 2, 5),
    "low3": (4, False, 2, 3),
}
for _r in ("wr7", "stoch", "ibs", "dip5", "low3"):
    SPEC[_r + "_trend"] = SPEC[_r]
RULES_ALL = RULES + [r + "_trend" for r in RULES]


def rp_for(name, o, h, l, c):
    r, at_close, ek, hn = SPEC[name]
    sig = signal(r, h, l, c)
    if name.endswith("_trend"):
        m = sma(c, 200)
        sig = sig & (c > np.where(np.isnan(m), np.inf, m))
    return run(o, h, c, sig, at_close, ek, hn)


def luck(name, o, h, l, c, start, n_perm, seed0):
    real = pf(rp_for(name, o, h, l, c)[0], start)
    better, vals = 1, []
    for k in range(n_perm):
        po, ph, pl, pc = permute(o, h, l, c, start, seed0 + k)
        v = pf(rp_for(name, po, ph, pl, pc)[0], start)
        vals.append(v)
        better += v >= real
    return {"real_bar_pf": round(float(real), 3), "p": round(better / (n_perm + 1), 4), "perm_median_pf": round(float(np.median(vals)), 3), "n": n_perm}


def intervals(rp, start):
    rets, tid = rp
    out = {}
    for i in range(start, len(tid)):
        k = int(tid[i])
        if k:
            a, b = out.get(k, (i, i))
            out[k] = (min(a, i), max(b, i))
    return sorted(out.values())


def overlap(x_rp, ref_rp, start):
    """Share of X's trades that overlap a reference (RSI(5)) trade in time, and share of X's market
    days that are also reference market days, plus the mean return of X's trades that do not overlap."""
    xi, ri = intervals(x_rp, start), intervals(ref_rp, start)
    ref_days = np.zeros(len(ref_rp[1]), dtype=bool)
    for a, b in ri:
        ref_days[a:b + 1] = True
    hit, solo = 0, []
    for a, b in xi:
        if ref_days[a:b + 1].any():
            hit += 1
        else:
            solo.append(float(np.expm1(x_rp[0][a:b + 1].sum())))
    xdays = np.zeros(len(x_rp[1]), dtype=bool)
    for a, b in xi:
        xdays[a:b + 1] = True
    shared_days = (xdays & ref_days).sum()
    return {"trades": len(xi), "trades_overlapping_rsi5": hit, "share_overlapping": round(hit / len(xi), 3) if xi else None,
            "share_of_days_also_rsi5": round(float(shared_days / xdays.sum()), 3) if xdays.sum() else None,
            "solo_trades": len(solo), "solo_mean_pct": round(float(np.mean(solo) * 100), 3) if solo else None,
            "solo_win_pct": round(float(np.mean(np.array(solo) > 0) * 100), 1) if solo else None}


def main():
    t0 = time.time()
    res = {"ibs_max": IBS_MAX, "data": "as traded, not dividend-adjusted", "spy": {}, "basket_2009_on": {}, "pooled_2009_on": {}}
    df = load("SPY", adjusted=False)
    O, H, L, C = (df[x].to_numpy() for x in ("open", "high", "low", "close"))
    idx = df.index
    s09 = int(np.searchsorted(idx.values, np.datetime64("2009-01-01")))
    base5 = float(np.mean(C[5:] / C[:-5] - 1) * 100)
    base3 = float(np.mean(C[3:] / C[:-3] - 1) * 100)
    res["spy_baseline"] = {"any_5day_pct": round(base5, 3), "any_3day_pct": round(base3, 3)}
    # what IBS threshold gives their 631 trades (information only; the test keeps 0.2)
    ibs_counts = {}
    for thr in (0.05, 0.1, 0.15, 0.2, 0.25):
        sig = np.zeros(C.size, dtype=np.bool_)
        rng_ = H > L
        sig[rng_] = (C[rng_] - L[rng_]) / (H[rng_] - L[rng_]) < thr
        ibs_counts[str(thr)] = stats(run(O, H, C, sig, False, 0, 0), idx)["trades"]
    res["ibs_trades_by_threshold"] = ibs_counts
    for name in ["wr7", "stoch", "stoch_close", "ibs", "dip5", "low3"] + [r + "_trend" for r in RULES]:
        rp = rp_for(name, O, H, L, C)
        row = {"full": stats(rp, idx), "since_2009": stats(rp, idx, s09)}
        if name != "stoch_close":
            row["luck_full"] = luck(name, O, H, L, C, 0, N_PERM, 1)
            row["luck_2009_on"] = luck(name, O, H, L, C, s09, N_PERM, 5001)
            row["overlap_rsi5_2009_on"] = overlap(rp, rsi5_next_open_rp(O, C, 1), s09)
        res["spy"][name] = row
        print("SPY", name, {k: row["full"][k] for k in ("trades", "win_rate", "avg_trade_pct", "trade_pf", "max_dd_pct")},
              "p", row.get("luck_full", {}).get("p"), "p09", row.get("luck_2009_on", {}).get("p"), round(time.time() - t0), "s", flush=True)
    pooled = {n: {"trades": [], "solo_n": 0, "solo_sum": 0.0, "overlap_hits": 0, "n_trades": 0, "p_lt_05": 0} for n in RULES_ALL}
    for sym in BASKET:
        d = load(sym, adjusted=False)
        o, h, l, c = (d[x].to_numpy() for x in ("open", "high", "low", "close"))
        st = int(np.searchsorted(d.index.values, np.datetime64("2009-01-01")))
        ref = rsi5_next_open_rp(o, c, 1)
        res["basket_2009_on"][sym] = {}
        for name in RULES_ALL:
            rp = rp_for(name, o, h, l, c)
            s_ = stats(rp, d.index, st)
            lk = luck(name, o, h, l, c, st, N_PERM_BASKET, 9001)
            ov = overlap(rp, ref, st)
            res["basket_2009_on"][sym][name] = {"stats": s_, "luck": lk, "overlap": ov}
            rets, tid = rp
            pooled[name]["trades"] += [float(np.expm1(t[2])) for t in trades_from_rp((rets[st:], tid[st:]), d.index[st:])]
            pooled[name]["overlap_hits"] += ov["trades_overlapping_rsi5"]
            pooled[name]["n_trades"] += ov["trades"]
            pooled[name]["p_lt_05"] += lk["p"] < 0.05
            if ov["solo_trades"]:
                pooled[name]["solo_n"] += ov["solo_trades"]
                pooled[name]["solo_sum"] += ov["solo_mean_pct"] * ov["solo_trades"]
        print("basket", sym, " ".join("%s p%.3f" % (n, res["basket_2009_on"][sym][n]["luck"]["p"]) for n in RULES_ALL), round(time.time() - t0), "s", flush=True)
    for name, pl in pooled.items():
        a = np.array(pl["trades"])
        res["pooled_2009_on"][name] = {"trades": int(a.size), "mean_pct": round(float(a.mean() * 100), 3),
                                       "win_pct": round(float((a > 0).mean() * 100), 1),
                                       "t": round(float(a.mean() / (a.std(ddof=1) / np.sqrt(a.size))), 2),
                                       "markets_p_lt_05": int(pl["p_lt_05"]),
                                       "share_overlapping_rsi5": round(pl["overlap_hits"] / pl["n_trades"], 3),
                                       "solo_trades": pl["solo_n"],
                                       "solo_mean_pct": round(pl["solo_sum"] / pl["solo_n"], 3) if pl["solo_n"] else None}
        print("pooled", name, res["pooled_2009_on"][name])
    res["runtime_s"] = round(time.time() - t0)
    json.dump(res, open(os.path.join(OUT, "results.json"), "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
