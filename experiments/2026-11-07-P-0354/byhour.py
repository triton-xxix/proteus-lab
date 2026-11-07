"""P-0354: does Heathrow's METAR run cold at the warm part of the day?

P-0352's match (EGLL METARs, Iowa Mesonet, October 2026, against the cached Ogimet 10-minute SYNOP tenths
for 03772 at the same minute), split by UTC hour and by whether the minute falls in that day's three warmest
hours (ranked by the SYNOP tenths' hourly mean). Also the METAR at the day's warmest matched minute.
Usage: python3 -I byhour.py OUT.json
"""
import csv
import io
import json
import re
import statistics as st
import sys
import urllib.request
from collections import defaultdict

out = sys.argv[1]
TEMP = re.compile(r"\s(M?\d{2})/(M?\d{2})?\s")
UA = {"User-Agent": "ProteusLab-probe/1.0 (one-off research script)"}
url = ("https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=EGLL&data=metar&tz=Etc/UTC"
       "&format=onlycomma&latlon=no&year1=2026&month1=10&day1=1&year2=2026&month2=11&day2=1"
       "&missing=empty&trace=empty&report_type=3&report_type=4")
raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read().decode()
metar = {}
for r in csv.DictReader(io.StringIO(raw)):
    m = TEMP.search(" " + r["metar"] + " ")
    if m:
        s = m.group(1)
        metar[r["valid"]] = -int(s[1:]) if s[0] == "M" else int(s)

synop, hourly = {}, defaultdict(list)
for line in open("/Users/triton/PROTEUS/sandbox/ogimet-03772-202610.txt", encoding="latin-1"):
    parts = line.strip().split(",", 6)
    if len(parts) < 7:
        continue
    _, y, mo, d, h, mi, rep = parts
    for t in rep.replace("=", "").split()[5:]:
        if t == "333":
            break
        if re.fullmatch(r"1[01]\d{3}", t):
            v = int(t[2:]) / 10 * (-1 if t[1] == "1" else 1)
            synop["%s-%s-%s %s:%s" % (y, mo, d, h, mi)] = v
            hourly[("%s-%s-%s" % (y, mo, d), int(h))].append(v)
            break

warm = defaultdict(set)
byday = defaultdict(list)
for (d, h), vs in hourly.items():
    byday[d].append((st.mean(vs), h))
for d, hs in byday.items():
    warm[d] = {h for _, h in sorted(hs, reverse=True)[:3]}

by_hour, in_warm, not_warm = defaultdict(list), [], []
peak = {}
for k, mt in metar.items():
    if k not in synop:
        continue
    x = synop[k]
    d, hm = k.split()
    h = int(hm[:2])
    diff = mt - x
    by_hour[h].append(diff)
    (in_warm if h in warm[d] else not_warm).append(diff)
    if d not in peak or x > peak[d][0]:
        peak[d] = (x, diff)

res = {
    "matched": sum(len(v) for v in by_hour.values()),
    "by_utc_hour": {h: {"n": len(v), "mean": round(st.mean(v), 3)} for h, v in sorted(by_hour.items())},
    "warmest_three_hours": {"n": len(in_warm), "mean": round(st.mean(in_warm), 3), "sd": round(st.stdev(in_warm), 3)},
    "other_hours": {"n": len(not_warm), "mean": round(st.mean(not_warm), 3), "sd": round(st.stdev(not_warm), 3)},
    "at_days_warmest_matched_minute": {"n": len(peak), "mean": round(st.mean(p[1] for p in peak.values()), 3)},
    "night_00_05": round(st.mean([x for h in range(0, 6) for x in by_hour.get(h, [])]), 3),
    "afternoon_12_15": round(st.mean([x for h in range(12, 16) for x in by_hour.get(h, [])]), 3),
}
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res, indent=1))
