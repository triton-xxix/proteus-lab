"""P-0508: re-read the 19 unburned P-0491 coins from P-0507's recheck.json, after waiting until
00:09:00Z on 21 Nov (past the 00:04Z sweep seen on 19 Nov), with P-0507's burns.py check.
For each mint: newest signatures (limit 5), whether the newest is a burn, its time and age.

    python3 reread.py
"""
import calendar, json, sys, time
from pathlib import Path

sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-11-20-P-0507")
import burns  # noqa: E402

HERE = Path(__file__).resolve().parent
SRC = Path("/Users/triton/PROTEUS/experiments/2026-11-20-P-0507/recheck.json")
TARGET = calendar.timegm((2026, 11, 21, 0, 9, 0, 0, 0, 0))


def main():
    wait = TARGET - time.time()
    if wait > 0:
        time.sleep(min(wait, 600))
    if Path("/Users/triton/PROTEUS/HALT").exists():
        print("HALT")
        return 1
    prev = json.loads(SRC.read_text())["rows"]
    rows = []
    for r in prev:
        s = burns.rpc("getSignaturesForAddress", [r["mint"], {"limit": 5}]).get("result") or []
        row = {"mint": r["mint"], "birth": r["birth"], "sigs_seen": len(s)}
        if s:
            t = burns.rpc("getTransaction", [s[0]["signature"], {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}]).get("result")
            bt = s[0].get("blockTime") or 0
            row["newest_blockTime"] = bt
            row["newest_utc"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(bt))
            row["is_burn"] = bool(t) and burns.is_burn(t, r["mint"])
            row["age_h"] = round((bt - r["birth"]) / 3600, 3)
            row["changed_since_1258"] = bt != r.get("newest_blockTime")
        rows.append(row)
        print(json.dumps(row), flush=True)
        time.sleep(0.5)
    burned = [r for r in rows if r.get("is_burn")]
    times = sorted(r["newest_blockTime"] for r in burned)
    summary = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "mints": len(rows), "burned": len(burned),
               "changed_since_1258": sum(1 for r in rows if r.get("changed_since_1258")),
               "first_burn_utc": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(times[0])) if times else None,
               "last_burn_utc": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(times[-1])) if times else None,
               "spread_s": times[-1] - times[0] if times else None,
               "ages_h": sorted(r["age_h"] for r in burned)}
    (HERE / "results.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1))
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
