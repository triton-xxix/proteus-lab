"""P-0323: P-0317's Heathrow lead curve with observations it lacked. Day highs from Ogimet's SYNOP archive for
03772 (keyless, one call per month, 4 Nov 2026): the 18 UTC report's section 333 group 1snTxTxTx, the UK's 06 to
18 UTC maximum. Forecasts: ICON seamless as issued 0 to 6 days before (sandbox/om-prevruns-london-lead0-6.json,
P-0317's pull), maxed per Europe/London day. Same columns as P-0317.

    python3 -I experiments/2026-11-04-P-0323/lead_curve.py
"""
import json
import math
import time
import urllib.request
from collections import defaultdict

ROOT = "/Users/triton/PROTEUS"
UA = {"User-Agent": "proteus-research/1.0"}
MONTHS = [("202609010000", "202609302359"), ("202610010000", "202610312359")]

obs, raw_lines = {}, 0
for begin, end in MONTHS:
    url = "https://www.ogimet.com/cgi-bin/getsynop?block=03772&begin=%s&end=%s" % (begin, end)
    text = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read().decode("latin-1")
    open(ROOT + "/sandbox/ogimet-03772-%s.txt" % begin[:6], "w").write(text)
    for line in text.splitlines():
        parts = line.split(",")
        if len(parts) < 7 or parts[0] != "03772":
            continue
        raw_lines += 1
        if parts[4] != "18":
            continue
        groups = parts[6].replace("=", "").split()
        if "333" not in groups:
            continue
        sec = groups[groups.index("333") + 1:]
        if "555" in sec:
            sec = sec[:sec.index("555")]
        g = next((x for x in sec if len(x) == 5 and x[0] == "1" and x[1] in "01"), None)
        if g is None:
            continue
        v = int(g[2:]) / 10 * (-1 if g[1] == "1" else 1)
        obs["%s-%s-%s" % (parts[1], parts[2], parts[3])] = v
    time.sleep(2)
print("synop lines", raw_lines, "days with 18Z max", len(obs), min(obs), max(obs))

h = json.load(open(ROOT + "/sandbox/om-prevruns-london-lead0-6.json"))["hourly"]
LEADS = {0: "temperature_2m"}
LEADS.update({k: "temperature_2m_previous_day%d" % k for k in range(1, 7)})


def rnd(x):
    return int(math.floor(x + 0.5))


res = {"source": "previous-runs-api.open-meteo.com icon_seamless 51.47,-0.4543, daily max over local day",
       "station": "Ogimet SYNOP 03772 Heathrow, 18 UTC 333 1snTxTxTx (06 to 18 UTC max)",
       "synop_lines": raw_lines, "obs_days": len(obs), "obs_range": [min(obs), max(obs)], "leads": {}}
for k, var in LEADS.items():
    dd = defaultdict(list)
    for i, t in enumerate(h["time"]):
        if h[var][i] is not None:
            dd[t[:10]].append(h[var][i])
    rows = [(d, max(v), obs[d]) for d, v in sorted(dd.items()) if len(v) >= 23 and d in obs]
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
                       "se": round(sd / n ** 0.5, 2), "hit_plus0": hit(0.0), "hit_plus1": hit(1.0),
                       "best_correction": best / 10, "best_hit_in_sample": hit(best / 10),
                       "first_last": [rows[0][0], rows[-1][0]]}
    print(k, res["leads"][k], flush=True)
json.dump(res, open(ROOT + "/experiments/2026-11-04-P-0323/results.json", "w"), indent=1)
