#!/usr/bin/env python3
"""P-0005: pump.fun graduation rate from keyless sources only.

Numerator: pools created on pumpswap (where graduated pump tokens trade), from GeckoTerminal's
new_pools feed, newest first, up to 10 pages, timestamps give a pools-per-hour rate.
Denominator: token creations on the pump.fun program, estimated from the public Solana RPC as
(transactions per hour on the program, from one getSignaturesForAddress call) times (fraction of a
random sample of those transactions whose logs carry "Instruction: Create"). pump.fun's own API is
geo-blocked from this machine (403 to static.pump.fun/blocked, rechecked tonight).
Output: REPORT.md next to this file. Diagnostic only.
"""
import json, random, time, urllib.request
from datetime import datetime, timezone
PUMP = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
RPC = "https://api.mainnet-beta.solana.com"
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "proteus-probe/0.1", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r: return json.load(r)
def rpc(method, params):
    req = urllib.request.Request(RPC, data=json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode(),
                                 headers={"Content-Type": "application/json", "User-Agent": "proteus-probe/0.1"})
    with urllib.request.urlopen(req, timeout=25) as r: return json.load(r).get("result")
L = ["# P-0005: pump.fun graduation rate, keyless", ""]
# numerator
pools, pages = [], 0
for page in range(1, 11):
    try:
        d = get("https://api.geckoterminal.com/api/v2/networks/solana/new_pools?page=%d" % page)
    except Exception as e:
        L.append("GeckoTerminal page %d failed: %s" % (page, str(e)[:60])); break
    pages += 1
    for p in d.get("data", []):
        a = p["attributes"]; dex = (p.get("relationships", {}).get("dex", {}).get("data", {}) or {}).get("id")
        pools.append((dex, a.get("pool_created_at"), a.get("name")))
    time.sleep(1.2)
ts = [datetime.fromisoformat(t.replace("Z", "+00:00")) for _, t, _ in pools if t]
span_h = (max(ts) - min(ts)).total_seconds() / 3600 if ts else 0
by_dex = {}
for dex, _, _ in pools: by_dex[dex] = by_dex.get(dex, 0) + 1
ps = by_dex.get("pumpswap", 0)
L += ["## Numerator: new pools on GeckoTerminal", "",
      "%d pools over %d pages, spanning %.2f hours (%s to %s). By dex: %s." % (
          len(pools), pages, span_h, min(ts).strftime("%H:%M"), max(ts).strftime("%H:%M"), ", ".join("%s %d" % kv for kv in sorted(by_dex.items(), key=lambda x: -x[1]))),
      "pumpswap pools per hour: **%.1f**" % (ps / span_h if span_h else 0), ""]
# denominator
sigs = rpc("getSignaturesForAddress", [PUMP, {"limit": 1000}]) or []
bt = [s["blockTime"] for s in sigs if s.get("blockTime")]
tx_span_h = (max(bt) - min(bt)) / 3600 if bt else 0
tx_per_h = len(sigs) / tx_span_h if tx_span_h else 0
random.seed(2)
sample = random.sample(sigs, min(30, len(sigs)))
creates, seen, errs = 0, 0, 0
for s in sample:
    try:
        tx = rpc("getTransaction", [s["signature"], {"encoding": "json", "maxSupportedTransactionVersion": 0}])
    except Exception:
        errs += 1; time.sleep(2); continue
    if not tx: errs += 1; continue
    seen += 1
    logs = (tx.get("meta") or {}).get("logMessages") or []
    if any("Instruction: Create" in l for l in logs): creates += 1
    time.sleep(0.6)
frac = creates / seen if seen else 0
creates_per_h = tx_per_h * frac
L += ["## Denominator: creations on the pump.fun program, public RPC", "",
      "Last %d signatures span %.1f minutes: **%.0f transactions per hour** on the program." % (len(sigs), tx_span_h * 60, tx_per_h),
      "Sample of %d transactions fetched (%d failed): %d carry `Instruction: Create`, fraction %.3f." % (seen, errs, creates, frac),
      "Estimated creations per hour: **%.0f** (wide error bars: %d of %d)." % (creates_per_h, creates, seen), ""]
rate = (ps / span_h) / creates_per_h if creates_per_h and span_h else None
L += ["## Graduation rate", "",
      ("pumpswap pools per hour over creations per hour: **%.1f percent**." % (100 * rate)) if rate else "Not computable: a zero in the chain above.",
      "Both rates are measured over windows of under an hour at different times of day; this is one reading, not the answer.", ""]
json.dump({"pools": pools, "sigs": len(sigs), "tx_span_h": tx_span_h, "sample": seen, "creates": creates},
          open("/Users/triton/PROTEUS/experiments/2026-09-24-P-0005/results.json", "w"))
open("/Users/triton/PROTEUS/experiments/2026-09-24-P-0005/REPORT.md", "w").write("\n".join(L) + "\n")
print("\n".join(L))
