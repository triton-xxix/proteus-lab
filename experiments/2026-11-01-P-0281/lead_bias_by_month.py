"""P-0281: P-0275 at lead one and two days. The ICON seamless Munich high as issued the day before
(Open-Meteo previous-runs API, hourly temperature_2m_previous_day1, maxed per calendar day in
Europe/Berlin) and two days before, against DWD 03379 Muenchen-Stadt observed daily highs, Sep and
Oct 2026. Same bias table as P-0275 (bias_by_month.py), one block per lead, so the three sit side by side.

    python3 experiments/2026-11-01-P-0281/lead_bias_by_month.py
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

src = json.load(open(ROOT + "/sandbox/om-prevruns-munich-hourly.json"))
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
obs = mfe.observed("10865")


def rnd(x):
    return int(math.floor(x + 0.5))


def table(icon):
    by = {}
    for d, f in sorted(icon.items()):
        if d in obs:
            by.setdefault(d[:7], []).append((d, f, obs[d]))
    months = {}
    for m, rows in sorted(by.items()):
        errs = [o - f for _, f, o in rows]
        n = len(rows)
        mean = sum(errs) / n
        sd = (sum((e - mean) ** 2 for e in errs) / (n - 1)) ** 0.5 if n > 1 else 0.0
        hits = {"+%.1f" % c: round(sum(1 for _, f, o in rows if rnd(f + c) == rnd(o)) / n, 3) for c in (0.0, 0.5, 1.0, 1.5)}
        best = max(range(-10, 31), key=lambda k: sum(1 for _, f, o in rows if rnd(f + k / 10) == rnd(o)))
        months[m] = {"days": n, "mean_obs_minus_icon": round(mean, 2), "sd": round(sd, 2),
                     "mae_after_plus1": round(sum(abs(o - (f + 1.0)) for _, f, o in rows) / n, 2),
                     "exact_degree_hit": hits, "best_correction": best / 10,
                     "best_hit": round(sum(1 for _, f, o in rows if rnd(f + best / 10) == rnd(o)) / n, 3),
                     "first_last": [rows[0][0], rows[-1][0]]}
    allrows = [r for rows in by.values() for r in rows]
    errs = [o - f for _, f, o in allrows]
    mean = sum(errs) / len(errs)
    return {"months": months, "all": {"days": len(allrows), "mean_obs_minus_icon": round(mean, 2),
                                      "sd": round((sum((e - mean) ** 2 for e in errs) / (len(errs) - 1)) ** 0.5, 2),
                                      "mae_after_plus1": round(sum(abs(e - 1.0) for e in errs) / len(errs), 2)}}


res = {"source": "previous-runs-api.open-meteo.com icon_seamless 48.1374,11.5755, hourly, daily max over 24 hours Europe/Berlin",
       "station": "DWD 03379 Muenchen-Stadt TXK", "leads": {}}
for k in LEADS:
    res["leads"][k] = table(highs[k])
    print(k, "all", res["leads"][k]["all"], flush=True)
    for m, row in res["leads"][k]["months"].items():
        print("  ", m, row, flush=True)
# how often does the day-ahead run differ from the latest by a whole degree or more
diffs = [highs["lead0_latest"][d] - highs["lead1_day_ahead"][d] for d in highs["lead1_day_ahead"] if d in highs["lead0_latest"]]
res["latest_minus_day_ahead"] = {"days": len(diffs), "mean": round(sum(diffs) / len(diffs), 2),
                                 "abs_mean": round(sum(abs(x) for x in diffs) / len(diffs), 2),
                                 "share_abs_ge_1": round(sum(1 for x in diffs if abs(x) >= 1.0) / len(diffs), 3)}
print("latest minus day-ahead", res["latest_minus_day_ahead"])
json.dump(res, open(ROOT + "/experiments/2026-11-01-P-0281/results.json", "w"), indent=1)
