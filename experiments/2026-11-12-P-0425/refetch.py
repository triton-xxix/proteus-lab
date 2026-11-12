"""P-0425: fetch the minute candles P-0419 found missing for the three voided Grinder trades, and
walk each under v0.2 from the stale entry price and from the live one.

Uses grinder/paths.py's own pool lookup, fetch, walk and cost model (imported, not edited). Candles are
saved in this folder, never in grinder/candles/. The ledger and VOIDED.csv are read only.

Usage: .venv/bin/python3 refetch.py
"""
import csv
import json
import os
import sys
import time

sys.path.insert(0, "/Users/triton/PROTEUS/grinder")
import paths  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
STAKE = 100.0
out = {"rows": []}
now = time.time()
for r in csv.DictReader(open("/Users/triton/PROTEUS/grinder/VOIDED.csv")):
    pid, entry = r["id"], float(r["entry_price_usd"])
    t0 = paths.parse(r["entered_at"]).timestamp()
    pool, dex, liq = paths.pool_for(r["mint"], r["entered_at"])
    row = {"id": pid, "token": r["token"], "pool": pool, "dex": dex, "stale_entry": entry,
           "entry_liq_usd": float(r["entry_liq_usd"])}
    if not pool:
        row["status"] = "no pool in SNAPSHOTS.csv"
        out["rows"].append(row)
        continue
    start = (int(t0) // 60 + 1) * 60
    try:
        c = paths.fetch(pool, start - 600, t0 + paths.TIME_STOP_H * 3600)
    except Exception as e:  # a refusal is a result
        row["status"] = "fetch failed: %s: %s" % (type(e).__name__, str(e)[:160])
        out["rows"].append(row)
        continue
    if c is None:
        row["status"] = "pool gone (404)"
        out["rows"].append(row)
        continue
    with open(os.path.join(HERE, pid + ".csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["ts", "o", "h", "l", "c", "v"])
        w.writerows(c)
    after = [x for x in c if x[0] >= start]
    row["candles"], row["candles_after_entry"] = len(c), len(after)
    if not after:
        row["status"] = "served, but no candle after entry"
        out["rows"].append(row)
        continue
    live = after[0][1]
    row["first_candle_at"], row["live_entry"] = paths.iso(after[0][0]), live
    row["stale_over_live_pct"] = round((entry / live - 1) * 100, 2)
    row["high_pct_of_live"] = round((max(x[2] for x in after) / live - 1) * 100, 1)
    row["low_pct_of_live"] = round((min(x[3] for x in after) / live - 1) * 100, 1)
    for label, px in (("stale", entry), ("live", live)):
        res = paths.walk(after, px, t0, now)
        ts, fill, reason = res
        row[label] = {"exit_at": paths.iso(ts), "exit_price": fill, "reason": reason,
                      "move_pct": round((fill / px - 1) * 100, 2),
                      "hours_held": round((ts - t0) / 3600, 2),
                      "pnl_gbp": paths.pnl_v02(px, fill, reason, STAKE, row["entry_liq_usd"])}
    row["status"] = "walked"
    out["rows"].append(row)
walked = [r for r in out["rows"] if r["status"] == "walked"]
out["walked"] = len(walked)
out["total_stale_gbp"] = round(sum(r["stale"]["pnl_gbp"] for r in walked), 2)
out["total_live_gbp"] = round(sum(r["live"]["pnl_gbp"] for r in walked), 2)
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
for r in out["rows"]:
    print(json.dumps(r))
print("walked", out["walked"], "stale total", out["total_stale_gbp"], "live total", out["total_live_gbp"])
