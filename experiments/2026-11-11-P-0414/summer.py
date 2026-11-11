"""P-0414: ICON lead-1 bias on the METAR day high at LFPG and LEMD, 1 Jun to 31 Aug 2026, by month.

Method is experiments/2026-11-11-P-0406/winter.py unchanged apart from the dates: Iowa State keyless
METAR archive, day high = max of routine and special reports (whole degrees), at least 12 reports a
day; icon_seamless previous-runs at the airport's coordinates, temperature_2m (lead 0) and
temperature_2m_previous_day1 (lead 1), hourly maxed per UTC day. Number: mean METAR minus forecast,
sd, se, n per airport, lead and month, plus the whole window. The raw pulls are not kept (P-0406's
were 600 KB); the script refetches them.
"""
import json
import pathlib
import time
import urllib.request
from collections import defaultdict

HERE = pathlib.Path(__file__).parent
UA = {"User-Agent": "research-script/1.0"}
AIRPORTS = {"LFPG": (49.0097, 2.5479), "LEMD": (40.4719, -3.5626)}
START, END = "2026-06-01", "2026-08-31"
MONTHS = ["2026-06", "2026-07", "2026-08"]


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()


def metar_highs(icao):
    u = (f"https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station={icao}&data=tmpc&year1=2026&month1=6&day1=1"
         "&year2=2026&month2=9&day2=1&tz=UTC&format=onlycomma&latlon=no&missing=empty&trace=empty&report_type=3&report_type=4")
    t = get(u).decode("latin-1").splitlines()
    m, hours = defaultdict(list), defaultdict(list)
    for line in t[1:]:
        p = line.split(",")
        if len(p) >= 3 and p[2]:
            try:
                m[p[1][:10]].append(float(p[2]))
                hours[p[1][:10]].append((float(p[2]), int(p[1][11:13])))
            except ValueError:
                pass
    return {k: max(v) for k, v in m.items() if len(v) >= 12}, {k: max(v)[1] for k, v in hours.items() if len(v) >= 12}


def highs(dd, var):
    h = dd["hourly"]
    key = var if var in h else f"{var}_icon_seamless"
    m = defaultdict(list)
    for t, v in zip(h["time"], h[key]):
        if v is not None:
            m[t[:10]].append(v)
    return {k: max(v) for k, v in m.items() if len(v) >= 23}


def stat(e):
    n = len(e)
    if n < 3:
        return {"n": n}
    mean = sum(e) / n
    sd = (sum((x - mean) ** 2 for x in e) / (n - 1)) ** 0.5
    se = sd / n ** 0.5
    return {"mean": round(mean, 2), "sd": round(sd, 2), "se": round(se, 2), "n": n, "outside_2se": abs(mean) > 2 * se}


out = {}
for icao, (lat, lon) in AIRPORTS.items():
    mh, peak_hour = metar_highs(icao)
    time.sleep(2)
    url = (f"https://previous-runs-api.open-meteo.com/v1/forecast?latitude={lat:.4f}&longitude={lon:.4f}"
           f"&hourly=temperature_2m,temperature_2m_previous_day1&start_date={START}&end_date={END}"
           "&timezone=UTC&models=icon_seamless")
    d = json.loads(get(url))
    time.sleep(2)
    row = {"model_point": [d["latitude"], d["longitude"]], "model_elevation_m": d.get("elevation"), "metar_days": len(mh),
           "mean_metar_high": round(sum(v for k, v in mh.items() if START <= k <= END) / max(1, sum(1 for k in mh if START <= k <= END)), 1)}
    for lead, var in ((0, "temperature_2m"), (1, "temperature_2m_previous_day1")):
        f = highs(d, var)
        days = sorted(x for x in set(f) & set(mh) if START <= x <= END)
        err = {x: mh[x] - f[x] for x in days}
        blk = {"all": stat(list(err.values()))}
        for mth in MONTHS:
            blk[mth] = stat([v for k, v in err.items() if k[:7] == mth])
        # hot days against the rest: is the miss bigger when the high is 35 C or more (Madrid) or 28 C or more (Paris)?
        line = 35 if icao == "LEMD" else 28
        blk["hot_days_line_c"] = line
        blk["hot"] = stat([v for k, v in err.items() if mh[k] >= line])
        blk["not_hot"] = stat([v for k, v in err.items() if mh[k] < line])
        row[f"lead{lead}"] = blk
    out[icao] = row
    print(icao, json.dumps(row, indent=1))

(HERE / "results.json").write_text(json.dumps(out, indent=1))
