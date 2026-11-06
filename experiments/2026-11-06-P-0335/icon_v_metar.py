"""P-0335: ICON against the highest EDDM METAR per UTC day, airport grid and the nightly's city rule.

Usage: python3 -I icon_v_metar.py IEM.csv AIRPORT.json CITY.json OUT.json
AIRPORT.json and CITY.json are Open-Meteo previous-runs responses, models=icon_seamless, UTC.
"""
import csv
import json
import math
import re
import statistics
import sys

metar_csv, airport_json, city_json, out = sys.argv[1:5]
TEMP = re.compile(r"\s(M?\d{2})/(M?\d{2})?\s")
TODAY = "2026-11-06"
FIELDS = {0: "temperature_2m", 1: "temperature_2m_previous_day1", 2: "temperature_2m_previous_day2"}

metar = {}
for r in csv.DictReader(open(metar_csv, newline="")):
    m = TEMP.search(" " + r["metar"] + " ")
    if m:
        s = m.group(1)
        t = -int(s[1:]) if s[0] == "M" else int(s)
        d = r["valid"][:10]
        metar[d] = max(metar.get(d, -99), t)


def highs(path):
    h = json.load(open(path))["hourly"]
    res = {}
    for lead, field in FIELDS.items():
        days = {}
        for when, v in zip(h["time"], h[field]):
            if v is not None:
                days.setdefault(when[:10], []).append(v)
        res[lead] = {d: max(v) for d, v in days.items() if len(v) == 24}
    return res


def rnd(x):
    return math.floor(x + 0.5)


def score(fc, add):
    days = [d for d in sorted(fc) if d in metar and d < TODAY]
    err = [metar[d] - (fc[d] + add) for d in days]
    hit = sum(rnd(fc[d] + add) == metar[d] for d in days)
    return {"days": len(days), "mean_metar_minus": round(statistics.mean(err), 2),
            "sd": round(statistics.pstdev(err), 2), "mae": round(statistics.mean(abs(e) for e in err), 2),
            "exact": hit, "exact_pct": round(100 * hit / len(days))}


air, city = highs(airport_json), highs(city_json)
res = {"note": "UTC days; correction +0.3 is the nightly's airport figure, +1.0 its city figure", "leads": {}}
for lead in FIELDS:
    res["leads"][lead] = {
        "city grid +1.0 (the nightly)": score(city[lead], 1.0),
        "city grid +0": score(city[lead], 0.0),
        "airport grid +0": score(air[lead], 0.0),
        "airport grid +0.3": score(air[lead], 0.3),
    }
# Half-sample check on the airport correction: fit on the first half, score on the second.
days = [d for d in sorted(air[1]) if d in metar and d < TODAY]
half = len(days) // 2
fit = statistics.mean(metar[d] - air[1][d] for d in days[:half])
test = days[half:]
res["lead1_split"] = {
    "fit_days": half, "test_days": len(test), "fitted_add": round(fit, 2),
    "test_exact_airport_fitted": sum(rnd(air[1][d] + fit) == metar[d] for d in test),
    "test_exact_city_plus1": sum(rnd(city[1][d] + 1.0) == metar[d] for d in test if d in city[1]),
}
res["days_lead1"] = [{
    "day": d, "metar": metar[d], "nightly_city_plus1": rnd(city[1][d] + 1.0) if d in city[1] else None,
    "airport_plus0.3": rnd(air[1][d] + 0.3),
} for d in days]
json.dump(res, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "days_lead1"}, indent=1))
for r in res["days_lead1"]:
    print(r["day"], r["metar"], r["nightly_city_plus1"], r["airport_plus0.3"])
