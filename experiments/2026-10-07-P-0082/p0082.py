"""P-0082: replicate five YouTube strategy claims on free daily data, then permutation-test them.

Run with the in-folder 3.12 venv (numba lives there):
    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 /Users/triton/PROTEUS/sandbox/p0082/p0082.py

Permutation test after neurotrader888/mcpt (bar_permute.py, insample_donchian_mcpt.py): shuffle the
gaps (open vs previous close) and the intrabar moves (high, low, close vs open) separately, rebuild
the series, run the same rules, and count how often the shuffled series does as well. Shuffling
keeps the drift and the size of moves but destroys their order, so a timing rule that only rides
the drift scores no better on real data than on shuffled data. Fitness is his: profit factor of the
strategy's bar log returns. Where a parameter was chosen from a sweep, every permutation gets the
same sweep and keeps its own best (his in-sample test), so the p-value pays for the search.
"""
import json, os, sys, time
import numpy as np
import pandas as pd
from numba import njit

HERE = "/Users/triton/PROTEUS/sandbox/p0082"
OUTDIR = "/Users/triton/PROTEUS/experiments/2026-10-07-P-0082"
os.makedirs(OUTDIR, exist_ok=True)
N_PERM = int(os.environ.get("N_PERM", "1000"))
N_PERM_OPT = int(os.environ.get("N_PERM_OPT", "500"))


def load(sym, adjusted=True):
    df = pd.read_csv(os.path.join(HERE, "data", sym + ".csv"), parse_dates=["date"]).set_index("date")
    if adjusted:
        k = df["adjclose"] / df["close"]
        for c in ("open", "high", "low", "close"):
            df[c] = df[c] * k
    return df[["open", "high", "low", "close"]].astype(float)


# ------------------------------------------------------------------ indicators (numba)

@njit(cache=True)
def sma(x, n):
    out = np.full(x.size, np.nan)
    s = 0.0
    for i in range(x.size):
        s += x[i]
        if i >= n:
            s -= x[i - n]
        if i >= n - 1:
            out[i] = s / n
    return out


@njit(cache=True)
def rsi_wilder(c, n):
    out = np.full(c.size, np.nan)
    if c.size <= n:
        return out
    g = 0.0
    l = 0.0
    for i in range(1, n + 1):
        d = c[i] - c[i - 1]
        if d > 0:
            g += d
        else:
            l -= d
    g /= n
    l /= n
    out[n] = 100.0 if l == 0 else 100.0 - 100.0 / (1.0 + g / l)
    for i in range(n + 1, c.size):
        d = c[i] - c[i - 1]
        up = d if d > 0 else 0.0
        dn = -d if d < 0 else 0.0
        g = (g * (n - 1) + up) / n
        l = (l * (n - 1) + dn) / n
        out[i] = 100.0 if l == 0 else 100.0 - 100.0 / (1.0 + g / l)
    return out


@njit(cache=True)
def atr_wilder(h, l, c, n):
    tr = np.empty(c.size)
    tr[0] = h[0] - l[0]
    for i in range(1, c.size):
        tr[i] = max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1]))
    out = np.full(c.size, np.nan)
    if c.size <= n:
        return out
    a = tr[1:n + 1].mean()
    out[n] = a
    for i in range(n + 1, c.size):
        a = (a * (n - 1) + tr[i]) / n
        out[i] = a
    return out


@njit(cache=True)
def permute(o, h, l, c, start, seed):
    """neurotrader888/mcpt get_permutation, one market, as a loop numba can compile."""
    np.random.seed(seed)
    lo, lh, ll, lc = np.log(o), np.log(h), np.log(l), np.log(c)
    n = c.size
    m = n - start - 1
    r_o = np.empty(m)
    r_h = np.empty(m)
    r_l = np.empty(m)
    r_c = np.empty(m)
    for k in range(m):
        i = start + 1 + k
        r_o[k] = lo[i] - lc[i - 1]
        r_h[k] = lh[i] - lo[i]
        r_l[k] = ll[i] - lo[i]
        r_c[k] = lc[i] - lo[i]
    p1 = np.random.permutation(m)
    p2 = np.random.permutation(m)
    po, ph, pl, pc = lo.copy(), lh.copy(), ll.copy(), lc.copy()
    for k in range(m):
        i = start + 1 + k
        po[i] = pc[i - 1] + r_o[p2[k]]
        ph[i] = po[i] + r_h[p1[k]]
        pl[i] = po[i] + r_l[p1[k]]
        pc[i] = po[i] + r_c[p1[k]]
    return np.exp(po), np.exp(ph), np.exp(pl), np.exp(pc)


