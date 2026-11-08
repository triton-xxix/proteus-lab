"""P-0363: Ogimet carries no :50 SYNOPs for 03772 (checked 20 Oct, 115 reports, none at :50), so P-0352 matched
only the :20 METARs. Here each :50 METAR is set against the tenths interpolated as the mean of :40 and the next
:00. Control: each :20 METAR against both its exact :20 tenths and the mean of :10 and :30, so the cost of
interpolating is measured on the same month. P-0352's parsing, unchanged.
Usage: python3 -I interp.py OUT.json
"""
import csv
import datetime as dt
import io
import json
import math
import re
import statistics
import sys
import urllib.request

out = sys.argv[1]
TEMP = re.compile(r"\s(M?\d{2})/(M?\d{2})?\s")
UA = {"User-Agent": "ProteusLab-probe/1.0 (one-off research script)"}
url = ("https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=EGLL&data=metar&tz=Etc/UTC"
       "&format=onlycomma&latlon=no&year1=2026&month1=10&day1=1&year2=2026&month2=11&day2=1"
       "&missing=empty&trace=empty&report_type=3&report_type=4")  # IEM files the :20s as type 4
raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read().decode()
metar = {}
for r in csv.DictReader(io.StringIO(raw)):
    m = TEMP.search(" " + r["metar"] + " ")
    if m:
        s = m.group(1)
        metar[dt.datetime.strptime(r["valid"], "%Y-%m-%d %H:%M")] = -int(s[1:]) if s[0] == "M" else int(s)

synop = {}
for line in open("/Users/triton/PROTEUS/sandbox/ogimet-03772-202610.txt"):
    parts = line.strip().split(",", 6)
    if len(parts) < 7:
        continue
    _, y, mo, d, h, mi, rep = parts
    for t in rep.replace("=", "").split()[5:]:
        if t == "333":
            break
        if re.fullmatch(r"1[01]\d{3}", t):
            v = int(t[2:]) / 10
            synop[dt.datetime(int(y), int(mo), int(d), int(h), int(mi))] = -v if t[1] == "1" else v
            break

M10 = dt.timedelta(minutes=10)


def score(pairs):
    if not pairs:
        return None
    n = len(pairs)
    diffs = [m - x for m, x in pairs]
    return {"n": n, "share_rounded": round(sum(m == math.floor(x + 0.5) for m, x in pairs) / n, 4),
            "mean_metar_minus_tenths": round(statistics.mean(diffs), 3),
            "sd": round(statistics.stdev(diffs), 3) if n > 1 else None}


fifty, twenty_exact, twenty_interp, twenty_both = [], [], [], []
skipped = {"50_missing_neighbour": 0, "20_missing": 0}
for t, mt in sorted(metar.items()):
    if t.minute == 50:
        a, b = synop.get(t - M10), synop.get(t + M10)
        if a is None or b is None:
            skipped["50_missing_neighbour"] += 1
            continue
        fifty.append((mt, (a + b) / 2))
    elif t.minute == 20:
        x, a, b = synop.get(t), synop.get(t - M10), synop.get(t + M10)
        if x is not None:
            twenty_exact.append((mt, x))
        else:
            skipped["20_missing"] += 1
        if a is not None and b is not None:
            twenty_interp.append((mt, (a + b) / 2))
            if x is not None:
                twenty_both.append((x, (a + b) / 2))

interp_err = [i - x for x, i in twenty_both]
res = {"metars_routine": len(metar), "synop_minutes": len(synop), "skipped": skipped,
       "fifty_interpolated": score(fifty),
       "twenty_exact": score(twenty_exact),
       "twenty_interpolated": score(twenty_interp),
       "interp_minus_exact_at_20": {"n": len(interp_err), "mean": round(statistics.mean(interp_err), 3),
                                    "sd": round(statistics.stdev(interp_err), 3),
                                    "within_0.2": round(sum(abs(e) <= 0.2 + 1e-9 for e in interp_err) / len(interp_err), 4)}
       if interp_err else None}
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res, indent=1))
