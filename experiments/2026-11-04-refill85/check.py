"""Refill #85 look: coverage of Meteostat 07156 (Paris-Montsouris) daily tmax and Open-Meteo previous-runs
meteofrance_seamless + icon_seamless at Montsouris, Sep 1 to Nov 2 2026."""
import csv
import gzip
import io
import json

S = "/Users/triton/PROTEUS/sandbox/"
rows = list(csv.reader(io.StringIO(gzip.decompress(open(S + "meteostat-07156.csv.gz", "rb").read()).decode())))
tx = {r[0]: r[3] for r in rows if len(r) > 3}
autumn = sorted(d for d in tx if "2026-09-01" <= d <= "2026-11-02")
print("meteostat rows", len(rows), "last", rows[-1][0], "sep-nov days", len(autumn),
      "with tmax", sum(1 for d in autumn if tx[d]))
h = json.load(open(S + "om-prevruns-paris-mf-lead0-6.json"))["hourly"]
for k in sorted(h):
    if k == "time":
        continue
    print(k, "non-null hours", sum(1 for v in h[k] if v is not None), "of", len(h[k]))
