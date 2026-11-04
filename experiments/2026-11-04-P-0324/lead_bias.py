"""P-0324: P-0319's method at Strasbourg-Entzheim. Observed TX from the Meteo-France dept 67 daily file
(OVH URL from the data.gouv.fr dataset API, pulled 4 Nov 2026), station picked by name ENTZHEIM. Forecasts: one
Open-Meteo previous-runs call at 48.5494 7.6400, meteofrance_seamless and icon_seamless, leads 0 to 3,
1 Sep to 2 Nov 2026, Europe/Paris, maxed per local day (sandbox/om-prevruns-strasbourg-mf.json).

    python3 -I experiments/2026-11-04-P-0324/lead_bias.py
"""
import csv
import gzip
import io
import json
import random
from collections import defaultdict

ROOT = "/Users/triton/PROTEUS"
S = ROOT + "/sandbox/"
rd = csv.DictReader(io.StringIO(gzip.decompress(open(S + "mf-q67-latest-2025-2026.csv.gz", "rb").read()).decode("latin-1")),
                    delimiter=";")
obs, station = {}, None
for r in rd:
    if "ENTZHEIM" in r["NOM_USUEL"] and r.get("TX", "").strip():
        station = (r["NUM_POSTE"].strip(), r["NOM_USUEL"].strip(), r["LAT"], r["LON"])
        d = r["AAAAMMJJ"]
        obs["%s-%s-%s" % (d[:4], d[4:6], d[6:8])] = float(r["TX"].replace(",", "."))
print("station", station, "TX days", len(obs), "last", max(obs))

h = json.load(open(S + "om-prevruns-strasbourg-mf.json"))["hourly"]
res = {"station": station, "obs_days": len(obs), "obs_last": max(obs), "models": {}}
errs_by = {}
for model in ("icon_seamless", "meteofrance_seamless"):
    res["models"][model] = {}
    for k in range(4):
        var = ("temperature_2m" if k == 0 else "temperature_2m_previous_day%d" % k) + "_" + model
        dd = defaultdict(list)
        for i, t in enumerate(h["time"]):
            if h[var][i] is not None:
                dd[t[:10]].append(h[var][i])
        rows = [(d, max(v), obs[d]) for d, v in sorted(dd.items()) if len(v) >= 23 and d in obs]
        n = len(rows)
        errs = [o - f for _, f, o in rows]
        mean = sum(errs) / n
        sd = (sum((e - mean) ** 2 for e in errs) / (n - 1)) ** 0.5
        res["models"][model][k] = {"days": n, "mean_obs_minus_fc": round(mean, 2), "sd": round(sd, 2),
                                   "se": round(sd / n ** 0.5, 2), "mae": round(sum(abs(e) for e in errs) / n, 2)}
        errs_by[(model, k)] = dict((d, o - f) for d, f, o in rows)
        print(model, k, res["models"][model][k], flush=True)

a, b = errs_by[("icon_seamless", 1)], errs_by[("meteofrance_seamless", 1)]
diffs = [a[d] - b[d] for d in sorted(set(a) & set(b))]
m = abs(sum(diffs) / len(diffs))
rng = random.Random(4)
more = sum(1 for _ in range(10000) if abs(sum(x if rng.random() < 0.5 else -x for x in diffs) / len(diffs)) >= m)
res["lead1_icon_minus_mf"] = {"days": len(diffs), "diff": round(sum(diffs) / len(diffs), 2), "p_signflip": more / 10000}
print(res["lead1_icon_minus_mf"])
json.dump(res, open(ROOT + "/experiments/2026-11-04-P-0324/results.json", "w"), indent=1)
