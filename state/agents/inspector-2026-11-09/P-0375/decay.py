"""P-0375: does English Wikipedia interest in Nolan's films decay on one curve?

Daily pageviews (user agents only) for four films, keyless. Day 0 is the film's peak day inside the pull window,
which avoids assuming a release date. Ratio is day 30 over day 7, each smoothed as a 7-day centred mean so the
weekly cycle does not decide the answer. Leave-one-out: the other three films' mean ratio times this film's day 7
predicts its day 30.
"""
import json
import math
import pathlib
import statistics
import time
import urllib.request

HERE = pathlib.Path(__file__).parent
API = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/"
       "%s/daily/%s/%s")
FILMS = {
    "Dunkirk": ("Dunkirk_(2017_film)", "20170701", "20171031"),
    "Tenet": ("Tenet_(film)", "20200801", "20201130"),
    "Oppenheimer": ("Oppenheimer_(film)", "20230701", "20231031"),
    "The Odyssey": ("The_Odyssey_(2026_film)", "20260701", "20261107"),
}


def pull(article, start, end):
    url = API % (urllib.request.quote(article, safe="_"), start, end)
    req = urllib.request.Request(url, headers={"User-Agent": "ProteusLab/1.0 (research probe)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return [(i["timestamp"][:8], i["views"]) for i in json.load(r)["items"]]


def smooth(series, day):
    win = series[max(0, day - 3):day + 4]
    return sum(win) / len(win)


res = {}
for name, (art, a, b) in FILMS.items():
    rows = pull(art, a, b)
    v = [x[1] for x in rows]
    peak = max(range(len(v)), key=v.__getitem__)
    after = v[peak:]
    logs = [(math.log(d), math.log(after[d])) for d in range(3, min(61, len(after))) if after[d] > 0]
    mx = sum(x for x, _ in logs) / len(logs)
    my = sum(y for _, y in logs) / len(logs)
    k = sum((x - mx) * (y - my) for x, y in logs) / sum((x - mx) ** 2 for x, _ in logs)
    res[name] = {
        "days": len(v), "peak_date": rows[peak][0], "peak_views": v[peak], "days_after_peak": len(after) - 1,
        "day7": round(smooth(after, 7)), "day30": round(smooth(after, 30)),
        "day30_over_peak": round(smooth(after, 30) / v[peak], 4),
        "ratio_30_over_7": round(smooth(after, 30) / smooth(after, 7), 4),
        "power_law_k_days3_60": round(k, 3),
    }
    time.sleep(1)

names = list(res)
loo = {}
for name in names:
    others = [res[o]["ratio_30_over_7"] for o in names if o != name]
    pred = res[name]["day7"] * statistics.mean(others)
    err = pred / res[name]["day30"] - 1
    loo[name] = {"predicted_day30": round(pred), "actual_day30": res[name]["day30"], "error": round(err, 3),
                 "within_25pct": abs(err) <= 0.25}
out = {"films": res, "leave_one_out": loo, "within_25pct": sum(x["within_25pct"] for x in loo.values()),
       "ratio_mean": round(statistics.mean(r["ratio_30_over_7"] for r in res.values()), 4),
       "ratio_min": min(r["ratio_30_over_7"] for r in res.values()),
       "ratio_max": max(r["ratio_30_over_7"] for r in res.values())}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
