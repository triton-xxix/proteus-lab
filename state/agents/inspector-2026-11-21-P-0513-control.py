#!/usr/bin/env python3
"""P-0513: a control for P-0499. Each of P-0499's seven appointees is read on the other six vacancies'
day-before-appointment, against his own median of days -37 to -8 before that vacancy (P-0499's
baseline). Linked-but-not-appointed names could not be pulled keyless in the time (see README), so the
control is managers in the news that season who did not get that job. Keyless Wikimedia pageviews.
"""
import json, os, statistics, time, urllib.parse, urllib.request
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "probe/1.0 (research script)"}
P499 = json.load(open("/Users/triton/PROTEUS/experiments/2026-11-19-P-0499/results.json"))["rows"]


def get(url):
    for i in range(4):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read())
        except Exception as e:  # noqa: BLE001
            err = str(e)
            time.sleep(4 * (i + 1))
    raise SystemExit("failed %s: %s" % (url[:90], err))


def d(s):
    return date(int(s[:4]), int(s[5:7]), int(s[8:10]))


a, b = date(2025, 9, 1), date(2026, 4, 2)
series = {}
for r in P499:
    u = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/%s/daily/%s/%s" % (
        urllib.parse.quote(r["title"], safe=""), a.strftime("%Y%m%d"), b.strftime("%Y%m%d"))
    series[r["name"]] = {date(int(x["timestamp"][:4]), int(x["timestamp"][4:6]), int(x["timestamp"][6:8])): x["views"] for x in get(u)["items"]}
    time.sleep(1.5)

pairs = []
for vac in P499:
    v0, app = d(vac["vacancy"]), d(vac["appointed"])
    for m in P499:
        s = series[m["name"]]
        base = statistics.median(s.get(v0 - timedelta(days=k), 0) for k in range(8, 38)) or 1
        x = s.get(app - timedelta(days=1), 0) / base
        pairs.append({"vacancy": vac["club"] + " " + vac["vacancy"], "manager": m["name"], "appointee": m["name"] == vac["name"],
                      "base": base, "day_before_x": round(x, 2)})

ctrl = [p for p in pairs if not p["appointee"]]
own = [p for p in pairs if p["appointee"]]
summary = {"appointee_pairs": len(own), "appointee_over_3x": sum(p["day_before_x"] >= 3 for p in own),
           "appointee_median_x": statistics.median(p["day_before_x"] for p in own),
           "control_pairs": len(ctrl), "control_over_3x": sum(p["day_before_x"] >= 3 for p in ctrl),
           "control_median_x": statistics.median(p["day_before_x"] for p in ctrl),
           "control_over_3x_list": [(p["manager"], p["vacancy"], p["day_before_x"]) for p in ctrl if p["day_before_x"] >= 3]}
print(json.dumps(summary, indent=1))
json.dump({"summary": summary, "pairs": pairs}, open(os.path.join(HERE, "results.json"), "w"), indent=1)
