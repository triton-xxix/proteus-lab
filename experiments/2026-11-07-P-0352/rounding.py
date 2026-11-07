"""P-0352: does Heathrow's METAR temperature round or truncate the station's tenths reading?

Matches every EGLL METAR in October 2026 (Iowa Mesonet asos.py, keyless, routine and specials) to the Ogimet
10-minute SYNOP for 03772 at the same minute (cached in sandbox/ogimet-03772-202610.txt, the 1sTTT group in
tenths). Counts how often the METAR whole degree equals the tenths reading rounded half up, floored, or
neither, and the mean METAR minus tenths.
Usage: python3 -I rounding.py OUT.json
"""
import csv
import io
import json
import math
import re
import statistics
import sys
import urllib.request
from collections import Counter

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

synop = {}
for line in open("/Users/triton/PROTEUS/sandbox/ogimet-03772-202610.txt"):
    parts = line.strip().split(",", 6)
    if len(parts) < 7:
        continue
    _, y, mo, d, h, mi, rep = parts
    toks = rep.replace("=", "").split()
    for t in toks[5:]:
        if t == "333":
            break
        if re.fullmatch(r"1[01]\d{3}", t):
            v = int(t[2:]) / 10
            synop["%s-%s-%s %s:%s" % (y, mo, d, h, mi)] = -v if t[1] == "1" else v
            break

c, diffs, halves = Counter(), [], Counter()
for k, mt in metar.items():
    if k not in synop:
        c["no synop at that minute"] += 1
        continue
    x = synop[k]
    rnd = math.floor(x + 0.5)
    flo = math.floor(x)
    c["matched"] += 1
    c["rounded"] += mt == rnd
    c["floored"] += mt == flo
    c["both (x.0)"] += mt == rnd == flo
    c["neither"] += mt not in (rnd, flo)
    if abs(x * 10 % 10 - 5) < 1e-6:
        halves["half up" if mt == rnd else "half down" if mt == flo else "other"] += 1
    diffs.append(mt - x)

n = c["matched"]
res = {"metars": len(metar), "synop_minutes": len(synop), "counts": dict(c),
       "share_rounded": round(c["rounded"] / n, 4), "share_floored": round(c["floored"] / n, 4),
       "share_neither": round(c["neither"] / n, 4),
       "share_rounded_excluding_x0": round((c["rounded"] - c["both (x.0)"]) / (n - c["both (x.0)"]), 4),
       "share_floored_excluding_x0": round((c["floored"] - c["both (x.0)"]) / (n - c["both (x.0)"]), 4),
       "x5_cases": dict(halves),
       "mean_metar_minus_tenths": round(statistics.mean(diffs), 3),
       "sd_metar_minus_tenths": round(statistics.stdev(diffs), 3),
       "diff_hist": dict(sorted(Counter(round(dd, 1) for dd in diffs).items()))}
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res, indent=1))
