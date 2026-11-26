"""P-0571, leg one: a fresh mayhem cohort, pre-registered against three age cuts.

P-0528's collection (P-0491's alive.py: the mayhem wallet's newest 1,000 signatures, 60 transactions
spread across them, the wallet's own token-balance mints, each mint's signatures; fewer than 1,000 back
means the oldest is the birth). For each dated mint: the first HH:04 at or after birth + cut, for cuts
24.25, 24.33 and 24.40 h. A mint is discriminating when those slots differ; its burn time in leg two
says which side of the cut it fell. Leg two reads burns with P-0545's sweep.py method.

Keyless, read only, standard library.

    python3 cohort.py
"""
import calendar, json, sys, time
from pathlib import Path

sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-11-19-P-0491")
import alive  # noqa: E402

HERE = Path(__file__).resolve().parent
CUTS = (24.25, 24.33, 24.40)


def slot(birth, cut_h):
    due = birth + cut_h * 3600
    g = time.gmtime(due)
    s = calendar.timegm((g.tm_year, g.tm_mon, g.tm_mday, g.tm_hour, 4, 0, 0, 0, 0))
    return s + 3600 if s < due else s


def utc(t):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))


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
    mints.pop("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", None)
    rows = []
    for m in mints:
        page = alive.rpc("getSignaturesForAddress", [m, {"limit": 1000}]).get("result") or []
        page = [x for x in page if x.get("blockTime")]
        row = {"mint": m, "sigs": len(page), "birth_seen": 0 < len(page) < 1000}
        if row["birth_seen"]:
            b = page[-1]["blockTime"]
            slots = {str(c): utc(slot(b, c)) for c in CUTS}
            row.update(birth=b, birth_utc=utc(b), age_h_now=round((time.time() - b) / 3600, 3),
                       slot_by_cut=slots, discriminating=len(set(slots.values())) > 1)
        rows.append(row)
        print(json.dumps(row), flush=True)
        time.sleep(0.8)
    born = [r for r in rows if r["birth_seen"]]
    disc = [r for r in born if r["discriminating"]]
    summary = {"at": utc(t0), "fetched": fetched, "distinct_mints": len(rows), "births_known": len(born),
               "discriminating": len(disc), "cuts_h": CUTS,
               "already_past_all_cuts": sum(1 for r in born if r["age_h_now"] > 24.40),
               "earliest_leg_two_utc": utc(max((slot(r["birth"], CUTS[-1]) for r in disc), default=t0) + 600),
               "rule": "leg two: a discriminating mint's burn within 3 min of one cut's slot names that cut; "
                       "the cut is the smallest candidate consistent with every discriminating burn"}
    name = "results-%s.json" % sys.argv[1] if len(sys.argv) > 1 else "results.json"
    (HERE / name).write_text(json.dumps({"summary": summary, "rows": rows}, indent=1))
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
