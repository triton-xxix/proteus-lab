"""pump_trades.py: read the latest pump.fun trades straight off Solana, keyless, and decode every
TradeEvent the program logs: amounts, fees in basis points and lamports, mayhem mode, cashback,
buyback, holder rewards, quote mint. Then check each fee against amount x bps.

Standard library only. Uses the public mainnet RPC (getSignaturesForAddress, getTransaction with
encoding "json"), so it is slow (about a quarter of a second per transaction) and rate-limited.

    python3 pump_trades.py                      # 60 transactions, summary to stdout
    python3 pump_trades.py --n 120 --out run.json
    python3 pump_trades.py --rpc https://your.rpc/ --n 300 --csv trades.csv

Layout: the TradeEvent in pump.fun's public IDL (pump-fun/pump-public-docs), read on 16 and 17 Nov 2026
by Proteus probes P-0464 and P-0465. Anchor logs events as a self-CPI whose data starts with
e445a52e51cb9a1d, then the event discriminator, then the fields. If pump.fun changes the event, the
fixed part still decodes and the tail is marked "short".

Caveat found by P-0465: buyback_fee_basis_points can read 5000, which is a share of the fee, not 50%
of the trade, so this tool never adds the bps fields into one total.
"""
import argparse
import csv
import json
import sys
import time
import urllib.request
from collections import Counter
from datetime import datetime, timezone

RPC = "https://api.mainnet-beta.solana.com"
PUMP = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
WRAP = bytes.fromhex("e445a52e51cb9a1d")
TRADE = bytes([189, 219, 127, 211, 78, 230, 97, 238])
SOL_LIKE = {"So11111111111111111111111111111111111111112", "11111111111111111111111111111111"}
B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58decode(s):
    n = 0
    for ch in s:
        n = n * 58 + B58.index(ch)
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
    return b"\0" * (len(s) - len(s.lstrip("1"))) + raw


def b58encode(b):
    n = int.from_bytes(b, "big")
    out = ""
    while n:
        n, r = divmod(n, 58)
        out = B58[r] + out
    return "1" * (len(b) - len(b.lstrip(b"\0"))) + out


def rpc(url, method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json",
                                                          "User-Agent": "pump-trades/0.1"})
    err = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read())
        except Exception as e:  # the public RPC answers 429 when pushed
            err = e
            time.sleep(1.5 * (attempt + 1))
    return {"error": str(err)}


def u64(d, i):
    return int.from_bytes(d[i:i + 8], "little")


def decode(d):
    """d: the event bytes after wrapper and discriminator."""
    e = {"mint": b58encode(d[0:32]), "sol_amount": u64(d, 32), "token_amount": u64(d, 40),
         "is_buy": d[48] == 1, "user": b58encode(d[49:81]),
         "timestamp": int.from_bytes(d[81:89], "little", signed=True),
         "virtual_sol_reserves": u64(d, 89), "virtual_token_reserves": u64(d, 97),
         "fee_bps": u64(d, 153), "fee": u64(d, 161),
         "creator_fee_bps": u64(d, 201), "creator_fee": u64(d, 209)}
    i = 250
    if len(d) < i + 4:
        e["tail"] = "short"
        return e
    n = int.from_bytes(d[i:i + 4], "little")
    e["ix_name"] = d[i + 4:i + 4 + n].decode("utf-8", "replace")
    i += 4 + n
    if len(d) < i + 37:
        e["tail"] = "short"
        return e
    e["mayhem"] = d[i] == 1
    i += 1
    e["cashback_bps"], e["cashback"] = u64(d, i), u64(d, i + 8)
    e["buyback_bps"], e["buyback"] = u64(d, i + 16), u64(d, i + 24)
    i += 32
    k = int.from_bytes(d[i:i + 4], "little")
    e["shareholders"] = k
    i += 4 + k * 34
    if len(d) >= i + 72:
        e["quote_mint"] = b58encode(d[i:i + 32])
        e["quote_amount"] = u64(d, i + 32)
        e["holder_rewards_bps"], e["holder_rewards"] = u64(d, i + 56), u64(d, i + 64)
        e["tail"] = "ok"
    else:
        e["tail"] = "no quote fields"
    return e


def fee_ok(amount, bps, fee):
    return abs(fee - amount * bps / 10000) <= 1


def fee_base(e):
    """The amount the fee is charged on: lamports for a SOL-quoted trade, the quote token's base units
    when sol_amount is 0 and quote_amount is set (found on this tool's first run, 17 Nov 2026)."""
    if e["sol_amount"] == 0 and e.get("quote_amount"):
        return e["quote_amount"]
    return e["sol_amount"]


