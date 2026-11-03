"""P-0317: P-0307's lead curve at a third city, London Heathrow. ICON seamless hourly temperature as issued 0 to 6
days before (Open-Meteo previous-runs API, 51.47 -0.4543, Europe/London, sandbox/om-prevruns-london-lead0-6.json),
maxed per local day, against Meteostat bulk daily tmax for 03772 (sandbox/meteostat-03772.csv.gz; GHCN-daily has
TAVG only for Heathrow and nothing after Aug 2025). Same columns as P-0307. Caveat: Meteostat tmax is its own
aggregate of SYNOP/METAR, not the Met Office's official daily maximum."""
import csv, gzip, io, json, math
from collections import defaultdict

ROOT = "/Users/triton/PROTEUS"
h = json.load(open(ROOT + "/sandbox/om-prevruns-london-lead0-6.json"))["hourly"]
obs = {}
for r in csv.reader(io.TextIOWrapper(gzip.open(ROOT + "/sandbox/meteostat-03772.csv.gz"), "utf-8")):
    if r and r[0] >= "2026-09-01" and len(r) > 3 and r[3]:
        obs[r[0]] = float(r[3])  # columns: date, tavg, tmin, tmax, ...
LEADS = {0: "temperature_2m"}
LEADS.update({k: "temperature_2m_previous_day%d" % k for k in range(1, 7)})

def rnd(x):
    return int(math.floor(x + 0.5))

res = {"source": "previous-runs-api.open-meteo.com icon_seamless 51.47,-0.4543, hourly, daily max over 24 local hours",
       "station": "Meteostat 03772 London Heathrow tmax", "obs_days": len(obs),
       "obs_range": [min(obs), max(obs)] if obs else None, "leads": {}}
for k, var in LEADS.items():
    dd = defaultdict(list)
    for i, t in enumerate(h["time"]):
        v = h[var][i]
        if v is not None:
            dd[t[:10]].append(v)
    rows = [(d, max(v), obs[d]) for d, v in sorted(dd.items()) if len(v) >= 23 and d in obs]
    n = len(rows)
    if n < 2:
        res["leads"][k] = {"days": n}
        continue
    errs = [o - f for _, f, o in rows]
    mean = sum(errs) / n
    sd = (sum((e - mean) ** 2 for e in errs) / (n - 1)) ** 0.5
    hit = lambda c: round(sum(1 for _, f, o in rows if rnd(f + c) == rnd(o)) / n, 3)  # noqa: E731
    best = max(range(-10, 31), key=lambda c: sum(1 for _, f, o in rows if rnd(f + c / 10) == rnd(o)))
    res["leads"][k] = {"days": n, "mean_obs_minus_icon": round(mean, 2), "sd": round(sd, 2),
                       "hit_plus0": hit(0.0), "hit_plus1": hit(1.0),
                       "best_correction": best / 10, "best_hit_in_sample": hit(best / 10),
                       "first_last": [rows[0][0], rows[-1][0]]}
    print(k, res["leads"][k])
print("obs days", len(obs), res["obs_range"])
json.dump(res, open(ROOT + "/experiments/2026-11-03-P-0317/results.json", "w"), indent=1)
