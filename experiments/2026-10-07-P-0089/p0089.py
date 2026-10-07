"""P-0089: two stricter luck tests for the systems book's RSI(5) basket, beside P-0083's in-sample p.

The RSI(5) rule has no fitted parameter, so a textbook walk-forward permutation (re-optimise each
window) has nothing to optimise. What was optimised, in P-0082 and P-0085, was the choice of rule:
RSI(5) was picked from a family on the full sample. So the walk-forward here re-makes that choice:

  walk-forward selection   candidates: rsi5 simple (variant 1), rsi5 triple (variant 3), Williams
                           %R(7), slow stochastic (7,3), IBS below 0.2, all with next-open fills
                           and the family's exits, no trend filter on the last three (as P-0085
                           ran them). Windows: calendar years 2012 to 2026, out of sample one at a
                           time; the training set is everything from 2009 up to the window. The
                           candidate with the best training trade profit factor is traded in the
                           window. OOS daily returns are chained across windows. Fitness: bar PF
                           of the chained OOS series. Permutation: neurotrader's bar shuffle of
                           the whole series from 2009, 1000 draws, the entire walk-forward re-run
                           on each (selection included). p = share of shuffles at or above real.
  random-entry control     the book's own exit (RSI(5) above 50 at the close, sell next open), the
                           same number of trades as the real rule, entry days drawn at random from
                           sessions above the 200-day average (so the trend filter is kept and only
                           the dip timing is tested); 10,000 draws per market; p = share of draws
                           whose mean trade is at or above the real mean.
Both on the nine ETFs from 2009, as traded. Reported next to P-0083's in-sample p per market.

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 /Users/triton/PROTEUS/experiments/2026-10-07-P-0089/p0089.py
"""
import json, os, sys, time
import numpy as np
from numba import njit

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/p0082")
sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-10-07-P-0083")
sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-10-07-P-0085")
from p0082 import load, rsi_wilder, sma, permute, pf, stats, trades_from_rp  # noqa: E402
from basket_backtest import rsi5_next_open_rp  # noqa: E402
from p0085 import rp_for as family_rp  # noqa: E402

OUT = "/Users/triton/PROTEUS/experiments/2026-10-07-P-0089"
BASKET = ["SPY", "QQQ", "DIA", "IWM", "EFA", "EEM", "EWU", "EWJ", "EWG"]
CANDS = ["rsi5_simple", "rsi5_triple", "wr7", "stoch", "ibs"]
N_PERM = int(os.environ.get("N_PERM", "1000"))
N_RAND = int(os.environ.get("N_RAND", "10000"))
FIRST_OOS_YEAR, LAST_YEAR = 2012, 2026
P0083 = json.load(open("/Users/triton/PROTEUS/experiments/2026-10-07-P-0083/basket_backtest.json"))


def cand_rp(name, o, h, l, c):
    if name == "rsi5_simple":
        return rsi5_next_open_rp(o, c, 1)
    if name == "rsi5_triple":
        return rsi5_next_open_rp(o, c, 3)
    return family_rp(name, o, h, l, c)


@njit(cache=True)
def trade_table(rets, tid):
    """Per trade: index of its last bar and its summed log return."""
    n = tid.max()
    ends = np.zeros(n + 1, dtype=np.int64)
    sums = np.zeros(n + 1)
    for i in range(rets.size):
        k = tid[i]
        if k:
            ends[k] = i
            sums[k] += rets[i]
    return ends[1:], sums[1:]


def pf_before(ends, sums, s09, a):
    v = sums[(ends < a) & (ends >= s09)]
    if v.size == 0:
        return 0.0
    gp, gl = v[v > 0].sum(), -v[v < 0].sum()
    return gp / gl if gl > 0 else (1e9 if gp > 0 else 0.0)


def walk_forward(o, h, l, c, years, s09):
    """Returns the chained OOS daily return series (zeros outside OOS) and the picks."""
    rps = {n: cand_rp(n, o, h, l, c) for n in CANDS}
    tabs = {n: trade_table(rps[n][0], rps[n][1]) for n in CANDS}
    oos = np.zeros(c.size)
    picks = {}
    for y in range(FIRST_OOS_YEAR, LAST_YEAR + 1):
        a = int(np.searchsorted(years, y))
        b = int(np.searchsorted(years, y + 1))
        if a >= c.size:
            break
        best = max(CANDS, key=lambda n: pf_before(tabs[n][0], tabs[n][1], s09, a))
        picks[y] = best
        oos[a:b] = rps[best][0][a:b]
    return oos, picks


