"""P-0511: P-0510's Elo plus Poisson, frozen before each judgement-book match day, scored on the
book's scored rows against my anchored column, my blind column and the market (3-way Brier, same
formula as pitch/JUDGEMENT.csv). Poisson fitted once on 2010 to the day before the first row.

    python3 judge.py results.csv JUDGEMENT.csv out.json
"""
import csv
import json
import math
import sys

SRC, JUD, OUT = sys.argv[1:4]
rows = [r for r in csv.DictReader(open(SRC, encoding="utf-8")) if r["home_score"] not in ("", "NA")]
rows.sort(key=lambda r: r["date"])
jud = [j for j in csv.DictReader(open(JUD, encoding="utf-8")) if j["result"] in ("H", "D", "A")]
ALIAS = {"Czechia": "Czech Republic", "Türkiye": "Turkey", "Turkiye": "Turkey", "Republic of Ireland": "Republic of Ireland",
         "Bosnia-Herzegovina": "Bosnia and Herzegovina", "North Macedonia": "North Macedonia", "Kosovo": "Kosovo"}


def k_of(t):
    if t == "FIFA World Cup":
        return 60
    if "qualification" in t:
        return 40
    if t in ("UEFA Euro", "Copa América", "African Cup of Nations", "AFC Asian Cup", "Gold Cup", "UEFA Nations League", "CONCACAF Nations League"):
        return 50
    return 20 if t == "Friendly" else 30


first_day = min(j["kickoff_utc"][:10] for j in jud)
elo, fit = {}, []
snap = {}  # date -> elo copy before that date's matches
days_needed = sorted({j["kickoff_utc"][:10] for j in jud})
di = 0
for r in rows:
    while di < len(days_needed) and r["date"] >= days_needed[di]:
        snap[days_needed[di]] = dict(elo)
        di += 1
    h, a = r["home_team"], r["away_team"]
    eh, ea = elo.get(h, 1500.0), elo.get(a, 1500.0)
    adv = 0 if r["neutral"] == "TRUE" else 100
    dr = eh + adv - ea
    hs, as_ = int(r["home_score"]), int(r["away_score"])
    if "2010-01-01" <= r["date"] < first_day and r["tournament"] != "Friendly":
        fit += [(dr, hs), (-dr, as_)]
    we = 1 / (10 ** (-dr / 400) + 1)
    w = 1.0 if hs > as_ else 0.5 if hs == as_ else 0.0
    gd = abs(hs - as_)
    g = 1 if gd <= 1 else 1.5 if gd == 2 else (11 + gd) / 8
    d = k_of(r["tournament"]) * g * (w - we)
    elo[h], elo[a] = eh + d, ea - d
while di < len(days_needed):
    snap[days_needed[di]] = dict(elo)
    di += 1

a_ = b_ = 0.0
for _ in range(30):
    ga = gb = haa = hab = hbb = 0.0
    for dr, y in fit:
        x = dr / 400
        mu = math.exp(a_ + b_ * x)
        ga += y - mu; gb += (y - mu) * x; haa += mu; hab += mu * x; hbb += mu * x * x
    det = haa * hbb - hab * hab
    a_ += (hbb * ga - hab * gb) / det
    b_ += (-hab * ga + haa * gb) / det


def three_way(dr):
    mh, ma = math.exp(a_ + b_ * dr / 400), math.exp(a_ - b_ * dr / 400)
    pm = lambda k, mu: math.exp(-mu) * mu ** k / math.factorial(k)
    p = [0.0, 0.0, 0.0]
    for i in range(11):
        for j in range(11):
            p[0 if i > j else 1 if i == j else 2] += pm(i, mh) * pm(j, ma)
    s = sum(p)
    return [x / s for x in p]


def brier(p, o):
    return sum((p[i] - (1 if i == o else 0)) ** 2 for i in range(3))


out, missing = [], []
tot = {"model": 0.0, "anchored": 0.0, "market": 0.0}
blind = {"model": 0.0, "blind": 0.0, "market": 0.0, "n": 0}
for j in jud:
    h, a = ALIAS.get(j["home"], j["home"]), ALIAS.get(j["away"], j["away"])
    e = snap[j["kickoff_utc"][:10]]
    if h not in e or a not in e:
        missing.append(f'{j["id"]} {h} v {a}')
        continue
    # home advantage: assume not neutral (Nations League and qualifiers are home games)
    p = three_way(e[h] + 100 - e[a])
    o = "HDA".index(j["result"])
    mk = [float(j["market_home"]), float(j["market_draw"]), float(j["market_away"])]
    s = sum(mk); mk = [x / s for x in mk]
    me = [float(j["p_home"]), float(j["p_draw"]), float(j["p_away"])]
    row = {"id": j["id"], "match": f"{h} v {a}", "result": j["result"], "model": [round(x, 3) for x in p],
           "b_model": round(brier(p, o), 4), "b_me": round(brier(me, o), 4), "b_market": round(brier(mk, o), 4)}
    tot["model"] += row["b_model"]; tot["anchored"] += row["b_me"]; tot["market"] += row["b_market"]
    if j["blind_home"]:
        bl = [float(j["blind_home"]), float(j["blind_draw"]), float(j["blind_away"])]
        blind["model"] += row["b_model"]; blind["blind"] += brier(bl, o); blind["market"] += row["b_market"]; blind["n"] += 1
    out.append(row)

n = len(out)
summary = {"scored_rows": len(jud), "used": n, "missing_team": missing,
           "brier_model": round(tot["model"] / n, 4), "brier_anchored": round(tot["anchored"] / n, 4),
           "brier_market": round(tot["market"] / n, 4),
           "model_minus_market": round((tot["model"] - tot["market"]) / n, 4),
           "blind_rows": blind["n"],
           "on_blind_rows": {k: round(v / blind["n"], 4) for k, v in blind.items() if k != "n"} if blind["n"] else None,
           "poisson_a_b": [round(a_, 4), round(b_, 4)]}
print(json.dumps(summary))
json.dump({"summary": summary, "rows": out}, open(OUT, "w"), indent=1)
