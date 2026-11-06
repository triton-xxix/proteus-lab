#!/usr/bin/env python3
"""EDDM's whole-degree METAR high against DWD 01262's daily TXK, 2021 to 2026, by month and by year.

METAR by Berlin local day. TXK is DWD's climate-day maximum, so the day edge can differ slightly; winter edge
cases are small but not zero. One IEM call a year, cached under sandbox/p0347/. Writes results.json.
"""
import csv
import datetime as dt
import io
import json
import math
import re
import time
import urllib.request
import zipfile
import zoneinfo
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = Path("/Users/triton/PROTEUS/sandbox/p0347")
CACHE.mkdir(parents=True, exist_ok=True)
BERLIN = zoneinfo.ZoneInfo("Europe/Berlin")
UA = {"User-Agent": "ProteusLab-probe/1.0 (one-off research script)"}
TEMP = re.compile(r"\s(M?\d{2})/(M?\d{2})?\s")
BASE = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/"


def fetch(url, name):
    p = CACHE / name
    if not p.exists():
        p.write_bytes(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180).read())
        time.sleep(1)
    return p


def kl(path):
    z = zipfile.ZipFile(path)
    name = next(n for n in z.namelist() if n.startswith("produkt_klima_tag"))
    out = {}
    for r in csv.DictReader(io.StringIO(z.read(name).decode("latin-1")), delimiter=";", skipinitialspace=True):
        key = {k.strip(): v for k, v in r.items()}
        v = float(key["TXK"])
        if v > -900:
            out[dt.datetime.strptime(key["MESS_DATUM"].strip(), "%Y%m%d").date()] = v
    return out


listing = urllib.request.urlopen(urllib.request.Request(BASE + "historical/", headers=UA), timeout=60).read().decode()
hist = re.search(r"tageswerte_KL_01262_\d+_\d+_hist\.zip", listing).group(0)
TX = kl(fetch(BASE + "historical/" + hist, "hist.zip"))
TX.update(kl(fetch(BASE + "recent/tageswerte_KL_01262_akt.zip", "recent.zip")))

M = defaultdict(lambda: -99)
reports = {}
for y in range(2021, 2027):
    url = (f"https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=EDDM&data=metar&tz=Etc/UTC"
           f"&format=onlycomma&latlon=no&year1={y}&month1=1&day1=1&year2={y + 1}&month2=1&day2=1"
           "&missing=empty&trace=empty&report_type=3&report_type=4")
    raw = fetch(url, f"eddm-{y}.csv").read_text()
    n = 0
    for r in csv.DictReader(io.StringIO(raw)):
        m = TEMP.search(" " + r["metar"] + " ")
        if not m:
            continue
        s = m.group(1)
        t = -int(s[1:]) if s[0] == "M" else int(s)
        d = dt.datetime.strptime(r["valid"], "%Y-%m-%d %H:%M").replace(tzinfo=dt.timezone.utc).astimezone(BERLIN).date()
        M[d] = max(M[d], t)
        n += 1
    reports[y] = n

# A day with few METARs would read as a false gap; keep gaps within 3 C and count the rest apart
days = sorted(d for d in M if d in TX and d.year >= 2021)
outliers = [d for d in days if abs(M[d] - TX[d]) > 3]
use = [d for d in days if abs(M[d] - TX[d]) <= 3]


def rnd(x):
    return math.floor(x + 0.5)


def summary(ds):
    if not ds:
        return None
    same = sum(1 for d in ds if M[d] == rnd(TX[d]))
    return {"days": len(ds), "same_share": round(same / len(ds), 3),
            "mean_gap": round(sum(M[d] - TX[d] for d in ds) / len(ds), 3)}


seasons = {"DJF": (12, 1, 2), "MAM": (3, 4, 5), "JJA": (6, 7, 8), "SON": (9, 10, 11)}
gaps = Counter(M[d] - rnd(TX[d]) for d in use)
out = {
    "reports_by_year": reports, "first": str(use[0]), "last": str(use[-1]),
    "all": summary(use), "gap_rounded": {str(k): gaps[k] for k in sorted(gaps)},
    "outliers_over_3C": len(outliers),
    "by_month": {m: summary([d for d in use if d.month == m]) for m in range(1, 13)},
    "by_season": {k: summary([d for d in use if d.month in v]) for k, v in seasons.items()},
    "by_year": {y: summary([d for d in use if d.year == y]) for y in range(2021, 2027)},
}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