@njit(cache=True)
def pf(rets, start):
    gp = 0.0
    gl = 0.0
    for i in range(start, rets.size):
        r = rets[i]
        if r > 0:
            gp += r
        elif r < 0:
            gl -= r
    if gl == 0:
        return 1e9 if gp > 0 else 0.0
    return gp / gl


# ------------------------------------------------------------------ strategies (numba)
# Each returns an array of daily strategy log returns, index t = return earned over bar t.

@njit(cache=True)
def ma_filter_rets(o, c, n):
    """QS 1: close above SMA(n) -> long from next open; close below -> flat from next open."""
    m = sma(c, n)
    rets = np.zeros(c.size)
    pos = 0
    for t in range(c.size - 1):
        rets[t] = pos * (np.log(o[t + 1]) - np.log(o[t]))
        if not np.isnan(m[t]):
            if c[t] > m[t]:
                pos = 1
            elif c[t] < m[t]:
                pos = 0
    return rets


@njit(cache=True)
def rsi5_rets(c, variant):
    """QS 2: SPY above SMA200, RSI(5)<30 -> buy at the close; RSI(5)>50 -> sell at the close.
    variant 1 simple, 2 adds RSI down three sessions running, 3 adds RSI three sessions ago < 60."""
    r = rsi_wilder(c, 5)
    m = sma(c, 200)
    rets = np.zeros(c.size)
    pos = 0
    for t in range(c.size - 1):
        if pos == 1:
            if r[t] > 50:
                pos = 0
        elif t >= 3 and not np.isnan(m[t]) and not np.isnan(r[t - 3]):
            ok = c[t] > m[t] and r[t] < 30
            if variant >= 2:
                ok = ok and r[t] < r[t - 1] and r[t - 1] < r[t - 2] and r[t - 2] < r[t - 3]
            if variant >= 3:
                ok = ok and r[t - 3] < 60
            if ok:
                pos = 1
        rets[t + 1] = pos * (np.log(c[t + 1]) - np.log(c[t]))
    return rets


@njit(cache=True)
def rsi2_rets(o, h, c, thr, exit_kind):
    """QS 3: SPY above SMA200 and RSI(2) < thr at the close -> buy next open. Exit candidates,
    because the video does not say: 0 close above yesterday's high, 1 RSI(2) > 50, 2 RSI(2) > 70,
    3 five-day hold; all exit at the close."""
    r = rsi_wilder(c, 2)
    m = sma(c, 200)
    rets = np.zeros(c.size)
    state = 0          # 0 flat, 1 entry pending for next open, 2 long
    held = 0
    for t in range(1, c.size):
        if state == 1:
            rets[t] = np.log(c[t]) - np.log(o[t])
            state = 2
            held = 1
        elif state == 2:
            rets[t] = np.log(c[t]) - np.log(c[t - 1])
            held += 1
        if state == 2:
            out = False
            if exit_kind == 0:
                out = c[t] > h[t - 1]
            elif exit_kind == 1:
                out = r[t] > 50
            elif exit_kind == 2:
                out = r[t] > 70
            else:
                out = held >= 5
            if out:
                state = 0
        if state == 0 and not np.isnan(m[t]) and not np.isnan(r[t]):
            if c[t] > m[t] and r[t] < thr:
                state = 1
    return rets


@njit(cache=True)
def davey_rets(o, c, long_sig, short_sig, atr, mult):
    """Kevin Davey's frame: enter next open on a signal, stop and reverse on the opposite signal,
    exit next open when open position profit at the close falls mult*ATR below its running max."""
    rets = np.zeros(c.size)
    pos = 0
    entry = 0.0
    maxp = 0.0
    for t in range(c.size - 1):
        rets[t] = pos * (np.log(o[t + 1]) - np.log(o[t]))
        new = pos
        if pos != 0 and not np.isnan(atr[t]):
            openp = pos * (c[t] - entry)
            if openp > maxp:
                maxp = openp
            if openp < maxp - mult * atr[t]:
                new = 0
        if long_sig[t]:
            new = 1
        elif short_sig[t]:
            new = -1
        if new != pos:
            pos = new
            if pos != 0:
                entry = o[t + 1]
                maxp = 0.0
        elif long_sig[t] or short_sig[t]:
            pass
    return rets


@njit(cache=True)
def golden_signals(c, fast, slow):
    f = sma(c, fast)
    s = sma(c, slow)
    up = np.zeros(c.size, dtype=np.bool_)
    dn = np.zeros(c.size, dtype=np.bool_)
    for t in range(1, c.size):
        if np.isnan(s[t - 1]):
            continue
        up[t] = f[t] > s[t] and f[t - 1] <= s[t - 1]
        dn[t] = f[t] < s[t] and f[t - 1] >= s[t - 1]
    return up, dn


