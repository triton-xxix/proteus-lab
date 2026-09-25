#!/usr/bin/env python3
"""The Grinder's price paths: minute candles per position, the v0.2 fill rule and cost model.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/grinder/paths.py

Run alone, it refreshes grinder/PATHS.csv for every ledger row (both rule versions) and prints the
nightly-versus-path comparison. paper.py imports it for v0.2 exits. Rules: grinder/RULES.md, v0.2.
Candles are GeckoTerminal's keyless minute OHLCV, saved under grinder/candles/<id>.csv; once a
position is closed its saved file is the record and is never fetched again.
"""
import csv
import math
import os
import time
from datetime import datetime, timezone, timedelta

import requests

ROOT = "/Users/triton/PROTEUS/"
LEDGER = ROOT + "grinder/LEDGER.csv"
SNAPS = ROOT + "grinder/SNAPSHOTS.csv"
PATHS = ROOT + "grinder/PATHS.csv"
CANDLES = ROOT + "grinder/candles/"
GT = "https://api.geckoterminal.com/api/v2/networks/solana/pools/"
UA = {"User-Agent": "proteus-lab/0.2", "Accept": "application/json"}

# v0.2 exits and costs (RULES.md). Exit levels are unchanged from v0.1.
TAKE_PROFIT, STOP_LOSS, RUG_DROP, TIME_STOP_H = 1.00, -0.50, -0.90, 24.0
POOL_FEE, NET_FEE_USD, GBPUSD = 0.01, 0.05, 1.30
SLIP = {"stop_loss": 0.03, "rug": 0.03, "take_profit": 0.01, "time_stop": 0.01}
# v0.1's own fee model, kept so v0.1 rows can be rescored on their own terms.
V01_FEE_PCT, V01_FLAT_USD = 0.01, 1.5

FIELDS = ["id", "rule_version", "token", "pool", "dex", "entered_at", "window_end", "status", "candles",
          "high", "high_at", "runup_pct", "low", "low_at", "drawdown_pct",
          "path_exit_at", "path_exit_price", "path_exit_reason", "path_move_pct", "gap_to_high_pts",
          "ledger_exit_at", "ledger_exit_price", "ledger_exit_reason", "ledger_move_pct",
          "ledger_pnl_gbp", "path_pnl_same_costs_gbp", "path_pnl_v02_costs_gbp", "path_pnl_v02_pct_stake"]


