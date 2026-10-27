"""P-0237: win rate against entry price on football closing odds.

Question (harvest H-0424): do heavy favourites win most often yet return at or below zero
at closing odds? Every outcome (home, draw, away) of every match in pitch/cache/ (nine
leagues, five seasons from football-data) is a one-unit back bet at the closing price,
bucketed by that price. Two books: Pinnacle closing (PSC*, the sharp line) and the market
average closing (AvgC*, what a punter shopping nowhere gets).
"""
import csv, glob, json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = "/Users/triton/PROTEUS/pitch/cache/"
BUCKETS = [(1.0, 1.3), (1.3, 1.5), (1.5, 1.8), (1.8, 2.2), (2.2, 3.0), (3.0, 5.0), (5.0, 10.0), (10.0, 1000.0)]
BOOKS = {"pinnacle": ("PSCH", "PSCD", "PSCA"), "average": ("AvgCH", "AvgCD", "AvgCA")}


def num(x):
    try:
        v = float(x)
        return v if v > 1.0 else None
    except (TypeError, ValueError):
        return None


rows = []
for path in sorted(glob.glob(CACHE + "*-*.csv")):
    name = os.path.basename(path)
    if name.startswith("fixtures"):
        continue
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f):
            if r.get("FTR") in ("H", "D", "A"):
                r["_file"] = name
                rows.append(r)

out = {"matches": len(rows), "books": {}}
for book, cols in BOOKS.items():
    stats = {b: {"n": 0, "wins": 0, "pnl": 0.0, "implied": 0.0} for b in BUCKETS}
    fav = {"n": 0, "wins": 0, "pnl": 0.0}
    used = 0
    for r in rows:
        odds = [num(r.get(c)) for c in cols]
        if None in odds:
            continue
        used += 1
        for side, o in zip("HDA", odds):
            won = r["FTR"] == side
            for b in BUCKETS:
                if b[0] <= o < b[1]:
                    s = stats[b]
                    s["n"] += 1
                    s["wins"] += won
                    s["pnl"] += (o - 1) if won else -1
                    s["implied"] += 1 / o
        o_min = min(odds[0], odds[2])
        side = "H" if odds[0] <= odds[2] else "A"
        fav["n"] += 1
        won = r["FTR"] == side
        fav["wins"] += won
        fav["pnl"] += (o_min - 1) if won else -1
    table = []
    for b in BUCKETS:
        s = stats[b]
        if not s["n"]:
            continue
        roi = s["pnl"] / s["n"]
        # standard error of the per-bet return, approximated from the win rate and mean price
        p = s["wins"] / s["n"]
        mean_o = s["n"] / s["implied"]
        se = math.sqrt(p * (1 - p)) * mean_o / math.sqrt(s["n"])
        table.append({"bucket": "%.1f-%.1f" % b, "bets": s["n"], "win_rate": round(p, 4),
                      "implied": round(s["implied"] / s["n"], 4), "roi": round(roi, 4), "roi_se": round(se, 4)})
    out["books"][book] = {"matches_with_odds": used, "buckets": table,
                          "favourite_every_match": {"bets": fav["n"], "win_rate": round(fav["wins"] / fav["n"], 4),
                                                    "roi": round(fav["pnl"] / fav["n"], 4)}}

json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
for book, d in out["books"].items():
    print(book, "matches", d["matches_with_odds"], "favourite every match", d["favourite_every_match"])
    for t in d["buckets"]:
        print("  %-11s bets %6d  win %.3f  implied %.3f  roi %+.4f  se %.4f" % (
            t["bucket"], t["bets"], t["win_rate"], t["implied"], t["roi"], t["roi_se"]))
