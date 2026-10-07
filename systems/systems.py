#!/usr/bin/env python3
"""The systems book: rule-based trading strategies paper-tracked forward. Rules and pass marks in
systems/RULES.md. Paper only.

    systems.py update     pull daily bars, log tonight's signals and last night's open fills
    systems.py score      closed trades, both fills, and the word against the pre-registered marks

Book 1 (7 Oct 2026, from P-0082 and P-0083): RSI(5) dip-buying inside an uptrend on nine broad stock
index ETFs. Book 2 (7 Oct 2026, from P-0085 and P-0091): IBS below 0.2, taken only while book 1 is
flat, same nine markets, first close 7 Oct. Keyless daily bars from Yahoo's chart endpoint, as
traded (not dividend-adjusted).

Append-only. SIGNALS.csv gets one row per market per trading day; EVENTS.csv gets one row per signal
or fill. Nothing already written is rewritten, so the commit history shows every signal was
logged before the next open.
"""
import csv
import json
import math
import statistics
import sys
import time
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

HERE = Path("/Users/triton/PROTEUS/systems")
SIGNALS = HERE / "SIGNALS.csv"
EVENTS = HERE / "EVENTS.csv"
BASKET = ["SPY", "QQQ", "DIA", "IWM", "EFA", "EEM", "EWU", "EWJ", "EWG"]
STRATEGIES = ["rsi5_simple", "rsi5_triple"]
BOOK_START = "2026-10-06"          # first close the book acts on
BOOK2 = "ibs_gated"
BOOK2_START = "2026-10-07"         # first close book 2 acts on (registered before it happened)
IBS_MAX = 0.2
SIGNALS2 = HERE / "SIGNALS_IBS.csv"
SIG2_FIELDS = ["date", "market", "high", "low", "close", "prev_high", "ibs", "rsi5_simple_after_close", "ibs_gated", "logged_utc"]
# Book 2's marks, pre-registered in RULES.md before its first close: next-open fills, net of a
# 0.05% round-trip cost, pooled. The edge is small per trade, so the marks need many trades.
B2_COST, B2_KILL_FROM, B2_LAST_AT = 0.0005, 200, 500
SIG_FIELDS = ["date", "market", "open", "close", "sma200", "rsi5", "rsi5_1", "rsi5_2", "rsi5_3",
              "rsi5_simple", "rsi5_triple", "logged_utc"]
EV_FIELDS = ["date", "market", "strategy", "event", "price", "logged_utc"]
# Pre-registered in RULES.md before the first trade. Primary: rsi5_simple, next-open fills, pooled.
KILL_FROM, KEEP_AT, LAST_AT, T_KEEP = 30, 60, 100, 1.65