def score(e):
    base = fee_base(e)
    e["fee_ok"] = fee_ok(base, e["fee_bps"], e["fee"])
    e["creator_fee_ok"] = fee_ok(base, e["creator_fee_bps"], e["creator_fee"])
    e["fee_class"] = fee_class(e)
    e["sol_quote"] = e.get("quote_mint") in SOL_LIKE or "quote_mint" not in e
    return e


def fee_class(e):
    if e["fee_bps"] == 0 and e["creator_fee_bps"] == 0:
        return "no fee"
    return "%d + %d bps" % (e["fee_bps"], e["creator_fee_bps"])


def events_in(tx):
    keys = list(tx["transaction"]["message"]["accountKeys"])
    loaded = (tx.get("meta") or {}).get("loadedAddresses") or {}
    keys += loaded.get("writable", []) + loaded.get("readonly", [])
    out = []
    for grp in (tx.get("meta") or {}).get("innerInstructions") or []:
        for ii in grp["instructions"]:
            if keys[ii["programIdIndex"]] != PUMP:
                continue
            d = b58decode(ii["data"])
            if d[:8] == WRAP and d[8:16] == TRADE and len(d) >= 16 + 217:
                out.append(decode(d[16:]))
    return out


def run(url, n):
    sigs = rpc(url, "getSignaturesForAddress", [PUMP, {"limit": min(1000, max(n * 8, 50))}]).get("result", [])
    rows, fetched, failed = [], 0, 0
    for s in sigs:
        if fetched >= n:
            break
        if s.get("err"):
            continue
        tx = (rpc(url, "getTransaction", [s["signature"], {"encoding": "json",
                                                            "maxSupportedTransactionVersion": 0}]) or {}).get("result")
        time.sleep(0.25)
        if not tx:
            failed += 1
            continue
        fetched += 1
        for e in events_in(tx):
            e["sig"] = s["signature"]
            rows.append(score(e))
    return rows, fetched, failed


def summarise(rows, fetched, failed):
    paid = [r for r in rows if r["fee_class"] != "no fee"]
    free = [r for r in rows if r["fee_class"] == "no fee"]
    sol = [r for r in rows if r["sol_quote"]]
    return {"at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "transactions": fetched, "fetch_failed": failed, "trades": len(rows),
            "buys": sum(r["is_buy"] for r in rows), "sells": sum(not r["is_buy"] for r in rows),
            "mints": len({r["mint"] for r in rows}), "users": len({r["user"] for r in rows}),
            "fee_classes": dict(Counter(r["fee_class"] for r in rows).most_common()),
            "ix_names": dict(Counter(r.get("ix_name", "-") for r in rows).most_common()),
            "mayhem": sum(bool(r.get("mayhem")) for r in rows),
            "mayhem_no_fee": sum(bool(r.get("mayhem")) for r in free),
            "mayhem_paid": sum(bool(r.get("mayhem")) for r in paid),
            "no_fee": len(free), "paid": len(paid),
            "non_sol_quote": len(rows) - len(sol),
            "fee_ok_paid": sum(r["fee_ok"] and r["creator_fee_ok"] for r in paid),
            "sol_volume": sum(r["sol_amount"] for r in sol) / 1e9,
            "fees_sol": sum(r["fee"] + r["creator_fee"] for r in sol) / 1e9,
            "tails": dict(Counter(r.get("tail") for r in rows))}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--n", type=int, default=60, help="transactions to read (default 60)")
    ap.add_argument("--rpc", default=RPC, help="RPC URL (default the public mainnet one)")
    ap.add_argument("--out", help="write summary and every decoded trade as JSON")
    ap.add_argument("--csv", help="write the decoded trades as CSV")
    ap.add_argument("--from", dest="src", help="re-score a saved --out file instead of fetching")
    a = ap.parse_args()
    if a.src:
        old = json.load(open(a.src))
        rows = [score(r) for r in old["rows"]]
        s = summarise(rows, old["summary"]["transactions"], old["summary"]["fetch_failed"])
        s["at"] = old["summary"]["at"]
    else:
        rows, fetched, failed = run(a.rpc, a.n)
        s = summarise(rows, fetched, failed)
    print(json.dumps(s, indent=1))
    if a.out:
        with open(a.out, "w") as f:
            json.dump({"summary": s, "rows": rows}, f, indent=1)
    if a.csv and rows:
        cols = sorted({k for r in rows for k in r})
        with open(a.csv, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
    return 0 if rows else 1


if __name__ == "__main__":
    sys.exit(main())
