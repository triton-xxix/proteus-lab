"""D-019 and D-021: pull the W1 rows of the 7 Nov scan for the four forward rules.

Usage: python3 -I read.py /Users/triton/PROTEUS/edges/scan/2026-11-07/results.json
Prints the structure of one rule's record and the four rules' W1 fields, nothing recomputed.
"""
import json
import sys

WANT = [
    ("E-013", "VWAP cross after 11:00, hold to close", "stock"),
    ("E-014", "ORB 15m fade (failed break)", "stock"),
    ("E-015", "ORB NY open 30m, target 1R", "crypto"),
    ("E-016", "Opening drive: first bar direction to 11:00", "stock"),
]

d = json.load(open(sys.argv[1]))
print("run_at:", d["run_at"], "span:", json.dumps(d["span"]))
for eid, name, kind in WANT:
    hits = [r for r in d["rules"] if r["rule"] == name and r["kind"] == kind]
    assert len(hits) == 1, (eid, len(hits))
    w = hits[0]["W1"]
    above_zero = w["total_pct"] > 0
    # The line compares the week against the control mean. W1 fields carry both on a per-trade
    # basis (mean_pct v control_mean_pct); the week total of the control is n times its mean.
    control_total = round(w["n"] * w["control_mean_pct"], 3)
    above_control = w["total_pct"] > control_total
    print(eid, name, json.dumps(w), "control_total_pct", control_total,
          "above_zero", above_zero, "above_control", above_control,
          "PASS" if above_zero and above_control else "FAIL")
