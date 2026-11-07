"""P-0339: P-0338's question, answered with 50 titles per request instead of one.

The Wikimedia REST pageviews API (one title per call) gave 429 after 92 pages on 6 Nov. The Wikipedia
Action API's prop=pageviews (PageViewInfo) takes up to 50 titles per call and returns daily user views for
the last pvipdays (max 60), so 395 pages is 8 calls plus continuations. October 2026 is summed from the
daily rows. The 12 REST values cached by P-0338 are used only as a cross-check of the two sources.
Usage: python3 -I views_batch.py WALKS.json OUT.json
"""
import json
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter

walks_file, out = sys.argv[1], sys.argv[2]
API = "https://en.wikipedia.org/w/api.php"
UA = {"User-Agent": "ProteusLab-pageviews-check/1.1"}
d = json.load(open(walks_file))
rows = d["rows"]
through, visits, steps = Counter(), Counter(), 0
for r in rows:
    path = r.get("path") or []
    steps += max(len(path) - 1, 0)
    for page in set(path[1:]):
        through[page] += 1
    visits.update(path[1:])

titles = list(through)
v, nulldays, calls, missing = {}, Counter(), 0, []
refusals = 0  # Python's urllib got 429 on every call (ua_test.py); curl fetched the files (make_curl.py)
conts = 0
for n in range(20):
    for data in [json.load(open("/Users/triton/PROTEUS/sandbox/p0339/batch%02d.json" % n))]:
        calls += 1
        conts += "continue" in data
        norm = {n["to"]: n["from"] for n in data.get("query", {}).get("normalized", [])}
        for p in data.get("query", {}).get("pages", []):
            t = norm.get(p["title"], p["title"])
            if p.get("missing"):
                missing.append(t)
                continue
            pv = p.get("pageviews")
            if pv is None:
                continue
            octo = {k: n for k, n in pv.items() if k.startswith("2026-10-")}
            if len(octo) < 31:
                continue
            nulldays[t] = sum(n is None for n in octo.values())
            v[t] = sum(n or 0 for n in octo.values())

rest = json.load(open("/Users/triton/PROTEUS/sandbox/p0338-views.json"))
cross = [{"page": t, "rest": rest[t], "action": v.get(t)} for t in rest]
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
    "walks_at": d.get("at"), "walks": len(rows), "steps": steps, "pages": len(through),
    "views_found": len(v), "calls": calls, "batches_with_continue": conts, "missing_pages": missing,
    "pages_with_null_days": sum(1 for n in nulldays.values() if n),
    "cross_check_rest_v_action": cross,
    "spearman_all_pages": round(spearman(xs, ys), 3),
    "spearman_pages_on_2plus_walks": round(spearman([v[p] for p in multi], [through[p] for p in multi]), 3),
    "pages_on_2plus_walks": len(multi),
    "share_of_steps_under_1000_views": round(low / total_visits, 4),
    "share_of_pages_under_1000_views": round(sum(n < 1000 for n in xs) / len(xs), 4),
    "median_views_all_pages": statistics.median(xs),
    "least_read_pages": [{"page": p, "walks_through": through[p], "october_views": v[p]}
                         for p in sorted(pages, key=lambda p: v[p])[:15]],
    "least_read_on_2plus_walks": [{"page": p, "walks_through": through[p], "october_views": v[p]}
                                  for p in sorted(multi, key=lambda p: v[p])[:10]],
}
json.dump(res, open(out, "w"), indent=1)
print(json.dumps({k: res[k] for k in res if k not in ("least_read_pages",)}, indent=1))
