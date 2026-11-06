#!/usr/bin/env python3
"""Whole-degree METAR high against SYNOP TX at three airports, 1 Sep to 31 Oct 2026.

Same window on both sides: SYNOP's 18 UTC report carries the 06 to 18 UTC maximum, so METARs are taken from
06:00 to 18:00 UTC only. Parser from docs/tools/synop-highs/synop_highs.py, METAR group as in P-0334.
"""
import csv
import datetime as dt
import io
import json
import math
import re
import statistics as st
import sys
import time
import urllib.request
from collections import Counter
from pathlib import Path

sys.path.insert(0, "/Users/triton/PROTEUS/docs/tools/synop-highs")
import synop_highs  # noqa: E402

HERE = Path(__file__).resolve().parent
TEMP = re.compile(r"\s(M?\d{2})/(M?\d{2})?\s")
UA = {"User-Agent": "ProteusLab-probe/1.0 (one-off research script)"}
AIRPORTS = [("Heathrow", "EGLL", "03772"), ("Orly", "LFPO", "07149"), ("Munich", "EDDM", "10870")]


def metar_highs(icao):
    url = (f"https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station={icao}&data=metar&tz=Etc/UTC"
           "&format=onlycomma&latlon=no&year1=2026&month1=9&day1=1&year2=2026&month2=11&day2=1"
           "&missing=empty&trace=empty&report_type=3&report_type=4")
    raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read().decode()
    out = {}
    for r in csv.DictReader(io.StringIO(raw)):
        m = TEMP.search(" " + r["metar"] + " ")
        if not m:
            continue
        when = dt.datetime.strptime(r["valid"], "%Y-%m-%d %H:%M")
        if not 6 <= when.hour < 18 and not (when.hour == 18 and when.minute == 0):
            continue
        s = m.group(1)
        t = -int(s[1:]) if s[0] == "M" else int(s)
        d = when.date().isoformat()
        out[d] = max(out.get(d, -99), t)
    return out


res = {}
for name, icao, wmo in AIRPORTS:
    obs = {}
    for y, mo in ((2026, 9), (2026, 10)):
        d, _, _ = synop_highs.parse(synop_highs.fetch(wmo, y, mo), wmo, "18")
        obs.update(d)
        time.sleep(3)
    met = metar_highs(icao)
    days = sorted(set(obs) & set(met))
    if not days:
        res[name] = {"days": 0, "synop_days": len(obs), "metar_days": len(met)}
        print(name, res[name])
        continue
    gaps = [met[d] - obs[d] for d in days]
    rnd = Counter(met[d] - math.floor(obs[d] + 0.5) for d in days)
    res[name] = {
        "icao": icao, "wmo": wmo, "days": len(days),
        "mean_metar_minus_tx": round(st.mean(gaps), 3), "sd": round(st.stdev(gaps), 3),
        "se": round(st.stdev(gaps) / math.sqrt(len(gaps)), 3),
        "same_as_rounded_tx": rnd[0], "same_share": round(rnd[0] / len(days), 3),
        "gap_rounded": {str(k): rnd[k] for k in sorted(rnd)},
    }
    print(name, res[name])
    time.sleep(3)
(HERE / "results.json").write_text(json.dumps(res, indent=1))
