"""P-0392: Munich METAR minus city-point ICON lead-1 high, 13 Oct to 9 Nov 2026, by day set and by week.

P-0335 read +0.03 on 24 days (13 Oct to 5 Nov, UTC days); P-0387 read -0.49 on 12 band days (28 Oct to 9 Nov, point maxed
on Europe/Berlin days, METAR days needing 24 reports). Same pulls, both day conventions, so the day set, the drift and the
method can be told apart. Keyless: Open-Meteo previous-runs icon_seamless at 48.137,11.575; Iowa State EDDM METAR.
"""
import json
import pathlib
import time
import urllib.request
from collections import defaultdict

HERE = pathlib.Path(__file__).parent
UA = {"User-Agent": "proteus-research/1.0"}
P0335 = [f"2026-10-{d}" for d in range(13, 32)] + [f"2026-11-0{d}" for d in range(1, 6)]
P0387 = ["2026-10-28", "2026-10-29", "2026-10-30", "2026-10-31", "2026-11-01", "2026-11-02", "2026-11-03", "2026-11-04",
         "2026-11-06", "2026-11-07", "2026-11-08", "2026-11-09"]


def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()


def point(tz):
    u = ("https://previous-runs-api.open-meteo.com/v1/forecast?latitude=48.137&longitude=11.575&hourly=temperature_2m_previous_day1"
         f"&start_date=2026-10-13&end_date=2026-11-09&timezone={tz}&models=icon_seamless")
    om = json.loads(get(u))
    (HERE / f"om-{tz.replace('%2F', '-')}.json").write_text(json.dumps(om))
    h = om["hourly"]
    key = next(k for k in h if k.startswith("temperature_2m_previous_day1"))
    m = defaultdict(list)
    for t, v in zip(h["time"], h[key]):
        if v is not None:
            m[t[:10]].append(v)
    return {k: max(v) for k, v in m.items() if len(v) >= 23}


pt = {"utc": point("UTC")}
time.sleep(2)
pt["berlin"] = point("Europe%2FBerlin")
time.sleep(2)
ie = get("https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=EDDM&data=tmpc&year1=2026&month1=10&day1=13&year2=2026&month2=11&day2=10"
         "&tz=UTC&format=onlycomma&latlon=no&missing=empty&trace=empty&report_type=3&report_type=4").decode("latin-1").splitlines()
(HERE / "iem-EDDM.csv").write_text("\n".join(ie))
mm = defaultdict(list)
for line in ie[1:]:
    p = line.split(",")
    if len(p) >= 3 and p[2]:
        try:
            mm[p[1][:10]].append(float(p[2]))
        except ValueError:
            pass
metar = {k: max(v) for k, v in mm.items() if len(v) >= 12}


def stat(e):
    n = len(e)
    if n < 2:
        return {"n": n}
    mean = sum(e) / n
    sd = (sum((x - mean) ** 2 for x in e) / (n - 1)) ** 0.5
    return {"mean": round(mean, 2), "se": round(sd / n ** 0.5, 2), "n": n}


WEEKS = [("13-19 Oct", "2026-10-13", "2026-10-19"), ("20-26 Oct", "2026-10-20", "2026-10-26"),
         ("27 Oct-2 Nov", "2026-10-27", "2026-11-02"), ("3-9 Nov", "2026-11-03", "2026-11-09")]
res = {}
for conv, p in pt.items():
    def err(days):
        return [metar[d] - p[d] for d in days if d in metar and d in p]
    res[conv] = {"p0335_days": stat(err(P0335)), "p0387_days": stat(err(P0387)),
                 "all_13oct_9nov": stat(err(sorted(set(p) & set(metar)))),
                 "weeks": {w: stat(err([d for d in sorted(p) if a <= d <= b])) for w, a, b in WEEKS},
                 "daily": {d: round(metar[d] - p[d], 1) for d in sorted(set(p) & set(metar))}}
(HERE / "results.json").write_text(json.dumps(res, indent=1))
print(json.dumps({c: {k: v for k, v in r.items() if k != "daily"} for c, r in res.items()}, indent=1))
