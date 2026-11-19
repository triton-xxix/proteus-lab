#!/usr/bin/env python3
"""Wikipedia top-1,000 half-life. Keyless, Wikimedia pageviews REST API, paced 2 s a call."""
import json, os, statistics, time, urllib.request
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
URL = "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/%04d/%02d/%02d"
LAST = date(2026, 11, 17)   # the 18th may not be complete yet
DAYS = 21                   # 7 earlier days so "new entrant" can be judged, then 14 to measure
SKIP = ("Special:", "Main_Page", "Wikipedia:", "Portal:", "File:", "Help:", "Category:", "Talk:")


def fetch(d):
    req = urllib.request.Request(URL % (d.year, d.month, d.day), headers={"User-Agent": "probe/1.0 (research script)"})
    for i in range(4):
        try:
            arts = json.loads(urllib.request.urlopen(req, timeout=30).read())["items"][0]["articles"]
            return [a["article"] for a in arts if not a["article"].startswith(SKIP)]
        except Exception as e:
            err = str(e)
            time.sleep(5 * (i + 1))
    raise SystemExit("fetch failed %s: %s" % (d, err))


days = [LAST - timedelta(days=DAYS - 1 - i) for i in range(DAYS)]
tops = []
for d in days:
    tops.append(set(fetch(d)))
    time.sleep(2)

# next-day survival over the last 14 day-pairs
pairs = [(days[i], len(tops[i] & tops[i + 1]) / len(tops[i])) for i in range(DAYS - 15, DAYS - 1)]
surv = [p for _, p in pairs]

# survival curve: share of day i's list still present k days later (present on day i+k, not necessarily all between)
curve = {}
for k in range(1, 8):
    vals = [len(tops[i] & tops[i + k]) / len(tops[i]) for i in range(7, DAYS - k)]
    curve[k] = round(statistics.mean(vals), 3)

# entrants: in the list on day i, absent on each of the 7 days before; run length = consecutive days present
runs, censored = [], 0
for i in range(7, DAYS - 1):
    seen_before = set().union(*tops[i - 7:i])
    for a in tops[i] - seen_before:
        n, j = 1, i + 1
        while j < DAYS and a in tops[j]:
            n, j = n + 1, j + 1
        if j == DAYS:
            censored += 1
        runs.append(n)
core = set.intersection(*tops)
out = {"last_day": str(LAST), "days_pulled": DAYS, "list_sizes": [len(t) for t in tops],
       "next_day_share_mean": round(statistics.mean(surv), 3), "next_day_share_min": round(min(surv), 3),
       "next_day_share_max": round(max(surv), 3), "next_day_pairs": [(str(d), round(p, 3)) for d, p in pairs],
       "share_still_listed_after_k_days": curve, "entrants": len(runs),
       "entrant_run_median_days": statistics.median(runs), "entrant_one_day_share": round(sum(1 for r in runs if r == 1) / len(runs), 3),
       "entrant_runs_cut_by_window_end": censored, "entrants_per_day": round(len(runs) / (DAYS - 8), 1),
       "in_all_%d_days" % DAYS: len(core)}
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps(out))
