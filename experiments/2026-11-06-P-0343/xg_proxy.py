#!/usr/bin/env python3
"""Does a team's rolling shots on target predict its next-match goals better than its rolling goals?

Data: the Pitch's cached football-data CSVs, nine leagues, seasons 2223 to 2526; the live 2627 season is not
read at all. Features use only earlier matches in the same season, last N=10 for that team, and
need all 10. One row per team per match, with an is_home flag. Fit OLS on matches before 1 Jul 2025, test on the
2025-26 season. Stdlib only.
"""
import csv
import json
import math
import random
from collections import defaultdict, deque
from datetime import datetime
from pathlib import Path

CACHE = Path("/Users/triton/PROTEUS/pitch/cache")
LEAGUES = ["E0", "E1", "SP1", "D1", "I1", "F1", "N1", "P1", "SC0"]
SEASONS = ["2223", "2324", "2425", "2526"]
N = 10
SPLIT = datetime(2025, 7, 1)


def parse_date(s):
    for f in ("%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(s, f)
        except ValueError:
            pass
    return None


def rows():
    out = []
    for lg in LEAGUES:
        for season in SEASONS:
            path = CACHE / f"{lg}-{season}.csv"
            if not path.exists():
                continue
            with open(path, newline="", encoding="utf-8-sig", errors="replace") as f:
                matches = []
                for r in csv.DictReader(f):
                    try:
                        m = (parse_date(r["Date"]), r["HomeTeam"], r["AwayTeam"], int(r["FTHG"]), int(r["FTAG"]),
                             int(r["HST"]), int(r["AST"]), int(r["HS"]), int(r["AS"]))
                    except (KeyError, ValueError, TypeError):
                        continue
                    if m[0]:
                        matches.append(m)
            matches.sort(key=lambda m: m[0])
            hist = defaultdict(lambda: deque(maxlen=N))
            for d, h, a, fh, fa, hst, ast, hs, as_ in matches:
                for team, is_home, g, st, sh in ((h, 1, fh, hst, hs), (a, 0, fa, ast, as_)):
                    q = hist[team]
                    if len(q) == N:
                        out.append({
                            "date": d, "league": lg, "y": g, "home": is_home,
                            "goals": sum(x[0] for x in q) / N,
                            "sot": sum(x[1] for x in q) / N,
                            "shots": sum(x[2] for x in q) / N,
                        })
                hist[h].append((fh, hst, hs))
                hist[a].append((fa, ast, as_))
    return out


def solve(A, b):
    n = len(A)
    M = [row[:] + [v] for row, v in zip(A, b)]
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[p] = M[p], M[i]
        for r in range(n):
            if r != i:
                f = M[r][i] / M[i][i]
                for c in range(i, n + 1):
                    M[r][c] -= f * M[i][c]
    return [M[i][n] / M[i][i] for i in range(n)]


def fit(data, feats):
    k = len(feats) + 2
    A = [[0.0] * k for _ in range(k)]
    b = [0.0] * k
    for r in data:
        x = [1.0, r["home"]] + [r[f] for f in feats]
        for i in range(k):
            b[i] += x[i] * r["y"]
            for j in range(k):
                A[i][j] += x[i] * x[j]
    return solve(A, b)


def errs(data, feats, beta):
    return [(r["y"] - sum(c * v for c, v in zip(beta, [1.0, r["home"]] + [r[f] for f in feats]))) ** 2 for r in data]


def main():
    data = rows()
    train = [r for r in data if r["date"] < SPLIT]
    test = [r for r in data if r["date"] >= SPLIT]
    models = {"home only": [], "goals": ["goals"], "sot": ["sot"], "shots": ["shots"], "goals+sot": ["goals", "sot"]}
    res = {}
    e = {}
    for name, feats in models.items():
        beta = fit(train, feats)
        e[name] = errs(test, feats, beta)
        res[name] = {"mse": round(sum(e[name]) / len(test), 5), "beta": [round(b, 4) for b in beta]}

    # Paired bootstrap of (goals - sot) MSE, resampling by match row
    random.seed(20261106)
    diffs = [a - b for a, b in zip(e["goals"], e["sot"])]
    n = len(diffs)
    mean = sum(diffs) / n
    sd = math.sqrt(sum((d - mean) ** 2 for d in diffs) / (n - 1))
    boots = sorted(sum(diffs[random.randrange(n)] for _ in range(n)) / n for _ in range(500))

    per_league = {}
    for lg in LEAGUES:
        idx = [i for i, r in enumerate(test) if r["league"] == lg]
        if idx:
            d = [diffs[i] for i in idx]
            per_league[lg] = {"n": len(idx), "goals_minus_sot_mse": round(sum(d) / len(d), 5)}

    out = {
        "train_rows": len(train), "test_rows": len(test), "N": N, "models": res,
        "goals_minus_sot": {"mean": round(mean, 5), "se": round(sd / math.sqrt(n), 5),
                            "boot_5": round(boots[25], 5), "boot_95": round(boots[474], 5),
                            "pct_of_goals_mse": round(100 * mean / res["goals"]["mse"], 3)},
        "skill_vs_home_only_pct": {k: round(100 * (res["home only"]["mse"] - v["mse"]) / res["home only"]["mse"], 3) for k, v in res.items()},
        "per_league": per_league,
        "leagues_sot_better": sum(1 for v in per_league.values() if v["goals_minus_sot_mse"] > 0),
    }
    Path(__file__).with_name("results.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
