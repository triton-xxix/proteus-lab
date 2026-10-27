"""P-0238: does the closing price drift toward the Pitch model's side?

For every committed prediction whose match is played and in pitch/cache/ (football-data), take
the market average before the close (AvgH/D/A, collected Friday or Tuesday afternoon per
notes.txt) and at the close (AvgCH/D/A), both de-margined. The model's side is the outcome with
the largest p_model minus pre-close market probability. A hit is the close probability of that
side above its pre-close probability. Control: the same count for a random side, 10,000 draws.
"""
import csv, glob, json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = "/Users/triton/PROTEUS/pitch/cache/"
PRED = "/Users/triton/PROTEUS/pitch/predictions.csv"


def demargin(row, cols):
    try:
        o = [float(row[c]) for c in cols]
    except (KeyError, TypeError, ValueError):
        return None
    if min(o) <= 1:
        return None
    inv = [1 / x for x in o]
    s = sum(inv)
    return [x / s for x in inv]


def ddmmyyyy(s):
    d, m, y = s.split("/")
    return "%s-%s-%s" % (y if len(y) == 4 else "20" + y, m, d)


games = {}
for path in glob.glob(CACHE + "*-2627.csv"):
    div = os.path.basename(path).split("-")[0]
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f):
            if r.get("FTR") not in ("H", "D", "A"):
                continue
            games[(div, ddmmyyyy(r["Date"]), r["HomeTeam"], r["AwayTeam"])] = r

rows, missing = [], 0
with open(PRED) as f:
    for p in csv.DictReader(f):
        key = (p["competition"], p["kickoff_utc"][:10], p["home"], p["away"])
        g = games.get(key)
        if not g:
            missing += 1
            continue
        pre = demargin(g, ("AvgH", "AvgD", "AvgA"))
        close = demargin(g, ("AvgCH", "AvgCD", "AvgCA"))
        if not pre or not close:
            missing += 1
            continue
        model = [float(p["p_home"]), float(p["p_draw"]), float(p["p_away"])]
        edge = [m - q for m, q in zip(model, pre)]
        side = max(range(3), key=lambda i: edge[i])
        moves = [c - q for c, q in zip(close, pre)]
        rows.append({"id": p["id"], "side": "HDA"[side], "edge": round(edge[side], 4),
                     "move": round(moves[side], 4), "moves": moves})

n = len(rows)
hits = sum(r["move"] > 0 for r in rows)
mean_move = sum(r["move"] for r in rows) / n if n else 0
rng = random.Random(238)
ctrl = []
for _ in range(10000):
    ctrl.append(sum(r["moves"][rng.randrange(3)] > 0 for r in rows))
p = (sum(c >= hits for c in ctrl) + 1) / (len(ctrl) + 1)
big = [r for r in rows if r["edge"] >= 0.05]
out = {"matched": n, "unmatched": missing, "hits": hits, "hit_rate": round(hits / n, 3) if n else None,
       "random_side_mean_hits": round(sum(ctrl) / len(ctrl), 2), "p_vs_random": round(p, 4),
       "mean_prob_move_on_model_side": round(mean_move, 5),
       "edge_5pts_plus": {"n": len(big), "hits": sum(r["move"] > 0 for r in big),
                          "mean_move": round(sum(r["move"] for r in big) / len(big), 5) if big else None},
       "rows": [{k: v for k, v in r.items() if k != "moves"} for r in rows]}
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print({k: v for k, v in out.items() if k != "rows"})
