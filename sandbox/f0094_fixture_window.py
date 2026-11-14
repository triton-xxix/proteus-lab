#!/usr/bin/env python3
"""F-0094 check: kickoffs per league in the cached fixturedownload calendars between two dates."""
import json
import sys
from datetime import datetime, timezone

CACHE = "/Users/triton/PROTEUS/pitch/cache/"
LEAGUES = ("E0", "E1", "SP1", "D1", "I1", "F1", "N1", "P1", "SC0")
lo = datetime.fromisoformat(sys.argv[1]).replace(tzinfo=timezone.utc)
hi = datetime.fromisoformat(sys.argv[2]).replace(tzinfo=timezone.utc)
for div in LEAGUES:
    n = 0
    first = None
    for m in json.load(open(CACHE + "fixturedownload-%s.json" % div)):
        t = datetime.fromisoformat(m["DateUtc"].replace("Z", "").strip()).replace(tzinfo=timezone.utc)
        if lo <= t <= hi:
            n += 1
            first = t if first is None or t < first else first
    print(div, n, first)
