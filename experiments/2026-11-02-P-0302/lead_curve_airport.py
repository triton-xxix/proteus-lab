"""P-0302: P-0293 for the Munich airport. ICON seamless hourly temperature at the airport grid point as issued
0 to 6 days before (Open-Meteo previous-runs API, one call 2 Nov 2026, 48.3538,11.7861, returned grid
48.3469,11.7705; sandbox/om-prevruns-airport-lead0-6.json), maxed per Berlin calendar day, against DWD 01262
Muenchen-Flughafen observed daily highs, Sep and Oct 2026. Per lead: mean and sd of observed minus ICON, the
exact-degree hit at +0.0, +0.3 (the nightly's airport correction) and +1.0, and the in-sample best correction.

    python3 -I experiments/2026-11-02-P-0302/lead_curve_airport.py
"""
import importlib.util
import json
import math
from collections import defaultdict

ROOT = "/Users/triton/PROTEUS"
spec = importlib.util.spec_from_file_location(
    "mfe", ROOT + "/experiments/2026-10-13-watched-weather-markets/munich_forecast_error.py")
mfe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mfe)

h = json.load(open(ROOT + "/sandbox/om-prevruns-airport-lead0-6.json"))["hourly"]
LEADS = {0: "temperature_2m"}
LEADS.update({k: "temperature_2m_previous_day%d" % k for k in range(1, 7)})
obs = mfe.observed("10870")
city = json.load(open(ROOT + "/experiments/2026-11-02-P-0293/results.json"))["leads"]


def rnd(x):
    return int(math.floor(x + 0.5))


res = {"source": "previous-runs-api.open-meteo.com icon_seamless 48.3538,11.7861 (grid 48.3469,11.7705), hourly, daily max over 24 hours Europe/Berlin",
       "station": "DWD 01262 Muenchen-Flughafen TXK", "leads": {}}
for k, var in LEADS.items():
    dd = defaultdict(list)
    for i, t in enumerate(h["time"]):
        v = h[var][i]
        if v is not None:
            dd[t[:10]].append(v)
    rows = [(d, max(v), obs[d]) for d, v in sorted(dd.items()) if len(v) == 24 and d in obs]
    n = len(rows)
    errs = [o - f for _, f, o in rows]
    mean = sum(errs) / n
    sd = (sum((e - mean) ** 2 for e in errs) / (n - 1)) ** 0.5
    hit = lambda c: round(sum(1 for _, f, o in rows if rnd(f + c) == rnd(o)) / n, 3)  # noqa: E731
    best = max(range(-10, 31), key=lambda c: sum(1 for _, f, o in rows if rnd(f + c / 10) == rnd(o)))
    c = city.get(str(k), {})
    res["leads"][k] = {"days": n, "mean_obs_minus_icon": round(mean, 2), "sd": round(sd, 2),
                       "hit_plus0": hit(0.0), "hit_plus03": hit(0.3), "hit_plus1": hit(1.0),
                       "best_correction": best / 10, "best_hit_in_sample": hit(best / 10),
                       "city_sd": c.get("sd"), "city_hit_plus1": c.get("hit_plus1"),
                       "first_last": [rows[0][0], rows[-1][0]]}
    print(k, res["leads"][k], flush=True)
ok = [k for k, r in res["leads"].items() if r["hit_plus03"] >= 0.25]
res["last_lead_hit_plus03_ge_25pct"] = max(ok) if ok else None
res["leads_hit_plus03_ge_25pct"] = ok
print("leads with +0.3 hit >= 25 pct:", ok)
json.dump(res, open(ROOT + "/experiments/2026-11-02-P-0302/results.json", "w"), indent=1)
