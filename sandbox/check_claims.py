#!/usr/bin/env python3
"""Check YouTube football-model claims against the Pitch desk's own data and fit (2026-09-22)."""
import json
import math
import sys
from collections import Counter

sys.path.insert(0, "/Users/triton/PROTEUS/pitch")
import data as D  # noqa: E402

p = json.load(open("/Users/triton/PROTEUS/pitch/cache/params.json"))
print("fitted rho", round(p["rho"], 4), "home adv", round(p["home"], 4), "n", p["n_matches"])

# Claim: teams averaging 1.4 and 1.1 goals -> 55-56% chance at least one fails to score
lam, mu = 1.4, 1.1
p00, p10, p01, p11 = (math.exp(-lam) * math.exp(-mu), lam * math.exp(-lam) * math.exp(-mu),
                      math.exp(-lam) * mu * math.exp(-mu), lam * math.exp(-lam) * mu * math.exp(-mu))
btts_yes = (1 - math.exp(-lam)) * (1 - math.exp(-mu))
print("poisson BTTS-no", round(1 - btts_yes, 4))
for rho in (-0.13, p["rho"]):
    d = p00 * (-lam * mu * rho) + p10 * (mu * rho) + p01 * (lam * rho) + p11 * (-rho)
    # d is the net shift from the four cells; BTTS-no cells are 00,10,01; 11 is BTTS-yes
    shift_no = p00 * (-lam * mu * rho) + p10 * (mu * rho) + p01 * (lam * rho)
    print("DC rho", round(rho, 3), "BTTS-no", round((1 - btts_yes + shift_no) / (1 + d), 4))

res = D.load_results()
for div in ("E0", "E1"):
    r = res[res["Div"] == div]
    n = len(r)
    btts_no = ((r["FTHG"] == 0) | (r["FTAG"] == 0)).mean()
    draw = (r["FTHG"] == r["FTAG"]).mean()
    sc = Counter(zip(r["FTHG"], r["FTAG"])).most_common(4)
    print(div, "n", n, "mean goals h/a", round(r["FTHG"].mean(), 3), round(r["FTAG"].mean(), 3),
          "BTTS-no", round(btts_no, 4), "draw", round(draw, 4), "top scores", sc)
    # empirical vs independent-Poisson frequency of 0-0 and 1-1
    lh, la = r["FTHG"].mean(), r["FTAG"].mean()
    for x, y in ((0, 0), (1, 1), (1, 0), (0, 1)):
        obs = ((r["FTHG"] == x) & (r["FTAG"] == y)).mean()
        exp = math.exp(-lh) * lh ** x / math.factorial(x) * math.exp(-la) * la ** y / math.factorial(y)
        print("  %d-%d observed %.4f poisson %.4f" % (x, y, obs, exp))
