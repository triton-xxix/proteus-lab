#!/usr/bin/env python3
"""P-0121, 13 Oct 2026: R01 (grinder/harness/VARIANTS-3.md) selection replayed on every snapshot from
2026-10-08T12:00Z, beside v0.2's own ranking. Read-only. Answers: can R01 be wired as written, i.e. does
MENTIONS.csv carry a Telegram row for the gate-passers R01 would reach, and how often does R01 pick
differently from v0.2?"""
import csv, json, sys
from collections import defaultdict
sys.path.insert(0, "/Users/triton/PROTEUS/grinder")
import paper as P

ROOT = "/Users/triton/PROTEUS/"
OUT = ROOT + "experiments/2026-10-13-P-0121/"
FROM = "2026-10-08T12:00:00Z"

snaps = defaultdict(list)
for r in csv.DictReader(open(ROOT + "grinder/SNAPSHOTS.csv")):
    if r["ts"] >= FROM:
        snaps[r["ts"]].append(r)
tg = {}
for m in csv.DictReader(open(ROOT + "grinder/research/MENTIONS.csv")):
    if m["source"] == "telegram":
        tg[(m["mint"], m["night"][:10])] = int(m["count"] or 0)


def markers(s):
    out = []
    if (s.get("rug_risks") or "").strip():
        out.append("rug_risk")
    if (P.fnum(s.get("chg_h1")) or 0) > 0:
        out.append("chg_h1_up")
    c = tg.get((s["mint"], s["ts"][:10]))
    if c == 0:
        out.append("tg_silent")
    return out, c


nights = []
for ts in sorted(snaps):
    passers = sorted([s for s in snaps[ts] if P.passes(s)], key=lambda s: -(P.fnum(s.get("vol_h1")) or 0))
    v02 = [s["symbol"] for s in passers[:4]]
    r01, tg_known, tg_unknown = [], 0, 0
    for s in passers:
        mk, c = markers(s)
        tg_known += c is not None; tg_unknown += c is None
        if not mk and len(r01) < 4:
            r01.append(s["symbol"])
    nights.append({"snapshot": ts, "passers": len(passers), "v02_top4": v02, "r01_top4": r01,
                   "same_picks": len(set(v02) & set(r01)), "tg_known": tg_known, "tg_unknown": tg_unknown})
json.dump(nights, open(OUT + "result.json", "w"), indent=1)
for n in nights:
    print(n["snapshot"], "passers", n["passers"], "v0.2", n["v02_top4"], "R01", n["r01_top4"],
          "overlap", n["same_picks"], "tg rows", n["tg_known"], "of", n["passers"])