@njit(cache=True)
def rsi_cross_signals(c, n, thr):
    r = rsi_wilder(c, n)
    up = np.zeros(c.size, dtype=np.bool_)
    dn = np.zeros(c.size, dtype=np.bool_)
    for t in range(1, c.size):
        if np.isnan(r[t - 1]):
            continue
        up[t] = r[t] > thr and r[t - 1] <= thr
        dn[t] = r[t] < 100 - thr and r[t - 1] >= 100 - thr
    return up, dn


GC_FAST = np.array([25, 50, 75, 100])
GC_SLOW = np.array([150, 200, 250, 300])
RSI_LEN = np.array([5, 10, 15, 20])
RSI_THR = np.array([15.0, 25.0, 35.0, 45.0])
ATR_MULT = np.array([3.0, 6.0, 9.0])


@njit(cache=True)
def golden_best(o, h, l, c, start):
    atr = atr_wilder(h, l, c, 14)
    best = 0.0
    bi = -1
    k = 0
    for f in GC_FAST:
        for s in GC_SLOW:
            up, dn = golden_signals(c, f, s)
            for m in ATR_MULT:
                v = pf(davey_rets(o, c, up, dn, atr, m), start)
                if v > best:
                    best = v
                    bi = k
                k += 1
    return best, bi


@njit(cache=True)
def rsi_best(o, h, l, c, start):
    atr = atr_wilder(h, l, c, 14)
    best = 0.0
    bi = -1
    k = 0
    for n in RSI_LEN:
        for thr in RSI_THR:
            up, dn = rsi_cross_signals(c, n, thr)
            for m in ATR_MULT:
                v = pf(davey_rets(o, c, up, dn, atr, m), start)
                if v > best:
                    best = v
                    bi = k
                k += 1
    return best, bi


@njit(cache=True)
def ma_sweep_best(o, c, start, lo, hi):
    best = 0.0
    bn = -1
    for n in range(lo, hi + 1):
        v = pf(ma_filter_rets(o, c, n), start)
        if v > best:
            best = v
            bn = n
    return best, bn


@njit(cache=True)
def count_entries(rets):
    k = 0
    inpos = False
    for i in range(rets.size):
        if rets[i] != 0 and not inpos:
            k += 1
            inpos = True
        elif rets[i] == 0:
            inpos = False
    return k


@njit(cache=True)
def rsi2_sweep_best(o, h, c, start, exit_kind, min_trades):
    best = 0.0
    bt = -1
    for thr in range(1, 51):
        rr = rsi2_rets(o, h, c, float(thr), exit_kind)
        if count_entries(rr) < min_trades:
            continue
        v = pf(rr, start)
        if v > best:
            best = v
            bt = thr
    return best, bt


# ------------------------------------------------------------------ trade-level stats (python)

def trades_from_rets(rets, index):
    """Group consecutive non-zero bars into trades. Approximation: a trade that exits and re-enters
    on adjacent bars merges, which slightly undercounts; flagged in the report where it matters."""
    out = []
    cur = None
    for i, r in enumerate(rets):
        if r != 0:
            if cur is None:
                cur = [i, 0.0]
            cur[1] += r
        elif cur is not None:
            out.append((index[cur[0]], index[i - 1], cur[1]))
            cur = None
    if cur is not None:
        out.append((index[cur[0]], index[len(rets) - 1], cur[1]))
    return out


def stats(rets, index, start=0):
    rets = np.asarray(rets)[start:]
    idx = index[start:]
    tr = trades_from_rets(rets, idx)
    simple = np.array([np.expm1(t[2]) for t in tr]) if tr else np.array([])
    eq = np.exp(np.cumsum(rets))
    dd = 1 - eq / np.maximum.accumulate(eq)
    wins = simple[simple > 0].sum()
    losses = -simple[simple < 0].sum()
    years = (idx[-1] - idx[0]).days / 365.25
    return {
        "trades": len(tr),
        "win_rate": round(float((simple > 0).mean() * 100), 1) if len(simple) else None,
        "avg_trade_pct": round(float(simple.mean() * 100), 2) if len(simple) else None,
        "trade_pf": round(float(wins / losses), 2) if losses > 0 else None,
        "growth_x": round(float(eq[-1]), 2),
        "cagr_pct": round(float((eq[-1] ** (1 / years) - 1) * 100), 2),
        "max_dd_pct": round(float(dd.max() * 100), 2),
        "exposure_pct": round(float((rets != 0).mean() * 100), 1),
        "bar_pf": round(float(pf(np.asarray(rets), 0)), 3),
    }


