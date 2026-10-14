#!/usr/bin/env python3
"""P-0149: P-0141 leg three. No RPC calls. From experiments/2026-10-14-P-0141/results.json (51 KOL-signed
trenchcat and Normie transactions inside 11 Oct 21:23:37Z to 23:23:37Z), place each trade before or after
the Grinder pick (G-0072 trenchcat, G-0074 Normie, both 22:28:10Z) and classify buy v sell from the sign of
the KOL token account's delta. Report, per KOL: net before, net after, and whether the KOL was a net buyer
before and a net seller after (the "KOL front-runs the pick" shape)."""
import json, time

SRC = "/Users/triton/PROTEUS/experiments/2026-10-14-P-0141/results.json"
OUT = "/Users/triton/PROTEUS/experiments/2026-10-14-P-0149/results.json"
PICK = 1791757690   # 2026-10-11T22:28:10Z
iso = lambda t: time.strftime("%H:%M:%SZ", time.gmtime(t))

R = json.load(open(SRC))
kols = []
for c in R["candidates"]:
    txs = [t for t in c.get("txs", []) if t.get("kol_signed") or t.get("ata_changed")]
    if not txs:
        continue
    before = [t for t in txs if t["time"] < PICK]
    after = [t for t in txs if t["time"] >= PICK]
    net = lambda L: round(sum(t.get("ata_delta") or 0 for t in L), 2)
    buys = sum(1 for t in txs if (t.get("ata_delta") or 0) > 0)
    sells = sum(1 for t in txs if (t.get("ata_delta") or 0) < 0)
    zero = sum(1 for t in txs if not t.get("ata_delta"))
    rec = {"name": c["name"], "symbol": c["symbol"], "txs": len(txs), "buys": buys, "sells": sells, "zero_delta": zero,
           "before_n": len(before), "after_n": len(after), "net_before": net(before), "net_after": net(after),
           "net_total": net(txs), "first": iso(txs[-1]["time"]), "last": iso(txs[0]["time"]),
           "mins_from_pick_first": round((min(t["time"] for t in txs) - PICK) / 60, 1),
           "mins_from_pick_last": round((max(t["time"] for t in txs) - PICK) / 60, 1),
           "trades": sorted([{"t": iso(t["time"]), "mins_from_pick": round((t["time"] - PICK) / 60, 1),
                              "delta": t.get("ata_delta"), "programs": t.get("programs")} for t in txs], key=lambda x: x["t"])}
    rec["net_buyer_before_net_seller_after"] = rec["net_before"] > 0 and rec["net_after"] < 0
    rec["all_before"] = not after
    rec["all_after"] = not before
    kols.append(rec)
    print("%-10s %-9s txs %2d (b %2d s %2d z %d) | before %2d net %14.2f | after %2d net %14.2f | total %14.2f | %s to %s (%+.0f to %+.0f min) %s" % (
        rec["name"], rec["symbol"], rec["txs"], buys, sells, zero, len(before), rec["net_before"], len(after), rec["net_after"],
        rec["net_total"], rec["first"], rec["last"], rec["mins_from_pick_first"], rec["mins_from_pick_last"],
        "FRONT-RUN SHAPE" if rec["net_buyer_before_net_seller_after"] else ""))

summary = {
    "kols": len(kols), "txs": sum(k["txs"] for k in kols),
    "net_buyer_before_and_net_seller_after": [k["name"] for k in kols if k["net_buyer_before_net_seller_after"]],
    "all_trades_before_pick": [k["name"] for k in kols if k["all_before"]],
    "all_trades_after_pick": [k["name"] for k in kols if k["all_after"]],
    "straddle": [k["name"] for k in kols if not k["all_before"] and not k["all_after"]],
    "net_sellers_overall": [k["name"] for k in kols if k["net_total"] < 0],
    "net_buyers_overall": [k["name"] for k in kols if k["net_total"] > 0],
    "flat_overall": [k["name"] for k in kols if k["net_total"] == 0],
    "txs_before": sum(k["before_n"] for k in kols), "txs_after": sum(k["after_n"] for k in kols),
}
json.dump({"probe": "P-0149", "pick_utc": PICK, "kols": kols, "summary": summary}, open(OUT, "w"), indent=1)
print(json.dumps(summary))
