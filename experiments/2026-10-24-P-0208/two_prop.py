#!/usr/bin/env python3
"""P-0208: two-proportion test on Lichess accept rates by opponent rating.

OpenIntro Statistics 4e, section 6.2 (difference of two proportions): under H0 p1 = p2 the
success-failure condition and the standard error both use the pooled proportion, and each group
needs at least 10 expected successes and 10 expected failures. This script checks that condition
on games/lichess/CHALLENGES.csv split at an opponent rating of 1750, runs the pooled z-test
anyway, and puts Fisher's exact test (hypergeometric, no scipy) beside it.

Stdlib only. Writes results.json beside this file.
"""
import csv
import json
import math
import os
import sys

ROOT = "/Users/triton/PROTEUS"
CSV = ROOT + "/games/lichess/CHALLENGES.csv"
HERE = os.path.dirname(os.path.abspath(__file__))
SPLIT = 1750


def norm_sf(z):
    """Upper tail of the standard normal."""
    return 0.5 * math.erfc(z / math.sqrt(2))


def fisher_two_sided(a, b, c, d):
    """Two-sided Fisher exact p for the table [[a, b], [c, d]]: sum of hypergeometric
    probabilities of every table (same margins) no more likely than the observed one."""
    r1, r2 = a + b, c + d
    c1 = a + c
    n = r1 + r2
    denom = math.comb(n, c1)

    def prob(x):
        return math.comb(r1, x) * math.comb(r2, c1 - x) / denom

    p_obs = prob(a)
    lo = max(0, c1 - r2)
    hi = min(r1, c1)
    total = 0.0
    for x in range(lo, hi + 1):
        p = prob(x)
        if p <= p_obs * (1 + 1e-9):
            total += p
    return min(1.0, total), p_obs


def main():
    groups = {"weak": {"n": 0, "accepted": 0}, "strong": {"n": 0, "accepted": 0}}
    verdicts = {}
    with open(CSV, newline="") as f:
        for row in csv.DictReader(f):
            try:
                rating = int(row["opp_rating"])
            except (TypeError, ValueError):
                continue
            g = "weak" if rating < SPLIT else "strong"
            groups[g]["n"] += 1
            v = row["verdict"].strip()
            verdicts[v] = verdicts.get(v, 0) + 1
            if v == "accepted":
                groups[g]["accepted"] += 1

    n1, a1 = groups["weak"]["n"], groups["weak"]["accepted"]
    n2, a2 = groups["strong"]["n"], groups["strong"]["accepted"]
    p1, p2 = a1 / n1, a2 / n2
    pooled = (a1 + a2) / (n1 + n2)

    # Success-failure under H0, pooled proportion (OpenIntro 6.2.3).
    expected = {
        "weak_successes": n1 * pooled,
        "weak_failures": n1 * (1 - pooled),
        "strong_successes": n2 * pooled,
        "strong_failures": n2 * (1 - pooled),
    }
    condition_met = all(v >= 10 for v in expected.values())

    se = math.sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n2))
    z = (p1 - p2) / se
    p_z = 2 * norm_sf(abs(z))

    # Confidence interval uses the unpooled SE (OpenIntro 6.2.1).
    se_ci = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    ci = [(p1 - p2) - 1.96 * se_ci, (p1 - p2) + 1.96 * se_ci]

    p_fisher, p_table = fisher_two_sided(a1, n1 - a1, a2, n2 - a2)

    out = {
        "probe": "P-0208",
        "source": CSV,
        "split_rating": SPLIT,
        "verdict_counts": verdicts,
        "weak": {"n": n1, "accepted": a1, "rate": p1},
        "strong": {"n": n2, "accepted": a2, "rate": p2},
        "difference_weak_minus_strong": p1 - p2,
        "pooled_proportion": pooled,
        "expected_under_h0": expected,
        "success_failure_condition_met": condition_met,
        "z_pooled": z,
        "p_two_sided_z": p_z,
        "ci95_unpooled": ci,
        "fisher_exact_p_two_sided": p_fisher,
        "fisher_observed_table_prob": p_table,
        "book_allows_z_test": condition_met,
    }
    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
