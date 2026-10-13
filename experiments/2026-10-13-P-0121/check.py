#!/usr/bin/env python3
"""P-0121 attempt 2, 13 Oct 2026: does the wired paper.select_r01 pick what replay.py picked on every
snapshot since R01_FROM? Read-only: no ledger written, no network."""
import csv, json, sys
from collections import defaultdict
sys.path.insert(0, "/Users/triton/PROTEUS/grinder")
import paper as P

OUT = "/Users/triton/PROTEUS/experiments/2026-10-13-P-0121/"
replay = {n["snapshot"]: n for n in json.load(open(OUT + "result.json"))}
snaps = defaultdict(list)
for r in csv.DictReader(open(P.SNAPS)):
    if r["ts"] >= P.R01_FROM:
        snaps[r["ts"]].append(r)
tg = P.telegram_counts()
rows, match = [], 0
for ts in sorted(snaps):
    wired = [s["symbol"] for s in P.select_r01(snaps[ts], set(), 4, tg)]
    old = replay.get(ts, {}).get("r01_top4")
    same = old is not None and wired == old
    match += same
    rows.append({"snapshot": ts, "wired": wired, "replay": old, "same": same})
    print(ts, "wired", wired, "replay", old, "SAME" if same else "DIFF")
print("match", match, "of", len(rows), "nights;", sum(r["replay"] is not None for r in rows), "in the replay")
json.dump({"nights": rows, "match": match, "of": len(rows)}, open(OUT + "check.json", "w"), indent=1)
