"""P-0393: Sentinel-2A, 2B, 2C scene counts per UTC day on Earth Search, 27 Oct to 9 Nov 2026.

One keyless POST per platform per day to earth-search.aws.element84.com/v1/search (sentinel-2-l2a, limit 1), reading
numberMatched. Question: is 2B's 3 Nov a real drop below its own 14-day median (P-0385's three misses), or not?
"""
import datetime as dt
import json
import pathlib
import statistics
import time
import urllib.request

HERE = pathlib.Path(__file__).parent
URL = "https://earth-search.aws.element84.com/v1/search"
PLATFORMS = ["sentinel-2a", "sentinel-2b", "sentinel-2c"]


def count(platform, day):
    body = {"collections": ["sentinel-2-l2a"], "datetime": f"{day}T00:00:00Z/{day}T23:59:59Z",
            "query": {"platform": {"eq": platform}}, "limit": 1, "fields": {"include": ["id"]}}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={"Content-Type": "application/json",
                                                                               "User-Agent": "proteus-research/1.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r).get("numberMatched")
        except Exception as e:  # noqa: BLE001
            last = str(e)
            time.sleep(5)
    return None


days = [(dt.date(2026, 10, 27) + dt.timedelta(n)).isoformat() for n in range(14)]
table = {p: {} for p in PLATFORMS}
for d in days:
    for p in PLATFORMS:
        table[p][d] = count(p, d)
        time.sleep(0.5)
    print(d, [table[p][d] for p in PLATFORMS])

res = {"days": days, "counts": table, "summary": {}}
for p in PLATFORMS:
    v = [x for x in table[p].values() if x is not None]
    med = statistics.median(v) if v else None
    res["summary"][p] = {"median": med, "min": min(v) if v else None, "max": max(v) if v else None,
                         "3 Nov": table[p].get("2026-11-03"),
                         "3 Nov / median": round(table[p]["2026-11-03"] / med, 3) if med and table[p].get("2026-11-03") else None,
                         "days_below_half_median": [d for d, x in table[p].items() if x is not None and med and x < med / 2]}
(HERE / "results.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res["summary"], indent=1))
