#!/usr/bin/env python3
"""P-0151: KOL overlap, batch two. P-0128's lookup + P-0141's KOL-signed filter + P-0149's before/after
placement in one keyless, read-only script, on the newest Grinder ledger batch.

Fixed before the run (15 Oct 2026, Trials):
- Wallets: the 91 Kolscan wallets with a profit figure (P-0127 page, parsed as in P-0128).
- Picks: every ledger row sharing the newest timestamp. Window: pick time plus or minus 3600 s.
- For each wallet x pick: derive the ATA, getSignaturesForAddress (limit 100); every signature in the
  window is fetched and kept only if the KOL wallet signed it or the ATA balance changed (P-0141).
- Each kept trade is before or after the pick; buy or sell from the ATA delta sign (P-0149).
- Report: wallets with a kept trade in the window; of those, how many had all trades before the pick
  ("out before"), and how many were net buyers before and net sellers after.
- Time budget 900 s; 3 worker threads, 0.3 s sleep each; progress every 10 lookups to progress.log.
"""
import calendar
import csv
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import requests

sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-10-12-P-0128")
ROOT = "/Users/triton/PROTEUS/"
HERE = os.path.dirname(os.path.abspath(__file__))
RPC = "https://api.mainnet-beta.solana.com"
ATA_PROGRAM = "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"
BUDGET = 900
B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
P = 2 ** 255 - 19
D = (-121665 * pow(121666, P - 2, P)) % P


def b58d(s):
    n = 0
    for c in s:
        n = n * 58 + B58.index(c)
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
    return b"\0" * (len(s) - len(s.lstrip("1"))) + raw


def b58e(b):
    n = int.from_bytes(b, "big")
    out = ""
    while n:
        n, r = divmod(n, 58)
        out = B58[r] + out
    return "1" * (len(b) - len(b.lstrip(b"\0"))) + out


def on_curve(b):
    y = int.from_bytes(b, "little") & ((1 << 255) - 1)
    if y >= P:
        return False
    y2 = y * y % P
    x2 = (y2 - 1) * pow(D * y2 + 1, P - 2, P) % P
    return x2 == 0 or pow(x2, (P - 1) // 2, P) == 1


def pda(seeds, program):
    import hashlib
    pid = b58d(program)
    for bump in range(255, -1, -1):
        h = hashlib.sha256(b"".join(seeds) + bytes([bump]) + pid + b"ProgramDerivedAddress").digest()
        if not on_curve(h):
            return b58e(h)
    raise ValueError("no bump")


calls = {"n": 0, "429": 0, "err": 0}
lock = threading.Lock()
T0 = time.time()
LOG = open(os.path.join(HERE, "progress.log"), "w")


def log(*a):
    with lock:
        LOG.write("[%5.0fs rpc %d 429 %d err %d] %s\n" % (time.time() - T0, calls["n"], calls["429"], calls["err"], " ".join(map(str, a))))
        LOG.flush()


def rpc(method, params):
    for _ in range(5):
        with lock:
            calls["n"] += 1
        try:
            r = requests.post(RPC, json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params}, timeout=30)
        except requests.RequestException:
            with lock:
                calls["err"] += 1
            time.sleep(2)
            continue
        if r.status_code == 429:
            with lock:
                calls["429"] += 1
            time.sleep(5)
            continue
        j = r.json()
        if "error" in j:
            with lock:
                calls["err"] += 1
            return {"__error": j["error"]}
        return j.get("result")
    return None


html = open(ROOT + "sandbox/p0127-kolscan.html", errors="replace").read()
wallets, seen = [], set()
for m in re.finditer(r'\\?"(wallet_address|wallet|address)\\?"\s*:\s*\\?"([1-9A-HJ-NP-Za-km-z]{32,44})\\?"', html):
    win = html[m.start(): m.start() + 600]
    pnl = re.search(r'\\?"(pnl|profit|realized_profit|total_pnl|sol_pnl|usd_pnl)\\?"\s*:\s*(-?[\d.]+)', win)
    name = re.search(r'\\?"(name|twitter|username)\\?"\s*:\s*\\?"([^"\\]{1,40})', win)
    w = m.group(2)
    if w in seen:
        continue
    seen.add(w)
    if pnl:
        wallets.append({"wallet": w, "name": name.group(2) if name else None})
assert len(wallets) == 91, len(wallets)

rows = [r for r in csv.reader(open(ROOT + "grinder/LEDGER.csv")) if r and r[0].startswith("G-")]
last_ts = rows[-1][1]
picks = [{"id": r[0], "ts": r[1], "symbol": r[2], "mint": r[3]} for r in rows if r[1] == last_ts]
PICK = calendar.timegm(time.strptime(last_ts[:19], "%Y-%m-%dT%H:%M:%S"))
lo, hi = PICK - 3600, PICK + 3600
assert hi < time.time(), "window not closed yet"
log("picks", [(p["id"], p["symbol"]) for p in picks], "pick", last_ts, "window", lo, hi)

