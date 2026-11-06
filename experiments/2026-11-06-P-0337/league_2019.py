"""P-0337: P-0330's matched MOT league table on DVSA 2019, then compared with P-0330's 2023 table.

Same rules as P-0330's league.py: class 4 normal tests, petrol or diesel, age 3 to 25, F or PRS = initial
fail, matched on age year x 20k-mile band x fuel. The only changes: the URL, and the zip's compression and
the file's delimiter are read from the file rather than assumed. The same MAX_ROWS is used, so the window
ends wherever 8M rows reaches in that file.
Usage: python3 league_2019.py MAX_ROWS P0330_RESULTS.json OUT.json
"""
import json
import struct
import sys
import urllib.request
import zlib
from collections import defaultdict

import inflate64

URL = "https://data.dft.gov.uk/anonymised-mot-test/test_data/dft_test_result_2019.zip"
max_rows, then_path, out = int(sys.argv[1]), sys.argv[2], sys.argv[3]
r = urllib.request.urlopen(urllib.request.Request(URL, headers={"User-Agent": "ProteusLab-mot-check/1.0"}), timeout=60)
head = r.read(30)
sig, _, _, method, _, _, _, _, _, nlen, xlen = struct.unpack("<IHHHHHIIIHH", head)
assert sig == 0x04034B50 and method in (8, 9), (hex(sig), method)
r.read(nlen + xlen)
print("zip method", method, flush=True)
if method == 9:
    decode = inflate64.Inflater().inflate
else:
    decode = zlib.decompressobj(-15).decompress


def family(make, model):
    m = model.split(" ")[0] if model else ""
    if make == "BMW" and m[:1] in "1234567" and m[1:3].isdigit():
        m = m[0] + " SERIES"
    if make == "MERCEDES-BENZ" and len(m) >= 2 and m[0] in "ABCES" and (m[1:].isdigit() or m[1:2] == " "):
        m = m[0] + " CLASS"
    return make + " " + m


stratum = defaultdict(lambda: [0, 0])
fam = defaultdict(lambda: defaultdict(lambda: [0, 0]))
buf = b""
rows = 0
H = None
delim = None
first = last = None
while rows < max_rows:
    chunk = r.read(1 << 20)
    if not chunk:
        break
    buf += decode(chunk)
    lines = buf.split(b"\n")
    buf = lines.pop()
    for ln in lines:
        text = ln.decode("utf-8", "replace").rstrip("\r")
        if H is None:
            delim = max("|,;\t", key=text.count)
            H = {h.strip().strip('"').lstrip("﻿").lower(): i for i, h in enumerate(text.split(delim))}
            print("delimiter", repr(delim), "header", list(H), flush=True)
            continue
        p = text.split(delim)
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

r.close()
tot_t = sum(v[0] for v in stratum.values())
tot_f = sum(v[1] for v in stratum.values())


def row(k):
    t = sum(v[0] for v in fam[k].values())
    fl = sum(v[1] for v in fam[k].values())
    exp = sum(v[0] * stratum[s][1] / stratum[s][0] for s, v in fam[k].items())
    raw = (fl / t) / (tot_f / tot_t)
    return {"family": k, "tests": t, "raw_rate": round(fl / t, 4), "raw_ratio": round(raw, 3),
            "matched_ratio": round(fl / exp, 3), "flattered_by_raw": round(raw - fl / exp, 3)}


then = {x["family"]: x for x in json.load(open(then_path))["table"]}
top = sorted(fam, key=lambda k: -sum(v[0] for v in fam[k].values()))[:20]
table = sorted((row(k) for k in top), key=lambda x: x["matched_ratio"])
compare = []
for k, old in then.items():
    if k in fam and sum(v[0] for v in fam[k].values()) >= 5000:
        new = row(k)
        compare.append({"family": k, "tests_2019": new["tests"], "matched_2019": new["matched_ratio"],
                        "matched_2023": old["matched_ratio"], "move": round(old["matched_ratio"] - new["matched_ratio"], 3),
                        "flatter_2019": new["flattered_by_raw"], "flatter_2023": old["flattered_by_raw"]})
compare.sort(key=lambda x: x["move"])
moves = [abs(x["move"]) for x in compare]
res = {"rows_read": rows, "tests_kept": tot_t, "fleet_rate": round(tot_f / tot_t, 4), "dates": [first, last],
       "families_compared": len(compare), "mean_abs_move": round(sum(moves) / len(moves), 3) if moves else None,
       "table": table, "compare": compare}
json.dump(res, open(out, "w"), indent=1)
print("rows", rows, "kept", tot_t, "fleet", res["fleet_rate"], "dates", first, last)
print("compared", res["families_compared"], "mean abs move", res["mean_abs_move"])
for x in compare:
    print("%-26s %8d  matched 2019 %.2f  2023 %.2f  move %+.2f  flatter %+.2f then %+.2f" % (
        x["family"], x["tests_2019"], x["matched_2019"], x["matched_2023"], x["move"], x["flatter_2019"], x["flatter_2023"]))
