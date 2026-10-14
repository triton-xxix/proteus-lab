#!/usr/bin/env python3
"""P-0141 follow-up: recount.py fetched only the 40 newest signatures for Daumen's trenchcat account and
found none in the window; its newest were after the window. Fetch up to 1000 and count properly."""
import json, time
import requests

RPC = "https://api.mainnet-beta.solana.com"
R = json.load(open("/Users/triton/PROTEUS/experiments/2026-10-14-P-0141/results.json"))
lo, hi = R["window"]
for c in R["candidates"]:
    if c["sigs_in_window"] == 0:
        sigs = requests.post(RPC, json={"jsonrpc": "2.0", "id": 1, "method": "getSignaturesForAddress",
                                        "params": [c["ata"], {"limit": 1000}]}, timeout=30).json().get("result") or []
        times = sorted(s["blockTime"] for s in sigs if s.get("blockTime"))
        win = [t for t in times if lo <= t <= hi]
        before = [t for t in times if t < lo]
        after = [t for t in times if t > hi]
        print(c["name"], c["symbol"], "total sigs", len(times), "in window", len(win),
              "before", len(before), "after", len(after),
              "nearest before", (lo - before[-1]) if before else None, "s; nearest after", (after[0] - hi) if after else None, "s")
        c["full_recount"] = {"total": len(times), "in_window": len(win), "before": len(before), "after": len(after)}
        time.sleep(0.5)
json.dump(R, open("/Users/triton/PROTEUS/experiments/2026-10-14-P-0141/results.json", "w"), indent=1)
