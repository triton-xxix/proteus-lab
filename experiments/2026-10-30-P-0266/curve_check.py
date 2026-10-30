"""P-0266: read live pump.fun bonding curves over the public RPC and compare the curve price with
DexScreener's quote. Stdlib only, keyless.

DexScreener's pairAddress for a dexId "pumpfun" pair is the bonding-curve account itself, so no PDA
derivation is needed. The account layout (Pump program, BondingCurve, from the SDK's src/state.ts and
the public IDL): 8-byte discriminator, then u64 virtualTokenReserves, u64 virtualSolReserves,
u64 realTokenReserves, u64 realSolReserves, u64 tokenTotalSupply, u8 complete, 32-byte creator.
The SDK's own math: price = virtualSol / virtualToken (bondingCurveMarketCap scales by supply), and
graduation progress = tokens sold over the 793.1M real tokens the curve launched with.
"""
import base64
import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RPC = "https://api.mainnet-beta.solana.com"
SEARCH = "https://api.dexscreener.com/latest/dex/search?q=pumpfun"
LAUNCH_REAL_TOKENS = 793_100_000 * 10**6
N = int(sys.argv[1]) if len(sys.argv) > 1 else 6


def get_json(url, data=None):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": "proteus-probe/0.1", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def u64(b, o):
    return int.from_bytes(b[o:o + 8], "little")


pairs = [p for p in get_json(SEARCH)["pairs"] if p.get("dexId") == "pumpfun" and p.get("quoteToken", {}).get("symbol") == "SOL"][:N]
dex_time = time.strftime("%H:%M:%SZ", time.gmtime())
rows = []
for p in pairs:
    acct = p["pairAddress"]
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "getAccountInfo", "params": [acct, {"encoding": "base64"}]}).encode()
    try:
        res = get_json(RPC, body)
    except Exception as e:  # noqa
        rows.append({"symbol": p["baseToken"]["symbol"], "error": repr(e)})
        continue
    val = res.get("result", {}).get("value")
    if not val:
        rows.append({"symbol": p["baseToken"]["symbol"], "error": "no account", "acct": acct})
        continue
    raw = base64.b64decode(val["data"][0])
    owner = val["owner"]
    vtok, vsol, rtok, rsol, supply = (u64(raw, 8 + 8 * i) for i in range(5))
    complete = raw[48] == 1
    price_sol = (vsol / 1e9) / (vtok / 1e6) if vtok else None
    progress = (LAUNCH_REAL_TOKENS - rtok) / LAUNCH_REAL_TOKENS if not complete else 1.0
    mcap_sol = price_sol * supply / 1e6 if price_sol else None
    dex_price = float(p["priceNative"])
    rows.append({
        "symbol": p["baseToken"]["symbol"], "mint": p["baseToken"]["address"], "curve": acct, "owner": owner,
        "len": len(raw), "complete": complete,
        "virtual_sol": vsol / 1e9, "virtual_tok_m": vtok / 1e12, "real_sol": rsol / 1e9, "real_tok_m": rtok / 1e12,
        "curve_price_sol": price_sol, "dex_price_sol": dex_price,
        "diff_pct": 100 * (price_sol / dex_price - 1) if price_sol else None,
        "progress_pct": 100 * progress, "mcap_sol": mcap_sol, "dex_fdv_usd": p.get("fdv"),
        "dex_h1_txns": p["txns"]["h1"]["buys"] + p["txns"]["h1"]["sells"],
    })
    time.sleep(0.4)

out = {"checked": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "dexscreener_fetched": dex_time, "rows": rows}
json.dump(out, open(os.path.join(HERE, "curve_check.json"), "w"), indent=1)
print("%-10s %-6s %9s %9s %8s %9s %8s %7s" % ("symbol", "owner", "curve SOL", "dex SOL", "diff%", "progress", "vSOL", "h1 tx"))
for r in rows:
    if "error" in r:
        print("%-10s error %s" % (r["symbol"], r["error"]))
        continue
    print("%-10s %-6s %9.3e %9.3e %+7.2f%% %8.1f%% %8.2f %7d" % (
        r["symbol"], r["owner"][:6], r["curve_price_sol"], r["dex_price_sol"], r["diff_pct"], r["progress_pct"], r["virtual_sol"], r["dex_h1_txns"]))
