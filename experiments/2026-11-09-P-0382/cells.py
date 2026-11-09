"""P-0382: does ICON's Heathrow offset stay put across neighbouring grid points?

Same observations and decode as P-0373 (Ogimet SYNOP 03772, 18 UTC 333 TX, Sep and Oct 2026). Forecast is icon_seamless from
Open-Meteo previous-runs at Heathrow's point and four points about 11 km N, S, E and W. Lead 0 and lead 1, same day set.
If the offset is the same everywhere the cause is not one bad cell (the observation or the region); if it moves, the cell matters.
"""
import json
import pathlib
import urllib.request
from collections import defaultdict

ROOT = "/Users/triton/PROTEUS"
HERE = pathlib.Path(__file__).parent
BASE = ("https://previous-runs-api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        "&hourly=temperature_2m,temperature_2m_previous_day1&start_date=2026-09-01&end_date=2026-10-31"
        "&timezone=Europe%2FLondon&models=icon_seamless")
UA = {"User-Agent": "proteus-research/1.0"}
POINTS = {"heathrow": (51.47, -0.4543), "north": (51.57, -0.4543), "south": (51.37, -0.4543),
          "west": (51.47, -0.6143), "east": (51.47, -0.2943)}

obs = {}
for name in ("202609", "202610"):
    for line in open(f"{ROOT}/sandbox/ogimet-03772-{name}.txt", encoding="latin-1"):
        parts = line.strip().split(",")
        if len(parts) < 7 or parts[0] != "03772" or parts[4] != "18":
            continue
        groups = parts[6].replace("=", "").split()
        if "333" not in groups:
            continue
        sec = groups[groups.index("333") + 1:]
        if "555" in sec:
            sec = sec[:sec.index("555")]
        g = next((x for x in sec if len(x) == 5 and x[0] == "1" and x[1] in "01"), None)
        if g:
            obs[f"{parts[1]}-{parts[2]}-{parts[3]}"] = int(g[2:]) / 10 * (-1 if g[1] == "1" else 1)


def stat(errs):
    n = len(errs)
    mean = sum(errs) / n
    sd = (sum((e - mean) ** 2 for e in errs) / (n - 1)) ** 0.5
    return {"mean_obs_minus_forecast": round(mean, 2), "sd": round(sd, 2), "se": round(sd / n ** 0.5, 2)}


raw = {}
for name, (lat, lon) in POINTS.items():
    d = json.loads(urllib.request.urlopen(urllib.request.Request(BASE.format(lat=lat, lon=lon), headers=UA), timeout=90).read())
    raw[name] = d
(HERE / "om-raw.json").write_text(json.dumps(raw))


def highs(d, var):
    h = d["hourly"]
    key = var if var in h else f"{var}_icon_seamless"
    dd = defaultdict(list)
    for t, v in zip(h["time"], h[key]):
        if v is not None:
            dd[t[:10]].append(v)
    return {k: max(v) for k, v in dd.items() if len(v) >= 23}


out = {"obs_days": len(obs), "points": {}, "leads": {}}
for name, d in raw.items():
    out["points"][name] = {"asked": POINTS[name], "got": [d["latitude"], d["longitude"]], "elevation_m": d.get("elevation")}
for lead, var in ((0, "temperature_2m"), (1, "temperature_2m_previous_day1")):
    tables = {n: highs(d, var) for n, d in raw.items()}
    days = sorted(set.intersection(*[set(t) for t in tables.values()]) & set(obs))
    row = {"days": len(days), "first_last": [days[0], days[-1]]}
    for n, t in tables.items():
        row[n] = stat([obs[x] - t[x] for x in days])
    base = tables["heathrow"]
    row["cell_minus_heathrow_mean"] = {n: round(sum(t[x] - base[x] for x in days) / len(days), 2) for n, t in tables.items()}
    out["leads"][lead] = row
(HERE / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
