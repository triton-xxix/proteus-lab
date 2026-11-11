#!/usr/bin/env python3
"""P-0404: how far was each R01 ledger entry price from the minute candles around the entry time?

For every row of grinder/LEDGER-R01.csv: the pool from grinder/PATHS.csv, the saved candles in
grinder/candles/<id>.csv (they start at the first full minute AFTER entry), and one keyless
GeckoTerminal fetch for the entry minute itself and the minutes just before it.
Reads only; writes results.json beside itself.
"""
import csv, json, os, statistics, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone

ROOT = "/Users/triton/PROTEUS/"
HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
GT = "https://api.geckoterminal.com/api/v2/networks/solana/pools/"
UA = {"User-Agent": "proteus-lab/0.2", "Accept": "application/json"}


def ts_of(s):
    return int(datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp())


def fetch(pool, before):
    url = GT + pool + "/ohlcv/minute?aggregate=1&limit=10&currency=usd&token=base&before_timestamp=%d" % before
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.load(r)["data"]["attributes"]["ohlcv_list"], None
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(20)
                continue
            return None, "http %d" % e.code
        except Exception as e:
            return None, type(e).__name__
    return None, "429 four times"


def pct(a, b):
    return round((a / b - 1) * 100, 3) if a and b else None


ledger = list(csv.DictReader(open(ROOT + "grinder/LEDGER-R01.csv")))
# The pool the scan saw for the mint at or before entry (same rule as grinder/paths.pool_for);
# R rows are not in PATHS.csv.
want = {r["mint"] for r in ledger}
snaps = {}
for s in csv.DictReader(open(ROOT + "grinder/SNAPSHOTS.csv")):
    if s["mint"] in want:
        snaps.setdefault(s["mint"], []).append(s)


def pool_for(mint, entered_at):
    best = None
    for s in snaps.get(mint, []):
        if s["ts"] <= entered_at and (best is None or s["ts"] > best["ts"]):
            best = s
    return best


rows, waits = [], 0
for led in ledger:
    pid, entry, t0 = led["id"], float(led["entry_price_usd"]), ts_of(led["entered_at"])
    minute = t0 // 60 * 60
    snap = pool_for(led["mint"], led["entered_at"])
    out = {"id": pid, "token": led["token"], "entered_at": led["entered_at"], "entry": entry,
           "sec_into_minute": t0 - minute, "pool": snap["pair"] if snap else None,
           "snapshot_ts": snap["ts"] if snap else None,
           "snapshot_price": snap.get("price_usd") if snap else None}
    saved = []
    p = ROOT + "grinder/candles/" + pid + ".csv"
    if os.path.exists(p):
        saved = [[int(r["ts"]), float(r["o"]), float(r["h"]), float(r["l"]), float(r["c"])] for r in csv.DictReader(open(p))]
    nxt = next((c for c in saved if c[0] > minute), None)
    if nxt:
        out["next_candle_lag_min"] = (nxt[0] - minute) // 60
        out["gap_next_open_pct"] = pct(entry, nxt[1])
        out["gap_next_close_pct"] = pct(entry, nxt[4])
    if out["pool"]:
        got, err = fetch(out["pool"], minute + 60)
        time.sleep(2.1)
        if got is None:
            out["fetch_error"] = err
        else:
            by = {int(x[0]): [float(v) for v in x[1:5]] for x in got}
            cur = by.get(minute)
            prev = max((k for k in by if k < minute), default=None)
            if cur:
                o, h, l, c = cur
                out["entry_minute"] = {"o": o, "h": h, "l": l, "c": c}
                out["gap_entry_close_pct"] = pct(entry, c)
                out["gap_entry_open_pct"] = pct(entry, o)
                out["inside_entry_candle"] = l <= entry <= h
                out["entry_candle_range_pct"] = pct(h, l)
            else:
                out["entry_minute"] = None
            if prev is not None:
                out["prev_candle_age_min"] = (minute - prev) // 60
                out["gap_prev_close_pct"] = pct(entry, by[prev][3])
    else:
        out["fetch_error"] = "no pool in PATHS.csv"
    rows.append(out)
    print(pid, out.get("gap_entry_close_pct"), out.get("gap_prev_close_pct"), out.get("gap_next_open_pct"),
          out.get("inside_entry_candle"), out.get("fetch_error", ""), flush=True)


def summary(key):
    v = [abs(r[key]) for r in rows if r.get(key) is not None]
    if not v:
        return {"n": 0}
    signed = [r[key] for r in rows if r.get(key) is not None]
    return {"n": len(v), "median_abs_pct": round(statistics.median(v), 3), "max_abs_pct": round(max(v), 3),
            "beyond_5pct": sum(1 for x in v if x > 5), "beyond_1pct": sum(1 for x in v if x > 1),
            "median_signed_pct": round(statistics.median(signed), 3),
            "entry_above": sum(1 for x in signed if x > 0), "entry_below": sum(1 for x in signed if x < 0)}


res = {"probe": "P-0404", "run_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "entries": len(rows),
       "entry_minute_candle_found": sum(1 for r in rows if r.get("entry_minute")),
       "inside_entry_candle": sum(1 for r in rows if r.get("inside_entry_candle")),
       "fetch_errors": sum(1 for r in rows if r.get("fetch_error")),
       "v_entry_minute_close": summary("gap_entry_close_pct"),
       "v_prev_candle_close": summary("gap_prev_close_pct"),
       "v_next_candle_open": summary("gap_next_open_pct"),
       "v_next_candle_close": summary("gap_next_close_pct"),
       "rows": rows}
json.dump(res, open(HERE + "results.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1))
