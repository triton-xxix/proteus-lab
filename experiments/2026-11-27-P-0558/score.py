"""Score the 24 Nov NOAA Kp three-day forecast against observed rows (P-0558, D-034). Method of P-0505."""
import json

HERE = "/Users/triton/PROTEUS/experiments/2026-11-27-P-0558/"
SNAP = "/Users/triton/PROTEUS/experiments/2026-11-24-kp-forecast-snapshot/forecast-2026-11-24.json"


def load(path):
    d = json.load(open(path))
    if d and isinstance(d[0], list):  # old array-of-arrays shape
        hdr = d[0]
        d = [dict(zip(hdr, r)) for r in d[1:]]
    return d


snap = load(SNAP)
obs_now = load(HERE + "kp-2026-11-27.json")

pred = {r["time_tag"]: float(r["kp"]) for r in snap if r["observed"] == "predicted"}
obs = {r["time_tag"]: float(r["kp"]) for r in obs_now if r.get("observed") == "observed"}

BASELINES = {"persistence_1.00": 1.00, "mean_17_23_nov_1.446": 1.446, "mean_23_nov_0.792": 0.792}

rows, missing = [], []
for t in sorted(pred):
    if t in obs:
        rows.append((t, pred[t], obs[t]))
    else:
        missing.append(t)

n = len(rows)
mae = lambda f: sum(abs(f(p) - o) for _, p, o in rows) / n
res = {
    "slots_predicted": len(pred),
    "slots_scored": n,
    "missing": missing,
    "observed_mean": round(sum(o for *_, o in rows) / n, 3),
    "forecast_mean": round(sum(p for _, p, _ in rows) / n, 3),
    "mae_noaa": round(mae(lambda p: p), 3),
    "mean_signed_error_noaa": round(sum(p - o for _, p, o in rows) / n, 3),
    "observed_max": max(o for *_, o in rows),
    "observed_ge5": [t for t, _, o in rows if o >= 5],
}
for name, v in BASELINES.items():
    res["mae_" + name] = round(mae(lambda p, v=v: v), 3)
res["pass"] = all(res["mae_noaa"] < res["mae_" + k] for k in BASELINES)
res["same_high_bias"] = res["mean_signed_error_noaa"] >= 0.5
res["rows"] = rows
json.dump(res, open(HERE + "results.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1))
