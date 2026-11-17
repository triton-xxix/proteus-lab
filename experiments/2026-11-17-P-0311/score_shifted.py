"""P-0311: the P-0310 band scoring rerun with the 10-90 bands moved up by SHIFT C.
The +1.0 shift was chosen on 3 Nov from the first 11 scored days, so days after 2 Nov are out of sample
for it; both splits are reported.

    python3 -I experiments/2026-11-17-P-0311/score_shifted.py
"""
import importlib.util
import json
import statistics

ROOT = "/Users/triton/PROTEUS"
OUT = ROOT + "/experiments/2026-11-17-P-0311"
SHIFT = 1.0
CUTOFF = "2026-11-02"  # last observed day P-0310 could see
spec = importlib.util.spec_from_file_location(
    "mfe", ROOT + "/experiments/2026-10-13-watched-weather-markets/munich_forecast_error.py")
mfe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mfe)
obs = mfe.observed("10865")


def score(rows, shift):
    n = len(rows)
    inside = sum(1 for r in rows if r["p10"] + shift <= r["obs"] <= r["p90"] + shift)
    above = sum(1 for r in rows if r["obs"] > r["p90"] + shift)
    below = sum(1 for r in rows if r["obs"] < r["p10"] + shift)
    return {"n": n, "inside": inside, "above": above, "below": below,
            "rate": round(inside / n, 3) if n else None}


res = {"station": "DWD 03379 Muenchen-Stadt TXK", "last_obs": max(obs), "shift": SHIFT, "books": {}}
pooled = {"all": [], "oos": []}
for name in ("icon_eps_band", "ecmwf_ens_band"):
    rows = []
    for line in open(ROOT + "/exchange/%s.jsonl" % name):
        r = json.loads(line)
        o = obs.get(r["day"])
        if o is None:
            continue
        rows.append({"day": r["day"], "p10": r["p10"], "p50": r["p50"], "p90": r["p90"], "obs": o})
    oos = [r for r in rows if r["day"] > CUTOFF]
    pooled["all"] += rows
    pooled["oos"] += oos
    b = {"days": [r["day"] for r in rows],
         "unshifted": score(rows, 0.0), "shifted": score(rows, SHIFT),
         "oos_unshifted": score(oos, 0.0), "oos_shifted": score(oos, SHIFT),
         "median_obs_minus_p50": statistics.median(r["obs"] - r["p50"] for r in rows) if rows else None,
         "oos_median_obs_minus_p50": statistics.median(r["obs"] - r["p50"] for r in oos) if oos else None,
         "width_median": statistics.median(r["p90"] - r["p10"] for r in rows) if rows else None,
         "rows": rows}
    res["books"][name] = b
    print(name, {k: v for k, v in b.items() if k not in ("rows", "days")})
    for r in rows:
        print("  ", r["day"], r["p10"], r["p50"], r["p90"], "obs", r["obs"])
res["pooled"] = {k: {"unshifted": score(v, 0.0), "shifted": score(v, SHIFT)} for k, v in pooled.items()}
# best shift on all days, for the record (in sample)
grid = {}
for s10 in range(0, 31):
    s = s10 / 10
    grid[str(s)] = score(pooled["all"], s)["rate"]
res["shift_grid_all_days"] = grid
print("pooled", res["pooled"])
print("grid", grid)
json.dump(res, open(OUT + "/results.json", "w"), indent=1)
