"""P-0510: Elo plus Poisson on international results, scored on the 2022 World Cup (3-way Brier).

Data: martj42/international_results results.csv (keyless). Elo (eloratings.net style: K by tournament,
goal-difference multiplier, +100 home unless neutral) is run over every match before 20 Nov 2022 and
frozen. Expected goals per side from the Elo gap, fitted by Poisson regression on 2010-2022 competitive
matches (log mu = a + b * dr/400), then a 3-way probability from independent Poissons. Scored on the 64
World Cup 2022 matches; the CSV's score includes extra time, so a knockout level after 120 minutes is
a draw here. Compared with uniform (1/3 each) and with a base-rate model (home/draw/away shares of
neutral World Cup matches 1998-2018). Writes results.json.
"""
import csv
import json
import math
import sys

SRC, OUT = sys.argv[1], sys.argv[2]
CUT = "2022-11-20"
rows = list(csv.DictReader(open(SRC, encoding="utf-8")))
rows = [r for r in rows if r["home_score"] not in ("", "NA")]
rows.sort(key=lambda r: r["date"])


def k_of(t):
    if t == "FIFA World Cup":
        return 60
    if "qualification" in t or t in ("UEFA Euro", "Copa América", "African Cup of Nations", "AFC Asian Cup", "Gold Cup", "UEFA Nations League", "CONCACAF Nations League"):
        return 40 if "qualification" in t else 50
    if t == "Friendly":
        return 20
    return 30


elo = {}
fit = []  # (dr, goals) for Poisson fit, 2010 on, not friendlies
for r in rows:
    if r["date"] >= CUT:
        break
    h, a = r["home_team"], r["away_team"]
    eh, ea = elo.get(h, 1500.0), elo.get(a, 1500.0)
    adv = 0 if r["neutral"] == "TRUE" else 100
    dr = eh + adv - ea
    hs, as_ = int(r["home_score"]), int(r["away_score"])
    if r["date"] >= "2010-01-01" and r["tournament"] != "Friendly":
        fit.append((dr, hs))
        fit.append((-dr, as_))
    we = 1 / (10 ** (-dr / 400) + 1)
    w = 1.0 if hs > as_ else 0.5 if hs == as_ else 0.0
    gd = abs(hs - as_)
    g = 1 if gd <= 1 else 1.5 if gd == 2 else (11 + gd) / 8
    d = k_of(r["tournament"]) * g * (w - we)
    elo[h], elo[a] = eh + d, ea - d

# Poisson regression by Newton's method on two parameters
a_, b_ = 0.0, 0.0
for _ in range(30):
    ga = gb = haa = hab = hbb = 0.0
    for dr, y in fit:
        x = dr / 400
        mu = math.exp(a_ + b_ * x)
        ga += y - mu
        gb += (y - mu) * x
        haa += mu
        hab += mu * x
        hbb += mu * x * x
    det = haa * hbb - hab * hab
    a_ += (hbb * ga - hab * gb) / det
    b_ += (-hab * ga + haa * gb) / det


def pmf(k, mu):
    return math.exp(-mu) * mu ** k / math.factorial(k)


def three_way(dr):
    mh, ma = math.exp(a_ + b_ * dr / 400), math.exp(a_ - b_ * dr / 400)
    ph = pd = pa = 0.0
    for i in range(11):
        for j in range(11):
            p = pmf(i, mh) * pmf(j, ma)
            if i > j:
                ph += p
            elif i == j:
                pd += p
            else:
                pa += p
    s = ph + pd + pa
    return ph / s, pd / s, pa / s


# base rate: earlier World Cups, listed-home side
base = [0, 0, 0]
for r in rows:
    if r["tournament"] == "FIFA World Cup" and "1998-01-01" <= r["date"] < "2022-01-01":
        hs, as_ = int(r["home_score"]), int(r["away_score"])
        base[0 if hs > as_ else 1 if hs == as_ else 2] += 1
nb = sum(base)
base = [x / nb for x in base]

wc = [r for r in rows if r["tournament"] == "FIFA World Cup" and "2022-11-20" <= r["date"] <= "2022-12-18"]
out = []
br = {"model": 0.0, "uniform": 0.0, "base": 0.0}
ll = 0.0
hits = 0
for r in wc:
    h, a = r["home_team"], r["away_team"]
    adv = 0 if r["neutral"] == "TRUE" else 100  # Qatar's games are not neutral in the CSV
    dr = elo.get(h, 1500) + adv - elo.get(a, 1500)
    p = three_way(dr)
    hs, as_ = int(r["home_score"]), int(r["away_score"])
    o = 0 if hs > as_ else 1 if hs == as_ else 2
    y = [1 if i == o else 0 for i in range(3)]
    br["model"] += sum((p[i] - y[i]) ** 2 for i in range(3))
    br["uniform"] += sum((1 / 3 - y[i]) ** 2 for i in range(3))
    br["base"] += sum((base[i] - y[i]) ** 2 for i in range(3))
    ll += -math.log(p[o])
    hits += 1 if max(range(3), key=lambda i: p[i]) == o else 0
    out.append({"date": r["date"], "home": h, "away": a, "score": f"{hs}-{as_}", "dr": round(dr), "p": [round(x, 3) for x in p], "outcome": "HDA"[o]})

n = len(wc)
summary = {
    "matches": n,
    "brier_model": round(br["model"] / n, 4),
    "brier_uniform": round(br["uniform"] / n, 4),
    "brier_base_rate": round(br["base"] / n, 4),
    "base_rate_HDA": [round(x, 3) for x in base],
    "logloss_model": round(ll / n, 4),
    "favourite_hit": hits,
    "poisson_a_b": [round(a_, 4), round(b_, 4)],
    "fit_rows": len(fit),
    "top5_elo": sorted(((round(v), k) for k, v in elo.items()), reverse=True)[:5],
}
print(json.dumps(summary))
json.dump({"summary": summary, "matches": out}, open(OUT, "w"), indent=1)
