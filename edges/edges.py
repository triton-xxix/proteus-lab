#!/usr/bin/env python3
"""The edge desk. Rules in RULES.md, one row an edge in REGISTER.csv.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/edges/edges.py status
    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/edges/edges.py score      # E-001/E-002 detections -> paper trades
    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/edges/edges.py admit E-001 # read E-001/admission.json against the admission rule
    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/edges/edges.py kill E-001  # the kill-line reading on forward trades

E-001 (delisting fade, short) and E-002 (delisting bounce, long) share one event stream, the
watcher's detections.jsonl, and one fill: entry at the open of the 1-minute perp bar at detection
plus 5 minutes, exit at the close of the bar 24 hours later (forced at the last bar before the perp
settles). Venue: Binance USDT-M if the perp is live at detection, else Bybit linear, else the event
is skipped. Costs: taker 0.05% a side, slippage 0.10% a side, funding over the hold. Each scored
event is one row in E-001/trades.jsonl (append-only, latest row per id wins) carrying both sides'
net. A row is "shadow" while the edge's register status is candidate; only rows scored while the
status is forward count towards the kill line. Keyless, stdlib only.
"""
import csv
import json
import os
import statistics
import sys
import time
import urllib.request
from datetime import datetime, timezone

EDGES = os.path.dirname(os.path.abspath(__file__))
REGISTER = os.path.join(EDGES, "REGISTER.csv")
E001 = os.path.join(EDGES, "E-001")
TRADES = os.path.join(E001, "trades.jsonl")
UA = {"User-Agent": "proteus-edges"}
MIN, H = 60_000, 3_600_000
DELAY_MIN, HOLD_H = 5, 24
FEE, SLIP = 0.0005, 0.0010
ROUND_TRIP = 2 * (FEE + SLIP)
# Kill line for E-001 and E-002, fixed 19 Oct 2026 before any forward trade (see RULES.md and E-001/REPORT.md).
KILL_LAST_N, KILL_CONSEC, KILL_SINGLE = 6, 4, -0.50
RETIRE_DAYS, RETIRE_MIN_TRADES = 60, 3


def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
            return json.load(r)
    except Exception as e:
        return {"__error": str(e)[:120]}


def register():
    with open(REGISTER, newline="") as fh:
        return list(csv.DictReader(fh))


def jl_read(path):
    if not os.path.exists(path):
        return []
    with open(path) as fh:
        return [json.loads(line) for line in fh if line.strip()]


def jl_append(path, row):
    with open(path, "a") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")


def utc(ms):
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


# ---------- fills ----------

def binance_bar(sym, t):
    d = get("https://fapi.binance.com/fapi/v1/klines?symbol=%s&interval=1m&startTime=%d&limit=1" % (sym, t))
    if isinstance(d, list) and d and d[0][0] == t:
        return {"open": float(d[0][1]), "close": float(d[0][4]), "volume": float(d[0][7])}
    return None


def binance_last_bar_before(sym, t_end):
    d = get("https://fapi.binance.com/fapi/v1/klines?symbol=%s&interval=1m&endTime=%d&limit=1" % (sym, t_end - 1))
    if isinstance(d, list) and d:
        return d[0][0], {"open": float(d[0][1]), "close": float(d[0][4])}
    return None, None


def binance_funding(sym, a, b):
    d = get("https://fapi.binance.com/fapi/v1/fundingRate?symbol=%s&startTime=%d&endTime=%d&limit=100" % (sym, a, b))
    return sum(float(r["fundingRate"]) for r in d if a < r["fundingTime"] <= b) if isinstance(d, list) else None


def bybit_bar(sym, t):
    d = get("https://api.bybit.com/v5/market/kline?category=linear&symbol=%s&interval=1&start=%d&limit=1" % (sym, t))
    lst = ((d.get("result") or {}).get("list") or []) if isinstance(d, dict) else []
    if lst and int(lst[0][0]) == t:
        return {"open": float(lst[0][1]), "close": float(lst[0][4]), "volume": float(lst[0][6])}
    return None


def bybit_funding(sym, a, b):
    d = get("https://api.bybit.com/v5/market/funding/history?category=linear&symbol=%s&startTime=%d&endTime=%d&limit=200" % (sym, a, b))
    lst = ((d.get("result") or {}).get("list") or []) if isinstance(d, dict) else None
    return sum(float(r["fundingRate"]) for r in lst if a < int(r["fundingRateTimestamp"]) <= b) if lst is not None else None


def venue_for(ticker, detected_ms, perps):
    s = perps.get(ticker + "USDT")
    if s and s["onboardDate"] <= detected_ms < s["deliveryDate"]:
        return "binance_usdtm", s["deliveryDate"]
    return None, None


