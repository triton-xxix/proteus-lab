#!/usr/bin/env python3
"""P-0042: what happens to a fresh pump.fun token, from the chain, keyless. Paper-free: nobody buys.

1. Hear 50 launches on the public RPC websocket (transactions mentioning pump.fun's mint authority,
   logging CreateV2). Record mint, creator (fee payer), slot, time.
2. When each is 30 minutes old, list the mint's transactions (getSignaturesForAddress, oldest first,
   up to 300) and read each one's token balance changes for that mint: who bought, who sold, when.
3. Report: creator's own buy, buyers in the creation slot (the first block), how many of those share
   a funding pattern (same slot, bought before any outside wallet: the bundle signature), when the
   first sells came, how much of the early buyers' holding was sold inside 5 and 30 minutes, and
   whether the token still traded at 30 minutes.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/experiments/2026-09-30-P-0042/observe.py [N]
"""
import asyncio
import json
import os
import statistics as st
import sys
import time

import requests
import websockets

HERE = os.path.dirname(os.path.abspath(__file__))
N = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 50
WSS, RPC = "wss://api.mainnet-beta.solana.com", "https://api.mainnet-beta.solana.com"
MINT_AUTH = "TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM"
UA = {"User-Agent": "proteus-lab/0.3 research"}
WAIT = 30 * 60
MAX_TX = 40    # first 40 transactions per mint: the public RPC allows about one getTransaction every 2 s
PACE = 2.0
TAKE = 30      # launches analysed of those heard


_last = [0.0]


def rpc(method, params):
    """The public RPC limits getTransaction per method (429 in the JSON body even at 1 a second, found
    30 Sep); one call every 2 seconds held. Version-1 transactions need maxSupportedTransactionVersion 1."""
    for attempt in range(5):
        gap = PACE - (time.time() - _last[0])
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
        if err:
            return None
        return d.get("result")
    return None


async def hear(n):
    out = []
    async with websockets.connect(WSS, ping_interval=20, max_size=2 ** 22) as ws:
        await ws.send(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "logsSubscribe",
                                  "params": [{"mentions": [MINT_AUTH]}, {"commitment": "confirmed"}]}))
        await ws.recv()
        while len(out) < n:
            m = json.loads(await ws.recv())
            v = m["params"]["result"]["value"]
            if v["err"] is None and any("Instruction: Create" in l for l in v["logs"]):
                out.append({"sig": v["signature"], "slot": m["params"]["result"]["context"]["slot"], "heard": time.time()})
    return out


def tx_changes(sig, mint):
    t = rpc("getTransaction", [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 1, "commitment": "confirmed"}])
    if not t or t["meta"].get("err"):
        return None
    pre = {(b["owner"]): float(b["uiTokenAmount"]["uiAmount"] or 0) for b in t["meta"].get("preTokenBalances") or [] if b["mint"] == mint}
    post = {(b["owner"]): float(b["uiTokenAmount"]["uiAmount"] or 0) for b in t["meta"].get("postTokenBalances") or [] if b["mint"] == mint}
    keys = t["transaction"]["message"]["accountKeys"]
    payer = keys[0]["pubkey"] if isinstance(keys[0], dict) else keys[0]
    sol = (t["meta"]["preBalances"][0] - t["meta"]["postBalances"][0]) / 1e9
    return {"slot": t["slot"], "time": t.get("blockTime"), "payer": payer, "sol_out": sol,
            "delta": {o: post.get(o, 0) - pre.get(o, 0) for o in set(pre) | set(post)}}


