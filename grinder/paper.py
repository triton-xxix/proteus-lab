#!/usr/bin/env python3
"""The Grinder: paper bankroll over the nightly snapshots. Rules v0.1 (see RULES.md).

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/grinder/paper.py --apply-rules
    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/grinder/paper.py --score

--apply-rules: close open positions that hit an exit rule (fresh price from DexScreener), then open
new positions from the latest snapshot that pass every entry rule. Appends to LEDGER.csv.
--score: fill score_24h and score_7d from later snapshots or a fresh price. No real money anywhere.
"""
import argparse
import csv
import os
import time
from datetime import datetime, timezone, timedelta

import requests

ROOT = "/Users/triton/PROTEUS/"
LEDGER = ROOT + "grinder/LEDGER.csv"
SNAPS = ROOT + "grinder/SNAPSHOTS.csv"
UA = {"User-Agent": "proteus-lab/0.1"}
FIELDS = ["id", "entered_at", "token", "mint", "entry_price_usd", "size_gbp", "rule_version", "entry_liq_usd",
          "exit_at", "exit_price_usd", "exit_reason", "pnl_gbp", "score_24h", "score_7d", "rugged"]

RULES = {
    "version": "v0.1",
    "bankroll_gbp": 100.0, "size_gbp": 5.0, "max_open": 4,
    "age_h_min": 1.0, "age_h_max": 48.0,
    "liq_usd_min": 20000, "vol_h24_min": 200000, "vol_h1_min": 10000,
    "top10_pct_max": 30.0, "holders_min": 300, "lp_locked_min": 90.0,
    "take_profit": 1.00, "stop_loss": -0.50, "time_stop_h": 24.0, "rug_drop": -0.90,
    "fee_pct": 0.01, "fee_flat_usd": 1.5, "gbpusd": 1.30,
}


def now():
    return datetime.now(timezone.utc)


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def fnum(x):
    try:
        return float(x)
    except Exception:
        return None


def load_ledger():
    if not os.path.exists(LEDGER):
        return []
    return list(csv.DictReader(open(LEDGER)))


def save_ledger(rows):
    with open(LEDGER, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})


def latest_snapshot():
    if not os.path.exists(SNAPS):
        return []
    rows = list(csv.DictReader(open(SNAPS)))
    if not rows:
        return []
    last_ts = max(r["ts"] for r in rows)
    return [r for r in rows if r["ts"] == last_ts]


def price_now(mint):
    try:
        r = requests.get("https://api.dexscreener.com/token-pairs/v1/solana/" + mint, headers=UA, timeout=25)
        pairs = [p for p in r.json() if (p.get("quoteToken") or {}).get("symbol") in ("SOL", "WSOL", "USDC", "USDT")]
        if not pairs:
            return None, None
        p = max(pairs, key=lambda x: ((x.get("liquidity") or {}).get("usd") or 0))
        return fnum(p.get("priceUsd")), fnum((p.get("liquidity") or {}).get("usd"))
    except Exception:
        return None, None


def pnl_gbp(entry, exit_, size_gbp):
    """Paper P&L in GBP after 1 percent each way and a flat fee. Optimistic for meme coins; stated in RULES."""
    usd = size_gbp * RULES["gbpusd"]
    units = usd * (1 - RULES["fee_pct"]) / entry
    out = units * exit_ * (1 - RULES["fee_pct"]) - RULES["fee_flat_usd"] * 2
    return round((out - usd) / RULES["gbpusd"], 2)


def passes(r):
    age = fnum(r.get("age_h")); liq = fnum(r.get("liq_usd")); v24 = fnum(r.get("vol_h24")); v1 = fnum(r.get("vol_h1"))
    top10 = fnum(r.get("top10_pct")); holders = fnum(r.get("holders")); lp = fnum(r.get("lp_locked_pct"))
    checks = [
        age is not None and RULES["age_h_min"] <= age <= RULES["age_h_max"],
        (r.get("mint_auth") or "") in ("", "None"),
        (r.get("freeze_auth") or "") in ("", "None"),
        liq is not None and liq >= RULES["liq_usd_min"],
        v24 is not None and v24 >= RULES["vol_h24_min"],
        v1 is not None and v1 >= RULES["vol_h1_min"],
        top10 is not None and top10 <= RULES["top10_pct_max"],
        holders is None or holders >= RULES["holders_min"],   # holder count missing = not held against it, noted
        lp is None or lp >= RULES["lp_locked_min"],
        fnum(r.get("price_usd")) not in (None, 0.0),
    ]
    return all(checks)


