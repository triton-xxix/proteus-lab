#!/usr/bin/env python3
"""Does the incoming manager's Wikipedia article climb before his appointment is announced?
Keyless: MediaWiki search to settle each title, Wikimedia per-article daily pageviews, paced 1.5 s."""
import json, os, statistics, time, urllib.parse, urllib.request
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "probe/1.0 (research script)"}
# name, search words, club, vacancy date, appointment date: from P-0489's changes-section.txt (2025-26 table)
ROWS = [("Sean Dyche", "Sean Dyche football manager", "Nottingham Forest", date(2025, 10, 18), date(2025, 10, 21)),
        ("Rob Edwards", "Rob Edwards footballer born 1982 manager", "Wolverhampton Wanderers", date(2025, 11, 2), date(2025, 11, 12)),
        ("Liam Rosenior", "Liam Rosenior football manager", "Chelsea", date(2026, 1, 1), date(2026, 1, 8)),
        ("Michael Carrick", "Michael Carrick footballer", "Manchester United", date(2026, 1, 5), date(2026, 1, 13)),
        ("Igor Tudor", "Igor Tudor football manager", "Tottenham Hotspur", date(2026, 2, 11), date(2026, 2, 14)),
        ("Vitor Pereira", "Vitor Pereira footballer born 1968 manager", "Nottingham Forest", date(2026, 2, 12), date(2026, 2, 15)),
        ("Roberto De Zerbi", "Roberto De Zerbi football manager", "Tottenham Hotspur", date(2026, 3, 29), date(2026, 3, 31))]


def get(url):
    for i in range(4):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read())
        except Exception as e:
            err = str(e)
            time.sleep(4 * (i + 1))
    raise SystemExit("failed %s: %s" % (url[:90], err))


def title(words):
    u = "https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srlimit=1&srsearch=" + urllib.parse.quote(words)
    return get(u)["query"]["search"][0]["title"].replace(" ", "_")


def views(t, a, b):
    u = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/%s/daily/%s/%s" % (
        urllib.parse.quote(t, safe=""), a.strftime("%Y%m%d"), b.strftime("%Y%m%d"))
    return {date(int(x["timestamp"][:4]), int(x["timestamp"][4:6]), int(x["timestamp"][6:8])): x["views"] for x in get(u)["items"]}


out = []
for name, words, club, vac, app in ROWS:
    t = title(words)
    time.sleep(1.5)
    v = views(t, vac - timedelta(days=37), app + timedelta(days=1))
    time.sleep(1.5)
    base = statistics.median(v.get(vac - timedelta(days=k), 0) for k in range(8, 38))  # days -37 to -8 before the vacancy
    wk = [v.get(vac - timedelta(days=k), 0) for k in range(1, 8)]                       # the week before the vacancy
    gap = [(vac + timedelta(days=k)) for k in range((app - vac).days)]                  # vacancy day to the day before appointment
    gapv = [v.get(d, 0) for d in gap]
    r = {"name": name, "title": t, "club": club, "vacancy": str(vac), "appointed": str(app), "gap_days": len(gap),
         "base_median": base, "week_before_vacancy_max_x": round(max(wk) / base, 2),
         "week_before_vacancy_median_x": round(statistics.median(wk) / base, 2),
         "gap_views": gapv, "gap_max_x": round(max(gapv) / base, 2), "day_before_x": round(gapv[-1] / base, 2),
         "vacancy_day_x": round(gapv[0] / base, 2), "appointment_day_x": round(v.get(app, 0) / base, 2),
         "first_gap_day_over_3x": next((i for i, x in enumerate(gapv) if x >= 3 * base), None)}
    out.append(r)
    print(name, t, "base", base, "wk-before max x", r["week_before_vacancy_max_x"], "gap x", [round(x / base, 1) for x in gapv],
          "appt day x", r["appointment_day_x"])
summary = {"n": len(out), "day_before_x_median": statistics.median(r["day_before_x"] for r in out),
           "day_before_over_3x": sum(1 for r in out if r["day_before_x"] >= 3),
           "gap_max_over_3x": sum(1 for r in out if r["gap_max_x"] >= 3),
           "vacancy_day_over_3x": sum(1 for r in out if r["vacancy_day_x"] >= 3),
           "week_before_vacancy_over_2x": sum(1 for r in out if r["week_before_vacancy_max_x"] >= 2),
           "appointment_day_x_median": statistics.median(r["appointment_day_x"] for r in out)}
json.dump({"rows": out, "summary": summary}, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps(summary))
