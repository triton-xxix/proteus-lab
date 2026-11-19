"""P-0474: did the mayhem wallet's leftovers burn at 24 hours?

Re-reads the 19 mints from experiments/2026-11-18-P-0473/results.json (read at about 12.8 hours old)
now that they are past 24 hours, and compares coin by coin: what the wallet held then and now, and
the supply then and now. If the leftovers were burned, held goes to zero and supply falls by what
was held.

    python3 burncheck.py

Keyless, read only, standard library. Writes results.json beside itself; does not touch P-0473.
"""
import json, statistics, sys, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / "2026-11-18-P-0473" / "results.json"
RPC = "https://api.mainnet-beta.solana.com"
WALLET = "BwWK17cbHxwWBKZkUYvzxLcNQ1YVyaFezduWbtm2de6s"
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


def main():
    if HALT.exists():
        print("HALT")
        return 1
    old = json.loads(OLD.read_text())
    b = rpc("getBalance", [WALLET])
    sol = b["result"]["value"] / 1e9 if "result" in b else None
    rows = []
    for o in old["rows"]:
        mint = o["mint"]
        row = {"mint": mint, "held_then": o.get("held"), "supply_then": o.get("supply")}
        r = rpc("getTokenAccountsByOwner", [WALLET, {"mint": mint}, {"encoding": "jsonParsed"}])
        if "result" in r:
            accs = r["result"]["value"]
            row["accounts"] = len(accs)
            row["held_now"] = sum(float(a["account"]["data"]["parsed"]["info"]["tokenAmount"]["uiAmountString"]) for a in accs)
        else:
            row["held_error"] = r["error"]
        time.sleep(0.6)
        s = rpc("getTokenSupply", [mint])
        if "result" in s:
            row["supply_now"] = float(s["result"]["value"]["uiAmountString"])
        else:
            row["supply_error"] = s["error"]
        time.sleep(0.6)
        g = rpc("getSignaturesForAddress", [mint, {"limit": 1}])
        if "result" in g and g["result"]:
            row["last_sig_age_h"] = round((time.time() - g["result"][0]["blockTime"]) / 3600, 2)
        time.sleep(0.6)
        if "held_now" in row and row["held_then"] is not None:
            row["held_change"] = row["held_now"] - row["held_then"]
        if "supply_now" in row and row["supply_then"] is not None:
            row["supply_change"] = row["supply_now"] - row["supply_then"]
        if "held_change" in row and "supply_change" in row and row["held_then"]:
            # 1.0 means the supply fell by exactly what the wallet held at 12.8 hours
            row["supply_drop_over_held_then"] = round(-row["supply_change"] / row["held_then"], 4)
        rows.append(row)
        print(json.dumps(row), flush=True)

    ok = [r for r in rows if "held_now" in r and "supply_now" in r]
    held_now = [r["held_now"] for r in ok]
    ratios = [r["supply_drop_over_held_then"] for r in ok if "supply_drop_over_held_then" in r and r["held_then"] > 1e6]
    summary = {
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "then_at": old["summary"]["at"],
        "wallet_sol_now": sol,
        "wallet_sol_then": old["summary"].get("wallet_sol"),
        "mints": len(rows),
        "answered": len(ok),
        "held_zero_now": sum(1 for x in held_now if x == 0),
        "held_under_1m_now": sum(1 for x in held_now if x < 1e6),
        "held_unchanged": sum(1 for r in ok if abs(r.get("held_change", 1)) < 1),
        "sum_held_then_bn": round(sum(r["held_then"] or 0 for r in ok) / 1e9, 3),
        "sum_held_now_bn": round(sum(held_now) / 1e9, 3),
        "median_supply_then_bn": round(statistics.median([r["supply_then"] for r in ok]) / 1e9, 4) if ok else None,
        "median_supply_now_bn": round(statistics.median([r["supply_now"] for r in ok]) / 1e9, 4) if ok else None,
        "supply_fell": sum(1 for r in ok if r.get("supply_change", 0) < -1),
        "supply_unchanged": sum(1 for r in ok if abs(r.get("supply_change", 1)) < 1),
        "median_supply_drop_over_held_then": statistics.median(ratios) if ratios else None,
        "min_supply_drop_over_held_then": min(ratios) if ratios else None,
        "max_supply_drop_over_held_then": max(ratios) if ratios else None,
        "last_sig_age_h": sorted(r["last_sig_age_h"] for r in rows if "last_sig_age_h" in r),
    }
    (HERE / "results.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1))
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
