#!/usr/bin/env python3
"""P-0139, 13 Oct 2026: backfill the R01 shadow book (grinder/harness/VARIANTS-3.md line 40) for the
snapshots from 2026-10-08T12:00Z that came before --apply-r01 was wired (P-0121). For each night, in order:
close R01's open rows at that night's paper time with exit_v02 on minute candles, then enter by
paper.select_r01 at the time v0.2 entered that night (its first G- row after the snapshot), price from
the snapshot. Then close what is still open as of now. Writes grinder/LEDGER-R01.csv and lists the ids
it wrote in backfill.json. Refuses to run if LEDGER-R01.csv already has rows.

    /Users/triton/PROTEUS/.venv/bin/python3 backfill.py
"""
import csv, json, sys, time
from collections import defaultdict
from datetime import timedelta
sys.path.insert(0, "/Users/triton/PROTEUS/grinder")
import paper as P

OUT = "/Users/triton/PROTEUS/experiments/2026-10-13-P-0139/"
existing = list(csv.DictReader(open(P.LEDGER_R01))) if P.os.path.exists(P.LEDGER_R01) else []
assert not existing, "LEDGER-R01.csv already has rows; backfill is for an empty book"

snaps = defaultdict(list)
for r in csv.DictReader(open(P.SNAPS)):
    if r["ts"] >= P.R01_FROM:
        snaps[r["ts"]].append(r)
g_rows = P.load_ledger() + (list(csv.DictReader(open(P.VOIDED))) if P.os.path.exists(P.VOIDED) else [])
tg = P.telegram_counts()
ledger, log, nid = [], [], 1
for ts in sorted(snaps):
    t_snap = P.parse(ts)
    after = sorted(r["entered_at"] for r in g_rows if r.get("rule_version") == "v0.2"
                   and t_snap <= P.parse(r["entered_at"]) <= t_snap + timedelta(hours=3))
    t_in = P.parse(after[0]) if after else t_snap + timedelta(minutes=5)
    for r in [r for r in ledger if not r.get("exit_at")]:
        P.exit_v02(r, t_in); time.sleep(0.5)
    still = [r for r in ledger if not r.get("exit_at")]
    realised = sum(P.fnum(r["pnl_gbp"]) or 0 for r in ledger if r.get("pnl_gbp"))
    bankroll = P.RULES["bankroll_gbp"] + realised - P.RULES["size_gbp"] * len(still)
    slots = P.RULES["max_open"] - len(still)
    picks = []
    if slots > 0 and bankroll >= P.RULES["size_gbp"]:
        picks = P.select_r01(snaps[ts], {r["mint"] for r in ledger}, slots, tg)
    for s in picks:
        ledger.append({"id": "R-%04d" % nid, "entered_at": P.iso(t_in), "token": s.get("symbol"), "mint": s["mint"],
                       "entry_price_usd": s["price_usd"], "size_gbp": P.RULES["size_gbp"], "rule_version": "R01",
                       "entry_liq_usd": s.get("liq_usd"), "rugged": ""})
        nid += 1
    log.append({"snapshot": ts, "entered_at": P.iso(t_in), "still_open_before": len(still), "slots": slots,
                "picks": [s.get("symbol") for s in picks]})
    print(ts, "entry", P.iso(t_in), "open before", len(still), "picks", [s.get("symbol") for s in picks])
t = P.now()
for r in [r for r in ledger if not r.get("exit_at")]:
    P.exit_v02(r, t); time.sleep(0.5)
with open(P.LEDGER_R01, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=P.FIELDS)
    w.writeheader()
    for r in ledger:
        w.writerow({k: r.get(k, "") for k in P.FIELDS})
closed = [r for r in ledger if r.get("exit_at")]
pnl = sum(P.fnum(r["pnl_gbp"]) or 0 for r in closed)
res = {"backfilled_ids": [r["id"] for r in ledger], "nights": log, "rows": len(ledger), "closed": len(closed),
       "rugged": sum(r.get("rugged") == "1" for r in closed), "pnl_gbp": round(pnl, 2),
       "reasons": sorted(r.get("exit_reason") for r in closed)}
json.dump(res, open(OUT + "backfill.json", "w"), indent=1)
print("rows", len(ledger), "closed", len(closed), "rugged", res["rugged"], "pnl GBP", res["pnl_gbp"], res["reasons"])
