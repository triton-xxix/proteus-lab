"""P-0464: decode pump.fun TradeEvents (Anchor self-CPI event wrapper e445a52e51cb9a1d) from live transactions
on the public RPC (keyless), and check them against the buy / sell instructions in the same transaction.

Layout from experiments/2026-11-16-ranit-solders/pump-idl.json (TradeEvent, fixed-width prefix):
mint 32 | sol_amount u64 | token_amount u64 | is_buy bool | user 32 | timestamp i64 | 4 x reserves u64 |
fee_recipient 32 | fee_basis_points u64 | fee u64 | creator 32 | creator_fee_basis_points u64 | creator_fee u64 ...

Checks, events paired with trade instructions in order within a transaction:
  buy:              token_amount == amount        and sol_amount <= max_sol_cost
  buy_exact_sol_in: sol_amount <= spendable_sol_in and token_amount >= min_tokens_out
  sell:             token_amount == amount        and sol_amount >= min_sol_output
  fee:              |fee - sol_amount * fee_bps / 10000| <= 1 lamport (same for creator_fee)

    python3 -I experiments/2026-11-17-P-0464/events.py
"""
import base64
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/solders-lib")
from solders.pubkey import Pubkey  # noqa: E402
from solders.transaction import VersionedTransaction  # noqa: E402

SRC = Path("/Users/triton/PROTEUS/experiments/2026-11-16-ranit-solders")
src = (SRC / "decode.py").read_text().split("\ndef main")[0]
ns = {"__file__": str(SRC / "decode.py"), "__name__": "decode"}
sys.argv = [sys.argv[0]]
exec(compile(src, "decode.py", "exec"), ns)
rpc, b58decode, PUMP = ns["rpc"], ns["b58decode"], ns["PUMP"]
IDL = json.loads((SRC / "pump-idl.json").read_text())
IX = {bytes(i["discriminator"]): i["name"] for i in IDL["instructions"]}
WRAP = bytes.fromhex("e445a52e51cb9a1d")
TRADE = bytes([189, 219, 127, 211, 78, 230, 97, 238])
OUT = Path(__file__).parent
MAX_FETCH = 60


def u64(b, i):
    return int.from_bytes(b[i:i + 8], "little")


def trade_event(d):
    return {"sol_amount": u64(d, 32), "token_amount": u64(d, 40), "is_buy": d[48] == 1,
            "fee_bps": u64(d, 153), "fee": u64(d, 161), "creator_fee_bps": u64(d, 201), "creator_fee": u64(d, 209)}


def fee_ok(amount, bps, fee):
    return abs(fee - amount * bps / 10000) <= 1


sigs = rpc("getSignaturesForAddress", [str(PUMP), {"limit": 120}]).get("result", [])
stats, kinds = Counter(), Counter()
checks = []
for s in sigs:
    if s.get("err"):
        continue
    tx = (rpc("getTransaction", [s["signature"], {"encoding": "base64", "maxSupportedTransactionVersion": 0}]) or {}).get("result")
    time.sleep(0.25)
    if not tx:
        stats["fetch_failed"] += 1
        continue
    stats["fetched"] += 1
    vt = VersionedTransaction.from_bytes(base64.b64decode(tx["transaction"][0]))
    msg = vt.message
    keys = list(msg.account_keys)
    loaded = (tx.get("meta") or {}).get("loadedAddresses") or {}
    keys += [Pubkey.from_string(k) for k in loaded.get("writable", []) + loaded.get("readonly", [])]
    ixs = [(keys[ix.program_id_index], bytes(ix.data)) for ix in msg.instructions]
    for grp in (tx.get("meta") or {}).get("innerInstructions") or []:
        for ii in grp["instructions"]:
            ixs.append((keys[ii["programIdIndex"]], b58decode(ii["data"])))
    trades, events = [], []
    for prog, d in ixs:
        if prog != PUMP or len(d) < 8:
            continue
        if d[:8] == WRAP and len(d) >= 16:
            kinds["event:" + d[8:16].hex()] += 1
            if d[8:16] == TRADE and len(d) >= 16 + 217:
                events.append(trade_event(d[16:]))
            continue
        name = IX.get(d[:8])
        kinds[name or "unknown"] += 1
        if name in ("buy", "sell", "buy_exact_sol_in") and len(d) >= 24:
            trades.append({"name": name, "a1": u64(d, 8), "a2": u64(d, 16)})
    stats["trade_ix"] += len(trades)
    stats["trade_events"] += len(events)
    for t, e in zip(trades, events):
        if t["name"] == "buy":
            ok = e["is_buy"] and e["token_amount"] == t["a1"] and e["sol_amount"] <= t["a2"]
        elif t["name"] == "buy_exact_sol_in":
            ok = e["is_buy"] and e["sol_amount"] <= t["a1"] and e["token_amount"] >= t["a2"]
        else:
            ok = (not e["is_buy"]) and e["token_amount"] == t["a1"] and e["sol_amount"] >= t["a2"]
        checks.append({"sig": s["signature"][:16], "ix": t["name"], "args_ok": bool(ok),
                       "fee_ok": fee_ok(e["sol_amount"], e["fee_bps"], e["fee"]),
                       "creator_fee_ok": fee_ok(e["sol_amount"], e["creator_fee_bps"], e["creator_fee"]),
                       **e, "a1": t["a1"], "a2": t["a2"]})
    if stats["fetched"] >= MAX_FETCH:
        break

n = len(checks)
summary = {"fetched": stats["fetched"], "trade_ix": stats["trade_ix"], "trade_events": stats["trade_events"],
           "paired": n,
           "args_ok": sum(c["args_ok"] for c in checks),
           "fee_ok": sum(c["fee_ok"] for c in checks),
           "creator_fee_ok": sum(c["creator_fee_ok"] for c in checks),
           "by_ix": dict(Counter(c["ix"] for c in checks)),
           "args_fail_by_ix": dict(Counter(c["ix"] for c in checks if not c["args_ok"])),
           "fee_bps_seen": dict(Counter(c["fee_bps"] for c in checks)),
           "creator_fee_bps_seen": dict(Counter(c["creator_fee_bps"] for c in checks)),
           "kinds": dict(kinds)}
print(json.dumps(summary, indent=1))
for c in [c for c in checks if not c["args_ok"] or not c["fee_ok"]][:6]:
    print(c)
(OUT / "results.json").write_text(json.dumps({"summary": summary, "checks": checks}, indent=1))
