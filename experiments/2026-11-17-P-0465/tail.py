"""P-0465: the TradeEvent fields after ix_name, and what the zero-fee trades are.

Reuses experiments/2026-11-17-P-0464/events.py (definitions only). After creator_fee (offset 217):
track_volume bool | total_unclaimed u64 | total_claimed u64 | current_sol_volume u64 | last_update i64 |
ix_name string (u32 len) | mayhem_mode bool | cashback_fee_bps u64 | cashback u64 | buyback_fee_bps u64 |
buyback_fee u64 | shareholders vec<(pubkey, u16)> | quote_mint 32 | quote_amount u64 |
virtual_quote_reserves u64 | real_quote_reserves u64 | holder_rewards_bps u64 | holder_rewards u64 |
creator_fee_unclaimed u64. Total take bps = fee + creator + cashback + buyback + holder_rewards bps.

    python3 -I experiments/2026-11-17-P-0465/tail.py
"""
import base64
import json
import sys
import time
from collections import Counter
from pathlib import Path

P464 = Path("/Users/triton/PROTEUS/experiments/2026-11-17-P-0464/events.py")
ns = {"__file__": str(P464), "__name__": "events"}
exec(compile(P464.read_text().split("\nsigs = ")[0], "events.py", "exec"), ns)
rpc, b58decode, PUMP, IX, WRAP, TRADE, u64 = (ns[k] for k in ("rpc", "b58decode", "PUMP", "IX", "WRAP", "TRADE", "u64"))
VersionedTransaction, Pubkey = ns["VersionedTransaction"], ns["Pubkey"]
SOL = "So11111111111111111111111111111111111111112"
OUT = Path(__file__).parent


def decode(d):
    e = ns["trade_event"](d)
    i = 250
    n = int.from_bytes(d[i:i + 4], "little")
    e["ix_name"] = d[i + 4:i + 4 + n].decode("utf-8", "replace")
    i += 4 + n
    if len(d) < i + 1 + 32:
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
    if len(d) >= i + 32 + 48:
        e["quote_mint"] = str(Pubkey.from_bytes(d[i:i + 32]))
        e["quote_amount"] = u64(d, i + 32)
        e["holder_rewards_bps"], e["holder_rewards"] = u64(d, i + 56), u64(d, i + 64)
    else:
        e["tail"] = "no quote fields"
    e["total_bps"] = (e["fee_bps"] + e["creator_fee_bps"] + e.get("cashback_bps", 0) + e.get("buyback_bps", 0)
                      + e.get("holder_rewards_bps", 0))
    return e


sigs = rpc("getSignaturesForAddress", [str(PUMP), {"limit": 120}]).get("result", [])
evs, fetched = [], 0
for s in sigs:
    if s.get("err"):
        continue
    tx = (rpc("getTransaction", [s["signature"], {"encoding": "base64", "maxSupportedTransactionVersion": 0}]) or {}).get("result")
    time.sleep(0.25)
    if not tx:
        continue
    fetched += 1
    vt = VersionedTransaction.from_bytes(base64.b64decode(tx["transaction"][0]))
    keys = list(vt.message.account_keys)
    loaded = (tx.get("meta") or {}).get("loadedAddresses") or {}
    keys += [Pubkey.from_string(k) for k in loaded.get("writable", []) + loaded.get("readonly", [])]
    for grp in (tx.get("meta") or {}).get("innerInstructions") or []:
        for ii in grp["instructions"]:
            d = b58decode(ii["data"])
            if keys[ii["programIdIndex"]] == PUMP and d[:8] == WRAP and d[8:16] == TRADE and len(d) >= 16 + 254:
                e = decode(d[16:])
                e["sig"] = s["signature"][:16]
                evs.append(e)
    if fetched >= 60:
        break

zero = [e for e in evs if e["fee_bps"] == 0]
paid = [e for e in evs if e["fee_bps"] > 0]


def prof(rows):
    return {"n": len(rows),
            "ix_name": dict(Counter(e["ix_name"] for e in rows)),
            "is_buy": dict(Counter(str(e["is_buy"]) for e in rows)),
            "mayhem": dict(Counter(str(e.get("mayhem")) for e in rows)),
            "quote_is_sol": dict(Counter(str(e.get("quote_mint") in (SOL, None, "11111111111111111111111111111111")) for e in rows)),
            "quote_mint": dict(Counter((e.get("quote_mint") or "-")[:8] for e in rows)),
            "cashback_bps": dict(Counter(e.get("cashback_bps") for e in rows)),
            "buyback_bps": dict(Counter(e.get("buyback_bps") for e in rows)),
            "holder_rewards_bps": dict(Counter(e.get("holder_rewards_bps") for e in rows)),
            "total_bps": dict(Counter(e.get("total_bps") for e in rows)),
            "sol_amount_zero": sum(1 for e in rows if e["sol_amount"] == 0),
            "quote_amount_pos": sum(1 for e in rows if e.get("quote_amount")),
            "tail": dict(Counter(e.get("tail", "ok") for e in rows))}


summary = {"fetched": fetched, "events": len(evs), "zero_fee": prof(zero), "paid_fee": prof(paid)}
print(json.dumps(summary, indent=1))
(OUT / "results.json").write_text(json.dumps({"summary": summary, "events": evs}, indent=1))
