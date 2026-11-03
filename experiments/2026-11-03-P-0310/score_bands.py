"""P-0310: score the nightly ensemble bands the exchange already captures (exchange/icon_eps_band.jsonl,
exchange/ecmwf_ens_band.jsonl, one lead-1 row a night since P-0232 and P-0249) against the DWD 03379
Muenchen-Stadt high that then happened: in or out of the 10-90 band, miss distance, band width.

    python3 -I experiments/2026-11-03-P-0310/score_bands.py
"""
import importlib.util
import json
import statistics

ROOT = "/Users/triton/PROTEUS"
spec = importlib.util.spec_from_file_location(
    "mfe", ROOT + "/experiments/2026-10-13-watched-weather-markets/munich_forecast_error.py")
mfe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mfe)
obs = mfe.observed("10865")

res = {"station": "DWD 03379 Muenchen-Stadt TXK", "last_obs": max(obs), "books": {}}
for name in ("icon_eps_band", "ecmwf_ens_band"):
    rows = []
    for line in open(ROOT + "/exchange/%s.jsonl" % name):
        r = json.loads(line)
        o = obs.get(r["day"])
        if o is None:
            rows.append({"day": r["day"], "scored": False})
            continue
        lo, hi = r["p10"], r["p90"]
        miss = 0.0 if lo <= o <= hi else round(min(abs(o - lo), abs(o - hi)), 2)
        rows.append({"day": r["day"], "scored": True, "p10": lo, "p90": hi, "width": round(hi - lo, 2),
                     "obs": o, "inside": lo <= o <= hi, "miss": miss, "above": o > hi,
                     "obs_minus_p50": round(o - r["p50"], 2)})
    s = [x for x in rows if x["scored"]]
    res["books"][name] = {
        "rows": rows, "scored": len(s), "inside": sum(1 for x in s if x["inside"]),
        "above_p90": sum(1 for x in s if x["above"]),
        "width_median": statistics.median(x["width"] for x in s) if s else None,
        "abs_obs_minus_p50_median": statistics.median(abs(x["obs_minus_p50"]) for x in s) if s else None,
        "miss_median": statistics.median(x["miss"] for x in s) if s else None}
    b = res["books"][name]
    print(name, {k: v for k, v in b.items() if k != "rows"})
    for x in s:
        print("  ", x["day"], x["p10"], x["p90"], "obs", x["obs"], "in" if x["inside"] else "OUT")
json.dump(res, open(ROOT + "/experiments/2026-11-03-P-0310/results.json", "w"), indent=1)
