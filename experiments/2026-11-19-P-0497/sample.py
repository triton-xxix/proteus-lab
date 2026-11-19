#!/usr/bin/env python3
"""P-0497: sample the mayhem wallet's SOL balance every 20 s for eight minutes. Keyless, public RPC."""
import json, os, statistics, time, urllib.request

RPC = "https://api.mainnet-beta.solana.com"
WALLET = "BwWK17cbHxwWBKZkUYvzxLcNQ1YVyaFezduWbtm2de6s"
HERE = os.path.dirname(os.path.abspath(__file__))
EVERY, N = 20, 25


def balance():
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "getBalance", "params": [WALLET]}).encode()
    req = urllib.request.Request(RPC, body, {"Content-Type": "application/json", "User-Agent": "probe/1.0"})
    out = json.loads(urllib.request.urlopen(req, timeout=20).read())["result"]
    return out["context"]["slot"], out["value"] / 1e9


rows, t0 = [], time.time()
for i in range(N):
    target = t0 + i * EVERY
    time.sleep(max(0, target - time.time()))
    try:
        slot, sol = balance()
        rows.append({"t": round(time.time() - t0, 1), "at": time.strftime("%H:%M:%SZ", time.gmtime()), "slot": slot, "sol": sol})
    except Exception as e:
        rows.append({"t": round(time.time() - t0, 1), "err": str(e)[:80]})
ok = [r for r in rows if "sol" in r]
sols = [r["sol"] for r in ok]
steps = [b["sol"] - a["sol"] for a, b in zip(ok, ok[1:])]
mins = (ok[-1]["t"] - ok[0]["t"]) / 60
summary = {"wallet": WALLET, "samples": len(ok), "errors": len(rows) - len(ok), "minutes": round(mins, 2),
           "first": sols[0], "last": sols[-1], "min": min(sols), "max": max(sols), "range": round(max(sols) - min(sols), 3),
           "net": round(sols[-1] - sols[0], 3), "net_per_day_if_steady": round((sols[-1] - sols[0]) / mins * 1440, 1),
           "median_abs_step": round(statistics.median(abs(s) for s in steps), 3),
           "max_abs_step": round(max(abs(s) for s in steps), 3), "steps_up": sum(1 for s in steps if s > 0),
           "steps_down": sum(1 for s in steps if s < 0),
           "earlier": {"2026-11-18T12:33Z": 71345.730972423, "2026-11-19T12:32Z": 71126.396791128}}
json.dump({"rows": rows, "summary": summary}, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps(summary))
