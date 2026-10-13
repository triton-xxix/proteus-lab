#!/usr/bin/env python3
"""P-0137: capture a cohort of 100 fresh pump.fun pools from GeckoTerminal new_pools now, committed
before their 24h outcome exists. `recheck` re-reads each pool's reserve_in_usd at least 24h later.

    python3 cohort.py capture
    python3 cohort.py recheck
"""
import json, sys, time
from datetime import datetime, timezone
import requests

B = "https://api.geckoterminal.com/api/v2"
H = {"Accept": "application/json", "User-Agent": "proteus-lab/0.1"}
OUT = "/Users/triton/PROTEUS/experiments/2026-10-13-P-0137/"
LIQ = 5000.0


def get(path):
    for _ in range(3):
        r = requests.get(B + path, headers=H, timeout=30)
        if r.status_code == 429:
            time.sleep(20); continue
        return r
    return r


def fnum(x):
    try:
        return float(x)
    except Exception:
        return None


def capture():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    pools, seen, pages, all_n = [], set(), 0, 0
    for page in range(1, 11):
        r = get("/networks/solana/new_pools?page=%d" % page); pages += 1
        for x in (r.json().get("data") or []):
            all_n += 1
            dex = x["relationships"]["dex"]["data"]["id"]
            a = x["attributes"]
            if dex != "pump-fun" or a["address"] in seen:
                continue
            seen.add(a["address"])
            pools.append({"pool": a["address"], "name": a.get("name"), "created": a.get("pool_created_at"),
                          "liq_at_capture": fnum(a.get("reserve_in_usd")), "fdv_at_capture": fnum(a.get("fdv_usd"))})
        if len(pools) >= 100:
            break
        time.sleep(2.5)
    pools = pools[:100]
    above = sum(1 for p in pools if (p["liq_at_capture"] or 0) > LIQ)
    out = {"captured_at": now, "pages": pages, "new_pools_seen": all_n, "pump_fun": len(pools),
           "above_5k_at_capture": above, "pools": pools}
    json.dump(out, open(OUT + "cohort.json", "w"), indent=1)
    print("captured", len(pools), "pump-fun pools of", all_n, "new pools on", pages, "pages;",
          above, "above 5k USD at capture; created", min(p["created"] for p in pools), "to", max(p["created"] for p in pools))


def recheck():
    c = json.load(open(OUT + "cohort.json"))
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    addrs = [p["pool"] for p in c["pools"]]
    liq = {}
    for i in range(0, len(addrs), 30):
        r = get("/networks/solana/pools/multi/" + ",".join(addrs[i:i + 30]))
        for x in (r.json().get("data") or []):
            liq[x["attributes"]["address"]] = fnum(x["attributes"].get("reserve_in_usd"))
        time.sleep(2.5)
    above = sum(1 for a in addrs if (liq.get(a) or 0) > LIQ)
    out = {"rechecked_at": now, "cohort": len(addrs), "returned": len(liq), "above_5k": above,
           "liq": liq}
    json.dump(out, open(OUT + "recheck.json", "w"), indent=1)
    print("rechecked", len(addrs), "returned", len(liq), "above 5k USD", above)


if __name__ == "__main__":
    {"capture": capture, "recheck": recheck}[sys.argv[1]]()
