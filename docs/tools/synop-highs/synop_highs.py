#!/usr/bin/env python3
"""Daily highs for any WMO station from Ogimet's SYNOP archive, keyless, current to the day.

Reads the 1snTxTxTx group in section 333 of the report at one hour (default 18 UTC, which in the UK
and much of Europe carries the 06 to 18 UTC maximum) and writes date,tmax. One request per month, two
seconds apart. Standard library only. The CSV feeds bias-check's --csv straight in.

  python3 synop_highs.py --wmo 03772 --start 2026-09 --end 2026-10 --csv heathrow.csv
  python3 synop_highs.py --wmo 07190 --start 2026-10 --end 2026-10 --hour 18 --json out.json
"""
import argparse
import calendar
import csv
import json
import sys
import time
import urllib.request

UA = {"User-Agent": "proteus-synop-highs/1.0 (github triton-xxix)"}
URL = "https://www.ogimet.com/cgi-bin/getsynop?block=%s&begin=%s&end=%s"


def months(start, end):
    y, m = int(start[:4]), int(start[5:7])
    while (y, m) <= (int(end[:4]), int(end[5:7])):
        yield y, m
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def fetch(wmo, y, m):
    last = calendar.monthrange(y, m)[1]
    url = URL % (wmo, "%d%02d010000" % (y, m), "%d%02d%02d2359" % (y, m, last))
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read().decode("latin-1")


def parse(text, wmo, hour="18"):
    """Returns ({day: tmax}, lines read, reports at the hour with no max group)."""
    out, lines, missing = {}, 0, 0
    for line in text.splitlines():
        parts = line.split(",")
        if len(parts) < 7 or parts[0] != wmo:
            continue
        lines += 1
        if parts[4] != hour:
            continue
        groups = parts[6].replace("=", "").split()
        sec = groups[groups.index("333") + 1:] if "333" in groups else []
        if "555" in sec:
            sec = sec[:sec.index("555")]
        g = next((x for x in sec if len(x) == 5 and x[0] == "1" and x[1] in "01" and x[2:].isdigit()), None)
        if g is None:
            missing += 1
            continue
        out["%s-%s-%s" % (parts[1], parts[2], parts[3])] = int(g[2:]) / 10 * (-1 if g[1] == "1" else 1)
    return out, lines, missing


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--wmo", required=True, help="five-digit WMO station id, e.g. 03772 Heathrow")
    ap.add_argument("--start", required=True, help="first month, YYYY-MM")
    ap.add_argument("--end", required=True, help="last month, YYYY-MM")
    ap.add_argument("--hour", default="18", help="UTC hour of the report that carries the max (default 18)")
    ap.add_argument("--csv", help="write date,tmax here")
    ap.add_argument("--json", help="write days and counts here")
    a = ap.parse_args()
    obs, lines, missing = {}, 0, 0
    for i, (y, m) in enumerate(months(a.start, a.end)):
        if i:
            time.sleep(2)
        d, n, miss = parse(fetch(a.wmo, y, m), a.wmo, a.hour.zfill(2))
        obs.update(d)
        lines += n
        missing += miss
    if not obs:
        sys.exit("no %s UTC max groups found for %s in %d report lines; try another --hour" % (a.hour, a.wmo, lines))
    days = sorted(obs)
    print("%s: %d report lines, %d days with a %s UTC max (%s to %s), %d reports at that hour without one"
          % (a.wmo, lines, len(days), a.hour, days[0], days[-1], missing))
    if a.csv:
        with open(a.csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["date", "tmax"])
            w.writerows([d, obs[d]] for d in days)
    if a.json:
        json.dump({"wmo": a.wmo, "hour": a.hour, "lines": lines, "missing": missing,
                   "days": [{"day": d, "tmax": obs[d]} for d in days]}, open(a.json, "w"), indent=1)


if __name__ == "__main__":
    main()
