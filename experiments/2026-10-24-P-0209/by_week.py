#!/usr/bin/env python3
"""P-0209: Lichess accept rate by ISO week, chi-square test of homogeneity (OpenIntro 4e, 6.4).

Deepen of P-0208, which found rating was the wrong axis. Buckets every challenge in
games/lichess/CHALLENGES.csv by ISO week, builds a weeks x {accepted, not} table, checks the
expected-count condition (OpenIntro: at least 5 expected in each cell), computes the chi-square
statistic, df and p (stdlib survival function, no scipy), and the cell that contributes most.
Run twice: denominator = every row, and denominator = declined plus accepted only (drops the
bot-side caps "refused 400", rate limits "refused 429" and "no answer").

Writes results.json beside this file.
"""
import csv
import datetime as dt
import json
import math
import os
import sys

ROOT = "/Users/triton/PROTEUS"
CSV = ROOT + "/games/lichess/CHALLENGES.csv"
HERE = os.path.dirname(os.path.abspath(__file__))


def chi2_sf(x, df):
    """Survival function of chi-square with integer df, closed forms for even and odd df."""
    if x <= 0:
        return 1.0
    if df % 2 == 0:
        m = df // 2
        term, total = 1.0, 1.0
        for i in range(1, m):
            term *= (x / 2) / i
            total += term
        return math.exp(-x / 2) * total
    m = (df - 1) // 2
    total = math.erfc(math.sqrt(x / 2))
    if m > 0:
        term = 1.0
        s = 1.0
        for i in range(1, m):
            term *= x / (2 * i + 1)
            s += term
        total += math.sqrt(2 * x / math.pi) * math.exp(-x / 2) * s
    return min(1.0, total)


def homogeneity(table):
    """table: dict week -> [accepted, not]. Returns stats dict."""
    weeks = sorted(table)
    rows = [table[w] for w in weeks]
    col_tot = [sum(r[j] for r in rows) for j in range(2)]
    n = sum(col_tot)
    stat = 0.0
    expected = {}
    contrib = {}
    for w, r in zip(weeks, rows):
        rt = sum(r)
        for j, label in enumerate(("accepted", "not")):
            e = rt * col_tot[j] / n
            o = r[j]
            c = (o - e) ** 2 / e if e > 0 else 0.0
            expected[f"{w}:{label}"] = e
            contrib[f"{w}:{label}"] = c
            stat += c
    df = (len(weeks) - 1) * 1
    p = chi2_sf(stat, df)
    top = max(contrib, key=contrib.get)
    return {
        "weeks": {w: {"accepted": table[w][0], "not": table[w][1],
                      "rate": table[w][0] / sum(table[w])} for w in weeks},
        "n": n,
        "expected": expected,
        "min_expected": min(expected.values()),
        "condition_met_5_per_cell": min(expected.values()) >= 5,
        "chi_square": stat,
        "df": df,
        "p": p,
        "largest_contribution": {"cell": top, "value": contrib[top]},
    }


def main():
    all_rows = {}
    decided = {}
    verdicts = {}
    with open(CSV, newline="") as f:
        for row in csv.DictReader(f):
            try:
                when = dt.datetime.strptime(row["utc"][:19], "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                continue
            week = "%d-W%02d" % when.isocalendar()[:2]
            v = row["verdict"].strip()
            verdicts[v] = verdicts.get(v, 0) + 1
            acc = 1 if v == "accepted" else 0
            all_rows.setdefault(week, [0, 0])[0 if acc else 1] += 1
            if v in ("accepted", "declined"):
                decided.setdefault(week, [0, 0])[0 if acc else 1] += 1

    out = {
        "probe": "P-0209",
        "source": CSV,
        "verdict_counts": verdicts,
        "all_rows": homogeneity(all_rows),
        "declined_plus_accepted": homogeneity(decided),
    }
    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
