"""P-0470: what does pump.fun's fee-free mayhem wallet actually do?

P-0466 and P-0469 found every fee-free mayhem trade is one wallet. This pulls that wallet's last
1,000 signatures (keyless, public RPC), reads how fast it trades from the block times alone, then
fetches a sample of the transactions and decodes its trades: per coin, how many buys and sells, SOL
in and out, tokens in and out, and the time between its first and last trade on the coin.

Read only. Standard library. Reuses the decoder in docs/tools/pump-trades.
"""
import json, statistics, sys, time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, "/Users/triton/PROTEUS/docs/tools/pump-trades")
import pump_trades as pt  # noqa: E402

HERE = Path(__file__).resolve().parent
WALLET = "BwWK17cbHxwWBKZkUYvzxLcNQ1YVyaFezduWbtm2de6s"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 150


def main():
    sigs = pt.rpc(pt.RPC, "getSignaturesForAddress", [WALLET, {"limit": 1000}]).get("result", [])
    times = [s["blockTime"] for s in sigs if s.get("blockTime")]
    errs = sum(1 for s in sigs if s.get("err"))
    span = (max(times) - min(times)) if times else 0
    per_min = Counter(t // 60 for t in times)
    head = {"signatures": len(sigs), "failed_on_chain": errs, "span_seconds": span,
            "per_minute_median": statistics.median(per_min.values()) if per_min else None,
            "per_minute_max": max(per_min.values()) if per_min else None,
            "newest": max(times) if times else None, "oldest": min(times) if times else None}
    print(json.dumps(head))
    rows, fetched, failed, other_users = [], 0, 0, Counter()
    payers = Counter()
    for s in sigs:
        if fetched >= N:
            break
        if s.get("err"):
            continue
        tx = (pt.rpc(pt.RPC, "getTransaction", [s["signature"], {"encoding": "json", "maxSupportedTransactionVersion": 0}]) or {}).get("result")
        time.sleep(0.3)
        if not tx:
            failed += 1
            continue
        fetched += 1
        payers[tx["transaction"]["message"]["accountKeys"][0]] += 1
        for e in pt.events_in(tx):
            e = pt.score(e)
            if e["user"] != WALLET:
                other_users[e["user"]] += 1
                continue
            e["sig"] = s["signature"]
            rows.append(e)
    coins = defaultdict(lambda: {"buys": 0, "sells": 0, "sol_in": 0, "sol_out": 0, "tok_in": 0, "tok_out": 0, "t": []})
    for r in rows:
        c = coins[r["mint"]]
        c["t"].append(r["timestamp"])
        if r["is_buy"]:
            c["buys"] += 1; c["sol_in"] += r["sol_amount"]; c["tok_in"] += r["token_amount"]
        else:
            c["sells"] += 1; c["sol_out"] += r["sol_amount"]; c["tok_out"] += r["token_amount"]
    per = []
    for m, c in coins.items():
        per.append({"mint": m, "buys": c["buys"], "sells": c["sells"],
                    "sol_spent": round(c["sol_in"] / 1e9, 4), "sol_received": round(c["sol_out"] / 1e9, 4),
                    "net_sol": round((c["sol_out"] - c["sol_in"]) / 1e9, 4),
                    "net_tokens_m": round((c["tok_in"] - c["tok_out"]) / 1e12, 2),
                    "seconds_first_to_last": max(c["t"]) - min(c["t"])})
    per.sort(key=lambda x: x["net_sol"])
    sizes = [r["sol_amount"] / 1e9 for r in rows]
    ts = [r["timestamp"] for r in rows]
    out = {"wallet": WALLET, "signatures": head, "transactions_fetched": fetched, "fetch_failed": failed,
           "fee_payers": payers.most_common(3), "events_by_other_users_in_same_tx": sum(other_users.values()),
           "trades": len(rows), "buys": sum(r["is_buy"] for r in rows), "sells": sum(not r["is_buy"] for r in rows),
           "fee_classes": dict(Counter(r["fee_class"] for r in rows)), "mayhem_flag_true": sum(bool(r.get("mayhem")) for r in rows),
           "coins": len(per), "sample_span_seconds": (max(ts) - min(ts)) if ts else 0,
           "trade_sol_median": round(statistics.median(sizes), 4) if sizes else None,
           "trade_sol_max": round(max(sizes), 4) if sizes else None,
           "sol_spent": round(sum(p["sol_spent"] for p in per), 4), "sol_received": round(sum(p["sol_received"] for p in per), 4),
           "net_sol": round(sum(p["net_sol"] for p in per), 4),
           "coins_net_sol_positive": sum(p["net_sol"] > 0 for p in per), "coins_net_sol_negative": sum(p["net_sol"] < 0 for p in per),
           "coins_sell_only": sum(p["buys"] == 0 for p in per), "coins_buy_only": sum(p["sells"] == 0 for p in per),
           "trades_per_coin_median": statistics.median([p["buys"] + p["sells"] for p in per]) if per else None}
    (HERE / "results.json").write_text(json.dumps({"summary": out, "per_coin": per, "rows": rows}, indent=1))
    print(json.dumps(out, indent=1))
    print("worst 3", json.dumps(per[:3]))
    print("best 3", json.dumps(per[-3:]))


if __name__ == "__main__":
    main()
