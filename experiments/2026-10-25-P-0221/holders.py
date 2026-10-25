"""P-0221: top-10 holder share of supply for ten recent Solana tokens, from public RPC alone.

Takes tonight's newest snapshot rows (grinder/SNAPSHOTS.csv), calls getTokenSupply and
getTokenLargestAccounts on api.mainnet-beta.solana.com, and compares the raw top-10 share with
the top10_pct rugcheck gave the scanner. Raw RPC counts every token account, including the pool
and burn accounts, so the gap between the two is the point.
"""
import csv, json, sys, time, urllib.request

RPC = "https://api.mainnet-beta.solana.com"
SNAP = "/Users/triton/PROTEUS/grinder/SNAPSHOTS.csv"
OUT = "/Users/triton/PROTEUS/experiments/2026-10-25-P-0221/results.json"


def rpc(method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(RPC, body, {"Content-Type": "application/json", "User-Agent": "proteus-probe"})
    t = time.time()
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.load(r)
    return data, time.time() - t


rows = list(csv.DictReader(open(SNAP)))
last_ts = rows[-1]["ts"][:13]
seen, picks = set(), []
for r in reversed(rows):
    if r["ts"][:13] != last_ts or r["mint"] in seen:
        continue
    seen.add(r["mint"])
    picks.append(r)
    if len(picks) == 10:
        break

out = []
for r in picks:
    rec = {"symbol": r["symbol"], "mint": r["mint"], "rugcheck_top10_pct": r["top10_pct"], "holders": r["holders"]}
    try:
        sup, t1 = rpc("getTokenSupply", [r["mint"]])
        big, t2 = rpc("getTokenLargestAccounts", [r["mint"]])
        if "error" in sup or "error" in big:
            rec["error"] = (sup.get("error") or big.get("error"))
        else:
            supply = float(sup["result"]["value"]["uiAmount"] or 0)
            accts = big["result"]["value"]
            top = [float(a["uiAmount"] or 0) for a in accts[:10]]
            rec["supply"] = supply
            rec["accounts_returned"] = len(accts)
            rec["rpc_top1_pct"] = round(100 * top[0] / supply, 2) if supply and top else None
            rec["rpc_top10_pct"] = round(100 * sum(top) / supply, 2) if supply else None
            rec["rpc_top10_ex_largest_pct"] = round(100 * sum(top[1:]) / supply, 2) if supply else None
            rec["secs"] = round(t1 + t2, 2)
    except Exception as e:
        rec["error"] = str(e)[:200]
    out.append(rec)
    time.sleep(0.6)

json.dump({"snapshot_hour": last_ts, "rpc": RPC, "tokens": out}, open(OUT, "w"), indent=1)
ok = [x for x in out if "rpc_top10_pct" in x]
print("tokens", len(out), "ok", len(ok), "errors", len(out) - len(ok))
for x in out:
    print(x["symbol"], "rugcheck", x["rugcheck_top10_pct"], "rpc", x.get("rpc_top10_pct"),
          "ex-largest", x.get("rpc_top10_ex_largest_pct"), "top1", x.get("rpc_top1_pct"), x.get("error", ""))
