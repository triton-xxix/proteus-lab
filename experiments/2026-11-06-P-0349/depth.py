#!/usr/bin/env python3
"""Sell-all books on Smarkets: is the gap real size, and is it still there a minute later? Read-only, paper only.

For every open market where every open contract has a bid, sum the best bids. Above 100 means selling every outcome
collects more than the one winner can pay. Lockable size is the smallest top-of-book quantity across the contracts.
Reads twice, 60 s apart. Quantity is reported raw and divided by 10,000; that unit is not confirmed by a document.

Commission is unverified, so two readings at a stated 2%: on net market profit, and the harsh one, 2% of all premium.
No per-contract prices are written or printed, so a later blind call on these markets stays blind.
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, "/Users/triton/PROTEUS/exchange")
import exchange as X  # noqa: E402

HERE = Path(__file__).resolve().parent
RATE = 0.02


def read(mkts):
    books = {}
    for batch in X.chunks(mkts, 15):
        ids = ",".join(m["id"] for m in batch)
        cs = X.get(f"/markets/{ids}/contracts/").get("contracts", [])
        time.sleep(1)
        qs = X.get(f"/markets/{ids}/quotes/")
        time.sleep(1)
        for m in batch:
            mine = [c for c in cs if c["market_id"] == m["id"] and c.get("state_or_outcome", "open") in ("open", None)]
            if len(mine) < 2:
                continue
            legs = []
            for c in mine:
                bids = qs.get(c["id"], {}).get("bids", [])
                if not bids:
                    legs = None
                    break
                top = max(bids, key=lambda b: b["price"])
                legs.append((top["price"] / 100, top["quantity"] / 10000))
            if legs:
                books[m["id"]] = {"name": m.get("name"), "n": len(legs), "sum": round(sum(p for p, _ in legs), 2),
                                  "size": round(min(q for _, q in legs), 2)}
    return books


def main():
    evs = X.events()
    mkts = []
    for ids in X.chunks([e["id"] for e in evs], 20):
        mkts += X.get(f"/events/{','.join(ids)}/markets/").get("markets", [])
        time.sleep(1)
    print("events", len(evs), "markets", len(mkts), flush=True)
    a = read(mkts)
    time.sleep(60)
    b = read(mkts)

    locks = {k: v for k, v in a.items() if v["sum"] > 100}
    still = {k: v for k, v in b.items() if k in locks and v["sum"] > 100}
    rows = []
    for k, v in locks.items():
        edge = v["sum"] - 100
        rows.append({
            "market": k, "name": v["name"], "contracts": v["n"], "sum_first": v["sum"], "size_first": v["size"],
            "sum_after_60s": b.get(k, {}).get("sum"), "size_after_60s": b.get(k, {}).get("size"),
            "edge_points": round(edge, 2),
            "survives_net_commission": edge * (1 - RATE) > 0,
            "survives_harsh_commission": edge - RATE * v["sum"] > 0,
            "max_lockable_units_gross": round(v["size"] * edge / 100, 4),
        })
    sums = sorted(v["sum"] for v in a.values())
    out = {
        "at": X.now(), "markets_read": len(mkts), "full_bid_books": len(a),
        "median_sell_all": sums[len(sums) // 2] if sums else None,
        "books_over_100_first": len(locks), "still_over_100_after_60s": len(still),
        "unchanged_after_60s": sum(1 for k, v in locks.items() if b.get(k, {}).get("sum") == v["sum"]),
        "rows": rows,
    }
    (HERE / "results.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
