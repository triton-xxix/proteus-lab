"""P-0391: ICON lead-1 bias on the METAR day high at EDDM, EHAM, LFPG, LEMD, 1 Sep to 31 Oct 2026.

Method from experiments/2026-11-09-P-0383 (metar.py, gatwick.py): Iowa State keyless METAR archive, day high = max of
routine and special reports (whole degrees), at least 12 reports a day; icon_seamless previous-runs at the airport's
published coordinates, temperature_2m (lead 0) and temperature_2m_previous_day1 (lead 1), hourly maxed per day, UTC days
on both sides. Number: mean METAR minus forecast, sd, se, n per airport and lead.
"""
import json
import pathlib
import time
import urllib.request
from collections import defaultdict

HERE = pathlib.Path(__file__).parent
UA = {"User-Agent": "proteus-research/1.0"}
AIRPORTS = {"EDDM": (48.3538, 11.7861), "EHAM": (52.3086, 4.7639), "LFPG": (49.0097, 2.5479), "LEMD": (40.4719, -3.5626)}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read()


def metar_highs(icao):
    u = (f"https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station={icao}&data=tmpc&year1=2026&month1=9&day1=1"
         "&year2=2026&month2=11&day2=1&tz=UTC&format=onlycomma&latlon=no&missing=empty&trace=empty&report_type=3&report_type=4")
    t = get(u).decode("latin-1").splitlines()
    (HERE / f"iem-{icao}.csv").write_text("\n".join(t))
    m = defaultdict(list)
    for line in t[1:]:
        p = line.split(",")
        if len(p) >= 3 and p[2]:
            try:
                m[p[1][:10]].append(float(p[2]))
            except ValueError:
                pass
    return {k: max(v) for k, v in m.items() if len(v) >= 12}


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
    mean = sum(e) / n
    sd = (sum((x - mean) ** 2 for x in e) / (n - 1)) ** 0.5
    se = sd / n ** 0.5
    return {"mean": round(mean, 2), "sd": round(sd, 2), "se": round(se, 2), "n": n, "outside_2se": abs(mean) > 2 * se}


out = {}
for icao, (lat, lon) in AIRPORTS.items():
    mh = metar_highs(icao)
    time.sleep(2)
    url = (f"https://previous-runs-api.open-meteo.com/v1/forecast?latitude={lat:.4f}&longitude={lon:.4f}"
           "&hourly=temperature_2m,temperature_2m_previous_day1&start_date=2026-09-01&end_date=2026-10-31"
           "&timezone=UTC&models=icon_seamless")
    d = json.loads(get(url))
    (HERE / f"om-{icao}.json").write_text(json.dumps(d))
    time.sleep(2)
    row = {"model_point": [d["latitude"], d["longitude"]], "model_elevation_m": d.get("elevation"), "metar_days": len(mh)}
    for lead, var in ((0, "temperature_2m"), (1, "temperature_2m_previous_day1")):
        f = highs(d, var)
        days = sorted(d_ for d_ in set(f) & set(mh) if "2026-09-01" <= d_ <= "2026-10-31")
        row[f"lead{lead}"] = stat([mh[x] - f[x] for x in days]) if len(days) > 2 else {"n": len(days)}
    out[icao] = row
    print(icao, json.dumps(row))

(HERE / "results.json").write_text(json.dumps(out, indent=1))
