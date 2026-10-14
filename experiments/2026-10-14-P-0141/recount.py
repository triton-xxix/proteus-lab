#!/usr/bin/env python3
"""P-0141: re-count P-0128's in-window KOL wallets, keeping only transactions the KOL wallet signed or
that changed the KOL token account's balance (P-0134 showed a no-op v1 tx spamming 7 KOL DOGEUS accounts,
so a signature on a KOL account is not a KOL action). Keyless public RPC, read-only.

Input: experiments/2026-10-12-P-0128/result.json. Its window_utc is an hour early (mktime bug, README),
so the right window is +3600 s on both ends, as page.py does.
"""
import json, sys, time
import requests

RPC = "https://api.mainnet-beta.solana.com"
SRC = "/Users/triton/PROTEUS/experiments/2026-10-12-P-0128/result.json"
OUT = "/Users/triton/PROTEUS/experiments/2026-10-14-P-0141/results.json"
SLEEP = 0.4
BUDGET_S = 330          # stay under the 420 s foreground limit
MAX_SIGS = 40           # per account, newest first; the in-window ones are what we decode

d = json.load(open(SRC))
lo, hi = d["window_utc"][0] + 3600, d["window_utc"][1] + 3600
mint_of = {p["symbol"]: p["mint"] for p in d["picks"]}
rows = [e for e in d["ever"] if e["first"] <= hi and e["last"] >= lo]      # P-0128's 9 (spans)
inside = [e for e in rows if lo <= e["first"] <= hi or lo <= e["last"] <= hi]  # the floor of 7
print(f"window {lo}..{hi}; spans rows {len(rows)} wallets {len({r['name'] for r in rows})}; "
      f"inside rows {len(inside)} wallets {len({r['name'] for r in inside})}", flush=True)

calls = {"n": 0, "429": 0, "err": 0}
t0 = time.time()


def rpc(method, params):
    for _ in range(5):
        calls["n"] += 1
        try:
            r = requests.post(RPC, json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params}, timeout=30)
        except requests.RequestException:
            calls["err"] += 1; time.sleep(2); continue
        if r.status_code == 429:
            calls["429"] += 1; time.sleep(5); continue
        j = r.json()
        if "error" in j:
            calls["err"] += 1
            return {"__error": j["error"]}
        return j.get("result")
    return None


def decode(tx, ata, wallet, mint):
    msg = tx["transaction"]["message"]
    keys = [a["pubkey"] for a in msg["accountKeys"]]
    signers = [a["pubkey"] for a in msg["accountKeys"] if a.get("signer")]
    pre = {b["accountIndex"]: b for b in tx["meta"].get("preTokenBalances") or []}
    post = {b["accountIndex"]: b for b in tx["meta"].get("postTokenBalances") or []}
    delta = None
    if ata in keys:
        i = keys.index(ata)
        before = float(((pre.get(i) or {}).get("uiTokenAmount") or {}).get("uiAmount") or 0)
        after = float(((post.get(i) or {}).get("uiTokenAmount") or {}).get("uiAmount") or 0)
        if i in pre or i in post:
            delta = after - before
    progs = sorted({ix.get("program") or ix.get("programId") for ix in msg["instructions"]})
    return {"signers": signers, "kol_signed": wallet in signers, "ata_in_keys": ata in keys,
            "ata_delta": delta, "ata_changed": bool(delta), "programs": progs,
            "n_keys": len(keys), "err": tx["meta"].get("err")}


out = {"probe": "P-0141", "window": [lo, hi], "candidates": [], "calls": calls}
for e in rows:
    rec = {k: e[k] for k in ("symbol", "name", "wallet", "ata", "sigs", "first", "last")}
    rec["txs"] = []
    if time.time() - t0 > BUDGET_S:
        rec["skipped"] = "budget"; out["candidates"].append(rec); continue
    sigs = rpc("getSignaturesForAddress", [e["ata"], {"limit": MAX_SIGS}])
    time.sleep(SLEEP)
    if not isinstance(sigs, list):
        rec["error"] = sigs; out["candidates"].append(rec); continue
    rec["sigs_fetched"] = len(sigs)
    win = [s for s in sigs if s.get("blockTime") and lo <= s["blockTime"] <= hi]
    rec["sigs_in_window"] = len(win)
    for s in win:
        if time.time() - t0 > BUDGET_S:
            rec["skipped"] = "budget"; break
        tx = rpc("getTransaction", [s["signature"], {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 1}])
        time.sleep(SLEEP)
        if not tx or "__error" in tx:
            rec["txs"].append({"sig": s["signature"], "time": s["blockTime"], "error": tx}); continue
        dec = decode(tx, e["ata"], e["wallet"], mint_of[e["symbol"]])
        dec.update({"sig": s["signature"], "time": s["blockTime"]})
        rec["txs"].append(dec)
    rec["real"] = [t for t in rec["txs"] if t.get("kol_signed") or t.get("ata_changed")]
    rec["survives"] = bool(rec["real"])
    out["candidates"].append(rec)
    print(f"{e['symbol']:10} {e['name']:12} sigs {rec.get('sigs_fetched')} in-window {rec.get('sigs_in_window')} "
          f"decoded {len(rec['txs'])} real {len(rec['real'])} survives {rec['survives']} "
          f"[{calls['n']} calls, {calls['429']} x429, {int(time.time()-t0)} s]", flush=True)

surv = {c["name"] for c in out["candidates"] if c.get("survives")}
spam = {c["name"] for c in out["candidates"] if c.get("sigs_in_window") and not c.get("survives") and not c.get("skipped")}
out["summary"] = {
    "spans_wallets": len({r["name"] for r in rows}), "inside_wallets_floor": len({r["name"] for r in inside}),
    "wallets_with_sig_in_window": len({c["name"] for c in out["candidates"] if c.get("sigs_in_window")}),
    "survive_wallets": sorted(surv), "survive": len(surv), "spam_only_wallets": sorted(spam),
    "skipped": [c["name"] for c in out["candidates"] if c.get("skipped")],
    "seconds": int(time.time() - t0),
}
json.dump(out, open(OUT, "w"), indent=1)
print(json.dumps(out["summary"]))
