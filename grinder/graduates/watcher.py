#!/usr/bin/env python3
"""The graduation book's watcher (rules: RULES.md in this folder). Paper only.

Listens for pump.fun migrations on the public Solana RPC websocket, finds the token, takes a paper
entry at the first Jupiter price, samples every open position every 15 seconds, and closes each at
30 minutes with all four exits recorded. Stops itself 7 days after first start, or on HALT.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/grinder/graduates/watcher.py run
    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/grinder/graduates/watcher.py load|unload|summary
"""
import asyncio
import json
import os
import statistics as st
import subprocess
import sys
import time

import requests
import websockets

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import paths  # noqa: E402

ROOT = "/Users/triton/PROTEUS/"
HALT = ROOT + "HALT"
START, DONE = HERE + "/START", HERE + "/DONE"
OPEN, CLOSED, EVENTS = HERE + "/open.json", HERE + "/closed.jsonl", HERE + "/events.jsonl"
LABEL, PLIST = "com.proteus.graduates", HERE + "/com.proteus.graduates.plist"
WSS, RPC = "wss://api.mainnet-beta.solana.com", "https://api.mainnet-beta.solana.com"
MIG = "39azUYFWPz3VHgKCf3VChUwbpURdCHRxjWVowf5jUJjg"
WSOL = "So11111111111111111111111111111111111111112"
DAYS, SAMPLE_S, HOLD_S = 7, 15, 30 * 60
UA = {"User-Agent": "proteus-lab/0.3 (+https://github.com/triton-xxix/proteus-lab)"}


def log(kind, **kw):
    kw.update(kind=kind, t=round(time.time(), 1))
    with open(EVENTS, "a") as fh:
        fh.write(json.dumps(kw) + "\n")


def domain():
    return "gui/%d" % os.getuid()


def load():
    r = subprocess.run(["/bin/launchctl", "bootstrap", domain(), PLIST], capture_output=True, text=True)
    print("load", r.returncode, r.stderr.strip())


def unload():
    subprocess.run(["/bin/launchctl", "bootout", domain() + "/" + LABEL], capture_output=True)


def should_stop():
    if os.path.exists(HALT):
        return "HALT"
    if os.path.exists(DONE):
        return "DONE"
    if time.time() - float(open(START).read()) > DAYS * 86400:
        open(DONE, "w").write(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        return "end time"
    return None


def jup_prices(mints):
    out = {}
    for i in range(0, len(mints), 50):
        try:
            d = requests.get("https://lite-api.jup.ag/price/v3", params={"ids": ",".join(mints[i:i + 50])}, headers=UA, timeout=15).json()
            for m, v in (d or {}).items():
                if v and v.get("usdPrice"):
                    out[m] = (float(v["usdPrice"]), float(v.get("liquidity") or 0))
        except Exception as e:
            log("jup_error", err=str(e)[:120])
    return out


def mint_of(sig):
    """The graduated token from the migration transaction; None if the RPC has not got it yet."""
    try:
        d = requests.post(RPC, json={"jsonrpc": "2.0", "id": 1, "method": "getTransaction",
                                     "params": [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 1, "commitment": "confirmed"}]},
                          headers=UA, timeout=20).json()
        res = d.get("result")
        if not res:
            return None, None
        mints = {b["mint"] for b in (res["meta"].get("postTokenBalances") or [])} - {WSOL}
        pick = sorted(mints, key=lambda m: (not m.endswith("pump"), m))
        return (pick[0] if pick else None), res.get("blockTime")
    except Exception as e:
        log("rpc_error", err=str(e)[:120])
        return None, None


