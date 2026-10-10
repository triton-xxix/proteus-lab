"""P-0106 sizing slice: how many getSignaturesForAddress pages (1,000 each) does it take to reach a
gate-passer's first transaction on the public RPC, and how fast does the RPC answer? Cap 30 pages a
mint. If the first transaction is reached, read it and the creator block's buys of the mint."""
import json
import time
import urllib.request

RPC = "https://api.mainnet-beta.solana.com"
OUT = "/Users/triton/PROTEUS/experiments/2026-10-10-P-0106/"
MINTS = {"Gary": "8ZCmwpW3MtC5UpNcZf7U4HMvRNTo71syU11BDiAFpump",
         "OWLNIGHT": "CmCHvr99aXrLDQB7jAtFtsBwg3DnXqq4spcTEMt7pump",
         "ZKDARK": "HXqxTwCzREUXNK4CbNDgNEUEh2jLzFKdC4tvTuojpump",
         "Gunner": "7thxAzq4B9KwPe4NqMNAntF2Njgqb9FTKQb4z6fYpump",
         "QPAWS": "2fDAjAjyvCFATm5ERrJnyqqcqiZ9akV9vEFZLLGfpump"}
stats = {"calls": 0, "429": 0, "errors": 0}


def rpc(method, params):
    for attempt in range(4):
        stats["calls"] += 1
        body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
        try:
            req = urllib.request.Request(RPC, data=body, headers={"Content-Type": "application/json"})
            d = json.loads(urllib.request.urlopen(req, timeout=30).read())
            if "error" in d:
                stats["errors"] += 1
                time.sleep(2 * (attempt + 1))
                continue
            return d["result"]
        except urllib.error.HTTPError as e:
            stats["429" if e.code == 429 else "errors"] += 1
            time.sleep(3 * (attempt + 1))
        except Exception:
            stats["errors"] += 1
            time.sleep(2)
    return None


res = []
t0 = time.time()
for sym, mint in MINTS.items():
    before, pages, total, first = None, 0, 0, None
    while pages < 30:
        p = {"limit": 1000}
        if before:
            p["before"] = before
        sigs = rpc("getSignaturesForAddress", [mint, p])
        if sigs is None:
            break
        pages += 1
        total += len(sigs)
        if len(sigs) < 1000:
            first = sigs[-1] if sigs else None
            break
        before = sigs[-1]["signature"]
        time.sleep(0.4)
    row = {"symbol": sym, "pages": pages, "signatures": total, "reached_first": first is not None,
           "first_slot": first and first.get("slot"), "first_time": first and first.get("blockTime")}
    print(row, flush=True)
    res.append(row)
stats["seconds"] = round(time.time() - t0, 1)
print(stats)
json.dump({"rows": res, "stats": stats}, open(OUT + "size.json", "w"), indent=1)
