#!/usr/bin/env python3
"""13 Oct 2026: does paper.open_book now refuse a stale snapshot? In memory only; nothing is saved."""
import sys
from datetime import timedelta
sys.path.insert(0, "/Users/triton/PROTEUS/grinder")
import paper as P

ledger = P.load_ledger()
snap_ts = P.parse(P.latest_snapshot()[0]["ts"])
held = {r["mint"] for r in ledger}
R = P.RULES
for label, t in (("now", P.now()), ("snapshot + 30 min", snap_ts + timedelta(minutes=30))):
    rows = list(ledger)
    n = P.open_book(rows, R["version"], 99, R["size_gbp"], 1e9, held, t)
    print(label, "latest snapshot", P.iso(snap_ts), "entries", n)