def mcpt(fitness, o, h, l, c, start, n_perm, seed0=1):
    """p = (1 + permutations at least as good) / (1 + n_perm), neurotrader's convention."""
    real = fitness(o, h, l, c)
    better = 1
    vals = []
    for k in range(n_perm):
        po, ph, pl, pc = permute(o, h, l, c, start, seed0 + k)
        v = fitness(po, ph, pl, pc)
        vals.append(v)
        if v >= real:
            better += 1
    return real, better / (n_perm + 1), float(np.median(vals))


# ------------------------------------------------------------------ the five tests

def main():
    t0 = time.time()
    res = {}
    spy = load("SPY")
    spy_raw = load("SPY", adjusted=False)
    O, H, L, C = (spy[x].to_numpy() for x in ("open", "high", "low", "close"))
    idx = spy.index
    WARM = 300  # bars before fitness counts, so every MA up to 300 exists

    # 1. 200 vs 222-day MA on SPY
    t1 = {"claim": {"200": {"trades": 111, "trade_pf": 3.20, "avg_trade_pct": 2.34, "max_dd_pct": 21.17, "growth_x": 8.24},
                    "222": {"trades": 98, "trade_pf": 3.84, "avg_trade_pct": 2.85, "max_dd_pct": 13.96, "growth_x": 9.76},
                    "220": {"growth_x": 9.52}, "225": {"growth_x": 9.31}, "250": {"growth_x": 7.84}}}
    for label, df in (("adjusted", spy), ("price_only", spy_raw)):
        o, c = df["open"].to_numpy(), df["close"].to_numpy()
        t1[label] = {str(n): stats(ma_filter_rets(o, c, n), idx) for n in (200, 220, 222, 225, 250)}
        growth = {n: stats(ma_filter_rets(o, c, n), idx)["growth_x"] for n in range(20, 301)}
        top = sorted(growth.items(), key=lambda kv: -kv[1])[:5]
        t1[label]["sweep_top5_growth"] = top
    real, p, med = mcpt(lambda o, h, l, c: pf(ma_filter_rets(o, c, 200), WARM), O, H, L, C, 0, N_PERM)
    t1["mcpt_fixed_200"] = {"real_bar_pf": round(real, 3), "p": round(p, 4), "perm_median_pf": round(med, 3), "n": N_PERM}
    real, p, med = mcpt(lambda o, h, l, c: ma_sweep_best(o, c, WARM, 20, 300)[0], O, H, L, C, 0, N_PERM_OPT)
    t1["mcpt_best_of_281"] = {"real_bar_pf": round(real, 3), "best_n": int(ma_sweep_best(O, C, WARM, 20, 300)[1]),
                              "p": round(p, 4), "perm_median_pf": round(med, 3), "n": N_PERM_OPT}
    res["qs_ma_200_vs_222"] = t1
    print("test 1 done", round(time.time() - t0), "s", flush=True)

    # 2. Simple, double, triple RSI(5) on SPY
    t2 = {"claim": {"simple": {"trades": 199, "growth_pct": 482},
                    "double": {"trades": 127, "growth_pct": 261},
                    "triple": {"trades": 90, "win_rate": 88.9, "avg_trade_pct": 1.25, "trade_pf": 5.53, "growth_pct": 201.6,
                               "exposure_pct": 5.2}}}
    for v, name in ((1, "simple"), (2, "double"), (3, "triple")):
        t2[name] = stats(rsi5_rets(C, v), idx)
        real, p, med = mcpt(lambda o, h, l, c, v=v: pf(rsi5_rets(c, v), WARM), O, H, L, C, 0, N_PERM)
        t2[name]["mcpt"] = {"real_bar_pf": round(real, 3), "p": round(p, 4), "perm_median_pf": round(med, 3), "n": N_PERM}
    res["qs_rsi5_simple_double_triple"] = t2
    print("test 2 done", round(time.time() - t0), "s", flush=True)

    # 3. RSI(2) threshold sweep on SPY, exit unknown
    t3 = {"claim": {"1": {"trades": 13, "trade_pf": 6.56}, "9": {"trades": 233, "trade_pf": 2.59, "win_rate": 76.8, "avg_trade_pct": 0.59},
                    "15": {"trade_pf": 2.34}, "30": {"trades": 613, "trade_pf": 1.84, "avg_trade_pct": 0.33}}}
    names = {0: "close_above_prev_high", 1: "rsi2_above_50", 2: "rsi2_above_70", 3: "five_day_hold"}
    for k, nm in names.items():
        t3[nm] = {str(thr): stats(rsi2_rets(O, H, C, float(thr), k), idx) for thr in (1, 9, 15, 30)}
    # pick the exit whose trade counts sit closest to the published 13 / 233 / 613
    target = {"1": 13, "9": 233, "30": 613}
    err = {nm: sum(abs(t3[nm][th]["trades"] - n) / n for th, n in target.items()) for nm in names.values()}
    best_exit = min(err, key=err.get)
    k_best = [k for k, nm in names.items() if nm == best_exit][0]
    t3["exit_match_error"] = {k: round(v, 3) for k, v in err.items()}
    t3["exit_used_for_tests"] = best_exit
    real, p, med = mcpt(lambda o, h, l, c: pf(rsi2_rets(o, h, c, 30.0, k_best), WARM), O, H, L, C, 0, N_PERM)
    t3["mcpt_fixed_30"] = {"real_bar_pf": round(real, 3), "p": round(p, 4), "perm_median_pf": round(med, 3), "n": N_PERM}
    real, p, med = mcpt(lambda o, h, l, c: rsi2_sweep_best(o, h, c, WARM, k_best, 100)[0], O, H, L, C, 0, N_PERM_OPT)
    t3["mcpt_best_of_50_min100trades"] = {"real_bar_pf": round(real, 3), "best_thr": int(rsi2_sweep_best(O, H, C, WARM, k_best, 100)[1]),
                                          "p": round(p, 4), "perm_median_pf": round(med, 3), "n": N_PERM_OPT}
    res["qs_rsi2_threshold_sweep"] = t3
    print("test 3 done", round(time.time() - t0), "s", flush=True)

    # 4 and 5. Kevin Davey's golden cross and RSI crossover, daily bars on 12 ETFs, 2007 onwards
    syms = ["SPY", "QQQ", "DIA", "IWM", "GLD", "SLV", "USO", "UNG", "TLT", "IEF", "FXE", "FXY"]
    t4, t5 = {}, {}
    for s in syms:
        df = load(s)
        o, h, l, c = (df[x].to_numpy() for x in ("open", "high", "low", "close"))
        start = max(int(np.searchsorted(df.index.values, np.datetime64("2007-01-01"))), 300)
        atr = atr_wilder(h, l, c, 14)
        up, dn = golden_signals(c, 50, 200)
        st = stats(davey_rets(o, c, up, dn, atr, 6.0), df.index, start)
        real, p, med = mcpt(lambda o, h, l, c: golden_best(o, h, l, c, start)[0], o, h, l, c, start, N_PERM_OPT)
        st.update({"best_of_48_bar_pf": round(real, 3), "best_of_48_p": round(p, 4), "perm_median_pf": round(med, 3),
                   "from": str(df.index[start].date())})
        t4[s] = st
        up, dn = rsi_cross_signals(c, 10, 25.0)
        st = stats(davey_rets(o, c, up, dn, atr, 6.0), df.index, start)
        real, p, med = mcpt(lambda o, h, l, c: rsi_best(o, h, l, c, start)[0], o, h, l, c, start, N_PERM_OPT)
        st.update({"best_of_48_bar_pf": round(real, 3), "best_of_48_p": round(p, 4), "perm_median_pf": round(med, 3),
                   "from": str(df.index[start].date())})
        t5[s] = st
        print("  ", s, "golden p", t4[s]["best_of_48_p"], "rsi p", t5[s]["best_of_48_p"], round(time.time() - t0), "s", flush=True)
    res["davey_golden_cross_daily_etfs"] = {"fixed": "50/200, ATR(14) x6 trail", "grid": "fast 25-100, slow 150-300, ATR x3/6/9 (my guess at his 48)",
                                            "markets": t4}
    res["davey_rsi_cross_daily_etfs"] = {"fixed": "RSI(10) over 25 / under 75, ATR(14) x6 trail", "grid": "RSI 5-20, threshold 15-45, ATR x3/6/9 (his 48)",
                                         "markets": t5}
    res["runtime_s"] = round(time.time() - t0)
    res["data"] = {"source": "Yahoo chart endpoint, keyless, daily, OHLC scaled by adjclose/close", "spy_from": str(idx[0].date()),
                   "spy_to": str(idx[-1].date())}
    with open(os.path.join(OUTDIR, "results.json"), "w") as fh:
        json.dump(res, fh, indent=1, default=str)
    print("done", res["runtime_s"], "s")


if __name__ == "__main__":
    main()
