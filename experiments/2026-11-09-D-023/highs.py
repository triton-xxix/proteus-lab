"""D-023: the METAR high per Berlin day and per UTC day for the rows the read needs.

Usage: python3 -I highs.py eddm-metar.csv
Uses the raw TT group, the same regex as P-0334's metar_rule.py.
"""
import csv
import datetime as dt
import re
import sys
import zoneinfo

TEMP = re.compile(r"\s(M?\d{2})/(M?\d{2})?\s")
BERLIN = zoneinfo.ZoneInfo("Europe/Berlin")
utc, loc = {}, {}
for r in csv.DictReader(open(sys.argv[1], newline="")):
    m = TEMP.search(" " + r["metar"] + " ")
    if not m:
        continue
    s = m.group(1)
    t = -int(s[1:]) if s[0] == "M" else int(s)
    when = dt.datetime.strptime(r["valid"], "%Y-%m-%d %H:%M").replace(tzinfo=dt.timezone.utc)
    u, l = when.date().isoformat(), when.astimezone(BERLIN).date().isoformat()
    utc[u] = max(utc.get(u, -99), t)
    loc[l] = max(loc.get(l, -99), t)
for d in sorted(set(utc) | set(loc)):
    print(d, "utc_high", utc.get(d), "berlin_high", loc.get(d))
