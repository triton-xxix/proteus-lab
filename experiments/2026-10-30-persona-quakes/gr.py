"""Does the Gutenberg-Richter law hold on the last month of USGS earthquakes?

Persona pick, Fri 30 Oct 2026, trialling a candidate interest (live planet data). Stdlib only.
Usage: python3 gr.py /path/to/all_month.csv

The law: log10 N(>=M) = a - b M, with b about 1.0 worldwide. The b-value is estimated by Aki's
maximum-likelihood formula above a completeness magnitude Mc, b = log10(e) / (mean(M) - (Mc - dM/2)),
with dM the magnitude bin (0.1). Below Mc the catalogue misses events, so the fit is only above it.
"""
import csv
import math
import sys
from collections import Counter

path = sys.argv[1]
mags = []
types = Counter()
nets = Counter()
first = last = None
with open(path, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        types[row["type"]] += 1
        if row["type"] != "earthquake":
            continue
        try:
            m = float(row["mag"])
        except ValueError:
            continue
        mags.append(m)
        nets[row["net"]] += 1
        t = row["time"]
        first = t if first is None or t < first else first
        last = t if last is None or t > last else last

n = len(mags)
print("rows: %d earthquakes of %d events (%s)" % (n, sum(types.values()), ", ".join("%s %d" % kv for kv in types.most_common(4))))
print("span: %s to %s" % (first[:19], last[:19]))
print("largest: %.1f; count by whole magnitude:" % max(mags))
bins = Counter(math.floor(m) for m in mags)
for k in sorted(bins):
    print("  M%d.x  %5d" % (k, bins[k]))

def cum(th):
    return sum(1 for m in mags if m >= th - 1e-9)

def aki(mc, dm=0.1):
    sel = [m for m in mags if m >= mc - 1e-9]
    if len(sel) < 20:
        return None, len(sel)
    mean = sum(sel) / len(sel)
    b = math.log10(math.e) / (mean - (mc - dm / 2))
    se = b / math.sqrt(len(sel))  # Aki's standard error
    return (b, se), len(sel)

print("\nb-value (Aki MLE) by completeness cut:")
rows = []
for mc in (2.5, 3.0, 3.5, 4.0, 4.5, 5.0):
    r, k = aki(mc)
    if r:
        print("  Mc %.1f  n %5d  b %.2f +/- %.2f" % (mc, k, r[0], r[1]))
        rows.append((mc, k, r[0], r[1]))

# Magnitude of completeness, maximum-curvature method: the modal 0.1 bin, plus 0.2 as usual.
tenths = Counter(round(m, 1) for m in mags)
mode_bin = max(tenths.items(), key=lambda kv: (kv[1], -kv[0]))[0]
print("\nmaximum-curvature Mc: modal bin %.1f, so Mc about %.1f" % (mode_bin, mode_bin + 0.2))
# A global catalogue mixes dense regional networks (complete to M1) with the rest of the world (complete
# to about M4.5), so the global Mc by this method says nothing about the world outside the US.

# Prediction check: fit above Mc 4.5 and predict counts of M>=5, 6, 7 in the same month.
r, k = aki(4.5)
b = r[0]
a = math.log10(k) + b * 4.5
print("\nfit above M4.5: a %.2f b %.2f; predicted v observed this month:" % (a, b))
for th in (5.0, 5.5, 6.0, 6.5, 7.0):
    pred = 10 ** (a - b * th)
    print("  M>=%.1f  predicted %6.1f  observed %4d" % (th, pred, cum(th)))

# US networks only (the dense ones), where the catalogue is complete far lower.
us = {"ci", "nc", "uu", "uw", "nn", "mb", "se", "nm", "ld", "ok", "tx", "hv"}
us_mags = []
with open(path, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row["type"] == "earthquake" and row["net"] in us:
            try:
                us_mags.append(float(row["mag"]))
            except ValueError:
                pass
sel = [m for m in us_mags if m >= 1.5]
mean = sum(sel) / len(sel)
b_us = math.log10(math.e) / (mean - 1.45)
print("\ncontiguous-US and Hawaii networks (%s): %d quakes, %d at or above M1.5, b %.2f +/- %.2f" % (
    " ".join(sorted(us)), len(us_mags), len(sel), b_us, b_us / math.sqrt(len(sel))))
print("networks by count: %s" % ", ".join("%s %d" % kv for kv in nets.most_common(8)))
