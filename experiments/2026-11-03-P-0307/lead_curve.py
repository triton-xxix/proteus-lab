"""P-0307: P-0293's lead curve at a second city. ICON seamless Berlin-Tempelhof hourly temperature as
issued 0 to 6 days before (Open-Meteo previous-runs API, one call 3 Nov 2026, timezone Europe/Berlin,
sandbox/om-prevruns-berlin-lead0-6.json), maxed per local day, against DWD 00433 Berlin-Tempelhof
observed daily highs (TXK), Sep and Oct 2026. Same columns as P-0293.

    python3 -I experiments/2026-11-03-P-0307/lead_curve.py
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
mfe.DWD_IDS["10384"] = "00433"  # WMO Berlin-Tempelhof -> DWD station id

h = json.load(open(ROOT + "/sandbox/om-prevruns-berlin-lead0-6.json"))["hourly"]
LEADS = {0: "temperature_2m"}
LEADS.update({k: "temperature_2m_previous_day%d" % k for k in range(1, 7)})
obs = mfe.observed("10384")


def rnd(x):
    return int(math.floor(x + 0.5))


res = {"source": "previous-runs-api.open-meteo.com icon_seamless 52.4675,13.4021, hourly, daily max over 24 local hours",
       "station": "DWD 00433 Berlin-Tempelhof TXK", "leads": {}}
for k, var in LEADS.items():
    dd = defaultdict(list)
    for i, t in enumerate(h["time"]):
        v = h[var][i]
        if v is not None:
            dd[t[:10]].append(v)
    rows = [(d, max(v), obs[d]) for d, v in sorted(dd.items()) if len(v) == 24 and d in obs]
    n = len(rows)
    if n < 2:
        res["leads"][k] = {"days": n}
        print(k, "days", n)
        continue
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
ok = [k for k, r in res["leads"].items() if r.get("hit_plus1", 0) >= 0.25]
res["leads_hit_plus1_ge_25pct"] = ok
print("leads with +1.0 hit >= 25 pct:", ok)
json.dump(res, open(ROOT + "/experiments/2026-11-03-P-0307/results.json", "w"), indent=1)
