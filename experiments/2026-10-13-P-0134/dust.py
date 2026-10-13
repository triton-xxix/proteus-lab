#!/usr/bin/env python3
"""P-0134: what is the 11 Oct 21:17:41Z DOGEUS transaction that touched 7 Kolscan KOL token accounts
(experiments/2026-10-12-P-0128/result.json)? One airdrop, or buys? Keyless public RPC, read-only."""
import json, time
import requests

RPC = "https://api.mainnet-beta.solana.com"
OUT = "/Users/triton/PROTEUS/experiments/2026-10-13-P-0134/"
SRC = json.load(open("/Users/triton/PROTEUS/experiments/2026-10-12-P-0128/result.json"))
MINT = "CnvQ6v525Mx4FSNNYwXVaiH2wboEMVdjxPhUjkpqpump"


def rpc(method, params):
    for _ in range(4):
        r = requests.post(RPC, json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params}, timeout=30)
        if r.status_code == 429:
            time.sleep(5); continue
        return r.json().get("result")
    return None


touches = [t for t in SRC["touches"] if t["symbol"] == "DOGEUS"]
kol_atas = {t["ata"]: t for t in touches}
sigs = {}
for t in touches:
    for s in rpc("getSignaturesForAddress", [t["ata"], {"limit": 5}]) or []:
        sigs.setdefault(s["signature"], []).append(t["name"])
    time.sleep(0.4)
print("distinct signatures across", len(touches), "KOL DOGEUS accounts:", len(sigs))
out = {"kol_accounts": len(touches), "signatures": {}}
for sig, names in sigs.items():
    tx = rpc("getTransaction", [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 1}])   # it is a v1 transaction: 0 gets error -32015
    time.sleep(0.4)
    if not tx:
        out["signatures"][sig] = {"kols": names, "error": "no tx"}; continue
    msg = tx["transaction"]["message"]
    signer = [a["pubkey"] for a in msg["accountKeys"] if a.get("signer")]
    pre = {(b["accountIndex"]): b for b in tx["meta"].get("preTokenBalances") or [] if b["mint"] == MINT}
    post = [b for b in tx["meta"].get("postTokenBalances") or [] if b["mint"] == MINT]
    keys = [a["pubkey"] for a in msg["accountKeys"]]
    moves = []
    for b in post:
        before = float((pre.get(b["accountIndex"]) or {}).get("uiTokenAmount", {}).get("uiAmount") or 0)
        after = float(b["uiTokenAmount"].get("uiAmount") or 0)
        moves.append({"account": keys[b["accountIndex"]], "owner": b.get("owner"), "delta": after - before,
                      "kol": keys[b["accountIndex"]] in kol_atas})
    progs = sorted({ix.get("program") or ix.get("programId") for ix in msg["instructions"]})
    sol_paid = [(keys[i], (tx["meta"]["postBalances"][i] - tx["meta"]["preBalances"][i]) / 1e9)
                for i in range(len(keys)) if abs(tx["meta"]["postBalances"][i] - tx["meta"]["preBalances"][i]) > 1000]
    rec = {"kols": names, "block_time": tx.get("blockTime"), "signers": signer, "kol_signed": any(
        t["wallet"] in signer for t in touches), "programs": progs, "token_moves": moves, "sol_changes": sol_paid}
    out["signatures"][sig] = rec
    kol_in = [m for m in moves if m["kol"]]
    print(sig[:12], "time", tx.get("blockTime"), "signers", [s[:6] for s in signer], "KOL signed", rec["kol_signed"],
          "| DOGEUS moves", len(moves), "to KOL accounts", len(kol_in), "amounts", sorted({round(m["delta"], 4) for m in kol_in}),
          "| programs", progs)
json.dump(out, open(OUT + "result.json", "w"), indent=1)
