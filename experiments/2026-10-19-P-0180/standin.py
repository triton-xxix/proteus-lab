#!/usr/bin/env python3
"""P-0180: the own-coin shots, scored keyless on pump.fun launches with no creator buy.

hear: listen on the public RPC websocket (P-0042's subscription) and keep creates whose logs carry no
      "Instruction: Buy", i.e. no buy in the creation transaction. Writes launches.json. Also counts
      creates with a buy, so the no-buy share is measured too.
read: read each kept launch with P-0042's analyse() (first MAX_TX transactions, 2 s pacing) and score
      the seven PLAN.md shots from the own-coin watch.py on each.

    .venv/bin/python3 standin.py hear N SECONDS
    .venv/bin/python3 standin.py read [MAX_TX]
"""
import asyncio
import importlib.util
import json
import os
import statistics as st
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(HERE)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


watch = load("watch", os.path.join(EXP, "2026-10-20-own-coin", "watch.py"))
obs = watch.obs


async def hear(n, secs):
    import websockets
    kept, with_buy, start = [], 0, time.time()
    async with websockets.connect(obs.WSS, ping_interval=20, max_size=2 ** 22) as ws:
        await ws.send(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "logsSubscribe",
                                  "params": [{"mentions": [obs.MINT_AUTH]}, {"commitment": "confirmed"}]}))
        await ws.recv()
        while len(kept) < n and time.time() - start < secs:
            try:
                m = json.loads(await asyncio.wait_for(ws.recv(), timeout=30))
            except asyncio.TimeoutError:
                continue
            v = m["params"]["result"]["value"]
            if v["err"] is not None or not any("Instruction: Create" in l for l in v["logs"]):
                continue
            if any("Instruction: Buy" in l for l in v["logs"]):
                with_buy += 1
                continue
            kept.append({"sig": v["signature"], "slot": m["params"]["result"]["context"]["slot"], "heard": time.time()})
    out = {"kept": kept, "creates_with_buy": with_buy, "seconds": round(time.time() - start)}
    json.dump(out, open(HERE + "/launches.json", "w"), indent=1)
    print("heard %d creates in %d s: %d with a buy in the creation tx, %d without" % (with_buy + len(kept), out["seconds"], with_buy, len(kept)))


_cache = {}
_rpc = obs.rpc


def cached_rpc(method, params):
    if method == "getTransaction" and params[0] in _cache:
        return _cache[params[0]]
    return _rpc(method, params)


def pin_mint(sig):
    """analyse() takes the first post-balance mint ending in 'pump'. On 19 Oct a no-buy create carried no
    balance for its own mint and analyse() read the PUMP token instead. The new mint signs the create, so
    take the signer that is not the fee payer, and keep only that mint's balances."""
    ct = _rpc("getTransaction", [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 1, "commitment": "confirmed"}])
    if not ct:
        return None
    signers = [k["pubkey"] for k in ct["transaction"]["message"]["accountKeys"] if isinstance(k, dict) and k.get("signer")]
    mint = signers[1] if len(signers) > 1 else None
    ct["meta"]["postTokenBalances"] = [b for b in ct["meta"].get("postTokenBalances") or [] if b["mint"] == mint]
    if mint and not ct["meta"]["postTokenBalances"]:   # keep the mint visible to analyse() with a zero row
        ct["meta"]["postTokenBalances"] = [{"mint": mint, "owner": "none", "uiTokenAmount": {"uiAmount": 0}}]
    _cache[sig] = ct
    return mint


def read(max_tx):
    obs.MAX_TX = max_tx
    obs.rpc = cached_rpc
    L = json.load(open(HERE + "/launches.json"))
    rows = []
    for la in L["kept"]:
        pinned = pin_mint(la["sig"])
        r = obs.analyse(la)
        r["pinned_mint"] = pinned
        r["sig"], r["age_s"] = la["sig"], round(time.time() - la["heard"])
        if r.get("status") == "ok":
            r["shots"] = {sid: bool(test(r)) for sid, p, test in watch.SHOTS}
        rows.append(r)
        print(r.get("mint"), r.get("status"), r.get("creator_buy_tokens"), r.get("shots"), flush=True)
        json.dump(rows, open(HERE + "/rows-v2.json", "w"), indent=1)
    ok = [r for r in rows if r.get("status") == "ok" and r["creator_buy_tokens"] == 0]
    res = {"read": len(rows), "ok_no_creator_buy": len(ok), "max_tx": max_tx,
           "median_age_at_read_s": st.median([r["age_s"] for r in ok]) if ok else None, "shots": []}
    for sid, p, test in watch.SHOTS:
        rate = sum(r["shots"][sid] for r in ok) / len(ok) if ok else None
        brier = st.mean([(p - r["shots"][sid]) ** 2 for r in ok]) if ok else None
        res["shots"].append({"shot": sid, "p": p, "rate": round(rate, 3) if rate is not None else None,
                             "brier": round(brier, 4) if brier is not None else None})
    if ok:
        res["mean_brier"] = round(st.mean(s["brier"] for s in res["shots"]), 4)
        for k in ("first_block_buyers", "buyers_first_60s", "buyers_total", "first_sell_s", "last_trade_s"):
            vals = [r[k] for r in ok if r.get(k) is not None]
            res["median_" + k] = st.median(vals) if vals else None
    json.dump(res, open(HERE + "/results-v2.json", "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    if sys.argv[1] == "hear":
        asyncio.run(hear(int(sys.argv[2]), int(sys.argv[3])))
    else:
        read(int(sys.argv[2]) if len(sys.argv) > 2 else 20)
