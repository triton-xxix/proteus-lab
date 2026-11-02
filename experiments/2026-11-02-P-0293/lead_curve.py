"""P-0293: P-0281 out to lead six. ICON seamless Munich hourly temperature as issued 0 to 6 days before
(Open-Meteo previous-runs API, one call 2 Nov 2026, sandbox/om-prevruns-munich-lead0-7.json; lead 7 came
back all null), maxed per Berlin calendar day, against DWD 03379 Muenchen-Stadt observed daily highs,
Sep and Oct 2026. Per lead: mean and sd of observed minus ICON, MAE after the +1.0 correction, the
exact-degree hit at +0.0 and +1.0, and the in-sample best correction's hit.

    python3 -I experiments/2026-11-02-P-0293/lead_curve.py
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

h = json.load(open(ROOT + "/sandbox/om-prevruns-munich-lead0-7.json"))["hourly"]
LEADS = {0: "temperature_2m"}
LEADS.update({k: "temperature_2m_previous_day%d" % k for k in range(1, 7)})
obs = mfe.observed("10865")


def rnd(x):
    return int(math.floor(x + 0.5))


res = {"source": "previous-runs-api.open-meteo.com icon_seamless 48.1374,11.5755, hourly, daily max over 24 hours Europe/Berlin",
       "station": "DWD 03379 Muenchen-Stadt TXK", "leads": {}}
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
    res["leads"][k] = {"days": n, "mean_obs_minus_icon": round(mean, 2), "sd": round(sd, 2),
                       "mae_after_plus1": round(sum(abs(e - 1.0) for e in errs) / n, 2),
                       "within_1_after_plus1": round(sum(1 for e in errs if abs(e - 1.0) <= 1.0) / n, 3),
                       "hit_plus0": hit(0.0), "hit_plus1": hit(1.0),
                       "best_correction": best / 10, "best_hit_in_sample": hit(best / 10),
                       "first_last": [rows[0][0], rows[-1][0]]}
    print(k, res["leads"][k], flush=True)
ok = [k for k, r in res["leads"].items() if r["hit_plus1"] >= 0.25]
res["last_lead_hit_plus1_ge_25pct"] = max(ok) if ok else None
res["leads_hit_plus1_ge_25pct"] = ok
print("leads with +1.0 hit >= 25 pct:", ok)
json.dump(res, open(ROOT + "/experiments/2026-11-02-P-0293/results.json", "w"), indent=1)