@njit(cache=True)
def run_rsi_exit(o, c, sig):
    """Entry on sig (next open), exit when RSI(5) > 50 at the close, filled next open."""
    r = rsi_wilder(c, 5)
    n = c.size
    rets = np.zeros(n)
    tid = np.zeros(n, dtype=np.int64)
    state = 0
    k = 0
    for t in range(1, n):
        if state == 1:
            rets[t] = np.log(c[t]) - np.log(o[t]); state = 2; k += 1; tid[t] = k
        elif state == 2:
            rets[t] = np.log(c[t]) - np.log(c[t - 1]); tid[t] = k
        elif state == 3:
            rets[t] = np.log(o[t]) - np.log(c[t - 1]); tid[t] = k; state = 0
        if state == 2 and r[t] > 50:
            state = 3
        elif state == 0 and sig[t]:
            state = 1
    return rets, tid


@njit(cache=True)
def trade_means(rets, tid):
    """Mean simple return per trade and count."""
    n = tid.max()
    s = np.zeros(n + 1)
    seen = np.zeros(n + 1, dtype=np.bool_)
    for i in range(rets.size):
        if tid[i]:
            s[tid[i]] += rets[i]
            seen[tid[i]] = True
    tot = 0.0
    cnt = 0
    for k in range(1, n + 1):
        if seen[k]:   # only trades inside the slice count (ids continue from before 2009)
            tot += np.exp(s[k]) - 1.0
            cnt += 1
    return tot / cnt if cnt else 0.0, cnt


def main():
    t0 = time.time()
    res = {"candidates": CANDS, "oos_years": [FIRST_OOS_YEAR, LAST_YEAR], "n_perm": N_PERM, "n_random": N_RAND, "markets": {}}
    pooled_real, pooled_rand_better = 0, 0
    for sym in BASKET:
        d = load(sym, adjusted=False)
        o, h, l, c = (d[x].to_numpy() for x in ("open", "high", "low", "close"))
        years = d.index.year.to_numpy()
        s09 = int(np.searchsorted(d.index.values, np.datetime64("2009-01-01")))
        # walk-forward selection
        oos, picks = walk_forward(o, h, l, c, years, s09)
        a12 = int(np.searchsorted(years, FIRST_OOS_YEAR))
        real = pf(oos, a12)
        better, vals = 1, []
        for k in range(N_PERM):
            po, ph, pl, pc = permute(o, h, l, c, s09, 20000 + k)
            v = pf(walk_forward(po, ph, pl, pc, years, s09)[0], a12)
            vals.append(v); better += v >= real
        wf = {"real_oos_bar_pf": round(float(real), 3), "p": round(better / (N_PERM + 1), 4),
              "perm_median_pf": round(float(np.median(vals)), 3), "picks": picks,
              "oos_total_log_return": round(float(oos[a12:].sum()), 4)}
        # random-entry control, book rule's own trades
        rp = rsi5_next_open_rp(o, c, 1)
        st = stats(rp, d.index, s09)
        real_mean, n_tr = trade_means(rp[0][s09:], rp[1][s09:])
        m200 = sma(c, 200)
        eligible = np.where((np.arange(c.size) >= s09 + 1) & (c > np.where(np.isnan(m200), np.inf, m200)) & (np.arange(c.size) < c.size - 2))[0]
        rng = np.random.default_rng(89)
        rb = 1
        means = np.empty(N_RAND)
        for k in range(N_RAND):
            sig = np.zeros(c.size, dtype=np.bool_)
            sig[rng.choice(eligible, size=n_tr, replace=False)] = True
            rr, tt = run_rsi_exit(o, c, sig)
            mm, _ = trade_means(rr[s09:], tt[s09:])
            means[k] = mm
            rb += mm >= real_mean
        ctl = {"real_trades": int(n_tr), "real_mean_pct": round(float(real_mean * 100), 3),
               "random_mean_median_pct": round(float(np.median(means) * 100), 3),
               "random_mean_95th_pct": round(float(np.percentile(means, 95) * 100), 3),
               "p": round(rb / (N_RAND + 1), 4)}
        pooled_real += n_tr
        p83 = P0083["markets"].get(sym, {})
        res["markets"][sym] = {"p0083_in_sample": {k: v.get("p") if isinstance(v, dict) else v for k, v in p83.items() if isinstance(v, dict) and "p" in v} or p83,
                               "walk_forward": wf, "random_entry": ctl, "book_stats_2009_on": st}
        print(sym, "wf pf", wf["real_oos_bar_pf"], "p", wf["p"], "| rand p", ctl["p"], "real", ctl["real_mean_pct"], "rand med", ctl["random_mean_median_pct"], round(time.time() - t0), "s", flush=True)
    res["summary"] = {"markets_wf_p_lt_05": int(sum(m["walk_forward"]["p"] < 0.05 for m in res["markets"].values())),
                      "markets_rand_p_lt_05": int(sum(m["random_entry"]["p"] < 0.05 for m in res["markets"].values())),
                      "markets_p0083_simple_next_open_p_lt_05": "see per market"}
    res["runtime_s"] = round(time.time() - t0)
    print(res["summary"])
    json.dump(res, open(os.path.join(OUT, "results.json"), "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
