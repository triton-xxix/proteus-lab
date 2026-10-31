"""P-0275: ICON seamless (Open-Meteo historical forecast archive, latest run per day) against DWD 03379
Munich Stadt observed daily highs, Sep and Oct 2026, bias by month and the exact-degree hit rate under
corrections of 0, +0.5 and +1.0 C.

    python3 experiments/2026-10-31-P-0275/bias_by_month.py
"""
import importlib.util
import json
import math

ROOT = "/Users/triton/PROTEUS"
spec = importlib.util.spec_from_file_location(
    "mfe", ROOT + "/experiments/2026-10-13-watched-weather-markets/munich_forecast_error.py")
mfe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mfe)

fc = json.load(open(ROOT + "/sandbox/om-hist-icon-munich.json"))
icon = dict(zip(fc["daily"]["time"], fc["daily"]["temperature_2m_max"]))
obs = mfe.observed("10865")


def rnd(x):
    return int(math.floor(x + 0.5))


by = {}
for d, f in icon.items():
    if f is None or d not in obs:
        continue
    m = d[:7]
    by.setdefault(m, []).append((d, f, obs[d]))

res = {"source": "historical-forecast-api.open-meteo.com icon_seamless 48.137,11.575, latest archived run per day",
       "station": "DWD 03379 Muenchen-Stadt TXK", "months": {}}
for m, rows in sorted(by.items()):
    errs = [o - f for _, f, o in rows]
    n = len(rows)
    mean = sum(errs) / n
    sd = (sum((e - mean) ** 2 for e in errs) / (n - 1)) ** 0.5 if n > 1 else 0.0
    hits = {}
    for corr in (0.0, 0.5, 1.0, 1.5):
        hits["+%.1f" % corr] = round(sum(1 for _, f, o in rows if rnd(f + corr) == rnd(o)) / n, 3)
    best = max(range(-10, 31), key=lambda k: sum(1 for _, f, o in rows if rnd(f + k / 10) == rnd(o)))
    res["months"][m] = {"days": n, "mean_obs_minus_icon": round(mean, 2), "sd": round(sd, 2),
                        "mae_after_plus1": round(sum(abs(o - (f + 1.0)) for _, f, o in rows) / n, 2),
                        "exact_degree_hit": hits, "best_correction": best / 10,
                        "best_hit": round(sum(1 for _, f, o in rows if rnd(f + best / 10) == rnd(o)) / n, 3),
                        "first_last": [rows[0][0], rows[-1][0]]}
    print(m, res["months"][m], flush=True)
allrows = [r for rows in by.values() for r in rows]
res["all"] = {"days": len(allrows), "mean_obs_minus_icon": round(sum(o - f for _, f, o in allrows) / len(allrows), 2)}
json.dump(res, open(ROOT + "/experiments/2026-10-31-P-0275/results.json", "w"), indent=1)
print("all", res["all"])
