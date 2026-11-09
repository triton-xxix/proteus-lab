"""P-0383, second attempt: ICON against METAR day highs at Gatwick and Heathrow, like for like.

Ogimet returned nothing at all for block 03776 (ogimet-03776-*.txt are empty), so the SYNOP comparison could not be made.
This uses Iowa State's keyless METAR archive (iem-EGKK.csv, iem-EGLL.csv, written by gatwick.py) and the icon_seamless previous-runs
pulls (om-icon.json for Gatwick, P-0382's heathrow entry). METAR highs are whole degrees and read below a SYNOP TX; both airports are
treated alike, so the difference between them is the number. METAR days are UTC, forecast days Europe/London; for a high that is under an hour's difference.
"""
import json
import pathlib
from collections import defaultdict

import numpy as np

HERE = pathlib.Path(__file__).parent
ROOT = "/Users/triton/PROTEUS"


def metar_highs(icao):
    m = defaultdict(list)
    for line in (HERE / f"iem-{icao}.csv").read_text().splitlines()[1:]:
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
    return {"mean": round(mean, 2), "sd": round(sd, 2), "se": round(sd / n ** 0.5, 2), "n": n}


k = metar_highs("EGKK")
l = metar_highs("EGLL")
g = json.load(open(HERE / "om-icon.json"))
h = json.load(open(f"{ROOT}/experiments/2026-11-09-P-0382/om-raw.json"))["heathrow"]
out = {"gatwick_model_point": [g["latitude"], g["longitude"]], "gatwick_model_elevation_m": g.get("elevation"), "leads": {}}
for lead, var in ((0, "temperature_2m"), (1, "temperature_2m_previous_day1")):
    gh, hh = highs(g, var), highs(h, var)
    days = sorted(set(gh) & set(hh) & set(k) & set(l) & {d for d in gh if "2026-09-01" <= d <= "2026-10-31"})
    ge = [k[d] - gh[d] for d in days]
    he = [l[d] - hh[d] for d in days]
    out["leads"][lead] = {"days": len(days), "first_last": [days[0], days[-1]], "gatwick_metar_minus_forecast": stat(ge),
                          "heathrow_metar_minus_forecast": stat(he), "gatwick_minus_heathrow": stat([a - b for a, b in zip(ge, he)]),
                          "corr_of_errors": round(float(np.corrcoef(ge, he)[0, 1]), 3)}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
