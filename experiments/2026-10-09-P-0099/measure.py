"""P-0099: what share of new pump.fun tokens would sniper bots' mint and freeze checks remove?

1. Every distinct mint in grinder/SNAPSHOTS.csv (rugcheck's mint_auth and freeze_auth as scanned),
   split by origin: pump.fun (mint ends 'pump' or dex pumpfun/pumpswap) versus everything else.
2. Ground truth for a sample: getAccountInfo (jsonParsed) on the public Solana RPC, keyless,
   reading mintAuthority and freezeAuthority straight from the mint account.

usage: python3 measure.py SNAPSHOTS.csv OUTDIR [sample_per_group]
"""
import csv
import json
import random
import sys
import time
import urllib.request

RPC = "https://api.mainnet-beta.solana.com"


def rpc_mint(mint):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "getAccountInfo",
                       "params": [mint, {"encoding": "jsonParsed"}]}).encode()
    req = urllib.request.Request(RPC, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        v = json.load(r).get("result", {}).get("value")
    if not v:
        return {"exists": False}
    info = v["data"]["parsed"]["info"]
    return {"exists": True, "program": v["owner"], "mintAuthority": info.get("mintAuthority"),
            "freezeAuthority": info.get("freezeAuthority")}


def main():
    path, outdir = sys.argv[1], sys.argv[2]
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    last = {}
    for row in csv.DictReader(open(path)):
        last[row["mint"]] = row   # last scan of each mint
    groups = {"pumpfun": [], "other": []}
    for m, r in last.items():
        pump = m.endswith("pump") or r["dex"] in ("pumpfun", "pumpswap")
        groups["pumpfun" if pump else "other"].append(r)
    flag = lambda v: str(v).strip().lower() not in ("", "none", "null", "false", "0")
    snap = {}
    for g, rows in groups.items():
        snap[g] = {"mints": len(rows),
                   "mint_auth_set": sum(flag(r["mint_auth"]) for r in rows),
                   "freeze_auth_set": sum(flag(r["freeze_auth"]) for r in rows),
                   "either_set": sum(flag(r["mint_auth"]) or flag(r["freeze_auth"]) for r in rows),
                   "fields_blank": sum(r["mint_auth"] == "" and r["freeze_auth"] == "" for r in rows),
                   "dexes": sorted({r["dex"] for r in rows})}
    print("snapshots:", json.dumps(snap))
    random.seed(9)
    chain = {}
    rows_out = []
    for g, rows in groups.items():
        sample = random.sample(rows, min(n, len(rows)))
        c = {"sampled": len(sample), "exists": 0, "mint_auth_live": 0, "freeze_auth_live": 0,
             "token2022": 0, "errors": 0}
        for r in sample:
            try:
                a = rpc_mint(r["mint"])
            except Exception as e:
                c["errors"] += 1
                rows_out.append({"group": g, "mint": r["mint"], "error": type(e).__name__})
                time.sleep(1)
                continue
            rows_out.append({"group": g, "mint": r["mint"], "symbol": r["symbol"], **a,
                             "snap_mint_auth": r["mint_auth"], "snap_freeze_auth": r["freeze_auth"]})
            if a["exists"]:
                c["exists"] += 1
                c["mint_auth_live"] += a["mintAuthority"] is not None
                c["freeze_auth_live"] += a["freezeAuthority"] is not None
                c["token2022"] += a["program"].startswith("TokenzQd")
            time.sleep(0.25)
        chain[g] = c
    print("on chain:", json.dumps(chain))
    json.dump({"snapshots": snap, "on_chain": chain, "rows": rows_out},
              open(outdir + "/results.json", "w"), indent=1)


if __name__ == "__main__":
    main()