infos = rpc("getMultipleAccounts", [[p["mint"] for p in picks], {"encoding": "base64", "dataSlice": {"offset": 0, "length": 0}}])["value"]
jobs = []
for p, inf in zip(picks, infos):
    p["token_program"] = inf["owner"] if inf else None
    if p["token_program"]:
        for w in wallets:
            jobs.append((p, w, pda([b58d(w["wallet"]), b58d(p["token_program"]), b58d(p["mint"])], ATA_PROGRAM)))
log("jobs", len(jobs))

done = {"n": 0}
results = []


def decode(tx, ata, wallet):
    msg = tx["transaction"]["message"]
    keys = [a["pubkey"] for a in msg["accountKeys"]]
    signers = [a["pubkey"] for a in msg["accountKeys"] if a.get("signer")]
    pre = {b["accountIndex"]: b for b in tx["meta"].get("preTokenBalances") or []}
    post = {b["accountIndex"]: b for b in tx["meta"].get("postTokenBalances") or []}
    delta = None
    if ata in keys:
        i = keys.index(ata)
        if i in pre or i in post:
            before = float(((pre.get(i) or {}).get("uiTokenAmount") or {}).get("uiAmount") or 0)
            after = float(((post.get(i) or {}).get("uiTokenAmount") or {}).get("uiAmount") or 0)
            delta = after - before
    return {"kol_signed": wallet in signers, "ata_delta": delta, "err": tx["meta"].get("err")}


def work(job):
    p, w, ata = job
    rec = {"id": p["id"], "symbol": p["symbol"], "name": w["name"], "wallet": w["wallet"], "ata": ata}
    if time.time() - T0 > BUDGET:
        rec["skipped"] = "budget"
        return rec
    sigs = rpc("getSignaturesForAddress", [ata, {"limit": 100}])
    time.sleep(0.3)
    if not isinstance(sigs, list):
        rec["error"] = str(sigs)[:200]
    else:
        rec["sigs"] = len(sigs)
        inw = [s for s in sigs if s.get("blockTime") and lo <= s["blockTime"] <= hi]
        rec["in_window"] = len(inw)
        rec["trades"] = []
        for s in inw:
            tx = rpc("getTransaction", [s["signature"], {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 1}])
            time.sleep(0.3)
            if not tx or "__error" in tx:
                rec["trades"].append({"time": s["blockTime"], "error": True})
                continue
            d = decode(tx, ata, w["wallet"])
            if d["kol_signed"] or d["ata_delta"]:
                d["time"] = s["blockTime"]
                rec["trades"].append(d)
    with lock:
        done["n"] += 1
        n = done["n"]
    if n % 10 == 0:
        log("lookups", n)
    return rec


with ThreadPoolExecutor(3) as ex:
    results = list(ex.map(work, jobs))

kols = {}
for r in results:
    for t in r.get("trades", []):
        if t.get("error"):
            continue
        k = kols.setdefault(r["name"] or r["wallet"], {"before": [], "after": [], "symbols": set()})
        k["symbols"].add(r["symbol"])
        (k["before"] if t["time"] < PICK else k["after"]).append(t.get("ata_delta") or 0)
summ = []
for name, k in kols.items():
    nb, na = sum(k["before"]), sum(k["after"])
    summ.append({"name": name, "symbols": sorted(k["symbols"]), "n_before": len(k["before"]), "n_after": len(k["after"]),
                 "net_before": round(nb, 2), "net_after": round(na, 2), "out_before": not k["after"],
                 "all_after": not k["before"], "buy_before_sell_after": nb > 0 and na < 0})
out = {"probe": "P-0151", "pick_ts": last_ts, "picks": picks, "window": [lo, hi], "wallets": len(wallets),
       "lookups_done": sum(1 for r in results if "sigs" in r),
       "skipped": sum(1 for r in results if r.get("skipped")), "errors": sum(1 for r in results if r.get("error")),
       "ever_touched": sum(1 for r in results if r.get("sigs")),
       "sig_in_window_rows": sum(1 for r in results if r.get("in_window")),
       "kol_wallets_trading": len(summ), "out_before": [s["name"] for s in summ if s["out_before"]],
       "all_after": [s["name"] for s in summ if s["all_after"]],
       "buy_before_sell_after": [s["name"] for s in summ if s["buy_before_sell_after"]],
       "kols": summ, "calls": calls, "seconds": int(time.time() - T0), "rows": results}
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
log("done", json.dumps({k: v for k, v in out.items() if k not in ("rows", "picks", "kols")}))
print(json.dumps({k: v for k, v in out.items() if k not in ("rows", "picks")}, indent=1))
