"""How many scored rows would my judgement book need to see an edge of a given size?

Read-it check of Foresight Arena (arXiv 2605.00420): 350 binary predictions to detect
alpha 0.02 at 80% power. My books are three-way, so measure my own per-row spread.
"""
import csv
import math
import statistics
import sys

path = sys.argv[1]
rows = list(csv.DictReader(open(path)))
d_anch, d_blind = [], []
for r in rows:
    if r["brier"] and r["market_brier"]:
        d_anch.append(float(r["brier"]) - float(r["market_brier"]))
    if r.get("blind_brier") and r["market_brier"]:
        d_blind.append(float(r["blind_brier"]) - float(r["market_brier"]))

z = 1.96 + 0.8416  # two-sided 5%, 80% power
for name, d in (("anchored", d_anch), ("blind", d_blind)):
    n = len(d)
    m = statistics.mean(d)
    sd = statistics.stdev(d)
    print(f"{name}: n {n}, mean diff {m:+.4f}, sd {sd:.4f}, se {sd / math.sqrt(n):.4f}")
    for edge in (0.005, 0.01, 0.02, 0.05):
        need = math.ceil((z * sd / edge) ** 2)
        print(f"  edge {edge}: rows needed {need}")
    print(f"  smallest edge detectable at n=60: {z * sd / math.sqrt(60):.4f}")
