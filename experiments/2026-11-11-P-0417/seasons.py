"""P-0417: ICON lead-1 bias on the METAR day high by season at Munich (EDDM) and Heathrow (EGLL).

P-0406's method: Iowa State keyless METAR archive, day high = max of routine and special reports
(whole degrees), at least 12 reports a day; Open-Meteo previous-runs icon_seamless, temperature_2m
(lead 0) and temperature_2m_previous_day1 (lead 1), hourly maxed per UTC day. Bias is METAR minus
forecast, so positive means ICON was cold. Munich is read at two forecast points: the airport, and the
city point 48.137,11.575 that the exchange book's calls use against the same EDDM METAR.
Windows: 1 Nov 2025 to 31 Mar 2026, and 1 Jun to 31 Aug 2026. Raw pulls are not kept.
"""
import json
import pathlib
import time
import urllib.request
from collections import defaultdict

HERE = pathlib.Path(__file__).parent
UA = {"User-Agent": "research-script/1.0"}
POINTS = [("EDDM", "airport", 48.3538, 11.7861), ("EDDM", "city_point_the_book_uses", 48.137, 11.575), ("EGLL", "airport", 51.4700, -0.4543)]
WINDOWS = {"winter": ("2025-11-01", "2026-03-31", (2025, 11, 1), (2026, 4, 1)), "summer": ("2026-06-01", "2026-08-31", (2026, 6, 1), (2026, 9, 1))}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()


def metar_highs(icao, a, b):
    u = (f"https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station={icao}&data=tmpc&year1={a[0]}&month1={a[1]}&day1={a[2]}"
         f"&year2={b[0]}&month2={b[1]}&day2={b[2]}&tz=UTC&format=onlycomma&latlon=no&missing=empty&trace=empty&report_type=3&report_type=4")
    m = defaultdict(list)
    for line in get(u).decode("latin-1").splitlines()[1:]:
        p = line.split(",")
        if len(p) >= 3 and p[2]:
            try:
                m[p[1][:10]].append(float(p[2]))
            except ValueError:
                pass
    return {k: max(v) for k, v in m.items() if len(v) >= 12}


def highs(h, var):
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
    return {"mean": round(mean, 2), "sd": round(sd, 2), "se": round(se, 2), "n": n, "outside_2se": abs(mean) > 2 * se,
            "mae": round(sum(abs(x) for x in e) / n, 2), "exact_degree": round(sum(1 for x in e if abs(x) < 0.5) / n, 3)}


out, metar = {}, {}
for wname, (start, end, a, b) in WINDOWS.items():
    for icao in ("EDDM", "EGLL"):
        metar[(icao, wname)] = metar_highs(icao, a, b)
        time.sleep(2)
    for icao, pname, lat, lon in POINTS:
        mh = metar[(icao, wname)]
        d = json.loads(get(f"https://previous-runs-api.open-meteo.com/v1/forecast?latitude={lat:.4f}&longitude={lon:.4f}"
                           f"&hourly=temperature_2m,temperature_2m_previous_day1&start_date={start}&end_date={end}&timezone=UTC&models=icon_seamless"))
        time.sleep(2)
        row = {"model_point": [d["latitude"], d["longitude"]], "model_elevation_m": d.get("elevation")}
        for lead, var in ((0, "temperature_2m"), (1, "temperature_2m_previous_day1")):
            f = highs(d["hourly"], var)
            err = {x: mh[x] - f[x] for x in sorted(set(f) & set(mh)) if start <= x <= end}
            blk = {"all": stat(list(err.values()))}
            if wname == "winter":
                blk["dec_to_feb"] = stat([v for k, v in err.items() if k[:7] in ("2025-12", "2026-01", "2026-02")])
            for mth in sorted({k[:7] for k in err}):
                blk[mth] = stat([v for k, v in err.items() if k[:7] == mth])
            row[f"lead{lead}"] = blk
        out[f"{icao}|{pname}|{wname}"] = row
        l1 = row["lead1"]
        print(icao, pname, wname, "lead1", {k: (v.get("mean"), v.get("se"), v.get("n"), v.get("outside_2se")) for k, v in l1.items()},
              "| mae", l1["all"].get("mae"), "exact", l1["all"].get("exact_degree"), "| lead0 all", row["lead0"]["all"].get("mean"))
(HERE / "results.json").write_text(json.dumps(out, indent=1))
