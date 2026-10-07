"""P-0088: Kaufman's efficiency ratio on P-0084's 28 ETFs. Which markets trend, and does trading only
the trendiest half, chosen on past data only, beat all 28 under the joint permutation test?

Fixed before the run:
  ER(n)        |log close_t - log close_{t-n}| / sum of |daily log changes| over the same n days,
               n = 252. 1 is a straight line, 0 is pure noise.
  ranking      (a) information only: each market's mean ER over the evaluation span (in-sample);
               (b) the rule: at every 5-day rebalance, the mean ER over the trailing 504 sessions,
               computed from data before that close only.
  portfolios   P-0084's 12-month time-series momentum, same sizing and costs, on
                 all28      the 28 markets (the P-0084 baseline, re-run here);
                 top14      only the 14 highest trailing-ER markets at each rebalance;
                 bottom14   only the 14 lowest, as the control (if ER means nothing, the halves tie).
               Signals for unselected markets are set to zero; the sizing divisor is the number of
               markets held (14), so gross exposure is comparable to all28.
  luck test    P-0084's joint shuffle of whole days across all 28 markets, the same shuffle applied
               to all three portfolios, 500 draws; fitness is the Sharpe ratio from 2008-05-01.
               Trailing ER is recomputed on the shuffled series, so the selection is tested too.
Data: Yahoo daily closes scaled to total return (sandbox/p0082/data).

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 /Users/triton/PROTEUS/experiments/2026-10-07-P-0088/p0088.py
"""
import json, os, sys, time
import numpy as np
import pandas as pd

sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-10-07-P-0084")
from p0084 import closes, signal_tsmom, sharpe, summarise, SYMS, UNIVERSE, VOL_N, VOL_TARGET, GROSS_CAP, REBAL, COST, LOOKBACK, EVAL_FROM  # noqa: E402

OUT = "/Users/triton/PROTEUS/experiments/2026-10-07-P-0088"
ER_N, ER_TRAIL, K = 252, 504, 14
N_PERM = int(os.environ.get("N_PERM", "500"))


def er(logp, n):
    """Efficiency ratio per market per day, NaN before n days."""
    d = np.abs(np.diff(logp, axis=0))
    path = np.vstack([np.zeros((1, logp.shape[1])), np.cumsum(d, axis=0)])
    out = np.full(logp.shape, np.nan)
    out[n:] = np.abs(logp[n:] - logp[:-n]) / np.maximum(path[n:] - path[:-n], 1e-12)
    return out


