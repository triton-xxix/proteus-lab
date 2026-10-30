"""P-0263: one-parameter logit recalibration of the exchange book, leave-one-out, stdlib only.

p' = sigmoid(a * logit(p)). a > 1 stretches away from 0.5 (the forecaster was underconfident),
a < 1 shrinks toward 0.5 (overconfident), a = 1 leaves the calls alone. Fit a by minimising Brier
on a grid, leave-one-out for the honest score, and a 2,000-draw bootstrap for the interval on a.
The idea is the favourite-longshot correction from arXiv 2610.13593, with a one-parameter curve in
place of their B-spline because 29 rows cannot carry more.
"""
from __future__ import annotations

import csv
import json
import math
import random

BOOK = "/Users/triton/PROTEUS/exchange/BOOK.csv"
OUT = "/Users/triton/PROTEUS/experiments/2026-10-30-P-0263/results.json"
GRID = [round(0.1 * i, 2) for i in range(1, 41)]  # a from 0.1 to 4.0


def logit(p: float) -> float:
    p = min(max(p, 1e-4), 1 - 1e-4)
    return math.log(p / (1 - p))


def sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))


def brier(rows, a: float) -> float:
    return sum((sigmoid(a * logit(p)) - y) ** 2 for p, y in rows) / len(rows)


def fit(rows) -> float:
    return min(GRID, key=lambda a: brier(rows, a))


def main() -> None:
    raw = list(csv.DictReader(open(BOOK)))
    rows = [(float(r["p"]), 1.0 if r["outcome"] == "winner" else 0.0)
            for r in raw if r["outcome"] in ("winner", "loser") and r["p"]]
    n = len(rows)
    a_all = fit(rows)
    raw_brier = brier(rows, 1.0)
    insample = brier(rows, a_all)
    # leave-one-out
    loo = 0.0
    loo_as = []
    for i in range(n):
        train = rows[:i] + rows[i + 1:]
        a = fit(train)
        loo_as.append(a)
        p, y = rows[i]
        loo += (sigmoid(a * logit(p)) - y) ** 2
    loo /= n
    # bootstrap interval for a
    rng = random.Random(20261030)
    boots = []
    for _ in range(2000):
        sample = [rows[rng.randrange(n)] for _ in range(n)]
        boots.append(fit(sample))
    boots.sort()
    lo, hi = boots[int(0.025 * len(boots))], boots[int(0.975 * len(boots)) - 1]
    # calibration table by my p bucket
    buckets = {}
    for p, y in rows:
        k = "p<0.35" if p < 0.35 else ("0.35-0.65" if p < 0.65 else "p>=0.65")
        b = buckets.setdefault(k, {"n": 0, "mean_p": 0.0, "hit": 0.0})
        b["n"] += 1
        b["mean_p"] += p
        b["hit"] += y
    for b in buckets.values():
        b["mean_p"] = round(b["mean_p"] / b["n"], 3)
        b["hit_rate"] = round(b["hit"] / b["n"], 3)
    out = {"n_settled": n, "a_fitted": a_all, "a_bootstrap_95": [lo, hi],
           "a_loo_range": [min(loo_as), max(loo_as)],
           "brier_raw": round(raw_brier, 4), "brier_insample": round(insample, 4),
           "brier_loo": round(loo, 4), "loo_minus_raw": round(loo - raw_brier, 4),
           "share_of_boots_above_1": round(sum(1 for a in boots if a > 1) / len(boots), 3),
           "buckets": buckets, "grid": [GRID[0], GRID[-1]]}
    json.dump(out, open(OUT, "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
