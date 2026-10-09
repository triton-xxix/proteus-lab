#!/usr/bin/env python3
"""Scores the two-week Lichess test registered in games/lichess/EXPERIMENT.md (9 Oct 2026, DUE D-010).

    chess-experiment.py        print the three readings so far; safe to run any night

Reads only GAMES.csv and CHALLENGES.csv. Writes nothing; the verdict goes into the run log and
EXPERIMENT.md by hand on 23 Oct, so the rules in that file stay untouched until then.
"""
import csv
import math
import os

ROOT = "/Users/triton/PROTEUS"
GAMES = ROOT + "/games/lichess/GAMES.csv"
CHALLENGES = ROOT + "/games/lichess/CHALLENGES.csv"
SCORE = {"win": 1.0, "draw": 0.5, "loss": 0.0}


def rows(path):
    return list(csv.DictReader(open(path))) if os.path.exists(path) else []


def expected(mine, opp):
    return 1 / (1 + 10 ** ((opp - mine) / 400))


def mean_se(xs):
    if not xs:
        return float("nan"), float("nan")
    m = sum(xs) / len(xs)
    if len(xs) < 2:
        return m, float("nan")
    var = sum((x - m) ** 2 for x in xs) / (len(xs) - 1)
    return m, math.sqrt(var / len(xs))


def line(label, games):
    edge = [g["edge"] for g in games]
    pts = [g["pts"] for g in games]
    e, ese = mean_se(edge)
    p, pse = mean_se(pts)
    return f"  {label:<18} n {len(games):>3}  edge {e:+.3f} (se {ese:.3f})  points/game {p:+.1f} (se {pse:.1f})"


def band(g):
    gap = g["opp"] - g["mine"]
    return "300+ below" if gap < -300 else ("300+ above" if gap > 300 else "within 300")


def job(utc):
    hour = int(utc[11:13])
    return "morning" if 4 <= hour < 12 else "nightly"


def main():
    games = []
    for r in rows(GAMES):
        if not r.get("think_s") or not r["my_rating_before"] or not r["my_rating_after"]:
            continue
        mine, opp = int(r["my_rating_before"]), int(r["opp_rating"])
        games.append({**r, "mine": mine, "opp": opp, "think": float(r["think_s"]),
                      "edge": SCORE[r["result"]] - expected(mine, opp),
                      "pts": int(r["my_rating_after"]) - mine, "plies": int(r["moves"] or 0)})
    print(f"Lichess test (EXPERIMENT.md, scored 23 Oct 2026): {len(games)} games under the rules")

    print("1. Think time")
    arms = {t: [g for g in games if g["think"] == t] for t in sorted({g["think"] for g in games})}
    for t, gs in arms.items():
        print(line(f"{t} s a move", gs))
    if 0.3 in arms and 1.0 in arms and len(arms[0.3]) > 1 and len(arms[1.0]) > 1:
        a, ase = mean_se([g["edge"] for g in arms[1.0]])
        b, bse = mean_se([g["edge"] for g in arms[0.3]])
        diff, se = a - b, math.sqrt(ase ** 2 + bse ** 2)
        print(f"  1.0 s minus 0.3 s: edge {diff:+.3f}, se {se:.3f}, {diff / se if se else float('nan'):+.1f} se")

    print("2. Opponent band")
    for b in ("300+ below", "within 300", "300+ above"):
        print(line(b, [g for g in games if band(g) == b]))
    ch = rows(CHALLENGES)
    for j in ("morning", "nightly"):
        cs = [c for c in ch if job(c["utc"]) == j]
        bad = [c for c in cs if c["verdict"] != "accepted"]
        rate = len(bad) / len(cs) if cs else float("nan")
        reasons = {}
        for c in bad:
            k = c["detail"] or c["verdict"]
            reasons[k[:30]] = reasons.get(k[:30], 0) + 1
        top = ", ".join(f"{k} {n}" for k, n in sorted(reasons.items(), key=lambda x: -x[1])[:4])
        print(f"  {j:<8} challenges {len(cs):>3}, refused or unanswered {len(bad):>3} ({rate:.0%}); {top}")

    print("3. Draws")
    draws = [g for g in games if g["result"] == "draw"]
    wins = [g for g in games if g["result"] == "win"]
    for g in draws:
        print(f"  {g['finished_utc'][:16]} v {g['opponent']} ({g['opp']}, {band(g)}): {g['draw_kind'] or '?'}, "
              f"{g['plies']} moves, {g['pts']:+d}")
    short_weak = sum(-g["pts"] for g in draws if g["plies"] < 30 and g["opp"] < g["mine"] and g["pts"] < 0)
    won = sum(g["pts"] for g in wins if g["pts"] > 0)
    print(f"  short draws v weaker bots cost {short_weak} points; wins earned {won}"
          f"{' (' + format(short_weak / won, '.0%') + ')' if won else ''}; the rule's line is 10%")


if __name__ == "__main__":
    main()
