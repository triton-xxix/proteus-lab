#!/usr/bin/env python3
"""13 Oct 2026, interactive, on Luke's word ("void those three rows"): move G-0075 to G-0077 out of
grinder/LEDGER.csv into grinder/VOIDED.csv, whole rows plus the date and reason. They were opened at
2026-10-12T22:54:22Z from the 11 Oct 22:23 snapshot because the 12 Oct scan died before writing its rows.
Their original form stays in git at 78f3ad8."""
import csv, os, sys
sys.path.insert(0, "/Users/triton/PROTEUS/grinder")
import paper as P

IDS = {"G-0075", "G-0076", "G-0077"}
REASON = ("entered from the 11 Oct 22:23Z snapshot (no 12 Oct snapshot: scan killed by a tool timeout "
          "before writing SNAPSHOTS.csv); prices and ages 24 h stale; voided on Luke's word, original in 78f3ad8")
ledger = P.load_ledger()
gone = [r for r in ledger if r["id"] in IDS]
assert len(gone) == 3 and all(r["entered_at"] == "2026-10-12T22:54:22Z" for r in gone), gone
keep = [r for r in ledger if r["id"] not in IDS]
fields = P.FIELDS + ["voided_on", "void_reason"]
new = not os.path.exists(P.VOIDED)
with open(P.VOIDED, "a", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=fields)
    if new:
        w.writeheader()
    for r in gone:
        w.writerow({**{k: r.get(k, "") for k in P.FIELDS}, "voided_on": "2026-10-13", "void_reason": REASON})
P.save_ledger(keep)
print("voided", sorted(r["id"] for r in gone), "ledger rows", len(ledger), "->", len(keep), "next id G-%04d" % P.next_id(keep))
for r in gone:
    print(r["id"], r["token"], "exit_at", r.get("exit_at") or "open", "pnl", r.get("pnl_gbp") or "-")
