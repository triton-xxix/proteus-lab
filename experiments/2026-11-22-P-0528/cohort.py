"""P-0528: collect a fresh mayhem cohort and pre-register when it burns.

P-0491's alive.py method: the mayhem wallet's newest 1,000 signatures, 60 transactions spread across
them, the mints of the wallet's own token balances, then each mint's signatures (fewer than 1,000 back
means the oldest is the birth). Adds the absolute birth time and the forecast burn time under the
hourly-at-:04 hypothesis with a 24.25 h age cut (P-0508): the first HH:04 at or after birth + 24.25 h.

    python3 cohort.py

Keyless, read only, standard library.
"""
import calendar, json, statistics, sys, time
from pathlib import Path

sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-11-19-P-0491")
import alive  # noqa: E402

HERE = Path(__file__).resolve().parent
CUT_H = 24.25


def forecast(birth):
    due = birth + CUT_H * 3600
    g = time.gmtime(due)
    slot = calendar.timegm((g.tm_year, g.tm_mon, g.tm_mday, g.tm_hour, 4, 0, 0, 0, 0))
    if slot < due:
        slot += 3600
    return slot


def main():
    if alive.HALT.exists():
        print("HALT")
        return 1
    t0 = time.time()
    sigs = alive.rpc("getSignaturesForAddress", [alive.WALLET, {"limit": 1000}]).get("result") or []
    if not sigs:
        print("wallet signatures refused")
        return 1
    step = max(1, len(sigs) // 60)
    mints, fetched = {}, 0
    for s in sigs[::step][:60]:
        res = alive.rpc("getTransaction", [s["signature"], {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}], tries=3).get("result")
        if not res:
            continue
        fetched += 1
        meta = res.get("meta") or {}
        for b in (meta.get("postTokenBalances") or []) + (meta.get("preTokenBalances") or []):
            if b.get("owner") == alive.WALLET:
                mints[b["mint"]] = 1
        time.sleep(0.45)
    mints.pop("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", None)  # USDC, not a coin
    print(json.dumps({"fetched": fetched, "distinct_mints": len(mints)}), flush=True)
    rows = []
    for m in mints:
        page = alive.rpc("getSignaturesForAddress", [m, {"limit": 1000}]).get("result") or []
        page = [x for x in page if x.get("blockTime")]
        row = {"mint": m, "sigs": len(page), "birth_seen": 0 < len(page) < 1000}
        if row["birth_seen"]:
            b = page[-1]["blockTime"]
            f = forecast(b)
            row.update(birth=b, birth_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(b)),
                       age_min=round((time.time() - b) / 60, 2),
                       forecast_burn_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(f)))
        rows.append(row)
        print(json.dumps(row), flush=True)
        time.sleep(0.8)
    born = [r for r in rows if r["birth_seen"]]
    fc = {}
    for r in born:
        fc[r["forecast_burn_utc"]] = fc.get(r["forecast_burn_utc"], 0) + 1
    summary = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)), "fetched": fetched,
               "distinct_mints": len(rows), "births_known": len(born),
               "median_age_min": statistics.median(r["age_min"] for r in born) if born else None,
               "oldest_birth_utc": min(r["birth_utc"] for r in born) if born else None,
               "newest_birth_utc": max(r["birth_utc"] for r in born) if born else None,
               "forecast_burn_slots": fc,
               "hypothesis": "hourly sweep at about HH:04, age cut 24.25 h (P-0508)"}
    (HERE / "results.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1))
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
