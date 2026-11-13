#!/usr/bin/env python3
"""P-0440: pump.fun creates per minute on the public RPC websocket, read-only, and the creator's
stake in the creation transaction as a share of the 1,000,000,000 supply. Nobody buys.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/experiments/2026-11-13-P-0440/listen.py [minutes] [sample]
Method from P-0042 (same mint authority filter, same 2 s pace on getTransaction).
"""
import asyncio, json, os, statistics as st, sys, time
import requests, websockets

HERE = os.path.dirname(os.path.abspath(__file__))
MIN = float(sys.argv[1]) if len(sys.argv) > 1 else 5
SAMPLE = int(sys.argv[2]) if len(sys.argv) > 2 else 20
WSS, RPC = "wss://api.mainnet-beta.solana.com", "https://api.mainnet-beta.solana.com"
MINT_AUTH = "TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM"
UA = {"User-Agent": "proteus-lab/0.3 research"}
SUPPLY = 1_000_000_000
_last = [0.0]


def rpc(method, params):
    for attempt in range(5):
        gap = 2.0 - (time.time() - _last[0])
        if gap > 0:
            time.sleep(gap)
        _last[0] = time.time()
        try:
            r = requests.post(RPC, json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params}, headers=UA, timeout=30)
            d = r.json()
        except Exception:
            time.sleep(3); continue
        err = d.get("error")
        if r.status_code == 429 or (err and err.get("code") == 429):
            time.sleep(5 * (attempt + 1)); continue
        return None if err else d.get("result")
    return None


async def hear(seconds):
    out, msgs = [], 0
    t_end = time.time() + seconds
    async with websockets.connect(WSS, ping_interval=20, max_size=2 ** 22) as ws:
        await ws.send(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "logsSubscribe",
                                  "params": [{"mentions": [MINT_AUTH]}, {"commitment": "confirmed"}]}))
        await ws.recv()
        while time.time() < t_end:
            try:
                m = json.loads(await asyncio.wait_for(ws.recv(), timeout=max(0.1, t_end - time.time())))
            except asyncio.TimeoutError:
                break
            msgs += 1
            v = m["params"]["result"]["value"]
            if v["err"] is None and any("Instruction: Create" in l for l in v["logs"]):
                out.append({"sig": v["signature"], "slot": m["params"]["result"]["context"]["slot"], "heard": time.time()})
    return out, msgs


def stake(sig):
    t = rpc("getTransaction", [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 1, "commitment": "confirmed"}])
    if not t or t["meta"].get("err"):
        return None
    keys = t["transaction"]["message"]["accountKeys"]
    creator = keys[0]["pubkey"] if isinstance(keys[0], dict) else keys[0]
    signer_mints = [k["pubkey"] for k in keys if isinstance(k, dict) and k.get("signer") and k["pubkey"] != creator]
    post = t["meta"].get("postTokenBalances") or []
    mint = next((m for m in signer_mints if any(b["mint"] == m for b in post)), None)   # P-0180: pin the signer mint
    if not mint:
        return {"sig": sig, "status": "no-mint"}
    held = sum(float(b["uiTokenAmount"]["uiAmount"] or 0) for b in post if b["mint"] == mint and b.get("owner") == creator)
    return {"sig": sig, "mint": mint, "creator": creator, "creator_tokens": held, "share": held / SUPPLY}


def bucket(s):
    return "0" if s == 0 else "under 1%" if s < 0.01 else "1 to 5%" if s < 0.05 else "5 to 10%" if s < 0.10 else "10% or more"


def main():
    t0 = time.time()
    creates, msgs = asyncio.run(hear(MIN * 60))
    mins = (time.time() - t0) / 60
    per_min = len(creates) / mins
    rows = [r for r in (stake(c["sig"]) for c in creates[:: max(1, len(creates) // SAMPLE)][:SAMPLE]) if r]
    good = [r for r in rows if "share" in r]
    shares = [r["share"] for r in good]
    buckets = {}
    for s in shares:
        buckets[bucket(s)] = buckets.get(bucket(s), 0) + 1
    res = {"listened_min": round(mins, 2), "log_messages": msgs, "creates": len(creates), "creates_per_min": round(per_min, 1),
           "sampled": len(rows), "with_mint": len(good),
           "creator_share_median": round(st.median(shares), 4) if shares else None,
           "creator_share_max": round(max(shares), 4) if shares else None,
           "buckets": buckets, "creators_distinct": len({r["creator"] for r in good}), "rows": rows}
    json.dump(res, open(os.path.join(HERE, "results.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1))


if __name__ == "__main__":
    main()
