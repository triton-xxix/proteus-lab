#!/usr/bin/env python3
"""P-0130 part one: do referees differ beyond chance in cards a game and home-win rate?

Data: the Pitch desk's football-data cache (pitch/cache/<DIV>-<season>.csv), divisions E0, E1, SC0,
seasons 2022-23 on. Columns Referee, HY AY HR AR (yellows and reds), FTR (H/D/A).
Statistic: between-referee sum of squares of the per-referee mean, weighted by games (one-way ANOVA
numerator), referees with at least MIN games. Permutation test: shuffle the referee labels across
matches within each division-season (so league and season effects cannot masquerade as referee
effects), 4000 draws, p = share of draws at or above the observed statistic.
Usage: referees.py OUT.json
"""
import csv
import json
import os
import random
import sys
from collections import defaultdict

CACHE = "/Users/triton/PROTEUS/pitch/cache/"
DIVS = {"E0", "E1", "SC0"}
MIN_GAMES = 20
DRAWS = 4000
random.seed(13)


def load():
    rows = []
    for f in sorted(os.listdir(CACHE)):
        if not f.endswith(".csv") or "-" not in f:
            continue
        div, season = f[:-4].split("-", 1)
        if div not in DIVS or not season.isdigit() or int(season[:2]) < 22:
            continue
        with open(CACHE + f, newline="", encoding="utf-8", errors="replace") as fh:
            for r in csv.DictReader(fh):
                ref = (r.get("Referee") or "").strip()
                if not ref or not r.get("FTR"):
                    continue
                try:
                    cards = sum(int(r.get(k) or 0) for k in ("HY", "AY", "HR", "AR"))
                    hbias = int(r.get("HY") or 0) + int(r.get("HR") or 0) - int(r.get("AY") or 0) - int(r.get("AR") or 0)
                except ValueError:
                    continue
                rows.append({"grp": div + "-" + season, "ref": ref, "cards": cards,
                             "hbias": hbias, "home": 1 if r["FTR"] == "H" else 0,
                             "over25": 1 if (int(r.get("FTHG") or 0) + int(r.get("FTAG") or 0)) > 2 else 0})
    return rows


def between_ss(values, labels, keep):
    tot = defaultdict(float)
    cnt = defaultdict(int)
    for v, l in zip(values, labels):
        if l in keep:
            tot[l] += v
            cnt[l] += 1
    n = sum(cnt.values())
    if n == 0:
        return 0.0
    grand = sum(tot.values()) / n
    return sum(cnt[l] * (tot[l] / cnt[l] - grand) ** 2 for l in cnt)


def perm_test(rows, key):
    labels = [r["ref"] for r in rows]
    values = [r[key] for r in rows]
    cnt = defaultdict(int)
    for l in labels:
        cnt[l] += 1
    keep = {l for l, c in cnt.items() if c >= MIN_GAMES}
    obs = between_ss(values, labels, keep)
    # shuffle labels within each division-season group
    groups = defaultdict(list)
    for i, r in enumerate(rows):
        groups[r["grp"]].append(i)
    hits = 0
    perm = list(labels)
    for _ in range(DRAWS):
        for idx in groups.values():
            sub = [labels[i] for i in idx]
            random.shuffle(sub)
            for i, l in zip(idx, sub):
                perm[i] = l
        if between_ss(values, perm, keep) >= obs:
            hits += 1
    means = {l: round(sum(v for v, lab in zip(values, labels) if lab == l) / cnt[l], 3) for l in keep}
    return {"stat": round(obs, 3), "p": round(hits / DRAWS, 4), "referees": len(keep),
            "games": sum(cnt[l] for l in keep), "top": sorted(means.items(), key=lambda x: -x[1])[:5],
            "bottom": sorted(means.items(), key=lambda x: x[1])[:5]}


def main():
    rows = load()
    out = {"matches": len(rows), "divisions": sorted({r["grp"][:3].rstrip("-") for r in rows}),
           "seasons": sorted({r["grp"].split("-")[1] for r in rows}), "min_games": MIN_GAMES, "draws": DRAWS}
    for key in ("cards", "hbias", "home", "over25"):
        out[key] = perm_test(rows, key)
        print("%-7s referees %3d games %5d  stat %8.3f  p %.4f" % (
            key, out[key]["referees"], out[key]["games"], out[key]["stat"], out[key]["p"]))
        print("   top", out[key]["top"])
        print("   bottom", out[key]["bottom"])
    json.dump(out, open(sys.argv[1], "w"), indent=1)


if __name__ == "__main__":
    main()
