"""P-0548: what does the fee sweeper FHpcNSe6... move in an hour? Keyless public RPC, read only.

Page its signatures back one hour, sample 100 successes spread over the hour (skipping the newest
minute), getTransaction each, and tally per transaction: the instruction names in the logs, native
SOL gained by accounts other than the signer, wrapped-SOL token gains, and the token mints touched.
Extrapolate per-transaction means to the hour's success count.

    python3 sweeper.py
"""
import collections, json, statistics, sys, time, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
RPC = "https://api.mainnet-beta.solana.com"
W = "FHpcNSe6tb2n15bAdq4BkeYWGyZKFD7yLYrH92ng7wCT"
WSOL = "So11111111111111111111111111111111111111112"
UA = "Mozilla/5.0 proteus-p0548/0.1"
DEADLINE = time.time() + 540


def rpc(m, p, tries=4):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": m, "params": p}).encode()
    for a in range(tries):
        try:
            req = urllib.request.Request(RPC, data=body, headers={"Content-Type": "application/json", "User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                out = json.loads(r.read())
            if out.get("result") is not None:
                return out["result"]
        except Exception:
            pass
        time.sleep(1.5 * (a + 1))
    return None


def main():
    if Path("/Users/triton/PROTEUS/HALT").exists():
        return 1
    now = time.time()
    sigs, before = [], None
    while time.time() < DEADLINE - 360:
        o = {"limit": 1000}
        if before:
            o["before"] = before
        page = rpc("getSignaturesForAddress", [W, o]) or []
        if not page:
            break
        sigs += page
        before = page[-1]["signature"]
        if (page[-1].get("blockTime") or now) < now - 3600:
            break
    hour = [s for s in sigs if s.get("blockTime") and now - 3600 <= s["blockTime"] <= now]
    covered_s = now - min(s["blockTime"] for s in hour) if hour else 0
    ok = [s for s in hour if not s.get("err") and s["blockTime"] < now - 60]
    step = max(1, len(ok) // 100)
    sample = ok[::step][:100]
    rows = []
    for s in sample:
        if time.time() > DEADLINE:
            break
        t = rpc("getTransaction", [s["signature"], {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0, "commitment": "confirmed"}])
        if not t:
            rows.append({"sig": s["signature"], "read": False})
            continue
        keys = [k["pubkey"] for k in t["transaction"]["message"]["accountKeys"]]
        m = t["meta"]
        sol_gain = collections.Counter()
        for i, k in enumerate(keys):
            d = m["postBalances"][i] - m["preBalances"][i]
            if d > 0 and k != W:
                sol_gain[k] += d / 1e9
        pre = {(b["accountIndex"]): b for b in m.get("preTokenBalances") or []}
        wsol_gain, mints = collections.Counter(), set()
        for b in m.get("postTokenBalances") or []:
            mints.add(b["mint"])
            if b["mint"] == WSOL:
                p0 = float((pre.get(b["accountIndex"]) or {}).get("uiTokenAmount", {}).get("uiAmount") or 0)
                d = float(b["uiTokenAmount"].get("uiAmount") or 0) - p0
                if d > 0:
                    wsol_gain[b.get("owner")] += d
        ins = [l.split("Instruction: ")[1] for l in m.get("logMessages") or [] if "Instruction: " in l]
        rows.append({"sig": s["signature"], "read": True, "ins": ins, "sol_gain": dict(sol_gain), "wsol_gain": dict(wsol_gain),
                     "mints": sorted(x for x in mints if x != WSOL), "fee": m["fee"] / 1e9})
        time.sleep(0.25)
    read = [r for r in rows if r["read"]]
    kinds = collections.Counter(i for r in read for i in set(r["ins"]) if i.startswith("Sweep"))
    per_tx = [sum(r["sol_gain"].values()) + sum(r["wsol_gain"].values()) for r in read]
    by_kind = collections.defaultdict(float)
    receivers = collections.Counter()
    for r in read:
        k = next((i for i in r["ins"] if i.startswith("Sweep")), "other")
        by_kind[k] += sum(r["sol_gain"].values()) + sum(r["wsol_gain"].values())
        for a, v in list(r["sol_gain"].items()) + list(r["wsol_gain"].items()):
            receivers[a] += v
    mints = {x for r in read for x in r["mints"]}
    scale = len(ok) / len(read) if read else 0
    res = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)), "signatures_paged": len(sigs),
           "hour_covered_s": round(covered_s), "hour_signatures": len(hour), "hour_failed": sum(1 for s in hour if s.get("err")),
           "sampled": len(rows), "read": len(read), "sweep_kinds_in_sample": dict(kinds),
           "sol_moved_in_sample": round(sum(per_tx), 4), "sol_per_tx_median": round(statistics.median(per_tx), 6) if per_tx else None,
           "sol_moved_by_kind_in_sample": {k: round(v, 4) for k, v in by_kind.items()},
           "hour_estimate_sol": round(sum(per_tx) * scale, 2), "distinct_mints_in_sample": len(mints),
           "top_receivers": [[a[:8], round(v, 4)] for a, v in receivers.most_common(5)],
           "fees_paid_sol_sample": round(sum(r["fee"] for r in read), 6)}
    (HERE / "results.json").write_text(json.dumps({"summary": res, "rows": rows}, indent=1))
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
