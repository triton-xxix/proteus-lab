"""P-0426: P-0418's three Munich forecast points on the November 2026 days it never saw.

Same method as experiments/2026-11-11-P-0418/points.py: Iowa State EDDM METAR day high (at least 12
reports), Open-Meteo previous-runs icon_seamless lead 1 maxed per UTC day (at least 23 hours), at the
city point (48.137,11.575), the airport point (48.3538,11.7861) and their mean. Error = METAR minus
forecast, so a negative bias means the forecast ran warm.
"""
import json
import pathlib
import urllib.request
from collections import defaultdict

HERE = pathlib.Path(__file__).parent
UA = {"User-Agent": "research-script/1.0"}
START, END = "2026-11-01", "2026-11-12"
NAMES = ("city", "airport", "mean")


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()


def metar_highs():
    u = ("https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=EDDM&data=tmpc&year1=2026&month1=11&day1=1"
         "&year2=2026&month2=11&day2=13&tz=UTC&format=onlycomma&latlon=no&missing=empty&trace=empty&report_type=3&report_type=4")
    m = defaultdict(list)
    for line in get(u).decode("latin-1").splitlines()[1:]:
        p = line.split(",")
        if len(p) >= 3 and p[2]:
            try:
                m[p[1][:10]].append(float(p[2]))
            except ValueError:
                pass
    return {k: (max(v), len(v)) for k, v in m.items()}


def lead1_highs(lat, lon):
    h = json.loads(get(f"https://previous-runs-api.open-meteo.com/v1/forecast?latitude={lat:.4f}&longitude={lon:.4f}"
                       f"&hourly=temperature_2m_previous_day1&start_date={START}&end_date={END}&timezone=UTC&models=icon_seamless"))["hourly"]
    key = next(k for k in h if k.startswith("temperature_2m_previous_day1"))
    m = defaultdict(list)
    for t, v in zip(h["time"], h[key]):
        if v is not None:
            m[t[:10]].append(v)
    return {k: max(v) for k, v in m.items() if len(v) >= 23}


def score(errs):
    n = len(errs)
    if not n:
        return {"n": 0}
    return {"n": n, "bias": round(sum(errs) / n, 2), "mae": round(sum(abs(e) for e in errs) / n, 3),
            "exact_degree": sum(1 for e in errs if abs(e) < 0.5), "within_1": sum(1 for e in errs if abs(e) < 1.5)}


raw = metar_highs()
mh = {k: v[0] for k, v in raw.items() if v[1] >= 40}  # a whole day of half-hourly reports, not a part day
city, air = lead1_highs(48.137, 11.575), lead1_highs(48.3538, 11.7861)
days = sorted(d for d in set(mh) & set(city) & set(air) if START <= d <= END)
rows = []
for d in days:
    f = {"city": city[d], "airport": air[d], "mean": (city[d] + air[d]) / 2}
    rows.append({"date": d, "metar": mh[d], **{n: round(f[n], 1) for n in NAMES}, **{"err_" + n: round(mh[d] - f[n], 2) for n in NAMES}})
out = {"days": len(days), "metar_reports": {k: v[1] for k, v in sorted(raw.items())},
       "scores": {n: score([r["err_" + n] for r in rows]) for n in NAMES}, "rows": rows,
       "nearest_by_day": {n: sum(1 for r in rows if min(NAMES, key=lambda m: abs(r["err_" + m])) == n) for n in NAMES},
       "p0418_year": {"city": 1.048, "airport": 1.049, "mean": 0.977}, "p0418_nov_2025_city_bias": -0.74}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
print("days", len(days), "reports", out["metar_reports"])
for r in rows:
    print(r["date"], "metar %5.1f city %5.1f airport %5.1f mean %5.1f | err %+.2f %+.2f %+.2f" % (
        r["metar"], r["city"], r["airport"], r["mean"], r["err_city"], r["err_airport"], r["err_mean"]))
print(json.dumps(out["scores"]))
print("nearest by day", out["nearest_by_day"])
