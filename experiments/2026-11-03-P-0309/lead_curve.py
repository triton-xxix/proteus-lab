"""P-0309: P-0293's lead curve for a second model. ECMWF IFS 0.25 deg Munich hourly temperature as issued
0 to 6 days before (Open-Meteo previous-runs API, models=ecmwf_ifs025, one call 3 Nov 2026, timezone
Europe/Berlin, sandbox/om-prevruns-munich-ifs-lead0-6.json; the grid point is 48.25, 11.5), maxed per local
day, against DWD 03379 Muenchen-Stadt TXK, Sep and Oct 2026. Same columns as P-0293, plus the sd slope
(least squares over leads 0 to 6) for IFS and for ICON from P-0293's results.json.

    python3 -I experiments/2026-11-03-P-0309/lead_curve.py
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

raw = json.load(open(ROOT + "/sandbox/om-prevruns-munich-ifs-lead0-6.json"))
h = raw["hourly"]
LEADS = {0: "temperature_2m"}
LEADS.update({k: "temperature_2m_previous_day%d" % k for k in range(1, 7)})
obs = mfe.observed("10865")


def rnd(x):
    return int(math.floor(x + 0.5))


def slope(pairs):
    xs, ys = zip(*pairs)
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    return sum((x - mx) * (y - my) for x, y in pairs) / sum((x - mx) ** 2 for x in xs)


res = {"source": "previous-runs-api.open-meteo.com ecmwf_ifs025 48.1374,11.5755 (grid %s,%s), hourly, daily max over local day"
       % (raw["latitude"], raw["longitude"]), "station": "DWD 03379 Muenchen-Stadt TXK",
       "hours": len(h["time"]), "leads": {}}
for k, var in LEADS.items():
    dd = defaultdict(list)
    nulls = 0
    for i, t in enumerate(h["time"]):
        v = h[var][i]
        if v is None:
            nulls += 1
        else:
            dd[t[:10]].append(v)
    rows = [(d, max(v), obs[d]) for d, v in sorted(dd.items()) if len(v) >= 23 and d in obs]
    n = len(rows)
    if n < 2:
        res["leads"][k] = {"days": n, "nulls": nulls}
        print(k, "days", n, "nulls", nulls)
        continue
    errs = [o - f for _, f, o in rows]
    mean = sum(errs) / n
    sd = (sum((e - mean) ** 2 for e in errs) / (n - 1)) ** 0.5
    hit = lambda c: round(sum(1 for _, f, o in rows if rnd(f + c) == rnd(o)) / n, 3)  # noqa: E731
    best = max(range(-10, 31), key=lambda c: sum(1 for _, f, o in rows if rnd(f + c / 10) == rnd(o)))
    res["leads"][k] = {"days": n, "nulls": nulls, "mean_obs_minus_ifs": round(mean, 2), "sd": round(sd, 2),
                       "mae_after_plus1": round(sum(abs(e - 1.0) for e in errs) / n, 2),
                       "hit_plus0": hit(0.0), "hit_plus1": hit(1.0),
                       "best_correction": best / 10, "best_hit_in_sample": hit(best / 10),
                       "hit_at_mean_bias": hit(round(mean, 1))}
    print(k, res["leads"][k], flush=True)

icon = json.load(open(ROOT + "/experiments/2026-11-02-P-0293/results.json"))["leads"]
ifs_pairs = [(int(k), r["sd"]) for k, r in res["leads"].items() if "sd" in r]
icon_pairs = [(int(k), r["sd"]) for k, r in icon.items() if "sd" in r]
res["sd_slope_per_day"] = {"ifs": round(slope(ifs_pairs), 3), "icon": round(slope(icon_pairs), 3)}
print("sd slope per day of lead:", res["sd_slope_per_day"])
json.dump(res, open(ROOT + "/experiments/2026-11-03-P-0309/results.json", "w"), indent=1)