def analyse(launch):
    ct = rpc("getTransaction", [launch["sig"], {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 1, "commitment": "confirmed"}])
    if not ct:
        return {"status": "no-create-tx"}
    keys = ct["transaction"]["message"]["accountKeys"]
    creator = keys[0]["pubkey"] if isinstance(keys[0], dict) else keys[0]
    mints = {b["mint"] for b in ct["meta"].get("postTokenBalances") or []}
    mint = next((m for m in mints if m.endswith("pump")), next(iter(mints), None))
    if not mint:
        return {"status": "no-mint"}
    sigs, before = [], None
    for _ in range(8):                                   # page back to the mint's first transactions
        opt = {"limit": 1000}
        if before:
            opt["before"] = before
        page = rpc("getSignaturesForAddress", [mint, opt]) or []
        sigs += page
        if len(page) < 1000:
            break
        before = page[-1]["signature"]
    sigs = sorted([s for s in sigs if not s.get("err")], key=lambda s: (s["slot"], s.get("blockTime") or 0))[:MAX_TX]
    t0, s0 = ct.get("blockTime"), ct["slot"]
    trades = []
    for s in sigs:
        c = tx_changes(s["signature"], mint) if s["signature"] != launch["sig"] else None
        if s["signature"] == launch["sig"]:
            c = {"slot": s0, "time": t0, "payer": creator, "sol_out": 0,
                 "delta": {}}
            post = {b["owner"]: float(b["uiTokenAmount"]["uiAmount"] or 0) for b in ct["meta"].get("postTokenBalances") or [] if b["mint"] == mint}
            c["delta"] = post
        if c:
            trades.append(c)
    # the bonding curve's own token account is the largest holder change; wallets are everyone else
    curve = max((o for tr in trades for o in tr["delta"]), key=lambda o: sum(abs(tr["delta"].get(o, 0)) for tr in trades), default=None)
    buys, sells = [], []
    for tr in trades:
        for o, d in tr["delta"].items():
            if o == curve or abs(d) < 1e-9:
                continue
            rec = {"owner": o, "amt": d, "slot": tr["slot"], "dt": (tr["time"] or t0) - t0, "payer": tr["payer"]}
            (buys if d > 0 else sells).append(rec)
    creator_buy = sum(b["amt"] for b in buys if b["owner"] == creator and b["slot"] == s0)
    first_block = {b["owner"] for b in buys if b["slot"] == s0 and b["owner"] != creator}
    first_3_slots = {b["owner"] for b in buys if b["slot"] <= s0 + 2 and b["owner"] != creator}
    early = {b["owner"] for b in buys if b["dt"] <= 60}
    bought = {}
    for b in buys:
        bought[b["owner"]] = bought.get(b["owner"], 0) + b["amt"]
    def sold_share(owners, within):
        tot = sum(bought.get(o, 0) for o in owners)
        s = sum(-x["amt"] for x in sells if x["owner"] in owners and x["dt"] <= within)
        return round(min(1.0, s / tot), 3) if tot else None
    first_sell = min((s["dt"] for s in sells), default=None)
    creator_sell = min((s["dt"] for s in sells if s["owner"] == creator), default=None)
    last_trade = max((tr["time"] or t0) - t0 for tr in trades) if trades else 0
    return {"status": "ok", "mint": mint, "creator": creator, "txs_read": len(trades), "sigs_listed": len(sigs),
            "creator_buy_tokens": round(creator_buy), "first_block_buyers": len(first_block), "first_3_slot_buyers": len(first_3_slots),
            "buyers_first_60s": len(early), "buyers_total": len(bought), "sellers_total": len({s["owner"] for s in sells}),
            "first_sell_s": first_sell, "creator_first_sell_s": creator_sell,
            "first_block_sold_5m": sold_share(first_block, 300), "first_block_sold_30m": sold_share(first_block, 1800),
            "early_sold_30m": sold_share(early, 1800), "last_trade_s": last_trade,
            "traded_after_10m": any(((tr["time"] or t0) - t0) > 600 for tr in trades)}


def report(rows):
    ok = [r for r in rows if r.get("status") == "ok"]
    med = lambda k: st.median([r[k] for r in ok if r.get(k) is not None]) if any(r.get(k) is not None for r in ok) else None
    share = lambda f: round(100 * sum(1 for r in ok if f(r)) / len(ok)) if ok else 0
    L = ["# P-0042: what happens to a fresh pump.fun token", "",
         "%d launches heard on the public RPC websocket on 30 Sep 2026, each read from the chain at least 30 minutes after "
         "creation (first %d transactions per mint). Nobody bought anything. %d analysed." % (len(rows), MAX_TX, len(ok)), "",
         "| Measure | Median | Share of launches |", "|---|---|---|",
         "| Creator bought in the creation transaction | | %d%% |" % share(lambda r: r["creator_buy_tokens"] > 0),
         "| Other wallets buying in the creation slot (first block) | %s | %d%% had any |" % (med("first_block_buyers"), share(lambda r: r["first_block_buyers"] > 0)),
         "| Wallets buying in the first 3 slots (about 1.2 s) | %s | |" % med("first_3_slot_buyers"),
         "| Buyers in the first 60 s | %s | |" % med("buyers_first_60s"),
         "| Buyers seen (first 40 transactions) | %s | |" % med("buyers_total"),
         "| Seconds to the first sell | %s | |" % med("first_sell_s"),
         "| Creator sold within 30 min | | %d%% |" % share(lambda r: r["creator_first_sell_s"] is not None),
         "| Seconds to the creator's first sell, where they sold | %s | |" % med("creator_first_sell_s"),
         "| Share of first-block buyers' tokens sold within 5 min | %s | |" % med("first_block_sold_5m"),
         "| Share of first-60s buyers' tokens sold within 30 min | %s | |" % med("early_sold_30m"),
         "| Still trading after 10 minutes | | %d%% |" % share(lambda r: r["traded_after_10m"]),
         "| Seconds from creation to last trade seen | %s | |" % med("last_trade_s")]
    open(HERE + "/REPORT.md", "w").write("\n".join(L) + "\n")
    print("\n".join(L))


def main():
    if "resume" in sys.argv and os.path.exists(HERE + "/launches.json"):
        launches = json.load(open(HERE + "/launches.json"))
    else:
        launches = asyncio.run(hear(N))
        json.dump(launches, open(HERE + "/launches.json", "w"), indent=1)
    print("heard %d launches in %.0f s" % (len(launches), launches[-1]["heard"] - launches[0]["heard"]), flush=True)
    wait = launches[-1]["heard"] + WAIT - time.time()
    if wait > 0:
        time.sleep(wait)
    rows = []
    for i, l in enumerate(launches[:TAKE]):
        r = analyse(l); r["sig"] = l["sig"]; rows.append(r)
        json.dump(rows, open(HERE + "/results.json", "w"), indent=1)
        print("%d/%d %s" % (i + 1, min(TAKE, len(launches)), r.get("status")), flush=True)
    json.dump(rows, open(HERE + "/results.json", "w"), indent=1)
    report(rows)


if __name__ == "__main__":
    main()
