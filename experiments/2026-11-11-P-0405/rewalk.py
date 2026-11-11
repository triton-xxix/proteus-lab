#!/usr/bin/env python3
"""P-0405: entry-price noise on the main Grinder book (grinder/LEDGER.csv, G rows).

For every row with saved candles: the gap between the ledger entry price (the scan snapshot's
price) and the open of the first saved candle after entry, the snapshot's age at entry, and the
path re-walked with grinder/paths.walk from the candle price instead of the snapshot price.
Both walks are costed with paths.pnl_v02 at a 100 pound stake, so the two totals differ only by
the entry price. Reads only; no fetch; writes results.json beside itself.
"""
import csv, json, os, statistics, sys, time
from datetime import datetime, timezone

ROOT = "/Users/triton/PROTEUS/"
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
sys.path.insert(0, ROOT + "grinder")
try:
    import requests  # noqa: F401
except ModuleNotFoundError:
    # paths.py imports requests for its fetch; this script never fetches, so a stub is enough
    # under the system python3, which does not have it.
    import types
    sys.modules["requests"] = types.ModuleType("requests")
import paths  # noqa: E402

ledger = list(csv.DictReader(open(ROOT + "grinder/LEDGER.csv")))
want = {r["mint"] for r in ledger}
snaps = {}
for s in csv.DictReader(open(ROOT + "grinder/SNAPSHOTS.csv")):
    if s["mint"] in want:
        snaps.setdefault(s["mint"], []).append(s)


def snap_before(mint, entered_at):
    best = None
    for s in snaps.get(mint, []):
        if s["ts"] <= entered_at and (best is None or s["ts"] > best["ts"]):
            best = s
    return best


def min_liq(mint, t0, t1):
    v = [paths.fnum(s["liq_usd"]) for s in snaps.get(mint, []) if t0 < s["ts"] <= t1]
    v = [x for x in v if x]
    return min(v) if v else None


now = time.time()
rows, skipped = [], []
for r in ledger:
    c = paths.load_saved(r["id"])
    entry = paths.fnum(r["entry_price_usd"])
    if not c or not entry:
        skipped.append([r["id"], "no saved candles" if not c else "no entry price"])
        continue
    t0 = paths.parse(r["entered_at"]).timestamp()
    snap = snap_before(r["mint"], r["entered_at"])
    age = round((t0 - paths.parse(snap["ts"]).timestamp()) / 60, 1) if snap else None
    liq = paths.fnum(r.get("entry_liq_usd")) or (paths.fnum(snap["liq_usd"]) if snap else None)
    alt = c[0][1]
    out = {"id": r["id"], "rule_version": r["rule_version"], "token": r["token"], "entered_at": r["entered_at"],
           "snapshot_age_min": age, "snapshot_price_is_entry": bool(snap) and paths.fnum(snap["price_usd"]) == entry,
           "first_candle_lag_min": round((c[0][0] - t0) / 60, 1),
           "entry_ledger": entry, "entry_candle": alt, "gap_pct": round((entry / alt - 1) * 100, 3)}
    for tag, e in (("ledger", entry), ("candle", alt)):
        ex = paths.walk(c, e, t0, now)
        if ex:
            ts, fill, reason = ex
            out[tag + "_reason"] = reason
            out[tag + "_exit_at"] = paths.iso(ts)
            out[tag + "_pnl_100"] = paths.pnl_v02(e, fill, reason, 100.0, liq, min_liq(r["mint"], r["entered_at"], paths.iso(ts)))
        else:
            out[tag + "_reason"] = "open"
    out["flip"] = out["ledger_reason"] != out["candle_reason"]
    rows.append(out)


def med(v):
    return round(statistics.median(v), 3) if v else None


def band(sel):
    g = [abs(x["gap_pct"]) for x in sel]
    return {"n": len(g), "median_abs_gap_pct": med(g), "max_abs_gap_pct": round(max(g), 3) if g else None,
            "beyond_5pct": sum(1 for x in g if x > 5)}


both = [x for x in rows if "ledger_pnl_100" in x and "candle_pnl_100" in x]
tot_l = round(sum(x["ledger_pnl_100"] for x in both), 2)
tot_c = round(sum(x["candle_pnl_100"] for x in both), 2)
flips = [x for x in rows if x["flip"]]
res = {"probe": "P-0405", "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
       "ledger_rows": len(ledger), "rows_with_candles": len(rows), "skipped": skipped,
       "snapshot_price_is_entry": sum(1 for x in rows if x["snapshot_price_is_entry"]),
       "gap_all": band(rows),
       "entry_above_candle": sum(1 for x in rows if x["gap_pct"] > 0),
       "entry_below_candle": sum(1 for x in rows if x["gap_pct"] < 0),
       "median_signed_gap_pct": med([x["gap_pct"] for x in rows]),
       "snapshot_age_min": {"median": med([x["snapshot_age_min"] for x in rows if x["snapshot_age_min"] is not None]),
                            "max": max([x["snapshot_age_min"] for x in rows if x["snapshot_age_min"] is not None], default=None)},
       "gap_by_snapshot_age": {"under_6_min": band([x for x in rows if x["snapshot_age_min"] is not None and x["snapshot_age_min"] < 6]),
                               "6_to_15_min": band([x for x in rows if x["snapshot_age_min"] is not None and 6 <= x["snapshot_age_min"] < 15]),
                               "15_min_plus": band([x for x in rows if x["snapshot_age_min"] is not None and x["snapshot_age_min"] >= 15])},
       "rows_closed_both_ways": len(both),
       "total_pnl_100_stake_ledger_entry": tot_l, "total_pnl_100_stake_candle_entry": tot_c,
       "total_moves_by": round(tot_c - tot_l, 2),
       "mean_per_trade_ledger": round(tot_l / len(both), 2) if both else None,
       "mean_per_trade_candle": round(tot_c / len(both), 2) if both else None,
       "exit_reason_flips": len(flips),
       "flips": [[x["id"], x["gap_pct"], x["ledger_reason"], x["candle_reason"], x.get("ledger_pnl_100"), x.get("candle_pnl_100")] for x in flips],
       "reasons_ledger": {k: sum(1 for x in rows if x["ledger_reason"] == k) for k in sorted({x["ledger_reason"] for x in rows})},
       "reasons_candle": {k: sum(1 for x in rows if x["candle_reason"] == k) for k in sorted({x["candle_reason"] for x in rows})},
       "rows": rows}
json.dump(res, open(HERE + "results.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1))