def parse(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def iso(ts):
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fnum(x):
    try:
        return float(x)
    except Exception:
        return None


def pool_for(mint, entered_at):
    """The pool, dex and liquidity the scan saw for this mint, at or before entry."""
    best = None
    for s in csv.DictReader(open(SNAPS)):
        if s["mint"] == mint and s["ts"] <= entered_at and (best is None or s["ts"] > best["ts"]):
            best = s
    return (best["pair"], best["dex"], fnum(best["liq_usd"])) if best else (None, None, None)


def min_liq_between(mint, t0, t1):
    """Lowest liquidity any snapshot observed for the mint strictly after entry and at or before t1."""
    vals = [fnum(s["liq_usd"]) for s in csv.DictReader(open(SNAPS)) if s["mint"] == mint and t0 < s["ts"] <= t1]
    vals = [v for v in vals if v]
    return min(vals) if vals else None


def fetch(pool, start, end):
    """Minute candles [ts, o, h, l, c, v] with start <= ts < end, oldest first. None if the pool is gone."""
    out, before, calls = {}, int(end), 0
    while True:
        r = requests.get(GT + pool + "/ohlcv/minute", params={"aggregate": 1, "limit": 1000, "currency": "usd", "token": "base",
                         "before_timestamp": before}, headers=UA, timeout=30)
        calls += 1
        if r.status_code == 404:
            return None
        if r.status_code == 429:
            time.sleep(20); continue
        r.raise_for_status()
        rows = r.json()["data"]["attributes"]["ohlcv_list"]
        for x in rows:
            if start <= x[0] < end:
                out[int(x[0])] = [int(x[0])] + [float(v) for v in x[1:6]]
        time.sleep(2.1)  # about 30 calls a minute keyless
        if not rows or min(x[0] for x in rows) <= start or calls >= 6:
            break
        before = int(min(x[0] for x in rows))
    return [out[k] for k in sorted(out)]


def load_saved(pid):
    p = CANDLES + pid + ".csv"
    if not os.path.exists(p):
        return None
    return [[int(r["ts"]), float(r["o"]), float(r["h"]), float(r["l"]), float(r["c"]), float(r["v"])] for r in csv.DictReader(open(p))]


def save(pid, candles):
    os.makedirs(CANDLES, exist_ok=True)
    with open(CANDLES + pid + ".csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["ts", "o", "h", "l", "c", "v"])
        w.writerows(candles)


def candles_for(row, pool, frozen):
    """Saved candles if the position is closed and saved; otherwise fetch the window and save."""
    pid = row["id"]
    if frozen:
        saved = load_saved(pid)
        if saved is not None:
            return saved
    t0 = parse(row["entered_at"]).timestamp()
    start = (int(t0) // 60 + 1) * 60                # first full minute after entry
    end = min(t0 + TIME_STOP_H * 3600, time.time())
    c = fetch(pool, start, end)
    if c is not None:
        save(pid, c)
    return c


def walk(candles, entry, t_entry, now_ts):
    """v0.2 fill rule. Returns (exit_ts, fill_price, reason) or None while still open."""
    stop, tp = entry * (1 + STOP_LOSS), entry * (1 + TAKE_PROFIT)
    horizon = t_entry + TIME_STOP_H * 3600
    for ts, o, h, l, c, v in candles:
        if ts >= horizon:
            break
        if l <= stop:                                   # stop first if both inside one candle
            if l <= entry * (1 + RUG_DROP):             # rug inside the trigger minute: the close, not the level (tightened 25 Sep, G-0005)
                return ts, min(c, o if o <= stop else stop), "rug"
            fill = o if o <= stop else stop
            return ts, fill, "rug" if fill <= entry * (1 + RUG_DROP) else "stop_loss"
        if h >= tp:
            return ts, (o if o >= tp else tp), "take_profit"
    if now_ts >= horizon:
        last = [x for x in candles if x[0] < horizon]
        if last:
            return last[-1][0], last[-1][4], "time_stop"
        return horizon, entry, "time_stop"             # no trade at all in 24h: flat, flagged by candles=0
    return None


def pnl_v02(entry, fill, reason, stake_gbp, entry_liq, later_liq=None):
    """Paper P&L in GBP under the v0.2 cost model: 1% pool fee and $0.05 per side, constant-product
    impact from the pool's depth, execution slippage on the exit fill."""
    usd = stake_gbp * GBPUSD
    q0 = (entry_liq or 1e12) / 2
    spend = usd - NET_FEE_USD
    tokens = spend * (1 - POOL_FEE) / (entry * (1 + spend / q0))
    px = fill * (1 - SLIP.get(reason.replace("_nightly", ""), 0.03))
    q1 = q0 * math.sqrt(max(fill, 1e-18) / entry)
    if later_liq:
        q1 = min(q1, later_liq / 2)
    value = tokens * px
    recv = value / (1 + value / q1) * (1 - POOL_FEE) - NET_FEE_USD
    return round((recv - usd) / GBPUSD, 2)


def pnl_v01(entry, exit_, stake_gbp):
    """v0.1's fee model exactly as paper.py applied it (1% each way, $1.50 flat per side)."""
    usd = stake_gbp * GBPUSD
    units = usd * (1 - V01_FEE_PCT) / entry
    return round((units * exit_ * (1 - V01_FEE_PCT) - V01_FLAT_USD * 2 - usd) / GBPUSD, 2)


def evaluate(row, now_ts=None):
    """Everything PATHS.csv records for one ledger row, plus the path exit if one has happened."""
    now_ts = now_ts or time.time()
    entry = fnum(row["entry_price_usd"]); t_entry = parse(row["entered_at"]).timestamp()
    pool, dex, snap_liq = pool_for(row["mint"], row["entered_at"])
    out = {"id": row["id"], "rule_version": row.get("rule_version"), "token": row.get("token"), "pool": pool, "dex": dex,
           "entered_at": row["entered_at"], "window_end": iso(t_entry + TIME_STOP_H * 3600)}
    frozen = bool(row.get("exit_at")) and os.path.exists(CANDLES + row["id"] + ".csv")
    c = candles_for(row, pool, frozen) if pool else None
    if c is None:
        out["status"] = "no-candles"
        return out, None
    out["candles"] = len(c)
    win = [x for x in c if x[0] < t_entry + TIME_STOP_H * 3600]
    if win:
        hi = max(win, key=lambda x: x[2]); lo = min(win, key=lambda x: x[3])
        out.update({"high": hi[2], "high_at": iso(hi[0]), "runup_pct": round(100 * (hi[2] / entry - 1), 1),
                    "low": lo[3], "low_at": iso(lo[0]), "drawdown_pct": round(100 * (lo[3] / entry - 1), 1)})
    ex = walk(c, entry, t_entry, now_ts)
    stake = fnum(row.get("size_gbp")) or 5.0
    entry_liq = fnum(row.get("entry_liq_usd")) or snap_liq
    if ex:
        ts, fill, reason = ex
        later = min_liq_between(row["mint"], row["entered_at"], iso(ts))
        move = 100 * (fill / entry - 1)
        v02 = pnl_v02(entry, fill, reason, 100.0, entry_liq, later)
        out.update({"status": "path-closed", "path_exit_at": iso(ts), "path_exit_price": fill, "path_exit_reason": reason,
                    "path_move_pct": round(move, 1),
                    "gap_to_high_pts": round(out["runup_pct"] - move, 1) if "runup_pct" in out else "",
                    "path_pnl_same_costs_gbp": pnl_v01(entry, fill, stake) if row.get("rule_version") == "v0.1" else pnl_v02(entry, fill, reason, stake, entry_liq, later),
                    "path_pnl_v02_costs_gbp": v02, "path_pnl_v02_pct_stake": round(v02, 1)})
    else:
        out["status"] = "path-open"
    if row.get("exit_at"):
        lx = fnum(row.get("exit_price_usd"))
        out.update({"ledger_exit_at": row["exit_at"], "ledger_exit_price": lx, "ledger_exit_reason": row.get("exit_reason"),
                    "ledger_move_pct": round(100 * (lx / entry - 1), 1) if lx else "", "ledger_pnl_gbp": row.get("pnl_gbp")})
    return out, ex


def write_paths(ledger, now_ts=None):
    rows = []
    for r in ledger:
        try:
            rec, _ = evaluate(r, now_ts)
        except Exception as e:
            rec = {"id": r["id"], "rule_version": r.get("rule_version"), "token": r.get("token"), "status": "error: %s" % str(e)[:60]}
        rows.append(rec)
    with open(PATHS, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        for rec in rows:
            w.writerow({k: rec.get(k, "") for k in FIELDS})
    return rows


if __name__ == "__main__":
    ledger = list(csv.DictReader(open(LEDGER)))
    for rec in write_paths(ledger):
        print("%s %-9s %-11s high %s at %s (%s%%), low %s at %s (%s%%) | path %s %s at %s -> £%s same costs, £%s at v0.2 £100 | ledger %s %s%% -> £%s" % (
            rec.get("id"), rec.get("token"), rec.get("status"), rec.get("high", ""), rec.get("high_at", ""), rec.get("runup_pct", ""),
            rec.get("low", ""), rec.get("low_at", ""), rec.get("drawdown_pct", ""), rec.get("path_exit_reason", "-"),
            rec.get("path_move_pct", ""), rec.get("path_exit_at", ""), rec.get("path_pnl_same_costs_gbp", ""),
            rec.get("path_pnl_v02_costs_gbp", ""), rec.get("ledger_exit_reason", "-"), rec.get("ledger_move_pct", ""), rec.get("ledger_pnl_gbp", "")))
