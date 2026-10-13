#!/usr/bin/env python3
"""P-0136: do the finite-difference and analytic-gradient fits predict the same probabilities?
ENG group (the one with the largest parameter gap): every ordered team pair, max abs difference in
p_home, p_draw, p_away, p_over25. Usage: predcheck.py OUT.json"""
import json
import sys

sys.path.insert(0, "/Users/triton/PROTEUS/pitch")
sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/p0136")
import data as D  # noqa: E402
import model as M  # noqa: E402
from dc_grad import fit_grad  # noqa: E402

res = D.load_results(D.LEAGUES)
sub = res[res["Div"].isin(D.GROUPS["ENG"])]
base = M.fit(sub)
new = fit_grad(sub)
worst = {"p_home": 0.0, "p_draw": 0.0, "p_away": 0.0, "p_over25": 0.0}
pairs = 0
for hm in base["teams"]:
    for aw in base["teams"]:
        if hm == aw:
            continue
        pb = M.predict(base, hm, aw); pn = M.predict(new, hm, aw)
        pairs += 1
        for k in worst:
            worst[k] = max(worst[k], abs(pb[k] - pn[k]))
out = {"group": "ENG", "pairs": pairs, "max_abs_prob_diff": {k: round(v, 5) for k, v in worst.items()},
       "home_fd": base["home"], "home_grad": new["home"], "rho_fd": base["rho"], "rho_grad": new["rho"]}
print(json.dumps(out, indent=1))
json.dump(out, open(sys.argv[1], "w"), indent=1)
