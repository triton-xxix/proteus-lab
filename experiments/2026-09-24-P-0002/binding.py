#!/usr/bin/env python3
"""P-0002: after the age gate, which Grinder gate binds next, per snapshot?

Same gate definitions as sandbox/diag_grinder.py (mirrors paper.py's passes()). For every snapshot
batch: rows in the 1-48h window, per-gate pass counts among those rows, leave-one-out among those
rows, and the single-gate drop that would add most entries. Diagnostic only; rules untouched.
Output: REPORT.md next to this file.
"""
import csv, itertools
PATH = "/Users/triton/PROTEUS/grinder/SNAPSHOTS.csv"
def fnum(x):
    try: return float(x)
    except Exception: return None
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
rows = [r for r in csv.DictReader(open(PATH)) if r["ts"].startswith("20")]
out = ["# P-0002: the next binding gate after age", ""]
for ts in sorted({r["ts"] for r in rows}):
    batch = [r for r in rows if r["ts"] == ts]
    win = [r for r in batch if GATES["age 1-48h"](r)]
    passing = [r for r in win if all(f(r) for f in GATES.values())]
    out += ["## %s: %d rows, %d in the age window, %d pass everything" % (ts, len(batch), len(win), len(passing)), "",
            "| gate | pass among in-window | drop it alone, entries become |", "|---|---|---|"]
    for name, fn in GATES.items():
        if name == "age 1-48h": continue
        p = sum(1 for r in win if fn(r))
        loo = sum(1 for r in win if all(f(r) for k, f in GATES.items() if k != name))
        out.append("| %s | %d / %d | %d |" % (name, p, len(win), loo))
    # which single gate is the sole reason for the most near-misses
    sole = {}
    for r in win:
        fails = [k for k, f in GATES.items() if not f(r)]
        if len(fails) == 1: sole[fails[0]] = sole.get(fails[0], 0) + 1
    out += ["", "Rows failing exactly one gate: " + (", ".join("%s %d" % kv for kv in sorted(sole.items(), key=lambda x: -x[1])) or "none"), ""]
    # vol1h and vol24 values for in-window rows, to see how far off they sit
    v1 = sorted(fnum(r.get("vol_h1")) or 0 for r in win); v24 = sorted(fnum(r.get("vol_h24")) or 0 for r in win)
    if win:
        out += ["In-window vol_h1 median $%.0f, top quartile $%.0f; vol_h24 median $%.0f, top quartile $%.0f." % (
            v1[len(v1)//2], v1[(3*len(v1))//4], v24[len(v24)//2], v24[(3*len(v24))//4]), ""]
open("/Users/triton/PROTEUS/experiments/2026-09-24-P-0002/REPORT.md", "w").write("\n".join(out) + "\n")
print("\n".join(out))
