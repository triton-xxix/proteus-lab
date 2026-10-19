#!/usr/bin/env python3
"""E-001 admission test: the Binance delisting fade on the RECENT window, as a perp short.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/edges/E-001/admission.py [--since 2026-06-01]

Fixed before the run (19 Oct 2026):
  Notices   Binance CMS catalogue 161, pages 1 and 2. "Binance Will Delist A, B on DATE" and
            "Monitoring Tag to Include A, B". Stablecoins skipped. Release time = releaseDate.
  Venue     Binance USDT-M perp <TICKER>USDT where the perp was live at the notice (onboardDate before
            it, deliveryDate after it). Binance still serves 1-minute klines and funding for SETTLING
            (delisted) perps, which is what makes the recent window measurable. Bybit linear is the
            second venue where it has the pair; its fills and funding are recorded beside Binance's.
            No perp anywhere = the trade cannot be taken, recorded as skipped, never filled from spot.
  Trade     short. Entry = open of the 1-minute bar at release + delay (delay 5 and 15 minutes).
            Exit = close of the bar at entry + hold (24 h and 72 h). If the perp is delisted before
            the exit, the last served bar closes it (flag forced).
  Costs     taker 0.05% a side, slippage 0.10% a side (0.30% round trip), plus funding over the hold:
            a short receives positive funding and pays negative funding, summed over the settlements
            inside the hold. All in the net figure.
  Control   random-entry shorts on the same perp, same hold, same costs and funding, entries at
            5-minute bar opens in the 21 days before the notice (the hold ends before the notice,
            so the control never sees the event). 300 draws a ticker. Reported per ticker (where the
            event trade ranks among the draws) and pooled (2,000 permutations of one draw a ticker).
  Windows   last 21 days; the last 11 tickers (the four most recent notices); everything since --since.
Writes admission.json beside this file and prints the tables. Keyless.

Every summary number rests on Binance's klines and funding, which repeated exactly across three runs
on 19 Oct 2026. The Bybit rows are a cross-check (fills within 0.3%, funding in agreement on the
24-hour hold); the first reading of them as "inconsistent" that night was my own arithmetic (hand
curls aimed three days late), not the endpoint.
"""
import argparse
import json
import os
import random
import re
import statistics
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
CMS = "https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&catalogId=161&pageNo=%d&pageSize=50"
FAPI = "https://fapi.binance.com"
BYBIT = "https://api.bybit.com"
UA = {"User-Agent": "proteus-e001"}
STABLES = {"USDP", "TUSD", "FDUSD", "AEUR", "USDC", "BUSD", "DAI"}
DELAYS = (5, 15)        # minutes after release
HOLDS = (24, 72)        # hours
FEE = 0.0005            # taker, a side
SLIP = 0.0010           # a side
ROUND_TRIP = 2 * (FEE + SLIP)
CONTROL_DRAWS = 300
PERMS = 2000
MIN = 60_000
H = 3_600_000
D = 24 * H


