"""P-0518: P-0511's Elo plus Poisson with one fitted draw multiplier.

Same Elo, Poisson and scoring as experiments/2026-11-20-P-0511/judge.py. Adds: the draw probability
is multiplied by m and the three outcomes renormalised; m is fitted by 3-way log-likelihood on
2010-01-01 to 2022-12-31 non-friendly matches, using the Elo before each match (grid 0.80 to 2.00).
Also fixes the "Bosnia & Herzegovina" alias that dropped two rows in P-0511.

    python3 draw.py results.csv JUDGEMENT.csv out.json
"""
import csv, json, math, sys

SRC, JUD, OUT = sys.argv[1:4]
rows = [r for r in csv.DictReader(open(SRC, encoding="utf-8")) if r["home_score"] not in ("", "NA")]
rows.sort(key=lambda r: r["date"])
jud = [j for j in csv.DictReader(open(JUD, encoding="utf-8")) if j["result"] in ("H", "D", "A")]
ALIAS = {"Czechia": "Czech Republic", "Türkiye": "Turkey", "Turkiye": "Turkey",
         "Bosnia-Herzegovina": "Bosnia and Herzegovina", "Bosnia & Herzegovina": "Bosnia and Herzegovina"}


def k_of(t):
    if t == "FIFA World Cup":
        return 60
    if "qualification" in t:
        return 40
    if t in ("UEFA Euro", "Copa América", "African Cup of Nations", "AFC Asian Cup", "Gold Cup", "UEFA Nations League", "CONCACAF Nations League"):
        return 50
    return 20 if t == "Friendly" else 30


first_day = min(j["kickoff_utc"][:10] for j in jud)
elo, fit, dfit = {}, [], []
snap = {}
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
    if "2010-01-01" <= r["date"] <= "2022-12-31" and r["tournament"] != "Friendly":
        dfit.append((dr, 0 if hs > as_ else 1 if hs == as_ else 2))
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

FACT = [math.factorial(k) for k in range(11)]


def base(dr):
    mh, ma = math.exp(a_ + b_ * dr / 400), math.exp(a_ - b_ * dr / 400)
    ph = [math.exp(-mh) * mh ** k / FACT[k] for k in range(11)]
    pa = [math.exp(-ma) * ma ** k / FACT[k] for k in range(11)]
    p = [0.0, 0.0, 0.0]
    for i in range(11):
        for j in range(11):
            p[0 if i > j else 1 if i == j else 2] += ph[i] * pa[j]
    s = sum(p)
    return [x / s for x in p]


def bump(p, m):
    q = [p[0], p[1] * m, p[2]]
    s = sum(q)
    return [x / s for x in q]


cache = {}
for dr, _ in dfit:
    k = round(dr)
    if k not in cache:
        cache[k] = base(k)
best = None
grid = []
for i in range(0, 121, 2):
    m = 0.80 + i / 100
    ll = sum(math.log(bump(cache[round(dr)], m)[o]) for dr, o in dfit)
    grid.append((round(m, 2), round(ll, 1)))
    if best is None or ll > best[1]:
        best = (round(m, 2), ll)
M = best[0]
draw_rate = sum(1 for _, o in dfit if o == 1) / len(dfit)
pred_draw = sum(cache[round(dr)][1] for dr, _ in dfit) / len(dfit)


def brier(p, o):
    return sum((p[i] - (1 if i == o else 0)) ** 2 for i in range(3))


out, missing = [], []
tot = {"model": 0.0, "bumped": 0.0, "anchored": 0.0, "market": 0.0}
bl = {"model": 0.0, "bumped": 0.0, "blind": 0.0, "market": 0.0, "n": 0}
for j in jud:
    h, a = ALIAS.get(j["home"], j["home"]), ALIAS.get(j["away"], j["away"])
    e = snap[j["kickoff_utc"][:10]]
    if h not in e or a not in e:
        missing.append(j["id"] + " " + h + " v " + a)
        continue
    p = base(e[h] + 100 - e[a])
    pb = bump(p, M)
    o = "HDA".index(j["result"])
    mk = [float(j["market_home"]), float(j["market_draw"]), float(j["market_away"])]
    s = sum(mk); mk = [x / s for x in mk]
    me = [float(j["p_home"]), float(j["p_draw"]), float(j["p_away"])]
    row = {"id": j["id"], "result": j["result"], "b_model": brier(p, o), "b_bumped": brier(pb, o),
           "b_me": brier(me, o), "b_market": brier(mk, o)}
    tot["model"] += row["b_model"]; tot["bumped"] += row["b_bumped"]; tot["anchored"] += row["b_me"]; tot["market"] += row["b_market"]
    if j["blind_home"]:
        b = [float(j["blind_home"]), float(j["blind_draw"]), float(j["blind_away"])]
        bl["model"] += row["b_model"]; bl["bumped"] += row["b_bumped"]; bl["blind"] += brier(b, o); bl["market"] += row["b_market"]; bl["n"] += 1
    out.append(row)
n = len(out)
summary = {"scored_rows": len(jud), "used": n, "missing_team": missing,
           "fit_matches": len(dfit), "draw_rate_actual": round(draw_rate, 4), "draw_rate_poisson": round(pred_draw, 4),
           "draw_multiplier": M,
           "brier": {k: round(v / n, 4) for k, v in tot.items()},
           "gap_closed": round((tot["model"] - tot["bumped"]) / (tot["model"] - tot["market"]), 3) if tot["model"] != tot["market"] else None,
           "draws_in_book": sum(1 for r in out if r["result"] == "D"),
           "blind_rows": bl["n"], "on_blind_rows": {k: round(v / bl["n"], 4) for k, v in bl.items() if k != "n"} if bl["n"] else None}
print(json.dumps(summary, indent=1))
json.dump({"summary": summary, "grid": grid, "rows": out}, open(OUT, "w"), indent=1)
