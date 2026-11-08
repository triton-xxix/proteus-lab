"""P-0367: ICON-D2 ensemble v global ICON ensemble for Munich's daily high, same call, same point as P-0232.

Prints each model's member count and 10/50/90 per day, beside DWD 03379 where observed and the band P-0232
committed for that day. Past days come from the API's past_days window: short-lead values, not the D-1
forecast the captured band was, which the README says plainly.
"""
import importlib.util, json, pathlib, urllib.error, urllib.request

HERE = pathlib.Path("/Users/triton/PROTEUS/experiments/2026-11-08-P-0367")
ROOT = "/Users/triton/PROTEUS"
BASE = ("https://ensemble-api.open-meteo.com/v1/ensemble?latitude=48.137&longitude=11.575&daily=temperature_2m_max"
        "&past_days=7&forecast_days=3&timezone=Europe%2FBerlin&models=")
MODELS = ["icon_d2", "icon_seamless"]


def pct(xs, q):
    xs = sorted(xs)
    k = (len(xs) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return round(xs[lo] + (xs[hi] - xs[lo]) * (k - lo), 2)


def fetch(model):
    try:
        with urllib.request.urlopen(BASE + model, timeout=40) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {"http_error": e.code, "body": e.read().decode()[:300]}


raw = {m: fetch(m) for m in MODELS}
(HERE / "raw.json").write_text(json.dumps(raw))

spec = importlib.util.spec_from_file_location("mfe", ROOT + "/experiments/2026-10-13-watched-weather-markets/munich_forecast_error.py")
mfe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mfe)
obs = mfe.observed("10865")
band = {}
for line in open(ROOT + "/exchange/icon_eps_band.jsonl"):
    r = json.loads(line)
    band[r["day"]] = r

days = {}
for m, d in raw.items():
    if "daily" not in d:
        print(m, "ERROR", d)
        continue
    daily = d["daily"]
    for i, day in enumerate(daily["time"]):
        mem = [daily[k][i] for k in daily if "member" in k and daily[k][i] is not None]
        days.setdefault(day, {})[m] = {"n": len(mem), "p10": pct(mem, .1), "p50": pct(mem, .5), "p90": pct(mem, .9)} if mem else {"n": 0}

out = []
for day in sorted(days):
    row = {"day": day, "obs": obs.get(day), "committed_p90": band.get(day, {}).get("p90"), **days[day]}
    a, b = row.get("icon_d2", {}), row.get("icon_seamless", {})
    row["d2_minus_global_p50"] = round(a["p50"] - b["p50"], 2) if a.get("n") and b.get("n") else None
    out.append(row)
    print(row)
(HERE / "results.json").write_text(json.dumps(out, indent=1))
both = [r["d2_minus_global_p50"] for r in out if r["d2_minus_global_p50"] is not None]
print("days with both models", len(both), "mean D2 minus global p50", round(sum(both) / len(both), 2) if both else None)
