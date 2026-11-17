"""P-0466: does the zero-fee class of pump.fun trades truly pay nothing?

The TradeEvent says fee 0 for some mayhem-mode trades (P-0465). An event can lie by omission, a
balance cannot. For each live transaction carrying exactly one SOL-quoted TradeEvent, compare the
trader's SOL balance change (meta.preBalances/postBalances, less the network fee when the trader is
the fee payer) with the event's sol_amount:

    buy:  gap = (SOL out of the wallet) - sol_amount
    sell: gap = sol_amount - (SOL into the wallet)

gap in bps of sol_amount is what the trade cost beyond the curve price: protocol and creator fees,
plus noise (token-account rent of about 0.002 SOL on a first buy, tips, router fees). Medians, not
means, because of that noise. Also kept, for P-0469: who signs the zero-fee trades, and the supply of
the mints involved (getTokenSupply).

Keyless, public RPC, standard library, read only. Reuses the decoder from docs/tools/pump-trades.
"""
import json, statistics, sys, time
from collections import Counter
from pathlib import Path

sys.path.insert(0, "/Users/triton/PROTEUS/docs/tools/pump-trades")
import pump_trades as pt  # noqa: E402

HERE = Path(__file__).resolve().parent
N = int(sys.argv[1]) if len(sys.argv) > 1 else 60


def main():
    sigs = pt.rpc(pt.RPC, "getSignaturesForAddress", [pt.PUMP, {"limit": min(1000, N * 8)}]).get("result", [])
    rows, fetched, failed, multi = [], 0, 0, 0
    for s in sigs:
        if fetched >= N:
            break
        if s.get("err"):
            continue
        tx = (pt.rpc(pt.RPC, "getTransaction", [s["signature"], {"encoding": "json", "maxSupportedTransactionVersion": 0}]) or {}).get("result")
        time.sleep(0.25)
        if not tx:
            failed += 1
            continue
        fetched += 1
        evs = [pt.score(e) for e in pt.events_in(tx)]
        if len(evs) != 1:
            multi += len(evs) > 1
            continue
        e = evs[0]
        meta = tx["meta"]
        keys = list(tx["transaction"]["message"]["accountKeys"])
        loaded = meta.get("loadedAddresses") or {}
        keys += loaded.get("writable", []) + loaded.get("readonly", [])  # balances cover these too
        e["sig"] = s["signature"]
        e["fee_payer"] = keys[0]
        e["user_is_payer"] = e["user"] == keys[0]
        e["user_in_keys"] = e["user"] in keys
        e["quote_mint_seen"] = e.get("quote_mint")
        if e["user"] in keys and e["sol_quote"] and e["sol_amount"] > 0:
            i = keys.index(e["user"])
            delta = meta["postBalances"][i] - meta["preBalances"][i]
            net = meta["fee"] if i == 0 else 0
            gap = (-delta - net - e["sol_amount"]) if e["is_buy"] else (e["sol_amount"] - (delta + net))
            e["balance_delta"], e["network_fee"], e["gap_lamports"] = delta, net, gap
            e["gap_bps"] = round(gap / e["sol_amount"] * 10000, 1)
            e["event_fee_bps_total"] = e["fee_bps"] + e["creator_fee_bps"]
        rows.append(e)

    def cls(r):
        return ("mayhem " if r.get("mayhem") else "plain ") + ("no fee" if r["fee_class"] == "no fee" else "paid")

    out = {"transactions": fetched, "fetch_failed": failed, "multi_event_skipped": multi, "single_event_trades": len(rows), "classes": {}}
    for name in sorted({cls(r) for r in rows}):
        rs = [r for r in rows if cls(r) == name]
        g = [r["gap_bps"] for r in rs if "gap_bps" in r]
        users = Counter(r["user"] for r in rs)
        out["classes"][name] = {
            "trades": len(rs), "with_gap": len(g),
            "gap_bps_median": round(statistics.median(g), 1) if g else None,
            "gap_bps_quartiles": [round(x, 1) for x in statistics.quantiles(g, n=4)] if len(g) >= 4 else None,
            "gap_bps_min": min(g) if g else None, "gap_bps_max": max(g) if g else None,
            "within_10bps_of_zero": sum(abs(x) <= 10 for x in g),
            "within_10bps_of_event_fee": sum(abs(r["gap_bps"] - r["event_fee_bps_total"]) <= 10 for r in rs if "gap_bps" in r),
            "buys": sum(r["is_buy"] for r in rs), "distinct_users": len(users),
            "top_user_share": round(users.most_common(1)[0][1] / len(rs), 2), "top_users": users.most_common(3),
            "user_is_fee_payer": sum(r["user_is_payer"] for r in rs),
            "distinct_fee_payers": len({r["fee_payer"] for r in rs}), "mints": len({r["mint"] for r in rs}),
            "ix_names": dict(Counter(r.get("ix_name", "-") for r in rs)),
        }
    supplies = {}
    for flag in (True, False):
        for m in list(dict.fromkeys(r["mint"] for r in rows if bool(r.get("mayhem")) == flag))[:4]:
            res = pt.rpc(pt.RPC, "getTokenSupply", [m]).get("result") or {}
            v = res.get("value") or {}
            supplies[m] = {"mayhem": flag, "ui_supply": v.get("uiAmount"), "decimals": v.get("decimals")}
            time.sleep(0.3)
    out["supplies"] = supplies
    (HERE / "results.json").write_text(json.dumps({"summary": out, "rows": rows}, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
