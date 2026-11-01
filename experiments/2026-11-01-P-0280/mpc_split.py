"""P-0280: P-0274 with n. The systems book's RSI(5) simple rule, next-open fills, split by whether the
signal day falls in the 5 trading days before any MPC decision (175 meeting dates since 2009 from the
Bank's mpcvoting.xlsx, Bank Rate sheet, pulled keyless 1 Nov 2026 to sandbox/boe-mpc-decision-dates.txt),
not just the 28 rate changes P-0274 used. Same backtest and random-entry control as P-0243 and P-0274,
plus a permutation test on the pre-window label (shuffle which trades carry the label, 5000 times).

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 experiments/2026-11-01-P-0280/mpc_split.py
"""
import json, sys
import numpy as np

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/p0082")
sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-10-07-P-0083")
from p0082 import load, sma  # noqa: E402
from basket_backtest import rsi5_next_open_rp, BASKET  # noqa: E402

OUT = "/Users/triton/PROTEUS/experiments/2026-11-01-P-0280/results.json"
DATES = "/Users/triton/PROTEUS/sandbox/boe-mpc-decision-dates.txt"
WINDOW = 5
N_DRAWS = 2000
N_PERM = 5000

decisions = [np.datetime64(l.strip()) for l in open(DATES) if l.strip()]
print("MPC decision dates since 2009:", len(decisions), "first", str(decisions[0]), "last", str(decisions[-1]), flush=True)

rng = np.random.default_rng(20261101)


def run(symbols, label):
    trades = {"pre": [], "rest": []}
    pool = {"pre": [], "rest": []}
    opens = {}
    pre_days = 0
    all_days = 0
    for s in symbols:
        df = load(s)
        o, c = df["open"].to_numpy(), df["close"].to_numpy()
        idx = df.index.values
        opens[s] = o
        start = int(np.searchsorted(idx, np.datetime64("2009-01-01")))
        cpos = np.unique(np.searchsorted(idx, np.array(decisions), side="left"))
        cpos = cpos[cpos < len(idx)]
        pre = np.zeros(len(idx), dtype=bool)
        for p in cpos:
            pre[max(0, p - WINDOW):p] = True      # the WINDOW trading days before the decision day
        pre_days += int(pre[start:].sum())
        all_days += int(len(idx) - start)
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
    out = {"pre_window_share_of_days_pct": round(100 * pre_days / all_days, 1)}
    for b in ("pre", "rest"):
        a = np.array([r for r, _ in trades[b]])
        holds = np.array([h for _, h in trades[b]])
        n = a.size
        P = pool[b]
        if n < 2 or not P:
            out[b] = {"trades": int(n), "note": "too few"}
            print(label, b, out[b], flush=True)
            continue
        sims = np.empty(N_DRAWS)
        for j in range(N_DRAWS):
            pick = rng.integers(0, len(P), n)
            hh = holds[rng.integers(0, n, n)]
            sims[j] = np.mean([opens[P[q][0]][P[q][1] + 1 + h] / opens[P[q][0]][P[q][1] + 1] - 1 for q, h in zip(pick, hh)])
        out[b] = {
            "trades": int(n), "mean_pct": round(a.mean() * 100, 3), "win_pct": round((a > 0).mean() * 100, 1),
            "t": round(float(a.mean() / (a.std(ddof=1) / np.sqrt(n))), 2) if n > 1 else None,
            "mean_hold_days": round(float(holds.mean()), 2),
            "control_mean_pct": round(float(sims.mean()) * 100, 3), "excess_pct": round((a.mean() - sims.mean()) * 100, 3),
            "p_v_control": round(float((sims >= a.mean()).mean()), 4), "pool_days": len(P)}
        print(label, b, out[b], flush=True)
    # permutation test on the label: is pre minus rest larger than a random split of the same sizes?
    pa = np.array([r for r, _ in trades["pre"]])
    ra = np.array([r for r, _ in trades["rest"]])
    if pa.size >= 2 and ra.size >= 2:
        allr = np.concatenate([pa, ra])
        obs = pa.mean() - ra.mean()
        perm = np.empty(N_PERM)
        for j in range(N_PERM):
            rng.shuffle(allr)
            perm[j] = allr[:pa.size].mean() - allr[pa.size:].mean()
        out["perm"] = {"obs_diff_pct": round(obs * 100, 3), "n_perm": N_PERM,
                       "p_two_sided": round(float((np.abs(perm) >= abs(obs)).mean()), 4),
                       "p_pre_better": round(float((perm >= obs).mean()), 4)}
        print(label, "perm", out["perm"], flush=True)
    return out


res = {"window_trading_days_before_decision": WINDOW, "mpc_decisions_since_2009": len(decisions),
       "decision_dates": [str(d) for d in decisions], "n_draws": N_DRAWS, "n_perm": N_PERM,
       "EWU": run(["EWU"], "EWU"), "SPY": run(["SPY"], "SPY"), "all_nine": run(BASKET, "all nine")}
json.dump(res, open(OUT, "w"), indent=1)
print("wrote", OUT)
