#!/usr/bin/env python3
"""P-0215: the called shots under the log score, beside Brier.

Good Judgment Open's FAQ (read 24 Oct 2026) defines Brier as the sum over every option of
(forecast - outcome)^2, so a binary 70% hit scores (1-0.7)^2 + (0-0.3)^2 = 0.18, the range is 0 to 2
and a coin flip scores 0.5. D-012 scored my shots one-sided, (p - hit)^2, where the coin is 0.25:
same ranking, half the number. The log score is -ln(p of what happened); Metaculus' baseline score
for a binary question is 100 * log2(p_outcome / 0.5), positive when better than the coin, and it
punishes a confident miss without limit where Brier caps it at 1 (or 2).

A shot: {"expect": kind, "p": stated probability that the verdict will be that kind}. Hit if the
recorded verdict equals the expected kind. Groups: by expected kind, by stated p, and the shots the
log score punishes hardest.
"""
import json
import math
import os
from collections import defaultdict

OUT = os.path.dirname(os.path.abspath(__file__))
raw = json.load(open("/Users/triton/PROTEUS/state/probes.json"))
probes = raw["items"] if isinstance(raw, dict) else raw   # {"next_id": n, "items": [...]}

rows = []
for p in probes:
    shot = p.get("shot")
    if not shot or not p.get("verdict") or p.get("status") != "done":
        continue
    prob = float(shot["p"])
    hit = p["verdict"] == shot["expect"]
    p_out = prob if hit else 1 - prob
    p_out = min(max(p_out, 1e-6), 1 - 1e-6)
    rows.append({
        "id": p["id"], "expect": shot["expect"], "verdict": p["verdict"], "p": prob, "hit": hit,
        "brier1": (prob - (1 if hit else 0)) ** 2,
        "brier_gjo": 2 * (prob - (1 if hit else 0)) ** 2,
        "log": -math.log(p_out),
        "baseline": 100 * math.log2(p_out / 0.5),
        "title": (p.get("title") or "")[:90],
    })

n = len(rows)


def mean(xs):
    return sum(xs) / len(xs) if xs else None


def summary(group):
    return {
        "n": len(group),
        "hit_rate": round(mean([r["hit"] for r in group]), 3),
        "mean_p": round(mean([r["p"] for r in group]), 3),
        "brier1": round(mean([r["brier1"] for r in group]), 4),
        "brier_gjo": round(mean([r["brier_gjo"] for r in group]), 4),
        "log": round(mean([r["log"] for r in group]), 4),
        "baseline": round(mean([r["baseline"] for r in group]), 1),
    }


by_kind = defaultdict(list)
for r in rows:
    by_kind[r["expect"]].append(r)
by_p = defaultdict(list)
for r in rows:
    by_p[r["p"]].append(r)

overall = summary(rows)
kinds = {k: summary(v) for k, v in by_kind.items()}
rank_brier = sorted(kinds, key=lambda k: kinds[k]["brier1"])
rank_log = sorted(kinds, key=lambda k: kinds[k]["log"])
# Constant forecasters for comparison: the coin, and "always works at the base rate".
base_rate = mean([r["verdict"] == "works" for r in rows])
const = []
for r in rows:
    hit = r["verdict"] == "works"
    p_out = base_rate if hit else 1 - base_rate
    const.append({"brier1": (base_rate - (1 if hit else 0)) ** 2, "log": -math.log(p_out)})
coin = {"brier1": 0.25, "log": math.log(2)}
hardest = sorted(rows, key=lambda r: -r["log"])[:8]
# Which shots change places: rank every shot by Brier and by log, count pairwise order flips.
by_b = sorted(rows, key=lambda r: r["brier1"])
by_l = sorted(rows, key=lambda r: r["log"])
pos_b = {r["id"]: i for i, r in enumerate(by_b)}
pos_l = {r["id"]: i for i, r in enumerate(by_l)}
flips = 0
pairs = 0
ids = [r["id"] for r in rows]
for i in range(len(ids)):
    for j in range(i + 1, len(ids)):
        pairs += 1
        if (pos_b[ids[i]] - pos_b[ids[j]]) * (pos_l[ids[i]] - pos_l[ids[j]]) < 0:
            flips += 1

result = {
    "scored_shots": n,
    "overall": overall,
    "by_expected_kind": kinds,
    "rank_by_brier": rank_brier,
    "rank_by_log": rank_log,
    "ranking_changes": rank_brier != rank_log,
    "by_stated_p": {str(k): summary(v) for k, v in sorted(by_p.items())},
    "constant_always_works_at_base_rate": {"base_rate": round(base_rate, 3), "brier1": round(mean([c["brier1"] for c in const]), 4), "log": round(mean([c["log"] for c in const]), 4)},
    "coin": coin,
    "pairwise_order_flips_between_rules": {"flips": flips, "pairs": pairs, "pct": round(100 * flips / pairs, 1) if pairs else None},
    "hardest_punished": [{k: r[k] for k in ("id", "expect", "verdict", "p", "log", "brier1", "title")} for r in hardest],
}
json.dump(result, open(OUT + "/results.json", "w"), indent=1)
print(json.dumps({k: v for k, v in result.items() if k != "hardest_punished"}, indent=1))
print("hardest punished:")
for r in hardest:
    print(" ", r["id"], r["expect"], "->", r["verdict"], "p", r["p"], "log", round(r["log"], 3), "brier", round(r["brier1"], 3), r["title"])