def score():
    """Turn detections into paper trades for E-001 (short) and E-002 (long)."""
    statuses = {r["id"]: r["status"] for r in register()}
    shadow = not (statuses.get("E-001") == "forward" or statuses.get("E-002") == "forward")
    rows = {r["id"]: r for r in jl_read(TRADES)}
    dets = [d for d in jl_read(os.path.join(E001, "detections.jsonl")) if d.get("event")]
    if not dets:
        print("score: no event detections yet")
        return
    info = get("https://fapi.binance.com/fapi/v1/exchangeInfo")
    perps = {s["symbol"]: s for s in info.get("symbols", [])}
    now = int(time.time() * 1000)
    done = 0
    for d in dets:
        t_det = d["detected_ms"]
        t_entry = (t_det // MIN + 1) * MIN + DELAY_MIN * MIN
        t_exit = t_entry + HOLD_H * H
        for tk in d["tickers"]:
            tid = "%s:%s" % (d["code"], tk)
            prev = rows.get(tid)
            if prev and prev["status"] in ("closed", "skipped"):
                continue
            venue, delivery = venue_for(tk, t_det, perps)
            sym = tk + "USDT"
            if venue is None:
                if bybit_bar(sym, t_entry) if now > t_entry + MIN else None:
                    venue = "bybit"
                elif now > t_entry + 2 * MIN:
                    jl_append(TRADES, {"id": tid, "ticker": tk, "kind": d["kind"], "code": d["code"], "detected_ms": t_det, "status": "skipped",
                                       "why": "no live perp on Binance USDT-M or Bybit at detection", "shadow": shadow, "scored_at": utc(now)})
                    done += 1
                    continue
                else:
                    continue
            if now < t_entry + MIN:
                continue
            bar = binance_bar(sym, t_entry) if venue == "binance_usdtm" else bybit_bar(sym, t_entry)
            if not bar:
                if now > t_entry + 10 * MIN:
                    jl_append(TRADES, {"id": tid, "ticker": tk, "kind": d["kind"], "code": d["code"], "detected_ms": t_det, "status": "skipped",
                                       "why": "no %s 1m bar at entry %s" % (venue, utc(t_entry)), "shadow": shadow, "scored_at": utc(now)})
                    done += 1
                continue
            row = {"id": tid, "ticker": tk, "kind": d["kind"], "code": d["code"], "detected_ms": t_det, "venue": venue, "shadow": shadow,
                   "t_entry": t_entry, "entry_px": bar["open"], "status": "open", "scored_at": utc(now)}
            forced = False
            x_t = t_exit
            if delivery and t_exit >= delivery:
                x_t, forced = None, True
            if now >= t_exit + MIN or forced:
                if forced:
                    if now < delivery:
                        jl_append(TRADES, row)
                        continue
                    x_t, xbar = binance_last_bar_before(sym, delivery)
                else:
                    xbar = binance_bar(sym, x_t) if venue == "binance_usdtm" else bybit_bar(sym, x_t)
                if xbar:
                    f = binance_funding(sym, t_entry, x_t) if venue == "binance_usdtm" else bybit_funding(sym, t_entry, x_t)
                    f = f or 0.0
                    gross_short = (row["entry_px"] - xbar["close"]) / row["entry_px"]
                    row.update({"status": "closed", "t_exit": x_t, "exit_px": xbar["close"], "forced": forced, "funding": round(f, 5),
                                "short_gross": round(gross_short, 5), "short_net": round(max(gross_short + f - ROUND_TRIP, -1.0), 5),
                                "long_net": round(-gross_short - f - ROUND_TRIP, 5)})
            jl_append(TRADES, row)
            done += 1
    print("score: %d detections, %d rows written, shadow=%s" % (len(dets), done, shadow))


# ---------- readings ----------

def trades(side="short_net", shadow=None):
    rows = {r["id"]: r for r in jl_read(TRADES)}
    out = [r for r in rows.values() if r["status"] == "closed" and (shadow is None or bool(r.get("shadow")) == shadow)]
    out.sort(key=lambda r: r["t_entry"])
    return [(r, r[side]) for r in out]


def kill_reading(edge):
    side = "short_net" if edge == "E-001" else "long_net"
    fwd = trades(side, shadow=False)
    nets = [v for _, v in fwd]
    if not nets:
        reg = {r["id"]: r for r in register()}.get(edge, {})
        if reg.get("status") == "forward" and reg.get("admitted"):
            days = (datetime.now(timezone.utc) - datetime.strptime(reg["admitted"], "%Y-%m-%d").replace(tzinfo=timezone.utc)).days
            if days >= RETIRE_DAYS:
                return "RETIRE: %d days forward, 0 trades (needs %d in %d)" % (days, RETIRE_MIN_TRADES, RETIRE_DAYS)
        return "RUNNING: 0 forward trades"
    last = nets[-KILL_LAST_N:]
    consec = 0
    for v in reversed(nets):
        if v <= 0:
            consec += 1
        else:
            break
    if min(nets) <= KILL_SINGLE:
        return "KILL: a single trade at %+.1f%% (line %+.0f%%)" % (min(nets) * 100, KILL_SINGLE * 100)
    if consec >= KILL_CONSEC:
        return "KILL: %d consecutive losses (line %d)" % (consec, KILL_CONSEC)
    if len(nets) >= KILL_LAST_N and statistics.mean(last) < 0:
        return "KILL: mean of last %d trades %+.2f%% (line below zero)" % (KILL_LAST_N, statistics.mean(last) * 100)
    return "RUNNING: %d forward trades, mean %+.2f%%, last %d mean %+.2f%%, %d losses running" % (
        len(nets), statistics.mean(nets) * 100, min(len(nets), KILL_LAST_N), statistics.mean(last) * 100, consec)


def side_summary(side):
    sh = [v for _, v in trades(side, shadow=True)]
    fw = [v for _, v in trades(side, shadow=False)]
    def s(x):
        return "n=%d mean %+.2f%% median %+.2f%% winners %d" % (len(x), statistics.mean(x) * 100, statistics.median(x) * 100, sum(1 for v in x if v > 0)) if x else "n=0"
    return "forward %s | shadow %s" % (s(fw), s(sh))


def admit(edge):
    """Read the admission file against the rule in RULES.md: most recent 8 tradable events, mean net
    above the random control's mean, permutation p below 0.10, at least 5 winners of 8."""
    if edge != "E-001":
        print("admit: only E-001 has an admission file so far")
        return
    p = os.path.join(E001, "admission.json")
    if not os.path.exists(p):
        print("admit: no admission.json; run E-001/admission.py")
        return
    a = json.load(open(p))
    rows = [r for r in a["rows"] if r["kind"] == "delist" and r["tradable"] and r["binance"].get("d5_h24")]
    rows.sort(key=lambda r: -r["release_ms"])
    last8 = rows[:8]
    nets = [r["binance"]["d5_h24"]["net"] for r in last8]
    ctl = [v for r in last8 for v in r["control"]["h24"]]
    winners = sum(1 for v in nets if v > 0)
    mean, cmean = statistics.mean(nets), statistics.mean(ctl)
    import random
    rng = random.Random(1)
    lists = [r["control"]["h24"] for r in last8]
    perm = sum(1 for _ in range(2000) if statistics.mean(rng.choice(l) for l in lists) >= mean) / 2000
    ok = mean > cmean and perm < 0.10 and winners >= 5
    print("admit %s (run %s): last 8 tradable delist tickers %s, back to %s" % (edge, a["run_utc"], [r["ticker"] for r in last8], last8[-1]["release_utc"]))
    print("  short +5min/24h net: mean %+.2f%% median %+.2f%% winners %d of %d | control mean %+.2f%% | perm p %.3f" % (
        mean * 100, statistics.median(nets) * 100, winners, len(nets), cmean * 100, perm))
    print("  ADMITTED" if ok else "  NOT ADMITTED (needs mean above control, p below 0.10, 5 winners of 8)")
    return ok


def status():
    print("Edge desk, %s" % datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%MZ"))
    for r in register():
        print("%s %-34s %-9s admitted=%s window=%s" % (r["id"], r["name"][:34], r["status"], r["admitted"] or "-", r["window"] or "-"))
        print("     admission: %s" % (r["admission"] or "-"))
        print("     kill line: %s" % (r["kill_line"] or "-"))
        if r["id"] in ("E-001", "E-002"):
            side = "short_net" if r["id"] == "E-001" else "long_net"
            print("     trades: %s" % side_summary(side))
            print("     kill reading: %s" % kill_reading(r["id"]))
        elif r["forward"]:
            print("     forward: %s" % r["forward"])
    sys.path.insert(0, E001)
    try:
        import watcher
        print("E-001 watcher:")
        watcher.status()
    except Exception as e:
        print("E-001 watcher status failed: %s" % e)
    skipped = [r for r in {r["id"]: r for r in jl_read(TRADES)}.values() if r["status"] == "skipped"]
    if skipped:
        print("skipped events: %d (%s)" % (len(skipped), ", ".join(r["ticker"] for r in skipped[-8:])))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "status":
        status()
    elif cmd == "score":
        score()
    elif cmd == "admit":
        admit(sys.argv[2] if len(sys.argv) > 2 else "E-001")
    elif cmd == "kill":
        print(kill_reading(sys.argv[2] if len(sys.argv) > 2 else "E-001"))
    else:
        print(__doc__)
