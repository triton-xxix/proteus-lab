#!/usr/bin/env python3
"""P-0128: do any of the 91 Kolscan leaderboard wallets (P-0127) touch a Grinder pick within an hour of the snapshot?

Picks: the latest Grinder ledger batch (11 Oct, 22:28Z; tonight's has not run at 12:30 BST).
Window: snapshot 22:23:37Z plus or minus one hour.
Method, keyless: derive each wallet's associated token account (ATA) for each pick mint in pure Python
(PDA with an ed25519 off-curve check), under the mint's actual token program, then ask the public Solana RPC
for that ATA's signatures. Any signature with a blockTime in the window is a touch; any signature at all is
"ever touched". getMultipleAccounts says who still holds an account now.
"""
import csv
import hashlib
import json
import os
import re
import sys
import time
import urllib.request

ROOT = "/Users/triton/PROTEUS/"
HERE = os.path.dirname(os.path.abspath(__file__))
RPC = "https://api.mainnet-beta.solana.com"
SNAP = 1760221417  # 2026-10-11T22:23:37Z, filled below from the ledger for safety
WIN = 3600
ATA_PROGRAM = "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"

B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58d(s):
    n = 0
    for c in s:
        n = n * 58 + B58.index(c)
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
    pad = len(s) - len(s.lstrip("1"))
    return b"\0" * pad + raw


def b58e(b):
    n = int.from_bytes(b, "big")
    out = ""
    while n:
        n, r = divmod(n, 58)
        out = B58[r] + out
    return "1" * (len(b) - len(b.lstrip(b"\0"))) + out


P = 2 ** 255 - 19
D = (-121665 * pow(121666, P - 2, P)) % P


