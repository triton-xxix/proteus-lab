#!/usr/bin/env python3
"""EDDM's highest METAR temperature against DWD 01262's 10-minute record at the same airport.

M  = highest whole-degree METAR temperature of the Berlin local day (raw METAR group, routine and specials).
X  = highest TX_10 (10-minute extreme) of that local day, in tenths.
T  = highest TT_10 (10-minute spot) at the :20 and :50 readings only, the times METARs are cut.
Questions: how often does M differ from round(X), by how much, and is the gap down to peaks between reports
(T rounded equals M, X rounded does not)? Downloads cached under sandbox/p0345/. Prints and writes results.json.
"""
import csv
import datetime as dt
import io
import json
import math
import re
import urllib.request
import zipfile
import zoneinfo
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = Path("/Users/triton/PROTEUS/sandbox/p0345")
CACHE.mkdir(parents=True, exist_ok=True)
BERLIN = zoneinfo.ZoneInfo("Europe/Berlin")
BASE = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/"
UA = {"User-Agent": "ProteusLab-probe/1.0 (one-off research script)"}
TEMP = re.compile(r"\s(M?\d{2})/(M?\d{2})?\s")


def fetch(url, name):
    p = CACHE / name
    if not p.exists():
        p.write_bytes(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180).read())
    return p


def dwd(url, name, field):
    z = zipfile.ZipFile(fetch(url, name))
    txt = z.read(z.namelist()[0]).decode("latin-1")
    out = {}
    for r in csv.DictReader(io.StringIO(txt), delimiter=";", skipinitialspace=True):
        key = {k.strip(): v for k, v in r.items()}
        v = float(key[field])
        if v > -900:
            out[dt.datetime.strptime(key["MESS_DATUM"].strip(), "%Y%m%d%H%M").replace(tzinfo=dt.timezone.utc)] = v
    return out


def rnd(x):
    return math.floor(x + 0.5)


tx = dwd(BASE + "extreme_temperature/recent/10minutenwerte_extrema_temp_01262_akt.zip", "tx.zip", "TX_10")
tt = dwd(BASE + "air_temperature/recent/10minutenwerte_TU_01262_akt.zip", "tt.zip", "TT_10")
first = min(tx).date()
last = max(tx).date()

url = ("https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=EDDM&data=metar&tz=Etc/UTC&format=onlycomma"
       f"&latlon=no&year1={first.year}&month1={first.month}&day1={first.day}"
       f"&year2={last.year}&month2={last.month}&day2={last.day}&missing=empty&trace=empty&report_type=3&report_type=4")
raw = fetch(url, "eddm.csv").read_text()

M, reports = defaultdict(lambda: -99), 0
for r in csv.DictReader(io.StringIO(raw)):
    m = TEMP.search(" " + r["metar"] + " ")
    if not m:
        continue
    s = m.group(1)
    t = -int(s[1:]) if s[0] == "M" else int(s)
    when = dt.datetime.strptime(r["valid"], "%Y-%m-%d %H:%M").replace(tzinfo=dt.timezone.utc)
    M[when.astimezone(BERLIN).date()] = max(M[when.astimezone(BERLIN).date()], t)
    reports += 1

X, T, nx = defaultdict(lambda: -99.0), defaultdict(lambda: -99.0), Counter()
for when, v in tx.items():
    d = when.astimezone(BERLIN).date()
    X[d] = max(X[d], v)
    nx[d] += 1
for when, v in tt.items():
    if when.minute in (20, 50):
        d = when.astimezone(BERLIN).date()
        T[d] = max(T[d], v)

days = sorted(d for d in M if d in X and d in T and nx[d] >= 140)
gaps = Counter(M[d] - rnd(X[d]) for d in days)
explained = sum(1 for d in days if M[d] != rnd(X[d]) and M[d] == rnd(T[d]))
differ = sum(1 for d in days if M[d] != rnd(X[d]))
spot = Counter(M[d] - rnd(T[d]) for d in days)
month = defaultdict(lambda: [0, 0])
for d in days:
    month[d.month][0] += 1
    month[d.month][1] += M[d] == rnd(X[d])
nov = [d for d in days if d >= dt.date(2026, 9, 1)]

out = {
    "reports": reports, "days": len(days), "first": str(days[0]), "last": str(days[-1]),
    "same_as_rounded_tx": len(days) - differ,
    "same_share": round((len(days) - differ) / len(days), 4),
    "gap_M_minus_roundX": {str(k): gaps[k] for k in sorted(gaps)},
    "mean_gap": round(sum((M[d] - X[d]) for d in days) / len(days), 3),
    "differ": differ,
    "differ_explained_by_report_times": explained,
    "same_as_rounded_spot_at_report_times": sum(1 for d in days if M[d] == rnd(T[d])),
    "gap_M_minus_roundT": {str(k): spot[k] for k in sorted(spot)},
    "by_month_same_share": {str(k): round(v[1] / v[0], 3) for k, v in sorted(month.items())},
    "since_1_sep": {"days": len(nov), "same": sum(1 for d in nov if M[d] == rnd(X[d]))},
}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
