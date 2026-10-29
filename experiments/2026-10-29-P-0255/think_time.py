"""P-0255: my Lichess bot's real think time per move against the result, every rated game.

Export (keyless, pulled 29 Oct 2026):
    curl -H "Accept: application/x-ndjson" "https://lichess.org/api/games/user/tritonxxix?rated=true&clocks=true&moves=false"
clocks[] are centiseconds remaining after each ply, white first. Think on my move j =
previous own clock + increment - own clock after the move. The first own move is skipped (no prior).

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 experiments/2026-10-29-P-0255/think_time.py
"""
import json
import numpy as np
from scipy.stats import mannwhitneyu

SRC = "/Users/triton/PROTEUS/sandbox/lichess-tritonxxix.ndjson"
OUT = "/Users/triton/PROTEUS/experiments/2026-10-29-P-0255/results.json"
ME = "tritonxxix"
games = []
for line in open(SRC):
    if not line.strip():
        continue
    g = json.loads(line)
    side = "white" if g["players"]["white"].get("user", {}).get("id") == ME else "black"
    cl = g.get("clocks") or []
    inc = g["clock"]["increment"] * 100 if g.get("clock") else 0
    own = cl[0::2] if side == "white" else cl[1::2]
    if len(own) < 3:
        continue
    th = [(own[j - 1] + inc - own[j]) / 100 for j in range(1, len(own))]
    w = g.get("winner")
    res = "draw" if w is None else ("win" if w == side else "loss")
    opp = g["players"]["black" if side == "white" else "white"]
    games.append({"id": g["id"], "result": res, "status": g["status"], "created": g["createdAt"],
                  "opp_rating": opp.get("rating"), "plies": len(cl), "tc": f'{g["clock"]["initial"]}+{g["clock"]["increment"]}',
                  "mean_think_s": round(float(np.mean(th)), 3), "median_think_s": round(float(np.median(th)), 3),
                  "max_think_s": round(float(np.max(th)), 2)})

by = {r: [x["mean_think_s"] for x in games if x["result"] == r] for r in ("win", "draw", "loss")}
out = {"games": len(games), "by_result": {r: {"n": len(v), "median_of_game_means_s": round(float(np.median(v)), 3) if v else None,
                                               "mean_of_game_means_s": round(float(np.mean(v)), 3) if v else None}
                                           for r, v in by.items()}}
if by["win"] and by["draw"]:
    u = mannwhitneyu(by["draw"], by["win"], alternative="two-sided")
    out["draw_v_win_mannwhitney"] = {"U": float(u.statistic), "p": round(float(u.pvalue), 4)}
    dr = np.array([x["opp_rating"] or 0 for x in games if x["result"] == "draw"])
    wr = np.array([x["opp_rating"] or 0 for x in games if x["result"] == "win"])
    out["opp_rating_median"] = {"draw": float(np.median(dr)), "win": float(np.median(wr))}
    allm = np.array([x["mean_think_s"] for x in games])
    allr = np.array([x["opp_rating"] or 0 for x in games])
    out["corr_think_v_opp_rating"] = round(float(np.corrcoef(allm, allr)[0, 1]), 3)
out["tc_counts"] = {t: sum(1 for x in games if x["tc"] == t) for t in sorted({x["tc"] for x in games})}
out["rows"] = games
json.dump(out, open(OUT, "w"), indent=1)
print({k: v for k, v in out.items() if k != "rows"})
