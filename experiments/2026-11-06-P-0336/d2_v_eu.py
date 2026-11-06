"""P-0336: ICON-D2 v ICON-EU day highs at the Munich city point, against DWD 03379 and the EDDM METAR high.

Usage: python3 -I d2_v_eu.py ICON.json IEM.csv OUT.json
ICON.json: Open-Meteo previous-runs, models=icon_d2,icon_eu, UTC. Only days with 24 hours of a field count.
"""
import csv
import io
import json
import math
import re
import statistics
import sys
import urllib.request
import zipfile

icon_path, metar_path, out = sys.argv[1:4]
TODAY = "2026-11-06"
TEMP = re.compile(r"\s(M?\d{2})/(M?\d{2})?\s")


def txk():
    url = ("https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/recent/"
           "tageswerte_KL_03379_akt.zip")
    req = urllib.request.Request(url, headers={"User-Agent": "proteus-settlecheck"})
    blob = urllib.request.urlopen(req, timeout=60).read()
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        name = [n for n in z.namelist() if n.startswith("produkt_klima_tag")][0]
        lines = z.read(name).decode("latin-1").splitlines()
    head = [h.strip() for h in lines[0].split(";")]
    res = {}
    for line in lines[1:]:
        r = dict(zip(head, [p.strip() for p in line.split(";")]))
        if r.get("TXK") not in (None, "", "-999", "-999.0"):
            d = r["MESS_DATUM"]
            res["%s-%s-%s" % (d[:4], d[4:6], d[6:8])] = float(r["TXK"])
    return res


metar = {}
for r in csv.DictReader(open(metar_path, newline="")):
    m = TEMP.search(" " + r["metar"] + " ")
    if m:
        s = m.group(1)
        t = -int(s[1:]) if s[0] == "M" else int(s)
        metar[r["valid"][:10]] = max(metar.get(r["valid"][:10], -99), t)

hourly = json.load(open(icon_path))["hourly"]


def highs(field):
    days = {}
    for when, v in zip(hourly["time"], hourly[field]):
        if v is not None:
            days.setdefault(when[:10], []).append(v)
    return {d: max(v) for d, v in days.items() if len(v) == 24}


SERIES = {
    "D2 lead 0": "temperature_2m_icon_d2",
    "D2 lead 1": "temperature_2m_previous_day1_icon_d2",
    "EU lead 0": "temperature_2m_icon_eu",
    "EU lead 1": "temperature_2m_previous_day1_icon_eu",
    "EU lead 2": "temperature_2m_previous_day2_icon_eu",
}
fc = {name: highs(field) for name, field in SERIES.items() if field in hourly}


def rnd(x):
    return math.floor(x + 0.5)


def score(f, obs, days):
    use = [d for d in days if d in f and d in obs]
    err = [obs[d] - f[d] for d in use]
    return {"days": len(use), "bias": round(statistics.mean(err), 2), "sd": round(statistics.pstdev(err), 2),
            "mae": round(statistics.mean(abs(e) for e in err), 2),
            "exact": sum(rnd(f[d]) == rnd(obs[d]) for d in use)}


dwd = txk()
targets = {"DWD 03379": dwd, "EDDM METAR": metar}
res = {"series_found": sorted(fc), "targets": {}}
for tname, obs in targets.items():
    common = [d for d in sorted(set.intersection(*[set(f) for f in fc.values()], set(obs))) if d < TODAY]
    res["targets"][tname] = {"common_days": len(common), "first": common[0] if common else None,
                             "last": common[-1] if common else None,
                             "scores": {n: score(f, obs, common) for n, f in fc.items()}}
    if "D2 lead 1" in fc and "EU lead 1" in fc and common:
        diff = [abs(obs[d] - fc["EU lead 1"][d]) - abs(obs[d] - fc["D2 lead 1"][d]) for d in common]
        res["targets"][tname]["eu_minus_d2_abs_error"] = {
            "mean": round(statistics.mean(diff), 3),
            "se": round(statistics.stdev(diff) / math.sqrt(len(diff)), 3),
        }
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res, indent=1))