def apply_rules():
    ledger = load_ledger()
    open_rows = [r for r in ledger if not r.get("exit_at")]
    t = now()
    # exits
    for r in open_rows:
        entry = fnum(r["entry_price_usd"]); px, liq = price_now(r["mint"])
        if entry is None or px is None:
            continue
        change = px / entry - 1
        held_h = (t - parse(r["entered_at"])).total_seconds() / 3600
        reason = None
        entry_liq = fnum(r.get("entry_liq_usd"))
        if change <= RULES["rug_drop"] or (entry_liq and liq is not None and liq < 0.1 * entry_liq):
            reason = "rug"
        elif change >= RULES["take_profit"]:
            reason = "take_profit"
        elif change <= RULES["stop_loss"]:
            reason = "stop_loss"
        elif held_h >= RULES["time_stop_h"]:
            reason = "time_stop"
        if reason:
            r["exit_at"] = iso(t); r["exit_price_usd"] = px; r["exit_reason"] = reason
            r["pnl_gbp"] = pnl_gbp(entry, px, fnum(r["size_gbp"]))
            r["rugged"] = "1" if reason == "rug" else "0"
        time.sleep(0.3)
    # entries
    still_open = [r for r in ledger if not r.get("exit_at")]
    held = {r["mint"] for r in ledger}
    slots = RULES["max_open"] - len(still_open)
    realised = sum(fnum(r["pnl_gbp"]) or 0 for r in ledger if r.get("pnl_gbp"))
    bankroll = RULES["bankroll_gbp"] + realised - RULES["size_gbp"] * len(still_open)
    opened = 0
    if slots > 0 and bankroll >= RULES["size_gbp"]:
        cands = [s for s in latest_snapshot() if s["mint"] not in held and passes(s)]
        cands.sort(key=lambda s: -(fnum(s.get("vol_h1")) or 0))
        for s in cands[:slots]:
            ledger.append({
                "id": "G-%04d" % (len(ledger) + 1), "entered_at": iso(t), "token": s.get("symbol"), "mint": s["mint"],
                "entry_price_usd": s["price_usd"], "size_gbp": RULES["size_gbp"], "rule_version": RULES["version"],
                "entry_liq_usd": s.get("liq_usd"), "rugged": "",
            })
            opened += 1
    save_ledger(ledger)
    print("exits", sum(1 for r in open_rows if r.get("exit_at")), "entries", opened, "open", len([r for r in ledger if not r.get("exit_at")]))


def score():
    ledger = load_ledger()
    snaps = list(csv.DictReader(open(SNAPS))) if os.path.exists(SNAPS) else []
    by_mint = {}
    for s in snaps:
        by_mint.setdefault(s["mint"], []).append((parse(s["ts"]), fnum(s.get("price_usd"))))
    t = now()
    changed = 0
    for r in ledger:
        entry = fnum(r["entry_price_usd"]); e_at = parse(r["entered_at"])
        if entry is None:
            continue
        for col, hours in (("score_24h", 24), ("score_7d", 168)):
            if r.get(col):
                continue
            target = e_at + timedelta(hours=hours)
            if t < target:
                continue
            px = None
            hist = [(ts, p) for ts, p in by_mint.get(r["mint"], []) if p and ts >= target]
            if hist:
                px = min(hist, key=lambda x: x[0])[1]
            elif t - target < timedelta(hours=36):
                px, _ = price_now(r["mint"]); time.sleep(0.3)
            if px is not None:
                r[col] = round(100.0 * (px / entry - 1), 1); changed += 1
    save_ledger(ledger)
    print("scored", changed)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply-rules", action="store_true")
    ap.add_argument("--score", action="store_true")
    a = ap.parse_args()
    if a.apply_rules:
        apply_rules()
    if a.score:
        score()
    if not (a.apply_rules or a.score):
        ap.print_help()


if __name__ == "__main__":
    main()
