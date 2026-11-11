#!/usr/bin/env python3
"""P-0419: the three voided Grinder trades, walked.

G-0075, G-0076 and G-0077 were entered on 12 Oct 2026 off the 11 Oct snapshot (24 hours stale) and
voided the next day, so they are in grinder/VOIDED.csv and P-0405 never walked them. Their candles are
saved. Same method as experiments/2026-11-11-P-0405/rewalk.py: grinder/paths.walk from the voided
entry price and from the first saved candle's open, costed with paths.pnl_v02 at 100 pounds.
Reads only; no fetch.
"""
import csv, json, os, sys, time

ROOT = "/Users/triton/PROTEUS/"
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
sys.path.insert(0, ROOT + "grinder")
try:
    import requests  # noqa: F401
except ModuleNotFoundError:
    import types
    sys.modules["requests"] = types.ModuleType("requests")
import paths  # noqa: E402

voided = list(csv.DictReader(open(ROOT + "grinder/VOIDED.csv")))
want = {r["mint"] for r in voided}
snaps = {}
for s in csv.DictReader(open(ROOT + "grinder/SNAPSHOTS.csv")):
    if s["mint"] in want:
        snaps.setdefault(s["mint"], []).append(s)


def min_liq(mint, t0, t1):
    v = [paths.fnum(s["liq_usd"]) for s in snaps.get(mint, []) if t0 < s["ts"] <= t1]
    v = [x for x in v if x]
    return min(v) if v else None


now, rows = time.time(), []
for r in voided:
    c = paths.load_saved(r["id"])
    entry = paths.fnum(r["entry_price_usd"])
    if not c or not entry:
        rows.append({"id": r["id"], "skipped": "no saved candles" if not c else "no entry price"})
        continue
    t0 = paths.parse(r["entered_at"]).timestamp()
    before = [s for s in snaps.get(r["mint"], []) if s["ts"] <= r["entered_at"]]
    snap = max(before, key=lambda s: s["ts"]) if before else None
    liq = paths.fnum(r.get("entry_liq_usd")) or (paths.fnum(snap["liq_usd"]) if snap else None)
    alt = c[0][1]
    out = {"id": r["id"], "token": r["token"], "entered_at": r["entered_at"], "candles": len(c),
           "snapshot_ts": snap["ts"] if snap else None,
           "snapshot_age_hours": round((t0 - paths.parse(snap["ts"]).timestamp()) / 3600, 1) if snap else None,
           "snapshot_price_is_entry": bool(snap) and paths.fnum(snap["price_usd"]) == entry,
           "first_candle_lag_min": round((c[0][0] - t0) / 60, 1),
           "entry_voided": entry, "entry_candle": alt, "gap_pct": round((entry / alt - 1) * 100, 3)}
    for tag, e in (("voided", entry), ("candle", alt)):
        ex = paths.walk(c, e, t0, now)
        if ex:
            ts, fill, reason = ex
            out[tag + "_reason"], out[tag + "_exit_at"] = reason, paths.iso(ts)
            out[tag + "_hours_held"] = round((ts - t0) / 3600, 1)
            out[tag + "_pnl_100"] = paths.pnl_v02(e, fill, reason, 100.0, liq, min_liq(r["mint"], r["entered_at"], paths.iso(ts)))
        else:
            out[tag + "_reason"] = "open"
    rows.append(out)

done = [x for x in rows if "voided_pnl_100" in x and "candle_pnl_100" in x]
res = {"probe": "P-0419", "rows": rows,
       "total_from_voided_price": round(sum(x["voided_pnl_100"] for x in done), 2),
       "total_from_candle_price": round(sum(x["candle_pnl_100"] for x in done), 2),
       "p0415_four_oldest_snapshot_rows": {"n": 4, "ledger_total": -256.80, "mean": -64.2}}
json.dump(res, open(HERE + "results.json", "w"), indent=1)
print(json.dumps(res, indent=1))
