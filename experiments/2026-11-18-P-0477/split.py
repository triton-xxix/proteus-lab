#!/usr/bin/env python3
"""P-0477: the exchange book's Brier gap, split by how the call was made.

Reads exchange/BOOK.csv (read-only). A counted row has an outcome, my Brier
and the market's Brier. "model" rows are the Munich daily-high markets, called
from a weather model with no web search; "search" rows are everything else,
called from public sources. Prints and saves n, mean me-minus-market, its
standard error, and the same with each group's worst row removed.
"""
import csv
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = "/Users/triton/PROTEUS/exchange/BOOK.csv"


def stats(d):
    n = len(d)
    if not n:
        return {"n": 0}
    m = sum(d) / n
    se = math.sqrt(sum((x - m) ** 2 for x in d) / (n - 1) / n) if n > 1 else None
    trimmed = sorted(d)[:-1]
    return {"n": n, "mean_me_minus_market": round(m, 4), "se": round(se, 4) if se else None,
            "worse_than_market": sum(1 for x in d if x > 0),
            "mean_without_worst_row": round(sum(trimmed) / len(trimmed), 4) if trimmed else None}


groups = {"model": [], "search": []}
detail = {"model": [], "search": []}
uncounted = {"model": 0, "search": 0}
my = {"model": [], "search": []}
mk = {"model": [], "search": []}
with open(BOOK, newline="") as f:
    for r in csv.DictReader(f):
        g = "model" if r["market"].strip() == "Highest Temperature" else "search"
        if not r["outcome"] or not r["brier"] or not r["market_brier"]:
            uncounted[g] += 1
            continue
        b, mb = float(r["brier"]), float(r["market_brier"])
        groups[g].append(b - mb)
        my[g].append(b)
        mk[g].append(mb)
        detail[g].append({"id": r["id"], "event": r["event"], "contract": r["contract"],
                          "p": float(r["p"]), "outcome": r["outcome"], "diff": round(b - mb, 4)})

out = {"book": BOOK, "uncounted_rows": uncounted}
for g in groups:
    s = stats(groups[g])
    if s["n"]:
        s["my_brier"] = round(sum(my[g]) / s["n"], 4)
        s["market_brier"] = round(sum(mk[g]) / s["n"], 4)
        s["worst_rows"] = sorted(detail[g], key=lambda x: -x["diff"])[:3]
    out[g] = s
out["all"] = stats(groups["model"] + groups["search"])
# the Munich half again, by whether the degree I called came in
for res in ("winner", "loser"):
    rows = [x for x in detail["model"] if x["outcome"] == res]
    s = stats([x["diff"] for x in rows])
    if rows:
        s["mean_my_p"] = round(sum(x["p"] for x in rows) / len(rows), 3)
    out["model_" + res] = s
with open(os.path.join(HERE, "results.json"), "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1))
