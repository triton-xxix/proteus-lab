"""P-0475: what the mayhem agent's fee payer spends on network fees.

P-0470 found one account, Gygj9QQb...BUpA, pays the network fee on every mayhem-agent transaction.
Three readings, keyless on the public RPC:

1. rate: getSignaturesForAddress (limit 1,000) on the fee payer, block-time span of the list;
2. fee: getTransaction on --fetch of those signatures spread evenly through the list, meta.fee, the
   number of signatures, and the fee payer's own pre/post balance change in each;
3. drift: getBalance before and after, --drift seconds apart.

    python3 feepayer.py --fetch 60 --drift 600

Read only. Standard library. Stops on HALT.
"""
import argparse, json, statistics, sys, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RPC = "https://api.mainnet-beta.solana.com"
PAYER = "Gygj9QQby4j2jryqyqBHvLP7ctv2SaANgh4sCb69BUpA"
WALLET = "BwWK17cbHxwWBKZkUYvzxLcNQ1YVyaFezduWbtm2de6s"
HALT = Path("/Users/triton/PROTEUS/HALT")


def rpc(method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(RPC, data=body, headers={"Content-Type": "application/json", "User-Agent": "proteus-feepayer/0.1"})
    err = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                out = json.loads(r.read())
            if "result" in out:
                return out
            err = out.get("error")
        except Exception as e:
            err = e
        time.sleep(2 * (attempt + 1))
    return {"error": str(err)[:200]}


def balance():
    b = rpc("getBalance", [PAYER])
    return (b["result"]["value"] / 1e9, time.time()) if "result" in b else (None, time.time())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", type=int, default=60)
    ap.add_argument("--drift", type=int, default=600)
    a = ap.parse_args()
    if HALT.exists():
        print("HALT")
        return 1
    out = {"at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "payer": PAYER}
    bal0, t0 = balance()
    out["balance_start"] = bal0

    s = rpc("getSignaturesForAddress", [PAYER, {"limit": 1000}])
    if "result" not in s:
        out["sig_error"] = s["error"]
        (HERE / "results.json").write_text(json.dumps(out, indent=1))
        print(json.dumps(out, indent=1))
        return 2
    sigs = s["result"]
    times = [x["blockTime"] for x in sigs if x.get("blockTime")]
    span = max(times) - min(times) if times else 0
    out["signatures"] = len(sigs)
    out["failed"] = sum(1 for x in sigs if x.get("err"))
    out["span_s"] = span
    out["newest_age_s"] = round(time.time() - max(times), 1) if times else None
    out["tx_per_s"] = round(len(sigs) / span, 2) if span else None
    print(json.dumps({k: out[k] for k in ("balance_start", "signatures", "failed", "span_s", "newest_age_s", "tx_per_s")}), flush=True)

    step = max(1, len(sigs) // a.fetch)
    rows, refused = [], 0
    for x in sigs[::step][: a.fetch]:
        if HALT.exists():
            break
        r = rpc("getTransaction", [x["signature"], {"encoding": "json", "maxSupportedTransactionVersion": 0}])
        tx = r.get("result")
        if not tx:
            refused += 1
            continue
        meta, msg = tx["meta"], tx["transaction"]["message"]
        keys = msg["accountKeys"]
        pi = keys.index(PAYER) if PAYER in keys else None
        rows.append({
            "sig": x["signature"][:16],
            "fee": meta["fee"],
            "n_sigs": len(tx["transaction"]["signatures"]),
            "payer_is_first": keys[0] == PAYER,
            "payer_delta": (meta["postBalances"][pi] - meta["preBalances"][pi]) if pi is not None else None,
            "wallet_in_tx": WALLET in keys,
            "cu": meta.get("computeUnitsConsumed"),
            "err": bool(meta.get("err")),
        })
        time.sleep(0.35)
    out["fetched"] = len(rows)
    out["refused"] = refused
    if rows:
        fees = [r["fee"] for r in rows]
        deltas = [r["payer_delta"] for r in rows if r["payer_delta"] is not None]
        out["fee_lamports_median"] = statistics.median(fees)
        out["fee_lamports_mean"] = round(statistics.mean(fees), 1)
        out["fee_lamports_min"] = min(fees)
        out["fee_lamports_max"] = max(fees)
        out["n_sigs_counts"] = {str(k): sum(1 for r in rows if r["n_sigs"] == k) for k in sorted({r["n_sigs"] for r in rows})}
        out["payer_is_first"] = sum(1 for r in rows if r["payer_is_first"])
        out["wallet_in_tx"] = sum(1 for r in rows if r["wallet_in_tx"])
        out["payer_delta_mean_lamports"] = round(statistics.mean(deltas), 1) if deltas else None
        out["payer_delta_equals_minus_fee"] = sum(1 for r in rows if r["payer_delta"] == -r["fee"])
        out["cu_median"] = statistics.median([r["cu"] for r in rows if r["cu"] is not None]) if any(r["cu"] is not None for r in rows) else None
        if out["tx_per_s"]:
            per_day = out["tx_per_s"] * 86400
            out["tx_per_day"] = round(per_day)
            out["fees_sol_per_day_from_rate"] = round(per_day * out["fee_lamports_mean"] / 1e9, 2)

    wait = a.drift - (time.time() - t0)
    if wait > 0:
        time.sleep(wait)
    bal1, t1 = balance()
    out["balance_end"] = bal1
    out["drift_s"] = round(t1 - t0, 1)
    if bal0 is not None and bal1 is not None:
        out["drift_sol"] = round(bal1 - bal0, 6)
        out["drift_sol_per_day"] = round((bal1 - bal0) / (t1 - t0) * 86400, 2)
        if bal1 < bal0:
            out["runway_days_from_drift"] = round(bal1 / ((bal0 - bal1) / (t1 - t0) * 86400), 1)
        if out.get("fees_sol_per_day_from_rate"):
            out["runway_days_from_rate"] = round(bal1 / out["fees_sol_per_day_from_rate"], 1)
    (HERE / "results.json").write_text(json.dumps({"summary": out, "rows": rows}, indent=1))
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
