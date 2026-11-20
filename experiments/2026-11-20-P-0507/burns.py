"""P-0507: when are mayhem coins burned? Two cohorts born a day apart.

Mints from P-0473 (born 17 Nov about 23:42 UK) and P-0491 (born 19 Nov about 12:35Z). For each:
getSignaturesForAddress limit 3 for the newest signature, getTransaction jsonParsed on it, and call it
a burn if any parsed instruction (outer or inner) is burn/burnChecked on this mint, or a log line says
Burn. Birth times come from P-0504's results (P-0491 cohort) or a paged signature read (P-0473).
Keyless public RPC, read only.

    python3 burns.py
"""
import json, statistics, sys, time, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = Path("/Users/triton/PROTEUS/experiments")
RPC = "https://api.mainnet-beta.solana.com"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) proteus-burns/0.1"


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


def birth(mint):
    before, oldest = None, None
    for _ in range(5):
        o = {"limit": 1000}
        if before:
            o["before"] = before
        r = rpc("getSignaturesForAddress", [mint, o])
        page = r.get("result") or []
        if not page:
            break
        oldest = page[-1].get("blockTime")
        if len(page) < 1000:
            return oldest
        before = page[-1]["signature"]
        time.sleep(0.5)
    return None


def is_burn(tx, mint):
    meta = tx.get("meta") or {}
    ins = list((tx.get("transaction") or {}).get("message", {}).get("instructions") or [])
    for inner in meta.get("innerInstructions") or []:
        ins += inner.get("instructions") or []
    for i in ins:
        p = i.get("parsed")
        if isinstance(p, dict) and p.get("type") in ("burn", "burnChecked") and (p.get("info") or {}).get("mint") == mint:
            return True
    return any("Instruction: Burn" in (l or "") for l in meta.get("logMessages") or [])


def main():
    if Path("/Users/triton/PROTEUS/HALT").exists():
        print("HALT")
        return 1
    p73 = json.loads((EXP / "2026-11-18-P-0473/results.json").read_text())
    p04 = json.loads((EXP / "2026-11-20-P-0504/results.json").read_text())
    rows73 = p73["rows"] if isinstance(p73, dict) and "rows" in p73 else p73
    cohorts = [("P-0473", r["mint"], None) for r in rows73]
    cohorts += [("P-0491", r["mint"], r["birth_utc"]) for r in p04["rows"] if r.get("complete")]
    now = time.time()
    rows = []
    for c, m, b in cohorts:
        bt = time.mktime(time.strptime(b, "%Y-%m-%dT%H:%M:%SZ")) - time.timezone if b else birth(m)
        s = rpc("getSignaturesForAddress", [m, {"limit": 3}]).get("result") or []
        row = {"cohort": c, "mint": m, "birth": bt}
        if s:
            newest = s[0]
            t = rpc("getTransaction", [newest["signature"], {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}]).get("result")
            row["newest_blockTime"] = newest.get("blockTime")
            row["newest_is_burn"] = bool(t) and is_burn(t, m)
            if bt and newest.get("blockTime"):
                row["newest_age_h"] = round((newest["blockTime"] - bt) / 3600, 3)
            row["age_now_h"] = round((now - bt) / 3600, 3) if bt else None
        rows.append(row)
        print(json.dumps(row), flush=True)
        time.sleep(0.6)
    summary = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))}
    for c in ("P-0473", "P-0491"):
        rs = [r for r in rows if r["cohort"] == c]
        burned = [r for r in rs if r.get("newest_is_burn")]
        ages = sorted(r["newest_age_h"] for r in burned if r.get("newest_age_h") is not None)
        times = sorted(r["newest_blockTime"] for r in burned)
        gaps = [b - a for a, b in zip(times, times[1:])]
        summary[c] = {"mints": len(rs), "burned": len(burned),
                      "burn_age_h_min": ages[0] if ages else None, "burn_age_h_max": ages[-1] if ages else None,
                      "burn_age_h_median": statistics.median(ages) if ages else None,
                      "burn_times_utc": [time.strftime("%H:%M:%S", time.gmtime(x)) for x in times],
                      "gaps_over_5min_s": [g for g in gaps if g > 300]}
    (HERE / "results.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1))
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
