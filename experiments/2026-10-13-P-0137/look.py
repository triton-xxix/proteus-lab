#!/usr/bin/env python3
"""P-0137 step 1: which keyless GeckoTerminal endpoints reach pump.fun pools 24h old?"""
import json, sys, time
import requests

B = "https://api.geckoterminal.com/api/v2"
H = {"Accept": "application/json", "User-Agent": "proteus-lab/0.1"}
tries = [
    "/networks/solana/dexes",
    "/networks/solana/new_pools?page=1",
    "/networks/solana/dexes/pumpswap/pools?sort=pool_created_at_desc&page=10",
    "/networks/solana/dexes/pump-fun/pools?sort=pool_created_at_desc&page=10",
]
for p in tries:
    r = requests.get(B + p, headers=H, timeout=30)
    try:
        d = r.json().get("data") or []
    except Exception:
        d = []
    print(p, r.status_code, len(d))
    if "dexes?" in p or p.endswith("/dexes"):
        print([x["id"] for x in d if "pump" in x["id"]])
    else:
        for x in d[:3] + d[-2:]:
            a = x["attributes"]
            print("  ", x["relationships"]["dex"]["data"]["id"], a.get("pool_created_at"), a.get("reserve_in_usd"), a.get("name"))
    time.sleep(2.5)