def get(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (418, 429):
                time.sleep(5 * (i + 1))
                continue
            return {"__error": "HTTP %d" % e.code}
        except Exception as e:
            time.sleep(1)
            err = str(e)[:120]
    return {"__error": err if "err" in dir() else "failed"}


def notices(since_ms):
    out = []
    for page in (1, 2):
        d = get(CMS % page)
        arts = (((d.get("data") or {}).get("catalogs") or [{}])[0].get("articles")) or []
        for a in arts:
            t, ms = a["title"], a["releaseDate"]
            if ms < since_ms:
                continue
            m = re.match(r"Binance Will Delist (.+?) on \d{4}-\d\d-\d\d", t) or re.search(r"Monitoring Tag to Include (.+?) on \d{4}", t)
            if not m:
                continue
            kind = "monitoring" if "Monitoring" in t else "delist"
            for tk in re.split(r",|&| and ", m.group(1)):
                tk = tk.strip()
                if tk and tk.isupper() and tk not in STABLES:
                    out.append({"ticker": tk, "kind": kind, "release_ms": ms, "title": t, "code": a.get("code")})
        time.sleep(0.5)
    out.sort(key=lambda r: -r["release_ms"])
    return out


def binance_perps():
    d = get(FAPI + "/fapi/v1/exchangeInfo")
    return {s["symbol"]: s for s in d.get("symbols", [])}


def fapi_klines(sym, interval, start, end):
    """All bars with open time in [start, end), paged."""
    out, cur = [], start
    while cur < end:
        d = get(FAPI + "/fapi/v1/klines?symbol=%s&interval=%s&startTime=%d&endTime=%d&limit=1500" % (sym, interval, cur, end - 1))
        if not isinstance(d, list) or not d:
            break
        out.extend(d)
        nxt = d[-1][0] + 1
        if nxt <= cur:
            break
        cur = nxt
        time.sleep(0.12)
    return [(r[0], float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in out]


def fapi_funding(sym, start, end):
    d = get(FAPI + "/fapi/v1/fundingRate?symbol=%s&startTime=%d&endTime=%d&limit=1000" % (sym, start, end))
    return [(r["fundingTime"], float(r["fundingRate"])) for r in d] if isinstance(d, list) else []


def bybit_bar(sym, interval, t):
    d = get(BYBIT + "/v5/market/kline?category=linear&symbol=%s&interval=%s&start=%d&limit=1" % (sym, interval, t))
    lst = ((d.get("result") or {}).get("list") or []) if isinstance(d, dict) else []
    if not lst or int(lst[0][0]) != t:
        return None
    r = lst[0]
    return (int(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4]))


def bybit_funding(sym, start, end):
    d = get(BYBIT + "/v5/market/funding/history?category=linear&symbol=%s&startTime=%d&endTime=%d&limit=200" % (sym, start, end))
    lst = ((d.get("result") or {}).get("list") or []) if isinstance(d, dict) else []
    return [(int(r["fundingRateTimestamp"]), float(r["fundingRate"])) for r in lst]


def funding_sum(fund, t_in, t_out):
    return sum(r for t, r in fund if t_in < t <= t_out)


def short_trade(bars_by_t, last_t, fund, t_entry, hold_ms):
    """Net short return from a bar map keyed by open time. None if no entry bar.

    A 1x short with its whole stake as margin is liquidated near +100%, so the loss is capped at the
    stake (net -1.0, flag liquidated); the raw figure is kept beside it. Bars after the perp's
    delivery time are not real (Binance serves flat zero-volume bars after settlement, seen on VIC
    7 Aug 2026), so the caller passes last_t = the last bar before delivery and the exit is forced there.
    """
    e = bars_by_t.get(t_entry)
    if not e:
        return None
    t_exit = t_entry + hold_ms
    x = bars_by_t.get(t_exit)
    forced = False
    if not x or (last_t is not None and t_exit > last_t):
        if last_t is None or last_t <= t_entry:
            return None
        x, t_exit, forced = bars_by_t[last_t], last_t, True
    entry_px, exit_px = e[1], x[4]
    gross = (entry_px - exit_px) / entry_px
    f = funding_sum(fund, t_entry, t_exit)
    raw = gross + f - ROUND_TRIP
    out = {"entry_px": entry_px, "exit_px": exit_px, "t_entry": t_entry, "t_exit": t_exit, "forced": forced,
           "gross": round(gross, 5), "funding": round(f, 5), "net": round(max(raw, -1.0), 5)}
    if raw < -1.0:
        out["liquidated"] = True
        out["net_raw"] = round(raw, 5)
    return out


def control(bars5, fund, hold_ms, notice_ms, rng):
    """Random-entry shorts whose hold ends before the notice."""
    by_t = {b[0]: b for b in bars5}
    starts = [b[0] for b in bars5 if b[0] + hold_ms + 5 * MIN <= notice_ms and (b[0] + hold_ms) in by_t]
    if len(starts) < 50:
        return []
    out = []
    for t in rng.sample(starts, min(CONTROL_DRAWS, len(starts))):
        e, x = by_t[t], by_t[t + hold_ms]
        gross = (e[1] - x[4]) / e[1]
        out.append(round(gross + funding_sum(fund, t, t + hold_ms) - ROUND_TRIP, 5))
    return out


def pct_rank(v, dist):
    return round(sum(1 for d in dist if d < v) / len(dist), 3) if dist else None


def summarise(rows, label):
    """Pooled event v control for one window, every delay x hold."""
    out = {"label": label, "tickers": [r["ticker"] for r in rows], "n_tickers": len(rows),
           "n_tradable": sum(1 for r in rows if r["tradable"]), "skipped": [r["ticker"] for r in rows if not r["tradable"]],
           "reaches_back_to": min((r["release_utc"] for r in rows), default=None), "cells": {}}
    rng = random.Random(1)
    for dl in DELAYS:
        for hd in HOLDS:
            key = "d%d_h%d" % (dl, hd)
            ev = [r["binance"][key]["net"] for r in rows if r["tradable"] and r["binance"].get(key)]
            ctl_lists = [r["control"]["h%d" % hd] for r in rows if r["tradable"] and r["binance"].get(key) and r["control"].get("h%d" % hd)]
            cell = {"n": len(ev), "mean_net": round(statistics.mean(ev), 4) if ev else None,
                    "median_net": round(statistics.median(ev), 4) if ev else None,
                    "winners": sum(1 for v in ev if v > 0),
                    "forced_exits": sum(1 for r in rows if r["tradable"] and r["binance"].get(key) and r["binance"][key]["forced"])}
            if ctl_lists:
                allc = [v for lst in ctl_lists for v in lst]
                cell["control_mean"] = round(statistics.mean(allc), 4)
                cell["control_median"] = round(statistics.median(allc), 4)
                cell["control_win_share"] = round(sum(1 for v in allc if v > 0) / len(allc), 3)
                if ev and len(ctl_lists) == len(ev):
                    m = statistics.mean(ev)
                    hits = 0
                    for _ in range(PERMS):
                        if statistics.mean(rng.choice(lst) for lst in ctl_lists) >= m:
                            hits += 1
                    cell["perm_p_mean"] = round(hits / PERMS, 4)
                    cell["mean_edge_over_control"] = round(m - cell["control_mean"], 4)
            out["cells"][key] = cell
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="2026-06-01")
    a = ap.parse_args()
    since_ms = int(datetime.strptime(a.since, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000)
    now_ms = int(time.time() * 1000)
    rng = random.Random(7)
    perps = binance_perps()
    rows = []
    for n in notices(since_ms):
        t_rel = n["release_ms"]
        t0 = t_rel // MIN * MIN + (MIN if t_rel % MIN else 0)   # first full minute after release
        sym = n["ticker"] + "USDT"
        p = perps.get(sym)
        row = {**n, "release_utc": datetime.fromtimestamp(t_rel / 1000, timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
               "binance_perp": None, "bybit_perp": False, "tradable": False, "binance": {}, "bybit": {}, "control": {}}
        if p and p["onboardDate"] <= t_rel < p["deliveryDate"]:
            row["binance_perp"] = {"status": p["status"], "delivery_utc": datetime.fromtimestamp(p["deliveryDate"] / 1000, timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
                                   "hours_from_notice_to_perp_delisting": round((p["deliveryDate"] - t_rel) / H, 1)}
            row["tradable"] = True
            bars = fapi_klines(sym, "1m", t0, min(t0 + 15 * MIN + 73 * H, p["deliveryDate"]))
            by_t = {b[0]: b for b in bars}
            last_t = max(by_t) if by_t else None
            fund = fapi_funding(sym, t_rel - 22 * D, t_rel + 4 * D)
            row["funding_readings"] = len(fund)
            row["funding_first_72h"] = [(datetime.fromtimestamp(t / 1000, timezone.utc).strftime("%dT%H"), round(r * 100, 3)) for t, r in fund if t_rel < t <= t_rel + 72 * H]
            for dl in DELAYS:
                for hd in HOLDS:
                    tr = short_trade(by_t, last_t, fund, t0 + dl * MIN, hd * H)
                    if tr:
                        if t0 + dl * MIN + hd * H > now_ms:
                            tr["open"] = True   # the hold has not finished yet (EPIC 72 h on 17 Oct is fine; guard anyway)
                        row["binance"]["d%d_h%d" % (dl, hd)] = tr
            bars5 = fapi_klines(sym, "5m", t_rel - 21 * D, t_rel)
            for hd in HOLDS:
                row["control"]["h%d" % hd] = control(bars5, fund, hd * H, t_rel, rng)
            # Bybit beside it, where it has the pair
            if bybit_bar(sym, "1", t0 + 5 * MIN):
                row["bybit_perp"] = True
                bf = bybit_funding(sym, t_rel, t_rel + 4 * D)
                for dl in DELAYS:
                    for hd in HOLDS:
                        e = bybit_bar(sym, "1", t0 + dl * MIN)
                        x = bybit_bar(sym, "1", t0 + dl * MIN + hd * H)
                        if e and x:
                            gross = (e[1] - x[4]) / e[1]
                            f = funding_sum(bf, t0 + dl * MIN, t0 + dl * MIN + hd * H)
                            row["bybit"]["d%d_h%d" % (dl, hd)] = {"entry_px": e[1], "exit_px": x[4], "gross": round(gross, 5), "funding": round(f, 5),
                                                                   "funding_readings": len(bf), "net": round(max(gross + f - ROUND_TRIP, -1.0), 5)}
                        time.sleep(0.1)
        else:
            row["why_skipped"] = "no Binance perp live at the notice" + ("" if not p else " (perp delisted %s)" % datetime.fromtimestamp(p["deliveryDate"] / 1000, timezone.utc).strftime("%Y-%m-%d"))
            if bybit_bar(sym, "1", t0 + 5 * MIN):
                row["bybit_perp"] = True
                row["why_skipped"] += "; Bybit has it (recorded, not filled: one venue per rule, see RULES.md)"
        # rank of each event trade among its own control
        for key, tr in row["binance"].items():
            c = row["control"].get("h" + key.split("_h")[1]) or []
            tr["rank_in_control"] = pct_rank(tr["net"], c)
            if c:
                tr["control_mean"] = round(statistics.mean(c), 5)
        rows.append(row)
        b = row["binance"].get("d5_h24")
        print("%s %-6s %-10s perp=%s%s" % (row["release_utc"], row["ticker"], row["kind"], "yes" if row["tradable"] else "no",
              ("  d5_h24 net %+.2f%% (gross %+.2f%%, funding %+.2f%%, ctl mean %+.2f%%, rank %.2f)" % (b["net"] * 100, b["gross"] * 100, b["funding"] * 100, b.get("control_mean", 0) * 100, b.get("rank_in_control") or 0)) if b else ""), flush=True)
    delist = [r for r in rows if r["kind"] == "delist"]
    windows = [summarise([r for r in delist if r["release_ms"] >= now_ms - 21 * D], "last 21 days"),
               summarise(delist[:11], "last 11 tickers (4 notices)"),
               summarise(delist, "all delist tickers since %s" % a.since),
               summarise([r for r in rows if r["kind"] == "monitoring"], "monitoring tags since %s" % a.since)]
    for w in windows:
        print("\n== %s: %d tickers, %d tradable, back to %s, skipped %s" % (w["label"], w["n_tickers"], w["n_tradable"], w["reaches_back_to"], w["skipped"]))
        for key, c in w["cells"].items():
            print("  %-8s n=%d mean %s median %s winners %d forced %d | control mean %s median %s win %s | edge %s perm p %s" % (
                key, c["n"], c["mean_net"], c["median_net"], c["winners"], c["forced_exits"], c.get("control_mean"), c.get("control_median"),
                c.get("control_win_share"), c.get("mean_edge_over_control"), c.get("perm_p_mean")))
    json.dump({"run_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "since": a.since, "costs": {"fee_side": FEE, "slip_side": SLIP, "round_trip": ROUND_TRIP},
               "windows": windows, "rows": rows}, open(os.path.join(HERE, "admission.json"), "w"), indent=1)
    print("\nwrote", os.path.join(HERE, "admission.json"))


if __name__ == "__main__":
    main()