def utcnow():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def bars(sym):
    """Daily bars, completed sessions only. Drops today's bar until 10 minutes after the close."""
    url = "https://query1.finance.yahoo.com/v8/finance/chart/%s?range=2y&interval=1d" % sym
    for attempt in range(3):
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30))
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(5 * (attempt + 1))
                continue
            raise
    r = d["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    off = r["meta"].get("gmtoffset", 0)
    reg = (r["meta"].get("currentTradingPeriod") or {}).get("regular") or {}
    out = []
    for i, ts in enumerate(r["timestamp"]):
        o, h, l, c = q["open"][i], q["high"][i], q["low"][i], q["close"][i]
        if o is None or c is None or h is None or l is None:
            continue
        out.append((datetime.fromtimestamp(ts + off, tz=timezone.utc).date().isoformat(), float(o), float(h), float(l), float(c), ts))
    if out and reg and out[-1][5] >= reg.get("start", 0) and time.time() < reg.get("end", 0) + 600:
        out.pop()
    return [b[:5] for b in out]


def rsi_wilder(cs, n=5):
    out = [None] * len(cs)
    if len(cs) <= n:
        return out
    g = sum(max(cs[i] - cs[i - 1], 0) for i in range(1, n + 1)) / n
    l = sum(max(cs[i - 1] - cs[i], 0) for i in range(1, n + 1)) / n
    out[n] = 100.0 if l == 0 else 100 - 100 / (1 + g / l)
    for i in range(n + 1, len(cs)):
        d = cs[i] - cs[i - 1]
        g = (g * (n - 1) + max(d, 0)) / n
        l = (l * (n - 1) + max(-d, 0)) / n
        out[i] = 100.0 if l == 0 else 100 - 100 / (1 + g / l)
    return out


def sma(cs, n=200):
    out = [None] * len(cs)
    s = 0.0
    for i, c in enumerate(cs):
        s += c
        if i >= n:
            s -= cs[i - n]
        if i >= n - 1:
            out[i] = s / n
    return out


def read(path):
    return list(csv.DictReader(open(path))) if path.exists() else []


def append(path, fields, rows):
    new = not path.exists()
    with open(path, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        if new:
            w.writeheader()
        for r in rows:
            w.writerow(r)


def state(events, market, strat):
    last = [e for e in events if e["market"] == market and e["strategy"] == strat]
    if not last:
        return "flat"
    return {"buy_signal": "pending_buy", "buy_open": "long", "sell_signal": "pending_sell", "sell_open": "flat"}[last[-1]["event"]]


def entry_ok(strat, c, m, r, r1, r2, r3):
    if None in (m, r, r1, r2, r3):
        return False
    ok = c > m and r < 30
    if strat == "rsi5_triple":
        ok = ok and r < r1 < r2 < r3 and r3 < 60
    return ok


def cmd_update():
    events = read(EVENTS)
    done, done2 = {}, {}
    for s in read(SIGNALS):
        done[s["market"]] = max(done.get(s["market"], ""), s["date"])
    for s in read(SIGNALS2):
        done2[s["market"]] = max(done2.get(s["market"], ""), s["date"])
    stamp = utcnow()
    for mkt in BASKET:
        try:
            bs = bars(mkt)
        except Exception as e:
            print(f"{mkt}: fetch failed ({type(e).__name__}); nothing logged")
            continue
        cs = [b[4] for b in bs]
        rs, ms = rsi_wilder(cs), sma(cs)
        new_sig, new_sig2, n_ev = [], [], 0
        fmt = lambda x: "" if x is None else "%.4f" % x
        for i, (d, o, h, l, c) in enumerate(bs):
            run1 = d >= BOOK_START and d > done.get(mkt, "")
            run2 = d >= BOOK2_START and d > done2.get(mkt, "") and i >= 1
            if not run1 and not run2:
                continue
            if not run1:
                n_ev += book2_day(events, mkt, d, o, h, l, c, bs[i - 1][2], stamp, new_sig2)
                continue
            states = {}
            for strat in STRATEGIES:
                st = state(events, mkt, strat)
                evs = []
                if st == "pending_buy":
                    evs.append({"event": "buy_open", "price": o})
                    st = "long"
                elif st == "pending_sell":
                    evs.append({"event": "sell_open", "price": o})
                    st = "flat"
                if st == "long" and rs[i] is not None and rs[i] > 50:
                    evs.append({"event": "sell_signal", "price": c})
                    st = "pending_sell"
                elif st == "flat" and i >= 3 and entry_ok(strat, c, ms[i], rs[i], rs[i - 1], rs[i - 2], rs[i - 3]):
                    evs.append({"event": "buy_signal", "price": c})
                    st = "pending_buy"
                for e in evs:
                    row = {"date": d, "market": mkt, "strategy": strat, "event": e["event"], "price": "%.4f" % e["price"], "logged_utc": stamp}
                    events.append(row)
                    append(EVENTS, EV_FIELDS, [row])
                    n_ev += 1
                states[strat] = st
            new_sig.append({"date": d, "market": mkt, "open": fmt(o), "close": fmt(c), "sma200": fmt(ms[i]), "rsi5": fmt(rs[i]),
                            "rsi5_1": fmt(rs[i - 1]), "rsi5_2": fmt(rs[i - 2]), "rsi5_3": fmt(rs[i - 3]),
                            "rsi5_simple": states["rsi5_simple"], "rsi5_triple": states["rsi5_triple"], "logged_utc": stamp})
            if run2:
                n_ev += book2_day(events, mkt, d, o, h, l, c, bs[i - 1][2], stamp, new_sig2)
        append(SIGNALS, SIG_FIELDS, new_sig)
        append(SIGNALS2, SIG2_FIELDS, new_sig2)
        last = new_sig[-1] if new_sig else None
        print(f"{mkt}: {len(new_sig)} new day(s), {n_ev} event(s)" +
              (f"; {last['date']} close {last['close']}, RSI(5) {last['rsi5']}, SMA200 {last['sma200']}, "
               f"simple {last['rsi5_simple']}, triple {last['rsi5_triple']}" if last else ""))
        time.sleep(0.5)


def book2_day(events, mkt, d, o, h, l, c, prev_h, stamp, sig_rows):
    """Book 2 for one session, after book 1 has made its decisions for that close."""
    st = state(events, mkt, BOOK2)
    evs = []
    if st == "pending_buy":
        evs.append({"event": "buy_open", "price": o})
        st = "long"
    elif st == "pending_sell":
        evs.append({"event": "sell_open", "price": o})
        st = "flat"
    ibs = (c - l) / (h - l) if h > l else None
    gate = state(events, mkt, "rsi5_simple")
    if st == "long" and c > prev_h:
        evs.append({"event": "sell_signal", "price": c})
        st = "pending_sell"
    elif st == "flat" and ibs is not None and ibs < IBS_MAX and gate == "flat":
        evs.append({"event": "buy_signal", "price": c})
        st = "pending_buy"
    for e in evs:
        row = {"date": d, "market": mkt, "strategy": BOOK2, "event": e["event"], "price": "%.4f" % e["price"], "logged_utc": stamp}
        events.append(row)
        append(EVENTS, EV_FIELDS, [row])
    sig_rows.append({"date": d, "market": mkt, "high": "%.4f" % h, "low": "%.4f" % l, "close": "%.4f" % c, "prev_high": "%.4f" % prev_h,
                     "ibs": "" if ibs is None else "%.4f" % ibs, "rsi5_simple_after_close": gate, "ibs_gated": st, "logged_utc": stamp})
    return len(evs)


def trades(events, strat, fill):
    """Closed trades as simple returns. fill 'close' pairs buy_signal/sell_signal prices,
    'next_open' pairs buy_open/sell_open."""
    buy_ev, sell_ev = ("buy_signal", "sell_signal") if fill == "close" else ("buy_open", "sell_open")
    out, openp = [], {}
    for e in events:
        if e["strategy"] != strat:
            continue
        if e["event"] == buy_ev:
            openp[e["market"]] = (e["date"], float(e["price"]))
        elif e["event"] == sell_ev and e["market"] in openp:
            d0, p0 = openp.pop(e["market"])
            out.append((e["market"], d0, e["date"], float(e["price"]) / p0 - 1))
    return out, openp


def summary(xs):
    n = len(xs)
    if n == 0:
        return n, float("nan"), float("nan"), float("nan")
    m = statistics.mean(xs)
    t = m / (statistics.stdev(xs) / math.sqrt(n)) if n > 1 and statistics.stdev(xs) > 0 else float("nan")
    return n, m, sum(x > 0 for x in xs) / n, t


def verdict():
    """One line for bin/killcheck.py: the primary book against its pre-registered marks."""
    tr, _ = trades(read(EVENTS), "rsi5_simple", "next_open")
    n, m, w, t = summary([x[3] for x in tr])
    if n >= KILL_FROM and m < 0:
        word = "KILL"
    elif n >= KEEP_AT and m > 0 and t >= T_KEEP:
        word = "KEEP"
    elif n >= LAST_AT:
        word = "KILL"
    else:
        nxt = KILL_FROM if n < KILL_FROM else (KEEP_AT if n < KEEP_AT else LAST_AT)
        word = f"RUNNING ({nxt - n} to the {nxt}-trade mark)"
    nums = f"{n} closed, mean {m:+.2%}, win {w:.0%}, t {t:.2f}" if n else "0 closed"
    return f"Systems book, RSI(5) simple, next-open fills, 9 index ETFs: {word}. {nums} (backtest 2009-26: +0.63%, 75%)"


def verdict2():
    """Book 2's line for bin/killcheck.py, against its marks in RULES.md."""
    tr, _ = trades(read(EVENTS), BOOK2, "next_open")
    n, m, w, t = summary([x[3] - B2_COST for x in tr])
    if n >= B2_KILL_FROM and m < 0:
        word = "KILL"
    elif n >= B2_LAST_AT:
        word = "KEEP" if m > 0 and t >= T_KEEP else "KILL"
    else:
        nxt = B2_KILL_FROM if n < B2_KILL_FROM else B2_LAST_AT
        word = f"RUNNING ({nxt - n} to the {nxt}-trade mark)"
    nums = f"{n} closed, mean after costs {m:+.2%}, win {w:.0%}, t {t:.2f}" if n else "0 closed"
    return f"Systems book 2, IBS below 0.2 while book 1 is flat, next-open fills: {word}. {nums} (backtest 2009-26: +0.27% before costs, 65%)"


def cmd_score():
    events = read(EVENTS)
    for strat in STRATEGIES:
        for fill in ("close", "next_open"):
            tr, openp = trades(events, strat, fill)
            n, m, w, t = summary([x[3] for x in tr])
            print(f"{strat:12s} {fill:9s}: {n:3d} closed" + (f", mean {m:+.2%}, win {w:.0%}, t {t:.2f}" if n else "") +
                  (f"; open: {', '.join(sorted(openp))}" if openp else ""))
    tr, openp = trades(events, BOOK2, "next_open")
    n, m, w, t = summary([x[3] for x in tr])
    print(f"{BOOK2:12s} next_open: {n:3d} closed" + (f", mean {m:+.2%}, win {w:.0%}, t {t:.2f}" if n else "") +
          (f"; open: {', '.join(sorted(openp))}" if openp else ""))
    print(verdict())
    print(verdict2())


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "score"
    {"update": cmd_update, "score": cmd_score}[cmd]()
