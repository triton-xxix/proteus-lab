"""P-0123: data.police.uk street-level crime, keyless. Latest month, three points, counts and timing."""
import collections
import json
import time
import urllib.error
import urllib.request

OUT = "/Users/triton/PROTEUS/experiments/2026-10-10-P-0123/"
UA = {"User-Agent": "proteus-probe"}


def get(url):
    t = time.time()
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60)
        body = r.read()
        return r.status, dict(r.headers), json.loads(body), time.time() - t, len(body)
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), None, time.time() - t, 0


s, h, dates, dt, n = get("https://data.police.uk/api/crimes-street-dates")
latest = dates[0]["date"]
print("dates status", s, "months listed", len(dates), "latest", latest, "%.2fs" % dt)
rl = {k: v for k, v in h.items() if "rate" in k.lower() or "limit" in k.lower()}
print("rate headers", rl or "none")

points = {"Leicester Square, London": (51.5103, -0.1301), "Leeds city centre": (53.7965, -1.5478),
          "Hawes, North Yorkshire (rural)": (54.3040, -2.1966)}
rows = []
for name, (lat, lng) in points.items():
    url = "https://data.police.uk/api/crimes-street/all-crime?lat=%s&lng=%s&date=%s" % (lat, lng, latest)
    s, h, d, dt, n = get(url)
    if d is None:
        print(name, "status", s, "%.2fs" % dt)
        rows.append({"point": name, "status": s})
        continue
    cats = collections.Counter(c["category"] for c in d).most_common(3)
    outcome_none = sum(1 for c in d if not c.get("outcome_status"))
    locs = len({c["location"]["street"]["id"] for c in d})
    print("%s: status %s, %d crimes, %d distinct snapped streets, %d with no outcome yet, top %s, %.2fs, %d KB"
          % (name, s, len(d), locs, outcome_none, cats, dt, n // 1024))
    rows.append({"point": name, "status": s, "crimes": len(d), "streets": locs, "no_outcome": outcome_none,
                 "top3": cats, "seconds": round(dt, 2), "bytes": n})
    time.sleep(0.2)

# Burst test: 20 quick calls of the cheapest endpoint, count non-200s.
codes = collections.Counter()
t = time.time()
for _ in range(20):
    codes[get("https://data.police.uk/api/forces")[0]] += 1
print("burst 20 calls in %.1fs: %s" % (time.time() - t, dict(codes)))
json.dump({"latest": latest, "months": len(dates), "rows": rows, "burst": dict(codes), "rate_headers": rl},
          open(OUT + "result.json", "w"), indent=1)
