"""P-0491: how many mayhem coins is the agent working at lunchtime, and how old are they?

1. getSignaturesForAddress on the mayhem wallet (limit 1000): the span gives the rate now.
2. getTransaction on 60 of those, spread evenly across the 1,000 (so the sample covers the whole
   span, not just its newest seconds). Distinct mints = the mints of token balances owned by the
   wallet in each transaction.
3. getSignaturesForAddress on each mint (limit 1000). Fewer than 1,000 back means the oldest is the
   birth; otherwise the oldest is only a lower bound on age.

    python3 alive.py

Keyless, read only, standard library.
"""
import json, statistics, sys, time, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
RPC = "https://api.mainnet-beta.solana.com"
WALLET = "BwWK17cbHxwWBKZkUYvzxLcNQ1YVyaFezduWbtm2de6s"
HALT = Path("/Users/triton/PROTEUS/HALT")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) proteus-inventory/0.1"
SAMPLE = 60


def rpc(method, params, tries=4):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(RPC, data=body, headers={"Content-Type": "application/json", "User-Agent": UA})
    err = None
    for attempt in range(tries):
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


def main():
    if HALT.exists():
        print("HALT")
        return 1
    t0 = time.time()
    r = rpc("getSignaturesForAddress", [WALLET, {"limit": 1000}])
    if "result" not in r:
        print("wallet signatures refused:", r)
        return 1
    sigs = r["result"]
    times = [s["blockTime"] for s in sigs if s.get("blockTime")]
    span = max(times) - min(times)
    failed = sum(1 for s in sigs if s.get("err") is not None)
    step = max(1, len(sigs) // SAMPLE)
    picks = sigs[::step][:SAMPLE]
    mints, fetched, refused, no_wallet_balance = {}, 0, 0, 0
    for s in picks:
        t = rpc("getTransaction", [s["signature"], {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}], tries=3)
        res = t.get("result")
        if not res:
            refused += 1
            time.sleep(0.5)
            continue
        fetched += 1
        meta = res.get("meta") or {}
        found = False
        for b in (meta.get("postTokenBalances") or []) + (meta.get("preTokenBalances") or []):
            if b.get("owner") == WALLET:
                mints[b["mint"]] = mints.get(b["mint"], 0) + 1
                found = True
        if not found:
            no_wallet_balance += 1
        time.sleep(0.45)
    # a transaction lists the balance in pre and post, so halve the counts
    mints = {m: (n + 1) // 2 for m, n in mints.items()}
    print(json.dumps({"span_s": span, "fetched": fetched, "refused": refused, "distinct_mints": len(mints)}), flush=True)

    now = time.time()
    rows = []
    for m, n in sorted(mints.items(), key=lambda kv: -kv[1]):
        g = rpc("getSignaturesForAddress", [m, {"limit": 1000}])
        row = {"mint": m, "sample_txs": n}
        if "result" in g and g["result"]:
            page = [x for x in g["result"] if x.get("blockTime")]
            row["sigs"] = len(g["result"])
            row["birth_seen"] = len(g["result"]) < 1000
            row["oldest_min_ago"] = round((now - page[-1]["blockTime"]) / 60, 2)
            row["newest_s_ago"] = round(now - page[0]["blockTime"], 1)
        else:
            row["error"] = str(g.get("error"))[:120]
        rows.append(row)
        print(json.dumps(row), flush=True)
        time.sleep(0.8)

    born = [r["oldest_min_ago"] for r in rows if r.get("birth_seen")]
    capped = [r["oldest_min_ago"] for r in rows if r.get("birth_seen") is False]
    med = statistics.median(born) if born else None
    summary = {
        "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)),
        "wallet_sigs": len(sigs), "span_s": span,
        "tx_per_s": round(len(sigs) / span, 2) if span else None,
        "failed_of_1000": failed,
        "sampled": len(picks), "fetched": fetched, "refused": refused,
        "fetched_without_wallet_token_balance": no_wallet_balance,
        "distinct_mints": len(mints),
        "ages_known": len(born), "ages_lower_bound_only": len(capped),
        "median_age_min": med,
        "min_age_min": min(born) if born else None,
        "max_age_min": max(born) if born else None,
        "born_in_last_10_min": sum(1 for a in born if a <= 10),
        "born_in_last_60_min": sum(1 for a in born if a <= 60),
        "lower_bounds_min": sorted(capped),
        # coins seen being worked that were born in the last hour = a floor on births an hour
        "implied_births_per_hour_live_over_median_age": round(len(mints) / med * 60, 1) if med else None,
    }
    (HERE / "results.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1))
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
