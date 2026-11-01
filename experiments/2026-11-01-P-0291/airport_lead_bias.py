"""P-0291: P-0281 for the Munich airport. ICON seamless hourly at the airport grid point (Open-Meteo
previous-runs API, 48.3538,11.7861, latest, day-ahead and two-days runs, maxed per calendar day in
Europe/Berlin) against DWD 01262 Muenchen-Flughafen observed daily highs (TXK), Sep and Oct 2026,
with P-0281's city table read back beside it.

    python3 experiments/2026-11-01-P-0291/airport_lead_bias.py
"""
import importlib.util
import json
from collections import defaultdict

ROOT = "/Users/triton/PROTEUS"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


mfe = load("mfe", ROOT + "/experiments/2026-10-13-watched-weather-markets/munich_forecast_error.py")

src = json.load(open(ROOT + "/sandbox/om-prevruns-airport-hourly.json"))
h = src["hourly"]
LEADS = {"lead0_latest": "temperature_2m", "lead1_day_ahead": "temperature_2m_previous_day1",
         "lead2_two_days": "temperature_2m_previous_day2"}
daily = {k: defaultdict(list) for k in LEADS}
for i, t in enumerate(h["time"]):
    for k, var in LEADS.items():
        v = h[var][i]
        if v is not None:
            daily[k][t[:10]].append(v)
highs = {k: {d: max(v) for d, v in dd.items() if len(v) == 24} for k, dd in daily.items()}
obs = mfe.observed("10870")

# reuse P-0281's table() with the airport observations swapped in
p281_src = open(ROOT + "/experiments/2026-11-01-P-0281/lead_bias_by_month.py").read()
start = p281_src.index("def rnd(x):")
end = p281_src.index("res = {")
ns = {"math": __import__("math"), "obs": obs}
exec(p281_src[start:end], ns)
table = ns["table"]

city = json.load(open(ROOT + "/experiments/2026-11-01-P-0281/results.json"))
res = {"source": "previous-runs-api.open-meteo.com icon_seamless %s,%s (grid point), hourly, daily max over 24 hours Europe/Berlin"
       % (src["latitude"], src["longitude"]), "station": "DWD 01262 Muenchen-Flughafen TXK", "leads": {}}
for k in LEADS:
    res["leads"][k] = table(highs[k])
    c = city["leads"][k]["all"]
    a = res["leads"][k]["all"]
    print(f"{k:16s} airport bias {a['mean_obs_minus_icon']:+.2f} sd {a['sd']:.2f} n {a['days']} | city bias {c['mean_obs_minus_icon']:+.2f} sd {c['sd']:.2f}")
    for m, row in res["leads"][k]["months"].items():
        cm = city["leads"][k]["months"].get(m, {})
        print(f"   {m} airport {row['mean_obs_minus_icon']:+.2f} sd {row['sd']:.2f} best {row['best_correction']:+.1f} hit {row['best_hit']:.3f} hits {row['exact_degree_hit']}"
              f" | city {cm.get('mean_obs_minus_icon', 0):+.2f} hits {cm.get('exact_degree_hit')}")
json.dump(res, open(ROOT + "/experiments/2026-11-01-P-0291/results.json", "w"), indent=1)
