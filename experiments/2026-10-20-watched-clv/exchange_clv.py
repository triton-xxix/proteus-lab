"""Closing-line value for the exchange book, from its own public snapshots.
For each call: the first snapshot mid at or after the commit (the anchor), and the last snapshot
mid with state open before settlement (or the latest one, if still open). CLV is the move from
anchor to close in the direction of my call: positive if the market came towards me.
Mids are Smarkets basis points (10000 = certain). Read-only on exchange/BOOK.csv and SNAPSHOTS.csv."""
import csv
from collections import defaultdict

BOOK = "/Users/triton/PROTEUS/exchange/BOOK.csv"
SNAPS = "/Users/triton/PROTEUS/exchange/SNAPSHOTS.csv"

calls = list(csv.DictReader(open(BOOK, encoding="utf-8")))
want = {c["contract_id"] for c in calls}
series = defaultdict(list)
with open(SNAPS, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["contract_id"] in want and r["mid"] and r["state"] == "open":
            try:
                series[r["contract_id"]].append((r["snap_utc"], float(r["mid"]) / 10000))
            except ValueError:
                pass

print("id      p     anchor  close   clv     n_snaps  outcome  contract")
rows = []
for c in calls:
    s = sorted(series.get(c["contract_id"], []))
    after = [x for x in s if x[0] >= c["committed_at"]]
    if c["settled_at"]:
        after = [x for x in after if x[0] < c["settled_at"]]
    if len(after) < 2:
        print(f"{c['id']}  {float(c['p']):.2f}  too few snapshots ({len(after)})  {c['outcome'] or 'open'}  {c['contract']}")
        continue
    a, z = after[0][1], after[-1][1]
    side = 1 if float(c["p"]) > a else -1
    clv = side * (z - a)
    rows.append((c["id"], clv, c["outcome"]))
    print(f"{c['id']}  {float(c['p']):.2f}  {a:.3f}  {z:.3f}  {clv:+.3f}  {len(after):7}  {c['outcome'] or 'open':8} {c['contract']}")

if rows:
    pos = sum(1 for _, v, _ in rows if v > 0)
    neg = sum(1 for _, v, _ in rows if v < 0)
    print(f"\n{len(rows)} calls with a line: mean CLV {sum(v for _, v, _ in rows)/len(rows):+.4f}; "
          f"market came towards me {pos}, away {neg}, flat {len(rows)-pos-neg}")
