"""P-0115: run founder-skill's unit_economics.py on its own example and compare with a hand
calculation done independently (worked on paper first, figures typed in below).

usage: python3 compare.py PATH_TO/unit_economics.py PATH_TO/example.json
"""
import json
import subprocess
import sys

tool, example = sys.argv[1], sys.argv[2]
out = subprocess.run([sys.executable, tool, example, "--json"], capture_output=True, text=True, check=True)
a = json.loads(out.stdout)

# Hand calculation from example.json (price 6.50, variable 0.92+0.38+0.24+0.20, fixed 15,500+11,040,
# startup 25,280, 30 days, plan 383, ramp 140..292).
hand = {
    "variable_per_unit": 1.74,
    "contribution": 4.76,
    "breakeven_per_day": 26540 / (4.76 * 30),          # 185.85, so 186 cups
    "margin_at_plan": (4.76 - 26540 / (383 * 30)) / 6.50,  # 0.377
    "year1_revenue": 2888 * 30 * 6.50,                  # 563,160
    "year1_profit": 2888 * 30 * 4.76 - 12 * 26540,      # 93,926.40
    "payback_month": 8,                                 # cumulative -1,572 after m7, +10,729 after m8
    "cash_needed": 34092.0,                             # deepest point, after month 2
}
rows, ok = [], 0
for k, h in hand.items():
    t = a[k]
    match = abs(t - h) < 0.01 if isinstance(h, float) else t == h
    ok += match
    rows.append({"field": k, "tool": t, "hand": round(h, 4), "match": match})
    print("%-18s tool %-14s hand %-14s %s" % (k, round(t, 4), round(h, 4), "ok" if match else "DIFF"))
print("%d of %d match" % (ok, len(hand)))
print("note: margin_at_plan uses plan_per_day 383, but the year-1 ramp tops out at 292 a day;"
      " at 292 the margin is %.1f%%" % (100 * (4.76 - 26540 / (292 * 30)) / 6.50))
json.dump({"rows": rows, "tool": a}, open(sys.argv[0].rsplit("/", 1)[0] + "/results.json", "w"), indent=1)