def trailing_mean(x, n):
    c = np.cumsum(np.nan_to_num(x), axis=0)
    cnt = np.cumsum(~np.isnan(x), axis=0)
    out = np.full(x.shape, np.nan)
    out[n:] = (c[n:] - c[:-n]) / np.maximum(cnt[n:] - cnt[:-n], 1)
    out[n:][(cnt[n:] - cnt[:-n]) < n // 2] = np.nan
    return out


def select_mask(tr_er, k, top=True):
    """At each rebalance, the k markets with the highest (or lowest) trailing ER, using the value
    at the previous close; held until the next rebalance."""
    T, N = tr_er.shape
    mask = np.zeros((T, N), dtype=bool)
    cur = np.zeros(N, dtype=bool)
    for t in range(T):
        if t % REBAL == 0 and t > 0:
            row = tr_er[t - 1]
            if np.isfinite(row).sum() >= k:
                order = np.argsort(np.where(np.isnan(row), -np.inf if top else np.inf, row))
                pick = order[-k:] if top else order[:k]
                cur = np.zeros(N, dtype=bool)
                cur[pick] = True
        mask[t] = cur
    return mask


def portfolio_n(rets, sig, n_div):
    """P-0084's portfolio with an explicit sizing divisor."""
    T, N = rets.shape
    lr = np.log1p(rets)
    c1 = np.cumsum(np.vstack([np.zeros((1, N)), lr]), axis=0)
    c2 = np.cumsum(np.vstack([np.zeros((1, N)), lr ** 2]), axis=0)
    vol = np.full((T, N), np.nan)
    m = (c1[VOL_N:] - c1[:-VOL_N]) / VOL_N
    v = (c2[VOL_N:] - c2[:-VOL_N]) / VOL_N - m ** 2
    vol[VOL_N - 1:] = np.sqrt(np.maximum(v, 1e-12) * 252)
    raw = np.nan_to_num(sig * (VOL_TARGET / vol) / n_div)
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
    return (held * rets).sum(axis=1)


def three(rets, logp):
    sig = signal_tsmom(logp)
    tr = trailing_mean(er(logp, ER_N), ER_TRAIL)
    top = select_mask(tr, K, True)
    bot = select_mask(tr, K, False)
    return (portfolio_n(rets, sig, len(SYMS)), portfolio_n(rets, sig * top, K), portfolio_n(rets, sig * bot, K)), top


def main():
    t0 = time.time()
    px = closes()
    idx = px.index
    rets = px.pct_change().fillna(0.0).to_numpy()
    logp = np.log(px.to_numpy())
    ev = idx >= pd.Timestamp(EVAL_FROM)
    E = idx[ev]
    res = {"er_n": ER_N, "er_trailing": ER_TRAIL, "k": K, "eval_from": EVAL_FROM, "to": str(idx[-1].date())}
    e = er(logp, ER_N)
    mean_er = np.nanmean(e[ev], axis=0)
    rank = sorted(zip(SYMS, mean_er), key=lambda x: -x[1])
    res["mean_er_in_sample"] = {s: round(float(v), 3) for s, v in rank}
    res["mean_er_by_class"] = {g: round(float(np.mean([mean_er[SYMS.index(s)] for s in ss])), 3) for g, ss in UNIVERSE.items()}
    (ra, rt, rb), top = three(rets, logp)
    res["all28"] = summarise(ra[ev], E)
    res["top14"] = summarise(rt[ev], E)
    res["bottom14"] = summarise(rb[ev], E)
    res["top14_share_selected"] = {s: round(float(top[ev][:, i].mean()), 2) for i, s in enumerate(SYMS)}
    res["corr_top_vs_all"] = round(float(np.corrcoef(rt[ev], ra[ev])[0, 1]), 3)
    print("rank", rank[:8], "...", rank[-5:])
    for k in ("all28", "top14", "bottom14"):
        print(k, {x: res[k][x] for x in ("cagr_pct", "vol_pct", "sharpe", "max_dd_pct", "growth_x")}, flush=True)
    # joint luck test, same shuffle for all three
    rng = np.random.default_rng(88)
    real = [sharpe(x[ev]) for x in (ra, rt, rb)]
    better = [1, 1, 1]
    perms = [[], [], []]
    first = max(0, np.where(ev)[0][0] - LOOKBACK - VOL_N)
    diff_real = real[1] - real[2]
    better_diff = 1
    for k in range(N_PERM):
        order = np.concatenate([np.arange(first), first + rng.permutation(len(rets) - first)])
        pr = rets[order]
        plogp = np.vstack([logp[:1], logp[0] + np.cumsum(np.log1p(pr[1:]), axis=0)])
        (pa, pt, pb), _ = three(pr, plogp)
        s = [sharpe(x[ev]) for x in (pa, pt, pb)]
        for i in range(3):
            perms[i].append(s[i])
            better[i] += s[i] >= real[i]
        better_diff += (s[1] - s[2]) >= diff_real
        if k % 100 == 99:
            print("perm", k + 1, round(time.time() - t0), "s", flush=True)
    res["mcpt"] = {"n": N_PERM}
    for i, name in enumerate(("all28", "top14", "bottom14")):
        res["mcpt"][name] = {"real_sharpe": round(real[i], 3), "p": round(better[i] / (N_PERM + 1), 4),
                             "perm_median": round(float(np.median(perms[i])), 3), "perm_95th": round(float(np.percentile(perms[i], 95)), 3)}
    res["mcpt"]["top_minus_bottom"] = {"real": round(diff_real, 3), "p": round(better_diff / (N_PERM + 1), 4)}
    res["runtime_s"] = round(time.time() - t0)
    print("mcpt", res["mcpt"])
    json.dump(res, open(os.path.join(OUT, "results.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
