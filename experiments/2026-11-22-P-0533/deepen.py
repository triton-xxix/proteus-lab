"""P-0533: P-0532's Aurora detector, deepened. (1) Add en Geomagnetic_storm daily views as a second
signal (same spike rule: above twice the trailing 30-day median). (2) For the calm-day Aurora spikes,
the en Wikipedia top-read articles of that day that mention aurora, eclipse, comet, northern or sky,
plus the day's top 5, as a hint of what drove the spike. Keyless Wikimedia REST.

    python3 deepen.py
"""
import json, os, statistics, urllib.request
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "proteus-research/1.0 (keyless research script)"}
P32 = json.load(open("/Users/triton/PROTEUS/experiments/2026-11-22-P-0532/results.json"))["rows"]


def get(url):
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())


pv = get("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Geomagnetic_storm/daily/2023120100/2026112200")
gs = {i["timestamp"][:4] + "-" + i["timestamp"][4:6] + "-" + i["timestamp"][6:8]: i["views"] for i in pv["items"]}


def gspike(d):
    dd = date.fromisoformat(d)
    prev = [gs.get((dd - timedelta(k)).isoformat()) for k in range(1, 31)]
    prev = [p for p in prev if p is not None]
    return len(prev) >= 20 and gs.get(d, 0) > 2 * statistics.median(prev)


kp = {r["day"]: r["kp_max"] for r in P32}
for r in P32:
    nd = (date.fromisoformat(r["day"]) + timedelta(1)).isoformat()
    r["g_spike"], r["g_spike_next"] = gspike(r["day"]), gspike(nd)
storm = [r for r in P32 if r["kp_max"] >= 7]
a_only = sum(1 for r in storm if r["spike"] or r["spike_next"])
either = sum(1 for r in storm if r["spike"] or r["spike_next"] or r["g_spike"] or r["g_spike_next"])
g_only = sum(1 for r in storm if r["g_spike"] or r["g_spike_next"])


def calm(d):
    dd = date.fromisoformat(d)
    return max(kp.get(d, 0), kp.get((dd - timedelta(1)).isoformat(), 0)) < 5


a_calm = [r["day"] for r in P32 if r["spike"] and calm(r["day"])]
g_calm = [r["day"] for r in P32 if r["g_spike"] and calm(r["day"])]
union_calm = sorted(set(a_calm) | set(g_calm))
hints = {}
KEYS = ("aurora", "eclipse", "comet", "northern", "sky", "solar", "meteor", "moon")
for d in a_calm:
    y, m, dd = d.split("-")
    try:
        arts = get("https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/%s/%s/%s" % (y, m, dd))["items"][0]["articles"]
        hints[d] = {"top5": [a["article"] for a in arts[2:7]],
                    "sky_related": [(a["article"], a["views"]) for a in arts[:1000] if any(k in a["article"].lower() for k in KEYS)][:6]}
    except Exception as e:
        hints[d] = {"error": str(e)[:100]}
out = {"kp7_days": len(storm), "caught_aurora_only": a_only, "caught_geomagnetic_only": g_only, "caught_either": either,
       "calm_spikes_aurora": len(a_calm), "calm_spikes_geomagnetic": len(g_calm), "calm_spikes_either": len(union_calm),
       "calm_aurora_spike_hints": hints}
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
