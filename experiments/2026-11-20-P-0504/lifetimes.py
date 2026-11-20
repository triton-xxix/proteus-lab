"""P-0504: how long did the mayhem coins P-0491 caught actually live?

For each mint in experiments/2026-11-19-P-0491/results.json, page getSignaturesForAddress back to the
first signature (birth) and take the newest successful signature as the end of life. Lifetime is the
gap between them. Keyless public RPC, read only, standard library.

    python3 lifetimes.py
"""
import calendar, json, statistics, sys, time, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = Path("/Users/triton/PROTEUS/experiments/2026-11-19-P-0491/results.json")
RPC = "https://api.mainnet-beta.solana.com"
HALT = Path("/Users/triton/PROTEUS/HALT")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) proteus-lifetimes/0.1"
MAX_PAGES = 8


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


def all_sigs(mint):
    out, before = [], None
    for _ in range(MAX_PAGES):
        opts = {"limit": 1000}
        if before:
            opts["before"] = before
        r = rpc("getSignaturesForAddress", [mint, opts])
        if "result" not in r:
            return out, False, r.get("error")
        page = r["result"]
        out.extend(page)
        if len(page) < 1000:
            return out, True, None
        before = page[-1]["signature"]
        time.sleep(0.6)
    return out, False, "page cap"


def main():
    if HALT.exists():
        print("HALT")
        return 1
    src = json.loads(SRC.read_text())
    caught_at = calendar.timegm(time.strptime(src["summary"]["at"], "%Y-%m-%dT%H:%M:%SZ"))
    now = time.time()
    rows = []
    for r0 in src["rows"]:
        m = r0["mint"]
        sigs, complete, err = all_sigs(m)
        ok = [s for s in sigs if s.get("blockTime") and s.get("err") is None]
        row = {"mint": m, "sigs_total": len(sigs), "sigs_ok": len(ok), "complete": complete}
        if err:
            row["error"] = str(err)[:120]
        if ok:
            birth = min(s["blockTime"] for s in sigs if s.get("blockTime"))
            last = max(s["blockTime"] for s in ok)
            row["birth_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(birth))
            row["lifetime_min"] = round((last - birth) / 60, 2)
            row["quiet_h"] = round((now - last) / 3600, 2)
            row["age_at_catch_min"] = round((caught_at - birth) / 60, 2)
            row["sigs_after_catch"] = sum(1 for s in ok if s["blockTime"] > caught_at)
            # the last few signatures: is the end a burst of trades or one lone late call?
            tail = sorted(s["blockTime"] for s in ok)[-5:]
            row["last5_gaps_min"] = [round((b - a) / 60, 2) for a, b in zip(tail, tail[1:])]
        rows.append(row)
        print(json.dumps(row), flush=True)
        time.sleep(0.8)

    full = [r for r in rows if r.get("complete") and "lifetime_min" in r]
    life = sorted(r["lifetime_min"] for r in full)
    summary = {
        "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)),
        "mints": len(rows), "complete": len(full),
        "median_lifetime_min": statistics.median(life) if life else None,
        "min_lifetime_min": life[0] if life else None,
        "max_lifetime_min": life[-1] if life else None,
        "dead_inside_10_min": sum(1 for x in life if x <= 10),
        "dead_inside_35_min": sum(1 for x in life if x <= 35),
        "dead_inside_60_min": sum(1 for x in life if x <= 60),
        "quiet_over_12h": sum(1 for r in full if r["quiet_h"] > 12),
        "quiet_under_1h": sum(1 for r in full if r["quiet_h"] < 1),
        "median_sigs": statistics.median([r["sigs_total"] for r in full]) if full else None,
        "lifetimes_min": life,
    }
    (HERE / "results.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1))
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
