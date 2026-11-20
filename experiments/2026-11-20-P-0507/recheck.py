"""P-0507 re-read: wait until 12:58:00Z, then read the P-0491 cohort's newest signatures again.

    python3 recheck.py
"""
import calendar, json, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import burns  # noqa: E402

HERE = Path(__file__).resolve().parent
TARGET = calendar.timegm((2026, 11, 20, 12, 58, 0, 0, 0, 0))


def main():
    wait = TARGET - time.time()
    if wait > 0:
        time.sleep(min(wait, 900))
    if Path("/Users/triton/PROTEUS/HALT").exists():
        print("HALT")
        return 1
    first = json.loads((HERE / "results.json").read_text())
    rows = []
    for r in first["rows"]:
        if r["cohort"] != "P-0491" or r.get("newest_is_burn"):
            continue
        s = burns.rpc("getSignaturesForAddress", [r["mint"], {"limit": 3}]).get("result") or []
        row = {"mint": r["mint"], "birth": r["birth"]}
        if s:
            t = burns.rpc("getTransaction", [s[0]["signature"], {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}]).get("result")
            row["newest_blockTime"] = s[0].get("blockTime")
            row["newest_utc"] = time.strftime("%H:%M:%S", time.gmtime(s[0].get("blockTime") or 0))
            row["is_burn"] = bool(t) and burns.is_burn(t, r["mint"])
            row["age_h"] = round((s[0]["blockTime"] - r["birth"]) / 3600, 3)
        rows.append(row)
        print(json.dumps(row), flush=True)
        time.sleep(0.5)
    burned = [r for r in rows if r.get("is_burn")]
    times = sorted(r["newest_blockTime"] for r in burned)
    summary = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "mints": len(rows), "burned": len(burned),
               "first_burn_utc": time.strftime("%H:%M:%S", time.gmtime(times[0])) if times else None,
               "last_burn_utc": time.strftime("%H:%M:%S", time.gmtime(times[-1])) if times else None,
               "spread_s": times[-1] - times[0] if times else None,
               "ages_h": sorted(r["age_h"] for r in burned)}
    (HERE / "recheck.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1))
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