def on_curve(b):
    y = int.from_bytes(b, "little") & ((1 << 255) - 1)
    if y >= P:
        return False
    y2 = y * y % P
    x2 = (y2 - 1) * pow(D * y2 + 1, P - 2, P) % P
    return x2 == 0 or pow(x2, (P - 1) // 2, P) == 1


def pda(seeds, program):
    pid = b58d(program)
    for bump in range(255, -1, -1):
        h = hashlib.sha256(b"".join(seeds) + bytes([bump]) + pid + b"ProgramDerivedAddress").digest()
        if not on_curve(h):
            return b58e(h)
    raise ValueError("no bump")


CALLS = {"n": 0, "errors": 0}


def rpc(method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    for attempt in range(5):
        CALLS["n"] += 1
        try:
            req = urllib.request.Request(RPC, body, {"Content-Type": "application/json", "User-Agent": "proteus-probe"})
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.load(r)
            if "error" in d:
                raise RuntimeError(d["error"])
            return d["result"]
        except Exception as e:
            CALLS["errors"] += 1
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError("rpc failed: %s" % method)


# wallets: re-parse P-0127's saved page the same way parse.py did
html = open(ROOT + "sandbox/p0127-kolscan.html", errors="replace").read()
wallets, seen = [], set()
for m in re.finditer(r'\\?"(wallet_address|wallet|address)\\?"\s*:\s*\\?"([1-9A-HJ-NP-Za-km-z]{32,44})\\?"', html):
    window = html[m.start(): m.start() + 600]
    pnl = re.search(r'\\?"(pnl|profit|realized_profit|total_pnl|sol_pnl|usd_pnl)\\?"\s*:\s*(-?[\d.]+)', window)
    name = re.search(r'\\?"(name|twitter|username)\\?"\s*:\s*\\?"([^"\\]{1,40})', window)
    w = m.group(2)
    if w in seen:
        continue
    seen.add(w)
    if pnl:
        wallets.append({"wallet": w, "pnl": float(pnl.group(2)), "name": name.group(2) if name else None})
assert len(wallets) == 91, len(wallets)
T0 = time.time()


def log(*a):
    print("[%5.1fs rpc %d err %d]" % (time.time() - T0, CALLS["n"], CALLS["errors"]), *a, flush=True)


# P-0132: optional limits, `run.py <wallets> <picks>`, so a short pass can show where the first run stalled
if len(sys.argv) > 1:
    wallets = wallets[:int(sys.argv[1])]
log("wallets", len(wallets))

# picks: the latest ledger batch
rows = [r for r in csv.reader(open(ROOT + "grinder/LEDGER.csv")) if r and r[0].startswith("G-")]
last_ts = rows[-1][1]
picks = [{"id": r[0], "ts": r[1], "symbol": r[2], "mint": r[3]} for r in rows if r[1] == last_ts]
# calendar.timegm, not mktime: the 12 Oct run used mktime minus time.timezone, which is an hour out under BST
import calendar
SNAP = calendar.timegm(time.strptime("2026-10-11T22:23:37Z", "%Y-%m-%dT%H:%M:%SZ"))
lo, hi = SNAP - WIN, SNAP + WIN
if len(sys.argv) > 2:
    picks = picks[:int(sys.argv[2])]
log("picks", [p["symbol"] for p in picks], "window", lo, hi)

# token program of each mint
infos = rpc("getMultipleAccounts", [[p["mint"] for p in picks], {"encoding": "base64", "dataSlice": {"offset": 0, "length": 0}}])["value"]
for p, inf in zip(picks, infos):
    p["token_program"] = inf["owner"] if inf else None

touches, ever, holding = [], [], []
per_pick = {}
for p in picks:
    prog = p["token_program"]
    if not prog:
        per_pick[p["symbol"]] = "mint not found"
        continue
    log(p["symbol"], "program", prog)
    atas = [(w, pda([b58d(w["wallet"]), b58d(prog), b58d(p["mint"])], ATA_PROGRAM)) for w in wallets]
    log(p["symbol"], "atas derived", len(atas))
    exists = []
    for i in range(0, len(atas), 100):
        chunk = atas[i:i + 100]
        v = rpc("getMultipleAccounts", [[a for _, a in chunk], {"encoding": "base64", "dataSlice": {"offset": 0, "length": 0}}])["value"]
        exists += [x is not None for x in v]
    n_ever = n_win = 0
    log(p["symbol"], "exists now", sum(exists))
    for k, ((w, ata), ex) in enumerate(zip(atas, exists)):
        sigs = rpc("getSignaturesForAddress", [ata, {"limit": 100}])
        time.sleep(0.3)
        if k % 10 == 9:
            log(p["symbol"], "lookups", k + 1)
        if ex:
            holding.append({"symbol": p["symbol"], "name": w["name"], "wallet": w["wallet"]})
        if sigs:
            n_ever += 1
            bt = [s.get("blockTime") for s in sigs if s.get("blockTime")]
            rec = {"symbol": p["symbol"], "name": w["name"], "wallet": w["wallet"], "ata": ata, "sigs": len(sigs),
                   "first": min(bt) if bt else None, "last": max(bt) if bt else None}
            ever.append(rec)
            inw = [t for t in bt if lo <= t <= hi]
            if inw:
                n_win += 1
                touches.append(dict(rec, in_window=len(inw)))
    per_pick[p["symbol"]] = {"ever": n_ever, "in_window": n_win, "program": prog}
    print(p["symbol"], per_pick[p["symbol"]], "calls so far", CALLS["n"], flush=True)

# sanity check of the PDA code: one known ATA must exist for a holder of a well-held mint would need a holder list;
# instead check the derivation is off-curve and stable (self-test against a published example below)
known = pda([b58d("9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM"), b58d("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"),
             b58d("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")], ATA_PROGRAM)

wallets_touching = sorted({t["wallet"] for t in touches})
out = {"picks": picks, "window_utc": [lo, hi], "wallets": len(wallets), "per_pick": per_pick,
       "wallets_touching_in_window": len(wallets_touching), "touches": touches, "ever": ever, "holding_now": holding,
       "rpc_calls": CALLS["n"], "rpc_errors": CALLS["errors"], "selftest_usdc_ata": known}
json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=2)
print(json.dumps({k: out[k] for k in ("per_pick", "wallets_touching_in_window", "rpc_calls", "rpc_errors", "selftest_usdc_ata")}, indent=1))
print("ever:", len(ever), "holding now:", len(holding))
