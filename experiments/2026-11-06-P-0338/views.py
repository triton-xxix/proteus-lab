"""P-0338: are the pages on the first-link walks ones people read?

Takes the 5 Nov walks P-0332 used for today (experiments/2026-11-05-philosophy/walks.json). For each page a
walk passes through (start page excluded, it is random and not a step), gets its October 2026 user views
from the Wikimedia pageviews API. A 404 means no recorded views, counted as 0 and reported.
Usage: python3 -I views.py WALKS.json OUT.json
"""
import json
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter

final, out = sys.argv[1], sys.argv[2]
DEADLINE = time.time() + 240
BASE = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/"
        "%s/monthly/2026100100/2026103100")
d = json.load(open(final))
date = d["at"]
rows = d["rows"]
through, steps = Counter(), 0
for r in rows:
    path = r.get("path") or []
    steps += max(len(path) - 1, 0)
    for page in set(path[1:]):
        through[page] += 1
visits = Counter()
for r in rows:
    visits.update((r.get("path") or [])[1:])


CACHE = "/Users/triton/PROTEUS/sandbox/p0338-views.json"
try:
    v = json.load(open(CACHE))
except (OSError, ValueError):
    v = {}
status = Counter({"cached": len(v)})
refused_in_a_row = 0
# One request at a time, hubs first: the first run at 4 threads got 80 of 395 and was throttled.
for title, _ in through.most_common():
    if title in v:
        continue
    if time.time() > DEADLINE:
        status["deadline"] += 1
        continue
    if refused_in_a_row >= 5:
        status["stopped after 5 refusals"] += 1
        continue
    url = BASE % urllib.parse.quote(title.replace(" ", "_"), safe="")
    req = urllib.request.Request(url, headers={"User-Agent": "ProteusLab-pageviews-check/1.0"})
    time.sleep(0.4)
    try:
        data = json.load(urllib.request.urlopen(req, timeout=30))
        v[title] = sum(i["views"] for i in data["items"])
        status["ok"] += 1
        refused_in_a_row = 0
    except urllib.error.HTTPError as e:
        if e.code == 404:
            v[title] = 0
            status["404"] += 1
        else:
            status["http %d" % e.code] += 1
            refused_in_a_row += 1
            time.sleep(3)
    except Exception as e:  # noqa: BLE001
        status[type(e).__name__] += 1
        refused_in_a_row += 1
        time.sleep(3)
json.dump(v, open(CACHE, "w"))
v = {t: n for t, n in v.items() if t in through}


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    out_r = [0.0] * len(xs)
    i = 0
    while i < len(xs):
        j = i
        while j + 1 < len(xs) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            out_r[order[k]] = (i + j) / 2
        i = j + 1
    return out_r


def spearman(a, b):
    ra, rb = ranks(a), ranks(b)
    ma, mb = statistics.mean(ra), statistics.mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return num / den


pages = sorted(v)
xs, ys = [v[p] for p in pages], [through[p] for p in pages]
total_visits = sum(visits[p] for p in pages)
low = sum(visits[p] for p in pages if v[p] < 1000)
multi = [p for p in pages if through[p] >= 2]
res = {
    "date": date, "walks": len(rows), "steps": steps, "pages": len(through), "views_found": len(v),
    "status": dict(status),
    "spearman_all_pages": round(spearman(xs, ys), 3),
    "spearman_pages_on_2plus_walks": round(spearman([v[p] for p in multi], [through[p] for p in multi]), 3) if len(multi) > 2 else None,
    "pages_on_2plus_walks": len(multi),
    "share_of_steps_under_1000_views": round(low / total_visits, 4) if total_visits else None,
    "share_of_pages_under_1000_views": round(sum(n < 1000 for n in xs) / len(xs), 4),
    "median_views_all_pages": statistics.median(xs),
    "top_hubs": [{"page": p, "walks_through": through[p], "october_views": v.get(p)} for p, _ in through.most_common(25)],
    "least_read_on_2plus_walks": [{"page": p, "walks_through": through[p], "october_views": v[p]}
                                  for p in sorted(multi, key=lambda p: v[p])[:15]],
}
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res, indent=1))
