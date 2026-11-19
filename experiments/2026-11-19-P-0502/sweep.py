#!/usr/bin/env python3
"""Is the mayhem 24-hour burn one daily sweep or a rolling one? Time the coins co-burned in P-0496's batches.
Keyless, Solana public RPC. Birth = oldest signature on the mint, paged back at most 5 pages of 1000."""
import json, os, statistics, time, urllib.request

RPC = "https://api.mainnet-beta.solana.com"
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "/Users/triton/PROTEUS/experiments/2026-11-19-P-0496/results.json"
WANT = 12


def rpc(method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    for i in range(5):
        try:
            req = urllib.request.Request(RPC, body, {"Content-Type": "application/json", "User-Agent": "probe/1.0"})
            out = json.loads(urllib.request.urlopen(req, timeout=30).read())
            if "result" in out:
                time.sleep(1.2)
                return out["result"]
            err = out.get("error")
        except Exception as e:
            err = str(e)
        time.sleep(3 * (i + 1))
    raise SystemExit("rpc failed: %s" % err)


src = json.load(open(SRC))["rows"]
done = {r["mint"] for r in src}
todo = []
for r in src:                       # round-robin so every batch is represented
    for m in r["burn_mints"]:
        if m not in done:
            todo.append((m, r["blockTime"], r["signature"][:8]))
todo = todo[:WANT]
rows = []
for mint, burn_t, batch in todo:
    before, oldest, pages, complete, n = None, None, 0, False, 0
    while pages < 5:
        p = {"limit": 1000}
        if before:
            p["before"] = before
        page = rpc("getSignaturesForAddress", [mint, p])
        pages += 1
        n += len(page)
        if page:
            oldest, before = page[-1]["blockTime"], page[-1]["signature"]
        if len(page) < 1000:
            complete = True
            break
    row = {"mint": mint, "batch": batch, "burn_blockTime": burn_t, "birth_blockTime": oldest, "signatures": n,
           "birth_complete": complete, "seconds_past_24h": burn_t - oldest - 86400 if complete else None,
           "age_hours_at_burn": round((burn_t - oldest) / 3600, 3) if complete else None}
    rows.append(row)
    print(mint[:8], batch, "sigs", n, "complete", complete, "past 24h s", row["seconds_past_24h"])
ok = [r["seconds_past_24h"] for r in rows if r["birth_complete"]]
summary = {"timed": len(ok), "incomplete": len(rows) - len(ok), "min_s": min(ok), "max_s": max(ok),
           "median_s": statistics.median(ok), "under_30_min_past": sum(1 for x in ok if 0 <= x <= 1800),
           "over_1_hour_past": sum(1 for x in ok if x > 3600), "p0496_five": [1035, 1081, 1291, 1068, 1162]}
json.dump({"rows": rows, "summary": summary}, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps(summary))
