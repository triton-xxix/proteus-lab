#!/usr/bin/env python3
"""P-0135 leg 2, 13 Oct 2026 18:0x BST: tonight's 8 Championship fixtures, the commit-time line v about
1.7 to 2 h before kick-off (snapshot "ko-1h45" in P-0129's snapshots.json), set beside the model's
probabilities in pitch/PREDICTIONS.csv. No judgement-book rows and no bets tonight, so the question is
narrower: after commit, did the market move toward the model's leans or away? Read-only."""
import csv, json

OUT = "/Users/triton/PROTEUS/experiments/2026-10-13-P-0135/"
snap = [s for s in json.load(open("/Users/triton/PROTEUS/experiments/2026-10-12-P-0129/snapshots.json"))
        if s["label"] == "ko-1h45"][-1]
pred = {(r["home"], r["away"]): r for r in csv.DictReader(open("/Users/triton/PROTEUS/pitch/PREDICTIONS.csv"))
        if r["kickoff_utc"].startswith("2026-10-13")}


def implied(o):
    inv = {k: 1 / o[k] for k in ("AvgH", "AvgD", "AvgA")}
    t = sum(inv.values())
    return {k: v / t for k, v in inv.items()}


rows, toward, away, flat = [], 0, 0, 0
for r in snap["rows"]:
    p = pred.get(tuple(r["match"].split(" v ", 1)))
    if not p or not r.get("commit") or not r.get("now"):
        continue
    a, b = implied(r["commit"]), implied(r["now"])
    model = {"AvgH": float(p["p_home"]), "AvgD": float(p["p_draw"]), "AvgA": float(p["p_away"])}
    for k in model:
        lean = model[k] - a[k]; move = b[k] - a[k]
        side = "flat" if abs(move) < 0.002 or abs(lean) < 0.02 else ("toward" if lean * move > 0 else "away")
        toward += side == "toward"; away += side == "away"; flat += side == "flat"
        rows.append({"match": r["match"], "outcome": k[3], "model": round(model[k], 3),
                     "commit_implied": round(a[k], 3), "ko_implied": round(b[k], 3), "lean": round(lean, 3),
                     "move": round(move, 4), "side": side})
res = {"snapshot_at": snap["at"], "outcomes": len(rows), "toward": toward, "away": away, "flat_or_no_lean": flat,
       "rows": rows}
json.dump(res, open(OUT + "result.json", "w"), indent=1)
for x in rows:
    if x["side"] != "flat":
        print(x["match"], x["outcome"], "lean", x["lean"], "move", x["move"], x["side"])
print("outcomes", len(rows), "toward", toward, "away", away, "flat or no lean", flat)
