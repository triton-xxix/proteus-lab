"""Refill 49: MOT fail rate by make for cars aged 10 to 12, from DfT's anonymised 2023 test results.

Stdlib only, streams the zip without unpacking it. Usage: python3 mot_by_make.py /path/to/dft_test_result_2023.zip
Rows: class 4 (cars and light vans up to 3,000 kg), normal tests (test_type NT), vehicle age 10 to 12
whole years at test. Initial fail = result F or PRS (pass after rectification at the station: the car
failed first). The national figure for comparison is P-0247's 27.5%.
"""
import csv
import io
import os
import sys
import zipfile
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
path = sys.argv[1]
MIN_TESTS = 20_000

tests = Counter()
fails = Counter()
prs = Counter()
total = Counter()  # all class-4 NT, any age
rows = 0
import contextlib
import gzip

# The 2017+ zips are Deflate64 (compress type 9), which Python's zipfile cannot read; the 2005 to 2016
# files are plain gzip of the same pipe-delimited layout, so either is accepted here.
OLD_COLS = ["test_id", "vehicle_id", "test_date", "test_class_id", "test_type", "test_result", "test_mileage",
            "postcode_area", "make", "model", "colour", "fuel_type", "cylinder_capacity", "first_use_date"]


def streams(path):
    if path.endswith(".gz"):
        yield os.path.basename(path), gzip.open(path, "rt", encoding="utf-8", errors="replace", newline="")
        return
    with zipfile.ZipFile(path) as z:
        for m in z.namelist():
            if not m.endswith("/"):
                yield m, io.TextIOWrapper(z.open(m), encoding="utf-8", errors="replace", newline="")


if True:
    for m, text in streams(path):
        with contextlib.closing(text):
            head = text.readline()
            delim = "|" if head.count("|") > head.count(",") else ","
            cols = [c.strip().lower() for c in head.strip().split(delim)]
            first_data = None
            if "test_result" not in cols:
                first_data = head
                cols = OLD_COLS
            print("member:", m, "columns:", cols)
            ix = {c: i for i, c in enumerate(cols)}
            c_class, c_type, c_res, c_date, c_first, c_make = (ix[k] for k in ("test_class_id", "test_type", "test_result", "test_date", "first_use_date", "make"))
            import itertools
            for line in (itertools.chain([first_data], text) if first_data else text):
                rows += 1
                f = line.rstrip("\n").split(delim)
                if len(f) <= c_make:
                    continue
                if f[c_class] != "4" or f[c_type] != "NT":
                    continue
                res = f[c_res]
                total["tests"] += 1
                if res in ("F", "PRS"):
                    total["fails"] += 1
                try:
                    age = int(f[c_date][:4]) - int(f[c_first][:4])
                except ValueError:
                    continue
                if not 10 <= age <= 12:
                    continue
                make = f[c_make].strip().upper()
                tests[make] += 1
                if res in ("F", "PRS"):
                    fails[make] += 1
                if res == "PRS":
                    prs[make] += 1

L = ["# MOT %s, class 4 normal tests, cars aged 10 to 12: initial fail rate by make" % os.path.basename(path), ""]
L.append("Rows read %d. All-age class-4 normal tests %d, initial fails (F or PRS) %d, rate %.1f%% (P-0247's national figure 27.5%%)." % (
    rows, total["tests"], total["fails"], 100 * total["fails"] / max(1, total["tests"])))
n10 = sum(tests.values())
f10 = sum(fails.values())
L.append("Aged 10 to 12: %d tests, %d initial fails, rate %.1f%%; makes with at least %d tests ranked below." % (n10, f10, 100 * f10 / max(1, n10), MIN_TESTS))
ranked = sorted(((100 * fails[m] / tests[m], m) for m in tests if tests[m] >= MIN_TESTS))
L += ["", "| rank | make | tests | initial fail rate | of which PRS |", "|---|---|---|---|---|"]
for i, (r, m) in enumerate(ranked[:3], 1):
    L.append("| least %d | %s | %d | %.1f%% | %.1f%% |" % (i, m, tests[m], r, 100 * prs[m] / tests[m]))
L.append("| ... | | | | |")
for i, (r, m) in enumerate(ranked[-3:][::-1], 1):
    L.append("| most %d | %s | %d | %.1f%% | %.1f%% |" % (i, m, tests[m], r, 100 * prs[m] / tests[m]))
L += ["", "Full table (%d makes):" % len(ranked), "", "| make | tests | fail rate |", "|---|---|---|"]
for r, m in ranked:
    L.append("| %s | %d | %.1f%% |" % (m, tests[m], r))
open(os.path.join(HERE, "RESULT.md"), "w").write("\n".join(L) + "\n")
print("\n".join(L[:14]))
