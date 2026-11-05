"""P-0331: which MOT defect sections carry the Corsa v 3 Series gap (P-0326)?

Tests: P-0326's rows (sandbox/mot/vx-bmw-2023.csv, 1 Jan to 6 Mar 2023), same filters and strata
(class 4, NT, petrol or diesel, age 3 to 25, age year x 20k-mile band x fuel).
Items: DVSA dft_test_item_2023.zip streamed whole; rows kept only for those test ids; failure items
are rfr_type_code F or P (PRS). Section = item_detail.test_item_set_section_id named from item_group.
Per section: share of tests with at least one failure item there, each car standardised to the
3 Series stratum mix, and the Corsa minus 3 Series difference as a share of the total gap.
Usage: python3 -I defects.py OUT.json
"""
import csv
import io
import json
import struct
import sys
import urllib.request
import zipfile
import zlib
from collections import defaultdict

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/mot")
out = sys.argv[1]

# tests and strata (same rules as sandbox/mot/compare.py)
tests = {}
with open("/Users/triton/PROTEUS/sandbox/mot/vx-bmw-2023.csv") as f:
    for r in csv.DictReader(f):
        if r["test_class_id"].strip() != "4" or r["test_type"].strip() != "NT":
            continue
        mk, md = r["make"].strip().upper(), r["model"].strip().upper()
        car = "Corsa" if mk == "VAUXHALL" and md.startswith("CORSA") else (
            "3 Series" if mk == "BMW" and ((md[:1] == "3" and md[1:3].isdigit()) or md.startswith("3 SERIES")) else None)
        if not car or r["test_result"].strip() not in ("P", "F", "PRS") or r["fuel_type"].strip() not in ("PE", "DI"):
            continue
        try:
            td, fu = r["test_date"][:10], r["first_use_date"][:10]
            age = int(td[:4]) - int(fu[:4]) - (td[5:10] < fu[5:10])
            miles = int(float(r["test_mileage"]))
        except ValueError:
            continue
        if age < 3 or age > 25 or miles <= 0:
            continue
        tests[r["test_id"].strip()] = (car, (age, min(miles // 20000, 10), r["fuel_type"].strip()))
print("tests", len(tests), flush=True)

# lookups
z = zipfile.ZipFile("/Users/triton/PROTEUS/sandbox/mot/lookup.zip")
names = {}
for row in csv.DictReader(io.TextIOWrapper(z.open("item_group.csv"), "utf-8", errors="replace"), delimiter="|"):
    if row["test_class_id"] == "4" and row["parent_id"] == "0":
        names[row["test_item_id"]] = row["item_name"]
section = {}
for row in csv.DictReader(io.TextIOWrapper(z.open("item_detail.csv"), "utf-8", errors="replace"), delimiter="|"):
    if row["test_class_id"] == "4":
        section[row["rfr_id"]] = names.get(row["test_item_set_section_id"], "section " + row["test_item_set_section_id"])

# stream items
r = urllib.request.urlopen(urllib.request.Request(
    "https://data.dft.gov.uk/anonymised-mot-test/test_data/dft_test_item_2023.zip",
    headers={"User-Agent": "ProteusLab-mot-check/1.0"}), timeout=60)
h = r.read(30)
sig, _, _, method, _, _, _, _, _, nlen, xlen = struct.unpack("<IHHHHHIIIHH", h)
r.read(nlen + xlen)
d = zlib.decompressobj(-15)
hit = defaultdict(set)  # test_id -> sections with a failure item
buf, header, n = b"", None, 0
while True:
    chunk = r.read(1 << 20)
    if not chunk:
        break
    buf += d.decompress(chunk)
    lines = buf.split(b"\n")
    buf = lines.pop()
    for ln in lines:
        p = ln.decode("utf-8", "replace").rstrip("\r").split("|")
        if header is None:
            header = {k.strip().lower(): i for i, k in enumerate(p)}
            print("item header", list(header), flush=True)
            ti, ri, ty = header["test_id"], header["rfr_id"], header["rfr_type_code"]
            continue
        n += 1
        if len(p) > ty and p[ti] in tests and p[ty] in ("F", "P"):
            hit[p[ti]].add(section.get(p[ri], "unknown"))
print("item rows", n, "tests with a failure item", len(hit), flush=True)
json.dump({t: sorted(v) for t, v in hit.items()}, open(out.replace(".json", "-hits.json"), "w"))

# per section, standardised to the 3 Series mix
cnt = defaultdict(lambda: [0, defaultdict(int)])  # (car, stratum) -> tests, section -> tests failing there
for t, (car, s) in tests.items():
    c = cnt[(car, s)]
    c[0] += 1
    for sec in hit.get(t, ()):
        c[1][sec] += 1
keys = set(cnt)
strata = [s for (car, s) in keys if car == "3 Series" and ("Corsa", s) in keys
          and cnt[("Corsa", s)][0] >= 20 and cnt[("3 Series", s)][0] >= 20]
w_tot = sum(cnt[("3 Series", s)][0] for s in strata)
secs = sorted({sec for v in cnt.values() for sec in v[1]})


def std(car, sec=None):
    tot = 0.0
    for s in strata:
        t, by = cnt[(car, s)]
        rate = by.get(sec, 0) / t
        tot += cnt[("3 Series", s)][0] / w_tot * rate
    return tot


rows = []
for sec in secs:
    c, b = std("Corsa", sec), std("3 Series", sec)
    rows.append({"section": sec, "corsa": round(c, 4), "3series": round(b, 4), "ratio": round(c / b, 2) if b else None, "diff": round(c - b, 4)})
rows.sort(key=lambda x: -x["diff"])
total_diff = sum(x["diff"] for x in rows)
for x in rows:
    x["share_of_summed_diff"] = round(x["diff"] / total_diff, 3) if total_diff else None
res = {"tests": len(tests), "item_rows": n, "tests_with_failure_item": len(hit), "strata": len(strata), "sections": rows}
json.dump(res, open(out, "w"), indent=1)
for x in rows[:14]:
    print("%-40s corsa %.3f  3s %.3f  x%s  diff %+.4f  share %s" % (x["section"][:40], x["corsa"], x["3series"], x["ratio"], x["diff"], x["share_of_summed_diff"]))
