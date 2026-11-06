#!/usr/bin/env python3
"""25% per doubling against constant product, for a buyer who sells when supply has reached 10x.

Power curve (the rLoop video): p(s) = p0 * 1.25 ** log2(s / s0) = p0 * (s / s0) ** k, k = log2(1.25).
Constant product, pump.fun's launch parameters as used on the Grinder desk: virtual tokens V = 1.073e9,
virtual SOL = 30, so cost to move from supply a to b is C(a, b) = 30 * V * (1/(V-b) - 1/(V-a)).
Tokens the curve can sell: 793.1M, so 10x is only reachable when entry supply is under 79.31M.

Both curves are normalised so their price matches at the buyer's entry. Multiple is proceeds over cost for
a buy of size d tokens at supply s0, with others taking supply to 10 * (s0 + d) before the sell, so the sell
walks down the top d tokens. Fees 1% each way on the constant product and the same on the power curve.
"""
import json
import math
from pathlib import Path

K = math.log2(1.25)
V = 1.073e9
SOL = 30.0
MAX_SOLD = 793.1e6
FEE = 0.01


def cp_cost(a, b):
    return SOL * V * (1 / (V - b) - 1 / (V - a))


def cp_price(s):
    return SOL * V / (V - s) ** 2


def pw_cost(a, b, p0, s0):
    return p0 * s0 ** -K * (b ** (K + 1) - a ** (K + 1)) / (K + 1)


rows = []
for pct in (0.1, 0.25, 0.5, 1, 2, 3, 3.33, 4, 5, 6, 7, 7.39):
    s0 = pct / 100 * V
    for frac in (0.0, 0.1, 0.5):  # buy size as a share of entry supply; 0 means marginal
        d = max(s0 * frac, 1.0)
        top = 10 * (s0 + d)
        if top > MAX_SOLD:
            continue
        p0 = cp_price(s0)
        cp = cp_cost(top - d, top) * (1 - FEE) / (cp_cost(s0, s0 + d) * (1 + FEE))
        pw = pw_cost(top - d, top, p0, s0) * (1 - FEE) / (pw_cost(s0, s0 + d, p0, s0) * (1 + FEE))
        rows.append({"entry_pct_of_V": pct, "entry_tokens_m": round(s0 / 1e6, 2), "buy_frac": frac,
                     "constant_product_x": round(cp, 3), "power_x": round(pw, 3), "winner": "power" if pw > cp else "cp"})

# Exact crossover for a marginal buy with no fees: ((V-s)/(V-10s))**2 = 10**K
root = 10 ** (K / 2)
cross = (root - 1) * V / (10 * root - 1)
out = {
    "k": round(K, 5),
    "power_marginal_x_no_fee": round(10 ** K, 4),
    "crossover_tokens_m": round(cross / 1e6, 2),
    "crossover_pct_of_V": round(100 * cross / V, 2),
    "crossover_pct_of_sellable": round(100 * cross / MAX_SOLD, 2),
    "crossover_sol_spent_from_launch": round(cp_cost(0, cross), 3),
    "rows": rows,
}
Path(__file__).with_name("results.json").write_text(json.dumps(out, indent=1))
print({k: v for k, v in out.items() if k != "rows"})
print("entry%  frac   CP      power   winner")
for r in rows:
    print(f"{r['entry_pct_of_V']:6} {r['buy_frac']:5} {r['constant_product_x']:7} {r['power_x']:7} {r['winner']}")
