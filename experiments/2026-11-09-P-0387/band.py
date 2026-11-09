"""P-0387: Munich deterministic ICON high against its own captured ICON-EPS 10 to 90 band.

Band: exchange/icon_eps_band.jsonl, ensemble-api for the city point at capture (normally the night before). Point: icon_seamless temperature_2m_previous_day1 at
48.137,11.575, daily max Europe/Berlin. Outcome: EDDM METAR highest temperature, Iowa State's keyless archive, UTC days. METAR is the settlement read since D-023.
"""
import json
import pathlib
import urllib.request
from collections import defaultdict

HERE = pathlib.Path(__file__).parent
ROOT = "/Users/triton/PROTEUS"
UA = {"User-Agent": "proteus-research/1.0"}


def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()


band = {}
for line in open(f"{ROOT}/exchange/icon_eps_band.jsonl"):
    r = json.loads(line)
    band[r["day"]] = r
days = sorted(band)
u = ("https://previous-runs-api.open-meteo.com/v1/forecast?latitude=48.137&longitude=11.575&hourly=temperature_2m_previous_day1"
     f"&start_date={days[0]}&end_date={days[-1]}&timezone=Europe%2FBerlin&models=icon_seamless")
om = json.loads(get(u))
(HERE / "om-prev.json").write_text(json.dumps(om))
h = om["hourly"]
key = next(k for k in h if k.startswith("temperature_2m_previous_day1"))
m = defaultdict(list)
for t, v in zip(h["time"], h[key]):
    if v is not None:
        m[t[:10]].append(v)
point = {k: max(v) for k, v in m.items() if len(v) >= 23}

ie = get("https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=EDDM&data=tmpc&year1=2026&month1=10&day1=25&year2=2026&month2=11&day2=10"
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
metar = {k: max(v) for k, v in mm.items() if len(v) >= 24}

rows, outside, above_band = [], 0, 0
for d in days:
    b = band[d]
    if d not in point:
        continue
    p = point[d]
    row = {"day": d, "point": round(p, 1), "p10": b["p10"], "p50": b["p50"], "p90": b["p90"], "control": b["control"], "metar": metar.get(d)}
    row["point_outside"] = p < b["p10"] or p > b["p90"]
    row["point_above_band"] = p > b["p90"]
    rows.append(row)
scored = [r for r in rows if r["metar"] is not None]


def mae(k):
    return round(sum(abs(r["metar"] - r[k]) for r in scored) / len(scored), 2)


def bias(k):
    return round(sum(r["metar"] - r[k] for r in scored) / len(scored), 2)


res = {"days_with_band_and_point": len(rows), "scored_against_metar": len(scored), "point_outside_band": sum(r["point_outside"] for r in rows),
       "point_above_band": sum(r["point_above_band"] for r in rows), "mae": {k: mae(k) for k in ("point", "p50", "control")},
       "bias_metar_minus": {k: bias(k) for k in ("point", "p50", "control")}, "outside_rows": [r for r in rows if r["point_outside"]], "all": rows}
res["point_closer_than_p50"] = sum(abs(r["metar"] - r["point"]) < abs(r["metar"] - r["p50"]) for r in scored)
res["p50_closer_than_point"] = sum(abs(r["metar"] - r["p50"]) < abs(r["metar"] - r["point"]) for r in scored)
res["metar_inside_band"] = sum(r["p10"] <= r["metar"] <= r["p90"] for r in scored)
out = [r for r in scored if r["point_outside"]]
res["on_outside_days_point_closer"] = sum(abs(r["metar"] - r["point"]) < abs(r["metar"] - r["p50"]) for r in out)
res["on_outside_days_p50_closer"] = sum(abs(r["metar"] - r["p50"]) < abs(r["metar"] - r["point"]) for r in out)
(HERE / "results.json").write_text(json.dumps(res, indent=1))
print(json.dumps({k: v for k, v in res.items() if k != "all"}, indent=1))
