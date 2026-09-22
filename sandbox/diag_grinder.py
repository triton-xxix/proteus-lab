"""Nightly diagnostic: why did the Grinder open zero positions?

Mirrors paper.py's `passes()` exactly, then reports per-gate pass counts and a
leave-one-out sweep, so a single binding gate is visible instead of a silent zero.
Diagnostic only. It never writes to the ledger and never changes the rules.
"""
import csv

PATH = "/Users/triton/PROTEUS/grinder/SNAPSHOTS.csv"


def fnum(x):
    try:
        return float(x)
    except Exception:
        return None


GATES = {
    "age 1-48h": lambda r: (lambda a: a is not None and 1.0 <= a <= 48.0)(fnum(r.get("age_h"))),
    "mint revoked": lambda r: (r.get("mint_auth") or "") in ("", "None"),
    "freeze revoked": lambda r: (r.get("freeze_auth") or "") in ("", "None"),
    "liq >= 20k": lambda r: (lambda v: v is not None and v >= 20000)(fnum(r.get("liq_usd"))),
    "vol24 >= 200k": lambda r: (lambda v: v is not None and v >= 200000)(fnum(r.get("vol_h24"))),
    "vol1h >= 10k": lambda r: (lambda v: v is not None and v >= 10000)(fnum(r.get("vol_h1"))),
    "top10 <= 30pct": lambda r: (lambda v: v is not None and v <= 30.0)(fnum(r.get("top10_pct"))),
    "holders >= 300": lambda r: (lambda v: v is None or v >= 300)(fnum(r.get("holders"))),
    "lp >= 90pct": lambda r: (lambda v: v is None or v >= 90.0)(fnum(r.get("lp_locked_pct"))),
    "price present": lambda r: fnum(r.get("price_usd")) not in (None, 0.0),
}

with open(PATH, newline="") as fh:
    rows = list(csv.DictReader(fh))
if not rows:
    raise SystemExit("no snapshot rows")

latest = max(r["ts"] for r in rows)
batch = [r for r in rows if r["ts"] == latest]
print("latest batch %s rows %d" % (latest, len(batch)))

blank = {}
for r in batch:
    for k, v in r.items():
        if not v:
            blank[k] = blank.get(k, 0) + 1
print("blank fields:", {k: v for k, v in sorted(blank.items(), key=lambda x: -x[1])})

for name, fn in GATES.items():
    print("%-16s pass %3d / %d" % (name, sum(1 for r in batch if fn(r)), len(batch)))

print("pass all: %d" % sum(1 for r in batch if all(f(r) for f in GATES.values())))

print("-- leave one out --")
for drop in GATES:
    n = sum(1 for r in batch if all(f(r) for k, f in GATES.items() if k != drop))
    print("%-16s drop -> %d" % (drop, n))
