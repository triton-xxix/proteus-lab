#!/usr/bin/env python3
"""Do real pump.fun launches open where the stated curve says? Keyless, GeckoTerminal.

Stated: 30 virtual SOL over 1.073bn virtual tokens, so the first price is 2.796e-8 SOL a token. For new pump.fun pools,
take the lowest low of the first three 1-minute candles in USD, and convert with tonight's SOL price from the pool's own
USD and native prices. A launch buy inside the first candle pushes the low up, so ratios a little over 1 are expected.
"""
import json
import statistics as st
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
API = "https://api.geckoterminal.com/api/v2/networks/solana"
UA = {"User-Agent": "ProteusLab-probe/1.0", "Accept": "application/json"}
LAUNCH = 30 / 1.073e9


def get(path):
    with urllib.request.urlopen(urllib.request.Request(API + path, headers=UA), timeout=30) as r:
        return json.load(r)


pools = []
dexes = {}
for page in (1, 2, 3):
    for p in get(f"/new_pools?page={page}").get("data", []):
        dex = p["relationships"]["dex"]["data"]["id"]
        dexes[dex] = dexes.get(dex, 0) + 1
        if dex == "pump-fun":
            pools.append(p)
    time.sleep(2.5)

rows = []
refused = 0
for p in pools[:12]:
    a = p["attributes"]
    usd, native = float(a["base_token_price_usd"] or 0), float(a["base_token_price_native_currency"] or 0)
    if not usd or not native:
        continue
    sol = usd / native
    time.sleep(8)
    try:
        candles = get(f"/pools/{a['address']}/ohlcv/minute?aggregate=1&limit=1000&currency=usd")["data"]["attributes"]["ohlcv_list"]
    except Exception as e:  # first run met a 429 at 2.5 s spacing; count it and move on
        refused += 1
        print("refused", e, flush=True)
        time.sleep(30)
        continue
    first = sorted(candles, key=lambda c: c[0])[:3]
    if not first:
        continue
    low = min(c[3] for c in first)
    rows.append({"pool": a["address"], "created": a["pool_created_at"], "sol_usd": round(sol, 2), "candles": len(candles),
                 "low_usd": low, "ratio_to_stated": round(low / sol / LAUNCH, 3)})

ratios = [r["ratio_to_stated"] for r in rows]
out = {"stated_first_price_sol": LAUNCH, "dexes_seen": dexes, "pump_pools": len(pools), "measured": len(rows), "refused": refused,
       "median_ratio": st.median(ratios) if ratios else None, "min": min(ratios, default=None), "max": max(ratios, default=None),
       "rows": rows}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
