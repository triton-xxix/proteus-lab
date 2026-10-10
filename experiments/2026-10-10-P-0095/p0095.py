"""P-0095: weak-Monday reversal, the harder test (follows P-0087, which found +0.71% a trade on SPY).

Fixed before the run (called shot in REPORT.md):
  weak_monday   Monday close below the previous session's (Friday's) low; buy Monday close, sell the
                week's last close. Per market, nine ETFs of the systems book, pooled.
  down_monday   control 1: Monday close below Friday's close but NOT below its low, same hold.
  any_dip       control 2: ANY weekday close below the previous session's low, held the same number
                of sessions as the weak-Monday trade it is paired with by weekday-free length: 4 sessions.
  random        luck test: 5000 draws of the same count of random weekday entries, 4-session hold,
                same markets in the same proportion; p = share with mean >= the weak-Monday mean.
  rsi_overlap   share of weak Mondays that are also book-1 simple entries that day (close above the
                200-day average and Wilder RSI(5) below 30), and the weak-Monday mean with those removed.
Data as traded, not dividend-adjusted, 2009 on (the systems book's span). No costs.

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 /Users/triton/PROTEUS/experiments/2026-10-10-P-0095/p0095.py
"""
import json
import numpy as np
import pandas as pd

OUT = "/Users/triton/PROTEUS/experiments/2026-10-10-P-0095/"
D = "/Users/triton/PROTEUS/sandbox/p0082/data/%s.csv"
MKTS = ["SPY", "QQQ", "DIA", "IWM", "EFA", "EEM", "EWU", "EWJ", "EWG"]
START = "2009-01-01"
HOLD = 4


def rsi_wilder(c, n=5):
    d = c.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn)


def stats(x):
    x = np.asarray(x)
    return {"n": int(x.size), "mean_pct": round(float(x.mean() * 100), 3) if x.size else None,
            "win_pct": round(float((x > 0).mean() * 100), 1) if x.size else None}


def main():
    rng = np.random.default_rng(95)
    wm, dm, dip, wm_rsi, wm_norsi, pools, per = [], [], [], [], [], {}, {}
    for m in MKTS:
        df = pd.read_csv(D % m, parse_dates=["date"]).set_index("date").sort_index()
        c, lo = df["close"], df["low"]
        sma200, rsi = c.rolling(200).mean(), rsi_wilder(c)
        idx = df.index
        week = idx.to_period("W-FRI")
        ca, la = c.to_numpy(), lo.to_numpy()
        fwd = c.shift(-HOLD) / c - 1
        keep = idx >= START
        mw = []
        for i in range(1, len(idx)):
            if not keep[i] or idx[i].weekday() != 0:
                continue
            j = i
            while j + 1 < len(idx) and week[j + 1] == week[i]:
                j += 1
            if j == i:
                continue
            ret = ca[j] / ca[i] - 1
            if ca[i] < la[i - 1]:
                mw.append(ret)
                book1 = c.iloc[i] > sma200.iloc[i] and rsi.iloc[i] < 30
                (wm_rsi if book1 else wm_norsi).append(ret)
            elif ca[i] < ca[i - 1]:
                dm.append(ret)
        wm.extend(mw)
        below = (c < lo.shift(1)) & keep & fwd.notna()
        dip.extend(fwd[below].tolist())
        pools[m] = fwd[keep & fwd.notna() & (idx.weekday < 5)].to_numpy()
        per[m] = stats(mw)
    # Luck test: random weekday entries, same count per market as weak Mondays
    counts = {m: per[m]["n"] for m in MKTS}
    real = np.mean(wm)
    draws = np.empty(5000)
    for k in range(5000):
        draws[k] = np.mean(np.concatenate([rng.choice(pools[m], counts[m], replace=False) for m in MKTS]))
    res = {"span_from": START, "hold_sessions_for_controls": HOLD, "per_market": per,
           "weak_monday": stats(wm), "down_monday_not_below_low": stats(dm), "any_weekday_dip_4d": stats(dip),
           "random_4d_mean_pct": round(float(draws.mean() * 100), 3),
           "luck_p_at_or_above": round(float((draws >= real).mean()), 4),
           "weak_monday_also_book1": stats(wm_rsi), "weak_monday_not_book1": stats(wm_norsi),
           "overlap_share_pct": round(100 * len(wm_rsi) / len(wm), 1)}
    for k, v in res.items():
        print(k, v)
    json.dump(res, open(OUT + "results.json", "w"), indent=1)


if __name__ == "__main__":
    main()
