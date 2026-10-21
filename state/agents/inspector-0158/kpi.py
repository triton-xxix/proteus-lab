"""P-0168: which 10-match team KPI best predicts the next 10 matches' points?

Soccermatics lesson 5 (Team KPIs) argues for tracking a shot-quality trend rather than points. football-data.co.uk
has shots on target (HST, AST) for every match in the nine leagues the Pitch covers. For each team and season, take
non-overlapping blocks: matches k..k+9 give the predictors (shots-on-target difference, goal difference, points,
all per game), matches k+10..k+19 give the target (points per game). Pearson r per predictor, pooled and per league.
"""
import csv
import io
import json
import statistics
import urllib.request
from collections import defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
LEAGUES = ["E0", "E1", "SP1", "D1", "I1", "F1", "N1", "P1", "SC0"]
SEASONS = ["2223", "2324", "2425", "2526"]


def fetch(div, s):
    url = f"https://www.football-data.co.uk/mmz4281/{s}/{div}.csv"
    raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "proteus-lab"}), timeout=30).read()
    return list(csv.DictReader(io.StringIO(raw.decode("latin-1"))))


def team_rows(rows):
    by = defaultdict(list)
    for r in rows:
        try:
            hg, ag, hst, ast = int(r["FTHG"]), int(r["FTAG"]), int(r["HST"]), int(r["AST"])
        except (KeyError, ValueError, TypeError):
            continue
        hp = 3 if hg > ag else 1 if hg == ag else 0
        ap = 3 if ag > hg else 1 if hg == ag else 0
        by[r["HomeTeam"]].append((hst - ast, hg - ag, hp))
        by[r["AwayTeam"]].append((ast - hst, ag - hg, ap))
    return by


def r(xs, ys):
    return statistics.correlation(xs, ys)


def main():
    pooled = defaultdict(list)
    per_league = {}
    for div in LEAGUES:
        lg = defaultdict(list)
        for s in SEASONS:
            try:
                rows = fetch(div, s)
            except Exception as e:  # noqa: BLE001
                print(div, s, "fetch failed", e)
                continue
            for team, ms in team_rows(rows).items():
                for k in range(0, len(ms) - 19, 10):
                    a, b = ms[k:k + 10], ms[k + 10:k + 20]
                    row = {"sot": sum(m[0] for m in a) / 10, "gd": sum(m[1] for m in a) / 10,
                           "ppg": sum(m[2] for m in a) / 10, "next": sum(m[2] for m in b) / 10}
                    for key, v in row.items():
                        lg[key].append(v)
                        pooled[key].append(v)
        per_league[div] = {"blocks": len(lg["next"]),
                           **{p: round(r(lg[p], lg["next"]), 3) for p in ("sot", "gd", "ppg")}}
        print(div, per_league[div])
    res = {"blocks": len(pooled["next"]),
           "r": {p: round(r(pooled[p], pooled["next"]), 4) for p in ("sot", "gd", "ppg")},
           "leagues_where_sot_beats_gd": sum(v["sot"] > v["gd"] for v in per_league.values()),
           "leagues_where_sot_beats_ppg": sum(v["sot"] > v["ppg"] for v in per_league.values()),
           "per_league": per_league}
    # bootstrap the pooled sot-minus-gd gap by resampling blocks
    import random
    rng = random.Random(16)
    n = res["blocks"]
    gaps = []
    for _ in range(1000):
        idx = [rng.randrange(n) for _ in range(n)]
        nx = [pooled["next"][i] for i in idx]
        gaps.append(r([pooled["sot"][i] for i in idx], nx) - r([pooled["gd"][i] for i in idx], nx))
    gaps.sort()
    res["sot_minus_gd_r_95ci"] = [round(gaps[25], 4), round(gaps[974], 4)]
    print(json.dumps({k: v for k, v in res.items() if k != "per_league"}, indent=1))
    (OUT / "result.json").write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
