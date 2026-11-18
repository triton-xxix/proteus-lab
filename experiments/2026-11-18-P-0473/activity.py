"""P-0473, second leg: pump.fun's coin endpoint answered 403 for every mint, so no creation times.

Instead: getSignaturesForAddress on each mint, newest 1,000. If fewer than 1,000 come back the
oldest one is the coin's birth; otherwise the oldest is only a lower bound on age. The newest
block time says whether the coin is still being traded now.

    python3 activity.py
"""
import json, statistics, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from inventory import rpc, HALT  # noqa: E402


def main():
    if HALT.exists():
        print("HALT")
        return 1
    res = json.loads((HERE / "results.json").read_text())
    now = time.time()
    for row in res["rows"]:
        r = rpc("getSignaturesForAddress", [row["mint"], {"limit": 1000}])
        if "result" not in r:
            row["sig_error"] = r["error"]
            print(json.dumps({"mint": row["mint"], "sig_error": r["error"]}), flush=True)
            continue
        sigs = [s for s in r["result"] if s.get("blockTime")]
        row["sigs"] = len(r["result"])
        if sigs:
            row["last_trade_min_ago"] = round((now - sigs[0]["blockTime"]) / 60, 1)
            row["oldest_seen_h_ago"] = round((now - sigs[-1]["blockTime"]) / 3600, 2)
            row["birth_seen"] = len(r["result"]) < 1000
        print(json.dumps({k: row.get(k) for k in ("mint", "sigs", "last_trade_min_ago", "oldest_seen_h_ago", "birth_seen")}), flush=True)
        time.sleep(0.8)
    rows = [r for r in res["rows"] if "sigs" in r]
    born = [r["oldest_seen_h_ago"] for r in rows if r.get("birth_seen")]
    res["summary"].update({
        "sig_answered": len(rows),
        "traded_in_last_10_min": sum(1 for r in rows if r.get("last_trade_min_ago", 1e9) <= 10),
        "quiet_over_60_min": sum(1 for r in rows if r.get("last_trade_min_ago", 0) > 60),
        "median_last_trade_min_ago": statistics.median([r["last_trade_min_ago"] for r in rows if "last_trade_min_ago" in r]) if rows else None,
        "births_seen": len(born),
        "birth_ages_h": sorted(born),
        "full_1000_oldest_h_ago": sorted(r["oldest_seen_h_ago"] for r in rows if r.get("birth_seen") is False),
    })
    (HERE / "results.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res["summary"], indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
