"""P-0087: calendar events on daily SPY, each against random days of the same kind and length.

Fixed before the run:
  fed_day     close-to-close return on the FOMC statement day (scheduled meetings only, from the
              Fed's own calendar pages, 2016-01 to 2026-09, 85 meetings; unscheduled ones excluded).
  pre_fed     the session before the statement day, close(t-2) to close(t-1): the daily version of
              the Lucca-Moench pre-FOMC drift.
  fed_3day    close(t-3) to close(t), the whole run-in and the decision.
  jobs_friday first Friday of each calendar month since 1993, close Thu to close Fri. This is an
              approximation of the BLS schedule (some releases fall on a Thursday or the second
              Friday), stated as such.
  weak_monday Monday close below the previous Friday's low: buy the Monday close, sell the Friday
              close (or the last session of that week). Claimed (A-05): about +0.6% a trade.
Controls: the same return measured on every other day of the same weekday class in the same span,
and a bootstrap of 5000 random draws of the same count from that population; p is the share of
draws with a mean at or above the real mean. Data as traded, not dividend-adjusted.

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 /Users/triton/PROTEUS/experiments/2026-10-07-P-0087/p0087.py
"""
import json, os
import numpy as np
import pandas as pd

OUT = "/Users/triton/PROTEUS/experiments/2026-10-07-P-0087"
DATA = "/Users/triton/PROTEUS/sandbox/p0082/data/SPY.csv"
N_BOOT = 5000
FED = """2016-01-27 2016-03-16 2016-04-27 2016-06-15 2016-07-27 2016-09-21 2016-11-02 2016-12-14
2017-02-01 2017-03-15 2017-05-03 2017-06-14 2017-07-26 2017-09-20 2017-11-01 2017-12-13
2018-01-31 2018-03-21 2018-05-02 2018-06-13 2018-08-01 2018-09-26 2018-11-08 2018-12-19
2019-01-30 2019-03-20 2019-05-01 2019-06-19 2019-07-31 2019-09-18 2019-10-30 2019-12-11
2020-01-29 2020-04-29 2020-06-10 2020-07-29 2020-09-16 2020-11-05 2020-12-16
2021-01-27 2021-03-17 2021-04-28 2021-06-16 2021-07-28 2021-09-22 2021-11-03 2021-12-15
2022-01-26 2022-03-16 2022-05-04 2022-06-15 2022-07-27 2022-09-21 2022-11-02 2022-12-14
2023-02-01 2023-03-22 2023-05-03 2023-06-14 2023-07-26 2023-09-20 2023-11-01 2023-12-13
2024-01-31 2024-03-20 2024-05-01 2024-06-12 2024-07-31 2024-09-18 2024-11-07 2024-12-18
2025-01-29 2025-03-19 2025-05-07 2025-06-18 2025-07-30 2025-09-17 2025-10-29 2025-12-10
2026-01-28 2026-03-18 2026-04-29 2026-06-17 2026-07-29 2026-09-16""".split()


def summarise(name, real, pool, rng):
    real, pool = np.asarray(real), np.asarray(pool)
    draws = np.array([pool[rng.choice(pool.size, real.size, replace=False)].mean() for _ in range(N_BOOT)])
    return {"n": int(real.size), "mean_pct": round(float(real.mean() * 100), 3), "win_pct": round(float((real > 0).mean() * 100), 1),
            "median_pct": round(float(np.median(real) * 100), 3),
            "control_n": int(pool.size), "control_mean_pct": round(float(pool.mean() * 100), 3),
            "control_win_pct": round(float((pool > 0).mean() * 100), 1),
            "boot_p_mean_at_or_above": round(float((draws >= real.mean()).mean()), 4),
            "boot_p_mean_at_or_below": round(float((draws <= real.mean()).mean()), 4)}


def main():
    rng = np.random.default_rng(11)
    df = pd.read_csv(DATA, parse_dates=["date"]).set_index("date")
    c, lo = df["close"], df["low"]
    r1 = c.pct_change()
    res = {"span": [str(df.index[0].date()), str(df.index[-1].date())]}

    # Fed
    fed = pd.to_datetime(FED)
    fed = fed[fed.isin(df.index)]
    span = (df.index >= "2016-01-01")
    pos = df.index.get_indexer(fed)
    all_pos = np.where(span)[0]
    all_pos = all_pos[all_pos >= 3]
    other = np.setdiff1d(all_pos, np.concatenate([pos, pos - 1, pos - 2, pos - 3]))
    r3 = c.pct_change(3).to_numpy()
    r1a = r1.to_numpy()
    res["fed_day"] = summarise("fed_day", r1a[pos], r1a[other], rng)
    res["pre_fed"] = summarise("pre_fed", r1a[pos - 1], r1a[other], rng)
    res["fed_3day"] = summarise("fed_3day", r3[pos], r3[other], rng)
    res["fed_dates_used"] = int(pos.size)

    # Jobs Fridays, first Friday of the month, 1993 on
    fri = df.index[df.index.weekday == 4]
    first_fri = fri.to_series().groupby([fri.year, fri.month]).first()
    jf = df.index.get_indexer(pd.DatetimeIndex(first_fri.values))
    jf = jf[jf > 0]
    all_fri = df.index.get_indexer(fri)
    other_fri = np.setdiff1d(all_fri, jf)
    other_fri = other_fri[other_fri > 0]
    res["jobs_friday"] = summarise("jobs_friday", r1a[jf], r1a[other_fri], rng)

    # Weak Monday: Monday close below previous Friday's low, hold Monday close to the week's last close
    idx = df.index
    week = idx.to_period("W-FRI")
    rows = []
    allmon = []
    for i in range(1, len(idx)):
        if idx[i].weekday() != 0:
            continue
        # previous session must be the prior week's last session
        prev = i - 1
        j = i
        while j + 1 < len(idx) and week[j + 1] == week[i]:
            j += 1
        if j == i:
            continue
        ret = c.iloc[j] / c.iloc[i] - 1
        allmon.append(ret)
        if c.iloc[i] < lo.iloc[prev]:
            rows.append((idx[i], ret))
    real = np.array([r for _, r in rows])
    res["weak_monday"] = summarise("weak_monday", real, np.array(allmon), rng)
    res["weak_monday"]["claimed_pct"] = 0.6
    res["weak_monday"]["since_2009"] = summarise("wm09", np.array([r for d, r in rows if d >= pd.Timestamp("2009-01-01")]),
                                                 np.array(allmon), rng)
    for k in ("fed_day", "pre_fed", "fed_3day", "jobs_friday", "weak_monday"):
        print(k, res[k])
    json.dump(res, open(os.path.join(OUT, "results.json"), "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
