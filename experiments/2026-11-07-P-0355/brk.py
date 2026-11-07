"""P-0355: is the 2026 drift in EDDM METAR high minus 01262 TXK a station change on 19 Apr 2026?

Cache only (P-0347's files in sandbox/p0347/, nothing fetched). Same day rule as P-0347 (METAR by Berlin local
day, gaps over 3 C dropped). Splits every year 2021 to 2026 at 20 Apr: before (1 Jan to 19 Apr) and after
(20 Apr to 31 Oct), so the seasonal shape is the control. Also prints the newer metadata in recent.zip.
Usage: python3 -I brk.py OUT.json
"""
import csv
import datetime as dt
import io
import json
import re
import statistics as st
import sys
import zipfile
import zoneinfo
from collections import defaultdict

out = sys.argv[1]
C = "/Users/triton/PROTEUS/sandbox/p0347/"
BERLIN = zoneinfo.ZoneInfo("Europe/Berlin")
TEMP = re.compile(r"\s(M?\d{2})/(M?\d{2})?\s")


def kl(path):
    z = zipfile.ZipFile(path)
    name = next(n for n in z.namelist() if n.startswith("produkt_klima_tag"))
    o = {}
    for r in csv.DictReader(io.StringIO(z.read(name).decode("latin-1")), delimiter=";", skipinitialspace=True):
        key = {k.strip(): v for k, v in r.items()}
        v = float(key["TXK"])
        if v > -900:
            o[dt.datetime.strptime(key["MESS_DATUM"].strip(), "%Y%m%d").date()] = v
    return o


TX = kl(C + "hist.zip")
TX.update(kl(C + "recent.zip"))
meta = {}
z = zipfile.ZipFile(C + "recent.zip")
for n in z.namelist():
    if n in ("Metadaten_Geraete_Lufttemperatur_Maximum_01262.txt", "Metadaten_Geographie_01262.txt"):
        meta[n] = z.read(n).decode("latin-1").strip().splitlines()

M = defaultdict(lambda: -99)
for y in range(2021, 2027):
    for r in csv.DictReader(io.StringIO(open(C + "eddm-%d.csv" % y).read())):
        m = TEMP.search(" " + r["metar"] + " ")
        if not m:
            continue
        s = m.group(1)
        t = -int(s[1:]) if s[0] == "M" else int(s)
        d = dt.datetime.strptime(r["valid"], "%Y-%m-%d %H:%M").replace(tzinfo=dt.timezone.utc).astimezone(BERLIN).date()
        M[d] = max(M[d], t)

use = [d for d in sorted(M) if d in TX and abs(M[d] - TX[d]) <= 3]


def summ(ds):
    g = [M[d] - TX[d] for d in ds]
    return {"days": len(g), "mean_gap": round(st.mean(g), 3), "se": round(st.stdev(g) / len(g) ** 0.5, 3)}


res = {"recent_zip_metadata": meta, "last_day": str(use[-1]), "by_year": {}}
for y in range(2021, 2027):
    b = [d for d in use if d.year == y and d < dt.date(y, 4, 20)]
    a = [d for d in use if d.year == y and dt.date(y, 4, 20) <= d <= dt.date(y, 10, 31)]
    sb, sa = summ(b), summ(a)
    res["by_year"][y] = {"before": sb, "after": sa, "shift": round(sa["mean_gap"] - sb["mean_gap"], 3)}
prior = [res["by_year"][y]["shift"] for y in range(2021, 2026)]
res["shift_2021_2025_mean"] = round(st.mean(prior), 3)
res["shift_2021_2025_range"] = [min(prior), max(prior)]
res["shift_2026"] = res["by_year"][2026]["shift"]
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res, indent=1))