class Book:
    def __init__(self):
        self.open = json.load(open(OPEN)) if os.path.exists(OPEN) else {}
        self.claimed = set(self.open)

    def save(self):
        tmp = OPEN + ".tmp"
        json.dump(self.open, open(tmp, "w")); os.replace(tmp, OPEN)

    async def enter(self, sig):
        mint, block_t = None, None
        for _ in range(12):                            # the RPC can lag the websocket by a few seconds
            mint, block_t = await asyncio.to_thread(mint_of, sig)
            if mint:
                break
            await asyncio.sleep(2)
        if not mint:
            log("no_mint", sig=sig); return
        if mint in self.claimed:
            return
        self.claimed.add(mint)
        for _ in range(20):
            px = (await asyncio.to_thread(jup_prices, [mint])).get(mint)
            if px:
                break
            await asyncio.sleep(3)
        if not px:
            log("no_price", sig=sig, mint=mint); return
        now = time.time()
        self.open[mint] = {"mint": mint, "sig": sig, "block_t": block_t, "entry_t": now, "entry": px[0], "liq": px[1],
                           "latency_s": round(now - block_t, 1) if block_t else None, "samples": [[round(now, 1), px[0]]]}
        self.save()
        log("enter", mint=mint, latency_s=self.open[mint]["latency_s"], price=px[0], liq=px[1])

    def close(self, p):
        e, s = p["entry"], p["samples"]
        def at(sec):
            later = [x for x in s if x[0] >= p["entry_t"] + sec]
            if later:
                return later[0][1], False
            last = s[-1]
            return (last[1], True) if p["entry_t"] + sec - last[0] <= 300 else (0.0, True)
        def with_stop(sec):
            for t, px in s:
                if t > p["entry_t"] + sec:
                    break
                if px <= e * 0.5:
                    return px, "stop_loss", False
            px, stale = at(sec)
            return px, "time_stop", stale
        rec = {k: p[k] for k in ("mint", "sig", "block_t", "entry_t", "entry", "liq", "latency_s")}
        rec["n_samples"] = len(s); rec["min"] = min(x[1] for x in s); rec["max"] = max(x[1] for x in s)
        for name, (px, reason, stale) in {"A": (*at(1200)[:1], "time_stop", at(1200)[1]), "B": (*at(1800)[:1], "time_stop", at(1800)[1]),
                                          "P": with_stop(1200), "D": with_stop(1800)}.items():
            rec[name] = paths.pnl_v02(e, max(px, 1e-18), reason, 100.0, p["liq"] or None) if px > 0 else -100.0
            rec[name + "_move"] = round(px / e - 1, 4); rec[name + "_stale"] = stale
        with open(CLOSED, "a") as fh:
            fh.write(json.dumps(rec) + "\n")

    async def sampler(self):
        while True:
            if should_stop():
                return
            if self.open:
                px = await asyncio.to_thread(jup_prices, list(self.open))
                now = round(time.time(), 1)
                for m, p in list(self.open.items()):
                    if m in px:
                        p["samples"].append([now, px[m][0]])
                    if now - p["entry_t"] >= HOLD_S + SAMPLE_S:
                        self.close(p); del self.open[m]
                self.save()
            await asyncio.sleep(SAMPLE_S)


async def listen(book):
    while not should_stop():
        try:
            async with websockets.connect(WSS, ping_interval=20, max_size=2 ** 22, open_timeout=30) as ws:
                await ws.send(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "logsSubscribe",
                                          "params": [{"mentions": [MIG]}, {"commitment": "confirmed"}]}))
                await ws.recv()
                log("subscribed")
                while not should_stop():
                    try:
                        m = json.loads(await asyncio.wait_for(ws.recv(), timeout=30))
                    except asyncio.TimeoutError:
                        continue
                    v = (m.get("params") or {}).get("result", {}).get("value") or {}
                    if v.get("err") is None and any("Instruction: Migrate" in l for l in v.get("logs") or []):
                        log("migration", sig=v["signature"])
                        asyncio.create_task(book.enter(v["signature"]))
        except Exception as e:
            log("ws_error", err=str(e)[:160]); await asyncio.sleep(10)


async def run():
    if not os.path.exists(START):
        open(START, "w").write(str(time.time()))
    why = should_stop()
    if why:
        log("stopped", why=why); unload(); return
    book = Book()
    log("start", open_positions=len(book.open))
    await asyncio.gather(listen(book), book.sampler())
    log("stopped", why=should_stop()); unload()


def summary():
    rows = [json.loads(l) for l in open(CLOSED)] if os.path.exists(CLOSED) else []
    ok = [r for r in rows if r["latency_s"] is not None and r["latency_s"] <= 120 and (r["liq"] or 0) >= 5000]
    print("closed %d, counted (latency <= 120 s, liquidity >= $5k) %d, open %d" % (len(rows), len(ok), len(json.load(open(OPEN))) if os.path.exists(OPEN) else 0))
    if rows:
        print("latency s: median %.0f, p90 %.0f" % (st.median(r["latency_s"] or 0 for r in rows), sorted(r["latency_s"] or 0 for r in rows)[int(.9 * (len(rows) - 1))]))
    for k in ("P", "A", "B", "D"):
        p = sorted(r[k] for r in ok)
        if p:
            trim = st.mean(p[:-10]) if len(p) > 10 else float("nan")
            print("%s: exp £%.1f, winners %d%%, best-10 removed £%.1f, at or below -50%%: %d%%" % (
                k, st.mean(p), 100 * sum(x > 0 for x in p) / len(p), trim, 100 * sum(r[k + "_move"] <= -0.5 for r in ok) / len(ok)))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "run"
    {"run": lambda: asyncio.run(run()), "load": load, "unload": unload, "summary": summary}[cmd]()
