"""P-0303: is the Munich ensemble as wide as the error says it should be? Tonight's ICON-EPS (40 members) and
ECMWF IFS (51) hourly forecasts for the city point (one call, sandbox/om-ens-munich-2026-11-02.json), maxed per
member per Berlin day, p10 to p90 width of the daily high for 3 to 8 Nov (leads 1 to 6 from a 2 Nov run).
A calibrated 10-90 band on a normal error is 2.56 sd wide, so each width is set against 2.56 x the sd P-0293
measured for ICON's deterministic high at that lead (city, 61 days). One night, one run: a reading, not a rate.

    python3 -I experiments/2026-11-02-P-0303/spread.py
"""
import json
from collections import defaultdict

ROOT = "/Users/triton/PROTEUS"
h = json.load(open(ROOT + "/sandbox/om-ens-munich-2026-11-02.json"))["hourly"]
sd = {int(k): v["sd"] for k, v in json.load(open(ROOT + "/experiments/2026-11-02-P-0293/results.json"))["leads"].items()}
days = sorted({t[:10] for t in h["time"]})


def q(xs, p):
    xs = sorted(xs)
    i = p * (len(xs) - 1)
    lo = int(i)
    return xs[lo] + (xs[min(lo + 1, len(xs) - 1)] - xs[lo]) * (i - lo)


res = {"run_pulled": "2026-11-02 about 23:45 UTC", "point": "48.137,11.575", "models": {}}
for model in ("icon_seamless_eps", "ecmwf_ifs025_ensemble"):
    keys = [k for k in h if k.startswith("temperature_2m") and k.endswith(model)]
    out = {"members": len(keys), "leads": {}}
    for lead, d in enumerate(days[:6], start=1):
        highs = []
        for k in keys:
            vals = [v for t, v in zip(h["time"], h[k]) if t.startswith(d) and v is not None]
            if len(vals) == 24:
                highs.append(max(vals))
        if len(highs) < 10:
            out["leads"][lead] = {"day": d, "members_with_24h": len(highs)}
            continue
        w = q(highs, 0.9) - q(highs, 0.1)
        want = 2.56 * sd[lead]
        out["leads"][lead] = {"day": d, "members_with_24h": len(highs), "median": round(q(highs, 0.5), 2),
                              "p10": round(q(highs, 0.1), 2), "p90": round(q(highs, 0.9), 2),
                              "width": round(w, 2), "calibrated_width": round(want, 2),
                              "ratio": round(w / want, 2)}
    res["models"][model] = out
    print(model, out["members"], "members")
    for lead, r in out["leads"].items():
        print("  lead", lead, r)
json.dump(res, open(ROOT + "/experiments/2026-11-02-P-0303/results.json", "w"), indent=1)
