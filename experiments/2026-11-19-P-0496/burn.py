#!/usr/bin/env python3
"""P-0496: decode the newest transaction on five of P-0474's mayhem mints. Keyless, public RPC."""
import json, os, time, urllib.request

RPC = "https://api.mainnet-beta.solana.com"
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "/Users/triton/PROTEUS/experiments/2026-11-19-P-0474/results.json"
N = 5


def rpc(method, params, tries=5):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    for i in range(tries):
        try:
            req = urllib.request.Request(RPC, body, {"Content-Type": "application/json", "User-Agent": "probe/1.0"})
            out = json.loads(urllib.request.urlopen(req, timeout=30).read())
            if "result" in out:
                time.sleep(1.2)
                return out["result"]
            err = out.get("error")
        except Exception as e:  # 429s land here
            err = str(e)
        time.sleep(3 * (i + 1))
    raise SystemExit("rpc failed: %s %s" % (method, err))


def birth(mint, newest_sig):
    """Oldest signature's blockTime, paging back at most 6 pages of 1000."""
    before, oldest, pages = newest_sig, None, 0
    while pages < 6:
        page = rpc("getSignaturesForAddress", [mint, {"limit": 1000, "before": before}])
        pages += 1
        if not page:
            return oldest, pages, True
        oldest, before = page[-1]["blockTime"], page[-1]["signature"]
        if len(page) < 1000:
            return oldest, pages, True
    return oldest, pages, False


rows = []
mints = [r["mint"] for r in json.load(open(SRC))["rows"]][:N]
for mint in mints:
    sigs = rpc("getSignaturesForAddress", [mint, {"limit": 1}])
    s = sigs[0]
    tx = rpc("getTransaction", [s["signature"], {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}])
    msg, meta = tx["transaction"]["message"], tx["meta"]
    keys = msg["accountKeys"]
    signers = [k["pubkey"] for k in keys if k.get("signer")]
    top = msg["instructions"]
    inner = [i for grp in (meta.get("innerInstructions") or []) for i in grp["instructions"]]
    burns, programs = [], []
    for where, ins in [("top", i) for i in top] + [("inner", i) for i in inner]:
        programs.append(ins.get("program") or ins.get("programId"))
        p = ins.get("parsed")
        if isinstance(p, dict) and p.get("type", "").startswith("burn"):
            info = p["info"]
            amt = info.get("amount") or (info.get("tokenAmount") or {}).get("amount")
            burns.append({"where": where, "program": ins.get("program"), "programId": ins.get("programId"),
                          "type": p["type"], "mint": info.get("mint"), "authority": info.get("authority"),
                          "amount_raw": amt})
    b, pages, complete = birth(mint, s["signature"])
    rows.append({"mint": mint, "signature": s["signature"], "blockTime": s["blockTime"], "slot": s["slot"],
                 "err": meta.get("err"), "fee_lamports": meta.get("fee"), "fee_payer": keys[0]["pubkey"],
                 "signers": signers, "n_top": len(top), "n_inner": len(inner),
                 "top_programs": [i.get("program") or i.get("programId") for i in top],
                 "burns": burns, "burn_mints": sorted({x["mint"] for x in burns if x["mint"]}),
                 "birth_blockTime": b, "birth_complete": complete, "pages": pages,
                 "hours_after_birth": round((s["blockTime"] - b) / 3600, 3) if b else None,
                 "seconds_past_24h": (s["blockTime"] - b - 86400) if b else None})
    print(mint[:8], "burns", len(burns), [x["type"] for x in burns], "payer", keys[0]["pubkey"][:8],
          "signers", len(signers), "top", rows[-1]["top_programs"], "after birth h", rows[-1]["hours_after_birth"],
          "complete", complete)

summary = {"mints": len(rows), "with_burn": sum(1 for r in rows if r["burns"]),
           "token2022": sum(1 for r in rows if any(x["programId"] == "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb" for x in r["burns"])),
           "distinct_signatures": len({r["signature"] for r in rows}),
           "fee_payers": sorted({r["fee_payer"] for r in rows}),
           "authorities": sorted({x["authority"] for r in rows for x in r["burns"] if x["authority"]}),
           "slots": [r["slot"] for r in rows], "seconds_past_24h": [r["seconds_past_24h"] for r in rows]}
json.dump({"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "rows": rows, "summary": summary},
          open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps(summary))
