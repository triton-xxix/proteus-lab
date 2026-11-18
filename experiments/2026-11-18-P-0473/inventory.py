"""P-0473: the mayhem wallet's inventory, coin by coin.

P-0471 could not list the wallet's Token-2022 accounts (HTTP 413). This asks one mint at a time:
getTokenAccountsByOwner with a `mint` filter, getTokenSupply, and the coin's age from pump.fun's
public coin endpoint (created_timestamp), falling back to "unknown" if that is refused.

    python3 inventory.py

Keyless, read only, standard library. Mints come from experiments/2026-11-17-P-0470/results.json.
"""
import json, statistics, sys, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "2026-11-17-P-0470" / "results.json"
RPC = "https://api.mainnet-beta.solana.com"
WALLET = "BwWK17cbHxwWBKZkUYvzxLcNQ1YVyaFezduWbtm2de6s"
PUMP = "https://frontend-api-v3.pump.fun/coins/"
HALT = Path("/Users/triton/PROTEUS/HALT")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) proteus-inventory/0.1"


def rpc(method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(RPC, data=body, headers={"Content-Type": "application/json", "User-Agent": UA})
    err = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                out = json.loads(r.read())
            if "result" in out:
                return out
            err = out.get("error")
        except Exception as e:
            err = e
        time.sleep(2 * (attempt + 1))
    return {"error": str(err)[:200]}


def pump(mint):
    req = urllib.request.Request(PUMP + mint, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)[:120]}


def main():
    if HALT.exists():
        print("HALT")
        return 1
    coins = json.loads(SRC.read_text())["per_coin"]
    now = time.time()
    b = rpc("getBalance", [WALLET])
    sol = (b.get("result") or {}).get("value", 0) / 1e9 if "result" in b else None
    rows = []
    for c in coins:
        mint = c["mint"]
        row = {"mint": mint}
        r = rpc("getTokenAccountsByOwner", [WALLET, {"mint": mint}, {"encoding": "jsonParsed"}])
        if "result" in r:
            accs = r["result"]["value"]
            row["accounts"] = len(accs)
            row["held"] = sum(float(a["account"]["data"]["parsed"]["info"]["tokenAmount"]["uiAmountString"]) for a in accs)
            row["program"] = accs[0]["account"]["data"]["program"] if accs else None
        else:
            row["held_error"] = r["error"]
        time.sleep(0.6)
        s = rpc("getTokenSupply", [mint])
        if "result" in s:
            row["supply"] = float(s["result"]["value"]["uiAmountString"])
        else:
            row["supply_error"] = s["error"]
        time.sleep(0.6)
        p = pump(mint)
        if "created_timestamp" in p:
            row["age_h"] = round((now - p["created_timestamp"] / 1000) / 3600, 2)
            row["symbol"] = p.get("symbol")
            row["complete"] = p.get("complete")
            row["usd_market_cap"] = p.get("usd_market_cap")
            row["is_mayhem"] = p.get("is_mayhem_mode")
        else:
            row["age_error"] = p.get("error", "no created_timestamp")
        if row.get("supply") and "held" in row:
            row["share"] = round(row["held"] / row["supply"], 4)
        rows.append(row)
        print(json.dumps(row), flush=True)

    answered = [r for r in rows if "held" in r]
    held = [r["held"] for r in answered]
    nonzero = [r for r in answered if r["held"] > 0]
    shares = [r["share"] for r in answered if "share" in r]
    ages = [r["age_h"] for r in rows if "age_h" in r]
    summary = {
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "wallet_sol": sol,
        "mints": len(rows),
        "answered": len(answered),
        "nonzero": len(nonzero),
        "above_1bn": sum(1 for x in held if x > 1e9),
        "median_held_m": round(statistics.median(held) / 1e6, 1) if held else None,
        "median_held_nonzero_m": round(statistics.median([r["held"] for r in nonzero]) / 1e6, 1) if nonzero else None,
        "sum_held_bn": round(sum(held) / 1e9, 3),
        "supplies_seen_bn": sorted({round(r["supply"] / 1e9, 3) for r in rows if "supply" in r}),
        "median_share": statistics.median(shares) if shares else None,
        "ages_known": len(ages),
        "median_age_h": statistics.median(ages) if ages else None,
        "min_age_h": min(ages) if ages else None,
        "max_age_h": max(ages) if ages else None,
        "older_than_24h": sum(1 for a in ages if a > 24),
        "older_than_24h_still_held": sum(1 for r in rows if r.get("age_h", 0) > 24 and r.get("held", 0) > 0),
    }
    (HERE / "results.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1))
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
