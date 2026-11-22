"""P-0532: are en Wikipedia Aurora pageviews a free geomagnetic storm detector?

Kp: GFZ Potsdam keyless JSON (kp.gfz.de/app/json, CC BY 4.0), three-hourly, 1 Jan 2024 to 21 Nov 2026,
reduced to the daily maximum. Views: Wikimedia REST per-article daily, en.wikipedia, all-access, user.
A spike = views above twice the trailing 30-day median (the 30 days before, not including the day).

    python3 aurora.py
"""
import json, os, statistics, urllib.request
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "proteus-research/1.0 (keyless research script)"}


def get(url):
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())


kp = get("https://kp.gfz.de/app/json/?start=2024-01-01T00:00:00Z&end=2026-11-21T21:00:00Z&index=Kp")
kpmax = {}
for t, v in zip(kp["datetime"], kp["Kp"]):
    if v is not None and v >= 0:
        d = t[:10]
        kpmax[d] = max(kpmax.get(d, 0), v)
pv = get("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Aurora/daily/2023120100/2026112100")
views = {i["timestamp"][:4] + "-" + i["timestamp"][4:6] + "-" + i["timestamp"][6:8]: i["views"] for i in pv["items"]}

days = sorted(d for d in kpmax if d in views)
rows = []
for d in days:
    dd = date.fromisoformat(d)
    prev = [views.get((dd - timedelta(k)).isoformat()) for k in range(1, 31)]
    prev = [p for p in prev if p is not None]
    nxt = views.get((dd + timedelta(1)).isoformat())
    med = statistics.median(prev) if len(prev) >= 20 else None
    rows.append({"day": d, "kp_max": kpmax[d], "views": views[d], "next_views": nxt, "median30": med,
                 "spike": bool(med) and views[d] > 2 * med,
                 "spike_next": bool(med) and nxt is not None and nxt > 2 * med})


def corr(xs, ys):
    return round(statistics.correlation(xs, ys), 3)


same = [r for r in rows]
nx = [r for r in rows if r["next_views"] is not None]
storm = [r for r in rows if r["kp_max"] >= 7]
storm5 = [r for r in rows if r["kp_max"] >= 5]
calm = [r for r in rows if r["kp_max"] < 5]
spikes = [r for r in rows if r["spike"] or r["spike_next"]]
out = {"days": len(rows), "first": days[0], "last": days[-1],
       "corr_same_day_kp_views": corr([r["kp_max"] for r in same], [r["views"] for r in same]),
       "corr_kp_next_day_views": corr([r["kp_max"] for r in nx], [r["next_views"] for r in nx]),
       "corr_kp_log_next_views": corr([r["kp_max"] for r in nx], [__import__("math").log(r["next_views"] + 1) for r in nx]),
       "kp7_days": len(storm), "kp7_with_spike_same_or_next": sum(1 for r in storm if r["spike"] or r["spike_next"]),
       "kp5_days": len(storm5), "kp5_with_spike_same_or_next": sum(1 for r in storm5 if r["spike"] or r["spike_next"]),
       "spike_days_any": len(spikes), "spike_days_with_kp5_same_or_previous_day": None,
       "kp7_list": [(r["day"], r["kp_max"], r["views"], r["next_views"], r["median30"]) for r in storm]}
spike_days = {r["day"] for r in rows if r["spike"]}
hit = 0
for d in spike_days:
    dd = date.fromisoformat(d)
    if max(kpmax.get(d, 0), kpmax.get((dd - timedelta(1)).isoformat(), 0)) >= 5:
        hit += 1
out["view_spike_days"] = len(spike_days)
out["spike_days_with_kp5_same_or_previous_day"] = hit
out["false_alarm_spikes_calm"] = len(spike_days) - hit
json.dump({"summary": out, "rows": rows}, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
