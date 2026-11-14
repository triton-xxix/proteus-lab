#!/usr/bin/env python3
"""Do the contracts of one Smarkets market add up to 100%?

Reads exchange/SNAPSHOTS.csv (my own public history, prices in 1/100 of a percent).
For each snapshot and market with at least two contracts, all two-sided and open:
  back_all = sum of offers: cost of buying every outcome. Below 100 is free money if the list is exhaustive.
  lay_all  = sum of bids: what selling every outcome collects. Above 100 is free money always,
             because at most one contract can win.
  width    = back_all - lay_all, the round-trip toll for the whole book.
Stdlib only. Prints totals and writes results.json next to this file. No per-market prices are printed
for markets still open tonight, so it cannot unblind a later call.
"""
import csv
import json
import os
import statistics as st
from collections import defaultdict

SRC = "/Users/triton/PROTEUS/exchange/SNAPSHOTS.csv"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")


def kind(event, market):
    text = (event + " " + market).lower()
    if "highest temperature" in text:
        return "weather"
    return "other"


def main():
    books = defaultdict(list)
    names = {}
    snaps = set()
    rows = 0
    with open(SRC, newline="") as f:
        for r in csv.DictReader(f):
            rows += 1
            snaps.add(r["snap_utc"])
            key = (r["snap_utc"], r["market_id"])
            names[r["market_id"]] = r["market"] or r["event"]
            books[key].append(r)

    latest = max(snaps)
    full = []
    for (snap, mid), cs in books.items():
        if len(cs) < 2:
            continue
        try:
            bids = [float(c["bid"]) for c in cs]
            offers = [float(c["offer"]) for c in cs]
        except ValueError:
            continue
        if any(c["state"] != "open" for c in cs) or min(bids) <= 0 or min(offers) <= 0:
            continue
        full.append(
            {
                "snap": snap,
                "market": mid,
                "kind": kind(cs[0]["event"], cs[0]["market"]),
                "n": len(cs),
                "back": sum(offers) / 100,
                "lay": sum(bids) / 100,
            }
        )

    out = {"rows": rows, "snapshots": len(snaps), "latest": latest, "full_books": len(full), "kinds": {}}
    for k in ("weather", "other"):
        sub = [b for b in full if b["kind"] == k]
        if not sub:
            continue
        back = [b["back"] for b in sub]
        lay = [b["lay"] for b in sub]
        width = [b["back"] - b["lay"] for b in sub]
        out["kinds"][k] = {
            "books": len(sub),
            "markets": len({b["market"] for b in sub}),
            "median_contracts": st.median(b["n"] for b in sub),
            "median_back_all": round(st.median(back), 2),
            "median_lay_all": round(st.median(lay), 2),
            "median_width": round(st.median(width), 2),
            "back_below_100": sum(1 for x in back if x < 100),
            "lay_above_100": sum(1 for x in lay if x > 100),
        }

    locks = [b for b in full if b["lay"] > 100]
    out["lay_locks"] = {
        "books": len(locks),
        "markets": len({b["market"] for b in locks}),
        "largest_pct_points": round(max((b["lay"] - 100 for b in locks), default=0), 2),
    }
    out["lay_lock_examples_closed"] = sorted(
        (
            {"snap": b["snap"], "market": names[b["market"]], "lay_all": round(b["lay"], 2)}
            for b in locks
            if b["snap"] != latest
        ),
        key=lambda x: -x["lay_all"],
    )[:5]
    tonight = [b for b in full if b["snap"] == latest]
    out["tonight"] = {
        "full_books": len(tonight),
        "median_back_all": round(st.median(b["back"] for b in tonight), 2) if tonight else None,
        "median_lay_all": round(st.median(b["lay"] for b in tonight), 2) if tonight else None,
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
