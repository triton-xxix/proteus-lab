#!/usr/bin/env python3
"""P-0007: Metaculus without an account. Can the public API list open questions and give the
community forecast, and how fast can it be polled before it throttles? Output: REPORT.md."""
import json, time, urllib.request, urllib.error
BASE = "https://www.metaculus.com/api"
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "proteus-probe/0.1", "Accept": "application/json"})
    t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, dict(r.headers), json.load(r), time.time() - t
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), None, time.time() - t
L = ["# P-0007: Metaculus API without an account", ""]
st, hd, d, dt = get(BASE + "/posts/?statuses=open&forecast_type=binary&limit=20&order_by=-hotness")
L.append("`/api/posts/` open binary, 20 newest by hotness: HTTP %d in %.2fs. Rate headers: %s" % (
    st, dt, {k: v for k, v in hd.items() if "rate" in k.lower() or "limit" in k.lower()} or "none"))
posts = (d or {}).get("results", []) if d else []
L.append("Returned %d posts. Fields on a post: %s" % (len(posts), ", ".join(sorted(posts[0].keys()))[:300] if posts else "n/a"))
rows = []
for p in posts[:10]:
    q = p.get("question") or {}
    agg = ((q.get("aggregations") or {}).get("recency_weighted") or {}).get("latest") or {}
    cp = agg.get("centers") or agg.get("means")
    rows.append((p.get("id"), (p.get("title") or "")[:70], q.get("scheduled_close_time", "")[:10], cp[0] if cp else None, agg.get("forecaster_count")))
L += ["", "| id | title | closes | community p | forecasters |", "|---|---|---|---|---|"]
for r in rows: L.append("| %s | %s | %s | %s | %s |" % r)
have_cp = sum(1 for r in rows if r[3] is not None)
L += ["", "Community forecast present on %d of %d without any login." % (have_cp, len(rows)), ""]
# one question in detail
if posts:
    st2, hd2, d2, dt2 = get(BASE + "/posts/%s/" % posts[0]["id"])
    q = (d2 or {}).get("question") or {}
    hist = (((q.get("aggregations") or {}).get("recency_weighted") or {}).get("history") or [])
    L.append("Single post detail: HTTP %d in %.2fs, recency-weighted history points: %d (a full forecast time series, keyless)." % (st2, dt2, len(hist)))
# burst: 30 calls as fast as possible
codes, times = [], []
t0 = time.time()
for i in range(30):
    st, hd, d, dt = get(BASE + "/posts/?statuses=open&limit=5&offset=%d" % (i * 5))
    codes.append(st); times.append(dt)
    if st == 429: L.append("429 at call %d after %.1fs; headers %s" % (i + 1, time.time() - t0, {k: v for k, v in hd.items() if 'retry' in k.lower() or 'rate' in k.lower()})); break
L += ["", "Burst: %d calls in %.1fs, codes %s, mean %.2fs per call, max %.2fs." % (
    len(codes), time.time() - t0, sorted(set(codes)), sum(times) / len(times), max(times)), ""]
open("/Users/triton/PROTEUS/experiments/2026-09-24-P-0007/REPORT.md", "w").write("\n".join(L) + "\n")
print("\n".join(L))
