"""P-0319: does ICON's Munich warm bias (obs minus forecast about +1.0 C on the day high) travel to Paris,
and does Meteo-France's own model (meteofrance_seamless, Arome/Arpege) carry it too?

Observations: Meteo-France open daily file, dept 75 (object.files.data.gouv.fr .../BASE/QUOT/
Q_75_latest-2025-2026_RR-T-Vent.csv.gz, keyless, pulled 4 Nov 2026), station 75114001 Paris-Montsouris, TX.
Forecasts: Open-Meteo previous-runs API, Montsouris 48.8217 2.3378, hourly temperature_2m and
previous_day1..3, models meteofrance_seamless and icon_seamless, 1 Sep to 2 Nov 2026, Europe/Paris,
one call 4 Nov 2026 (sandbox/om-prevruns-paris-mf-lead0-6.json), maxed per local day.

    python3 -I experiments/2026-11-04-P-0319/lead_bias.py
"""
import csv
import gzip
import io
import json
import math
import random
from collections import defaultdict

ROOT = "/Users/triton/PROTEUS"
S = ROOT + "/sandbox/"
text = gzip.decompress(open(S + "mf-q75-latest-2025-2026.csv.gz", "rb").read()).decode("latin-1")
rd = csv.DictReader(io.StringIO(text), delimiter=";")
obs = {}
cols = rd.fieldnames
for r in rd:
    if r["NUM_POSTE"].strip() == "75114001" and r.get("TX", "").strip():
        d = r["AAAAMMJJ"]
        obs["%s-%s-%s" % (d[:4], d[4:6], d[6:8])] = float(r["TX"].replace(",", "."))
print("columns", cols[:8], "... Montsouris TX days", len(obs), "last", max(obs) if obs else None)

h = json.load(open(S + "om-prevruns-paris-mf-lead0-6.json"))["hourly"]


def rnd(x):
    return int(math.floor(x + 0.5))


res = {"obs_source": "meteo.data.gouv.fr Q_75 latest-2025-2026, NUM_POSTE 75114001 TX",
       "fc_source": "previous-runs-api.open-meteo.com 48.8217,2.3378 hourly max per Europe/Paris day",
       "obs_days": len(obs), "obs_last": max(obs) if obs else None, "models": {}}
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
        hit = lambda c: round(sum(1 for _, f, o in rows if rnd(f + c) == rnd(o)) / n, 3)  # noqa: E731
        res["models"][model][k] = {"days": n, "mean_obs_minus_fc": round(mean, 2), "sd": round(sd, 2),
                                   "se": round(sd / n ** 0.5, 2), "mae": round(sum(abs(e) for e in errs) / n, 2),
                                   "hit_plus0": hit(0.0), "hit_plus1": hit(1.0),
                                   "hit_at_mean": hit(round(mean, 1))}
        errs_by[(model, k)] = dict((d, o - f) for d, f, o in rows)
        print(model, k, res["models"][model][k], flush=True)

# Paired sign-flip test at lead 1: is ICON minus Arome error difference real?
a, b = errs_by[("icon_seamless", 1)], errs_by[("meteofrance_seamless", 1)]
common = sorted(set(a) & set(b))
diffs = [a[d] - b[d] for d in common]
obsd = abs(sum(diffs) / len(diffs))
rng = random.Random(4)
more = sum(1 for _ in range(10000)
           if abs(sum(x if rng.random() < 0.5 else -x for x in diffs) / len(diffs)) >= obsd)
res["lead1_icon_minus_arome_bias"] = {"days": len(common), "diff": round(sum(diffs) / len(diffs), 2),
                                     "p_signflip": round(more / 10000, 4)}
print("lead1 icon minus arome mean error", res["lead1_icon_minus_arome_bias"])
json.dump(res, open(ROOT + "/experiments/2026-11-04-P-0319/results.json", "w"), indent=1)
