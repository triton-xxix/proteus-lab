"""Score the 20 Nov NOAA Kp three-day forecast against observed rows (P-0505, D-030)."""
import json
import sys

HERE = "/Users/triton/PROTEUS/experiments/2026-11-23-P-0505/"
SNAP = "/Users/triton/PROTEUS/experiments/2026-11-20-kp-forecast-snapshot/forecast-2026-11-20T1243Z.json"

snap = json.load(open(SNAP))
obs_now = json.load(open(HERE + "kp-2026-11-23.json"))
if obs_now and isinstance(obs_now[0], list):  # old array-of-arrays shape
    hdr = obs_now[0]
    obs_now = [dict(zip(hdr, r)) for r in obs_now[1:]]

pred = {r["time_tag"]: float(r["kp"]) for r in snap if r["observed"] == "predicted"}
base_rows = [float(r["kp"]) for r in snap
             if r["observed"] == "observed" and "2026-11-13" <= r["time_tag"][:10] <= "2026-11-19"]
base_mean = sum(base_rows) / len(base_rows)
obs = {r["time_tag"]: float(r["kp"]) for r in obs_now if r.get("observed") == "observed"}

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
    "baseline_rows": len(base_rows),
    "baseline_mean": round(base_mean, 3),
    "observed_mean": round(sum(o for *_, o in rows) / n, 3),
    "forecast_mean": round(sum(p for _, p, _ in rows) / n, 3),
    "mae_noaa": round(mae(lambda p: p), 3),
    "mae_persistence_0.67": round(mae(lambda p: 0.67), 3),
    "mae_baseline_mean": round(mae(lambda p: base_mean), 3),
    "observed_max": max(o for *_, o in rows),
    "observed_ge5": [t for t, _, o in rows if o >= 5],
    "rows": rows,
}
res["pass"] = res["mae_noaa"] < res["mae_persistence_0.67"] and res["mae_noaa"] < res["mae_baseline_mean"]
json.dump(res, open(HERE + "results.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1))
