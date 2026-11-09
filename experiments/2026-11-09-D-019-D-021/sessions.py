"""Which dates does scan.py's prepare() keep for the stock W1, and what does Yahoo actually hold?

Usage: /Users/triton/PROTEUS/.venv/bin/python3 sessions.py
Reads Yahoo chart meta and timestamps for SPY through the scanner's own functions. Writes nothing.
"""
import collections
import datetime as dt
import json
import sys
import urllib.request
import zoneinfo

sys.path.insert(0, "/Users/triton/PROTEUS/edges/scan")
import scan  # noqa: E402

NY = zoneinfo.ZoneInfo("America/New_York")
url = "https://query1.finance.yahoo.com/v8/finance/chart/SPY?range=60d&interval=5m"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
r = json.load(urllib.request.urlopen(req, timeout=40))["chart"]["result"][0]
print("gmtoffset", r["meta"].get("gmtoffset"), "tz", r["meta"].get("exchangeTimezoneName"))

true_ny = collections.Counter()
first_ny = {}
for ts in r["timestamp"]:
    d = dt.datetime.fromtimestamp(ts, tz=NY)
    k = d.date().isoformat()
    true_ny[k] += 1
    first_ny.setdefault(k, d.strftime("%H:%M"))

rows = scan.yahoo_5m("SPY")
labelled = collections.Counter(x[1] for x in rows)
first_lab = {}
for x in rows:
    first_lab.setdefault(x[1], "%02d:%02d" % (x[2] // 60, x[2] % 60))
kept = {D["date"]: D["n"] for D in scan.prepare(rows, "stock")}

print("date, bars true NY, first bar true NY, bars as labelled, first bar as labelled, kept n by prepare")
for k in sorted(set(true_ny) | set(labelled)):
    if k >= "2026-10-19":
        print(k, true_ny.get(k), first_ny.get(k), labelled.get(k), first_lab.get(k), kept.get(k))
print("blocks (stock, size 5):")
for b in scan.blocks(set(kept), 5)[:4]:
    print(sorted(b))
