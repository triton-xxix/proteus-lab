"""P-0330: matched MOT league table for the 20 most-tested model families.

Streams the DVSA 2023 results zip (Deflate64, via inflate64) and aggregates as it goes, so nothing
large is written. Class 4 normal tests, petrol or diesel, age 3 to 25, F or PRS = initial fail.
Family = make + first word of the model (CORSA, FIESTA, 3xx for BMW numbers collapsed to 3 SERIES etc.).
Expected fails for a family = sum over its tests of the all-car fail rate in the same stratum
(age year x 20k-mile band x fuel). Ratio = observed / expected (1.0 = fleet average for its mix).
Usage: python3 -I league.py MAX_ROWS OUT.json
"""
import json
import struct
import sys
import urllib.request
from collections import defaultdict

import inflate64

URL = "https://data.dft.gov.uk/anonymised-mot-test/test_data/dft_test_result_2023.zip"
max_rows, out = int(sys.argv[1]), sys.argv[2]
r = urllib.request.urlopen(urllib.request.Request(URL, headers={"User-Agent": "ProteusLab-mot-check/1.0"}), timeout=60)
head = r.read(30)
sig, _, _, method, _, _, _, _, _, nlen, xlen = struct.unpack("<IHHHHHIIIHH", head)
assert sig == 0x04034B50 and method == 9
r.read(nlen + xlen)
inf = inflate64.Inflater()


def family(make, model):
    m = model.split(" ")[0] if model else ""
    if make == "BMW" and m[:1] in "1234567" and m[1:3].isdigit():
        m = m[0] + " SERIES"
    if make == "MERCEDES-BENZ" and len(m) >= 2 and m[0] in "ABCES" and (m[1:].isdigit() or m[1:2] == " "):
        m = m[0] + " CLASS"
    if make == "AUDI" and m[:1] == "A" and m[1:].isdigit():
        m = m
    return make + " " + m


stratum = defaultdict(lambda: [0, 0])           # (age, mband, fuel) -> tests, fails
fam = defaultdict(lambda: defaultdict(lambda: [0, 0]))  # family -> stratum -> tests, fails
buf = b""
rows = 0
header = None
first = last = None
while rows < max_rows:
    chunk = r.read(1 << 20)
    if not chunk:
        break
    buf += inf.inflate(chunk)
    lines = buf.split(b"\n")
    buf = lines.pop()
    for ln in lines:
        p = ln.decode("utf-8", "replace").rstrip("\r").split("|")  # the 2023 file is pipe-delimited
        if header is None:
            header = {h.strip().strip('"').lstrip("﻿").lower(): i for i, h in enumerate(p)}
            H = header
            print("header", list(header), flush=True)
            continue
        rows += 1
        if rows >= max_rows:
            break
        try:
            if p[H["test_class_id"]] != "4" or p[H["test_type"]] != "NT":
                continue
            res = p[H["test_result"]]
            if res not in ("P", "F", "PRS"):
                continue
            fuel = p[H["fuel_type"]]
            if fuel not in ("PE", "DI"):
                continue
            td, fu = p[H["test_date"]][:10], p[H["first_use_date"]][:10]
            age = int(td[:4]) - int(fu[:4]) - (td[5:10] < fu[5:10])
            miles = int(float(p[H["test_mileage"]]))
        except (ValueError, IndexError):
            continue
        if age < 3 or age > 25 or miles <= 0:
            continue
        first = td if first is None or td < first else first
        last = td if last is None or td > last else last
        s = (age, min(miles // 20000, 10), fuel)
        f = res != "P"
        stratum[s][0] += 1
        stratum[s][1] += f
        c = fam[family(p[H["make"]].strip().upper(), p[H["model"]].strip().upper())][s]
        c[0] += 1
        c[1] += f

tot_t = sum(v[0] for v in stratum.values())
tot_f = sum(v[1] for v in stratum.values())
top = sorted(fam, key=lambda k: -sum(v[0] for v in fam[k].values()))[:20]
table = []
for k in top:
    t = sum(v[0] for v in fam[k].values())
    fl = sum(v[1] for v in fam[k].values())
    exp = sum(v[0] * stratum[s][1] / stratum[s][0] for s, v in fam[k].items())
    table.append({"family": k, "tests": t, "raw_rate": round(fl / t, 4), "raw_ratio": round((fl / t) / (tot_f / tot_t), 3),
                  "matched_ratio": round(fl / exp, 3), "flattered_by_raw": round((fl / t) / (tot_f / tot_t) - fl / exp, 3)})
table.sort(key=lambda x: x["matched_ratio"])
res = {"rows_read": rows, "tests_kept": tot_t, "fleet_rate": round(tot_f / tot_t, 4), "dates": [first, last], "table": table}
json.dump(res, open(out, "w"), indent=1)
print("rows", rows, "kept", tot_t, "fleet", res["fleet_rate"], "dates", first, last)
for x in table:
    print("%-26s %8d  raw %.3f  raw x%.2f  matched x%.2f  raw minus matched %+.2f" % (
        x["family"], x["tests"], x["raw_rate"], x["raw_ratio"], x["matched_ratio"], x["flattered_by_raw"]))
