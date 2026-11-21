"""P-0526: are UEFA Nations League games drawier than qualifiers, and is the last group matchday
drawier still? From sandbox/intl-results.csv (martj42 international results), no network.

Nations League group stage = NL matches from June to November of an even year 2018-2026 (finals and
promotion play-offs, in March and June of odd years, are left out). A team's matchday is the rank
of its date within that edition; a match counts as last-matchday if it is either side's last.
Qualifiers and friendlies are restricted to matches where both sides played in the NL (UEFA).
"""
import csv
import json
import math
import os
from collections import defaultdict

SRC = "/Users/triton/PROTEUS/sandbox/intl-results.csv"
HERE = os.path.dirname(os.path.abspath(__file__))
rows = [r for r in csv.DictReader(open(SRC)) if r["home_score"] not in ("", "NA")]

nl = [r for r in rows if r["tournament"] == "UEFA Nations League"]
uefa = {r["home_team"] for r in nl} | {r["away_team"] for r in nl}
group = [r for r in nl if int(r["date"][:4]) % 2 == 0 and 6 <= int(r["date"][5:7]) <= 11 and r["date"] >= "2018-09"]

by_team = defaultdict(list)
for r in group:
    ed = r["date"][:4]
    by_team[(ed, r["home_team"])].append(r["date"])
    by_team[(ed, r["away_team"])].append(r["date"])
for k in by_team:
    by_team[k].sort()


def md(r, side):
    dates = by_team[(r["date"][:4], r[side])]
    return dates.index(r["date"]) + 1, len(dates)


def draw(r):
    return r["home_score"] == r["away_score"]


def rate(rs):
    n = len(rs)
    d = sum(draw(r) for r in rs)
    p = d / n if n else float("nan")
    se = math.sqrt(p * (1 - p) / n) if n else float("nan")
    return {"n": n, "draws": d, "rate": round(100 * p, 1), "se_pts": round(100 * se, 1)}


table = {}
table["NL group stage 2018-26"] = rate(group)
by_md = defaultdict(list)
last, earlier = [], []
for r in group:
    h, hn = md(r, "home_team")
    a, an = md(r, "away_team")
    by_md[min(h, a)].append(r)
    (last if (h == hn or a == an) else earlier).append(r)
table["NL last matchday (either side's last)"] = rate(last)
table["NL earlier matchdays"] = rate(earlier)
for k in sorted(by_md):
    table["NL matchday %d" % k] = rate(by_md[k])
table["NL finals and play-offs"] = rate([r for r in nl if r not in group])
for label, t in (("World Cup qualifiers, UEFA v UEFA", "FIFA World Cup qualification"),
                 ("Euro qualifiers", "UEFA Euro qualification")):
    table[label + " 2018-26"] = rate([r for r in rows if r["tournament"] == t and "2018" <= r["date"][:4] <= "2026"
                                      and r["home_team"] in uefa and r["away_team"] in uefa])
table["Friendlies, UEFA v UEFA 2018-26"] = rate([r for r in rows if r["tournament"] == "Friendly" and "2018" <= r["date"][:4] <= "2026"
                                                 and r["home_team"] in uefa and r["away_team"] in uefa])
table["All internationals 2010-22 (P-0518 base)"] = rate([r for r in rows if "2010" <= r["date"][:4] <= "2022" and r["tournament"] != "Friendly"])
out = {"source": SRC, "last_date": max(r["date"] for r in rows), "table": table}
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
for k, v in table.items():
    print("%-42s n %5d  draws %4d  %5.1f%% (se %.1f)" % (k, v["n"], v["draws"], v["rate"], v["se_pts"]))
print("last date in file", out["last_date"])
