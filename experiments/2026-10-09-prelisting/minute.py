"""Pre-listing research, step 2: what is "sell two or three minutes after the announcement" worth to
someone who already holds the coin? P-0107's 68 events (60 Upbit KRW, 8 Binance spot, each with a
prior USDT market elsewhere) re-measured on 1-minute candles.

Rules, fixed before the run (9 Oct 2026):
- Announcement time to the second: Upbit first_listed_at, Binance releaseDate (data/ from collect.py),
  matched to P-0107's rows by venue, ticker and minute.
- Price: the same venue P-0107 used (events.json price_source), 1-minute USDT candles. Gate keeps
  no 1-minute history that old, so Gate events fall back to Binance, OKX, Bybit in that order, and
  are dropped if none has the minute bars. Dropped events are counted.
- Holding price: the close of the last full minute that ended before the announcement.
- Exit at +k minutes (k = 1, 2, 3, 5, 10): the bar that contains announcement + k minutes. The
  announcement's own minute is never an exit. Two prices per exit: PESSIMISTIC is that bar's low
  (the worst fill inside the minute), TYPICAL is that bar's close.
- Costs: 0.5% round trip (0.1% fee each side plus 0.3% slippage selling into a rush), taken off
  every exit.
- Also recorded: the minute of the highest high in the first 30 minutes, and the 24-hour-before
  drift (the cost of having held the day before, from the same bars at 5-minute level, P-0107).
Writes minute_events.json and minute_summary.json beside this file.
"""
import json
import os
import statistics
import sys
import time
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
P107 = os.path.join(os.path.dirname(HERE), "2026-10-09-P-0107", "events.json")
UA = {"User-Agent": "Mozilla/5.0"}
COST = 0.005
KS = (1, 2, 3, 5, 10)


def get(url):
    for a in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.load(r)
        except Exception:
            time.sleep(2 * (a + 1))
    return None


def m1_binance(sym, s, e):
    d = get("https://data-api.binance.vision/api/v3/klines?symbol=%sUSDT&interval=1m&limit=1000&startTime=%d&endTime=%d" % (sym, s * 1000, e * 1000))
    return [(r[0] / 1000, float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in d] if isinstance(d, list) else []


def m1_okx(sym, s, e):
    rows, after = [], e * 1000
    for _ in range(4):
        d = get("https://www.okx.com/api/v5/market/history-candles?instId=%s-USDT&bar=1m&limit=100&after=%d" % (sym, after)) or {}
        data = d.get("data") or []
        if not data:
            break
        rows += [(int(r[0]) / 1000, float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in data]
        after = int(data[-1][0])
        if after / 1000 <= s:
            break
        time.sleep(0.12)
    return sorted(r for r in rows if r[0] >= s)


def m1_bybit(sym, s, e):
    d = get("https://api.bybit.com/v5/market/kline?category=spot&symbol=%sUSDT&interval=1&limit=1000&start=%d&end=%d" % (sym, s * 1000, e * 1000)) or {}
    lst = (d.get("result") or {}).get("list") or []
    return sorted((int(r[0]) / 1000, float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in lst)


SOURCES = {"binance": m1_binance, "okx": m1_okx, "bybit": m1_bybit}


def exact_times():
    data = os.path.join(HERE, "data")
    up = json.load(open(os.path.join(data, "upbit_notices.json")))
    bn = json.load(open(os.path.join(data, "binance_notices.json")))
    out = {}
    for a in up + bn:
        if a.get("symbol"):
            key = (a["venue"], a["symbol"], datetime.fromtimestamp(a["t"], timezone.utc).strftime("%Y-%m-%d %H:%M"))
            out[key] = a["t"]
    return out


def measure(ev, t, src, c):
    m0 = int(t // 60 * 60)
    before = [x for x in c if x[0] + 60 <= t]
    if not before or before[-1][0] < m0 - 300:
        return None
    hold = before[-1][4]
    out = {"venue": ev["venue"], "symbol": ev["symbol"], "announced": ev["announced"], "t": t, "src": src,
           "sec_into_minute": round(t - m0)}
    for k in KS:
        bar = next((x for x in c if x[0] <= t + 60 * k < x[0] + 60), None)
        if bar is None or bar[0] == m0:
            bar = next((x for x in c if x[0] > m0 and x[0] >= m0 + 60 * k), None)
        if bar is None or bar[0] > t + 60 * k + 300:
            continue
        out["pess_%d" % k] = round(bar[3] / hold - 1 - COST, 4)
        out["typ_%d" % k] = round(bar[4] / hold - 1 - COST, 4)
    w = [x for x in c if m0 <= x[0] < m0 + 1800]
    if w:
        top = max(w, key=lambda x: x[2])
        out["peak_30m"] = round(top[2] / hold - 1, 4)
        out["peak_minute"] = int((top[0] - m0) // 60)
    out["leak_24h_before"] = ev.get("leak_24h_before")
    return out


def summarise(rows):
    s = {"events": len(rows)}
    keys = ["pess_%d" % k for k in KS] + ["typ_%d" % k for k in KS] + ["peak_30m", "leak_24h_before"]
    for k in keys:
        xs = [r[k] for r in rows if r.get(k) is not None]
        if xs:
            s[k] = {"n": len(xs), "median_pct": round(100 * statistics.median(xs), 2), "mean_pct": round(100 * statistics.mean(xs), 2),
                    "share_positive": round(sum(x > 0 for x in xs) / len(xs), 2),
                    "p25_pct": round(100 * sorted(xs)[len(xs) // 4], 2)}
    pm = [r["peak_minute"] for r in rows if r.get("peak_minute") is not None]
    if pm:
        s["peak_minute"] = {"median": statistics.median(pm), "share_in_first_3": round(sum(p <= 2 for p in pm) / len(pm), 2),
                            "share_in_first_5": round(sum(p <= 4 for p in pm) / len(pm), 2)}
    return s


def main():
    evs = json.load(open(P107))
    times = exact_times()
    rows, dropped = [], []
    for ev in evs:
        t = times.get((ev["venue"], ev["symbol"], ev["announced"]))
        if t is None:
            dropped.append((ev["symbol"], "no exact time"))
            continue
        s, e = int(t) - 1800, int(t) + 3600
        order = [ev["price_source"]] if ev["price_source"] in SOURCES else []
        order += [x for x in ("binance", "okx", "bybit") if x not in order]
        got = None
        for src in order:
            if ev["venue"] == "binance" and src == "binance":
                continue
            c = SOURCES[src](ev["symbol"], s, e)
            if c and any(x[0] + 60 <= t for x in c) and any(x[0] >= t + 600 for x in c):
                got = measure(ev, t, src, c)
                if got:
                    break
        if got:
            rows.append(got)
        else:
            dropped.append((ev["symbol"], "no 1-minute bars around the announcement"))
        print(ev["venue"], ev["symbol"], "ok" if got else "dropped", flush=True)
    summary = {v: summarise([r for r in rows if r["venue"] == v]) for v in ("upbit", "binance")}
    summary["all"] = summarise(rows)
    summary["dropped"] = dropped
    json.dump(rows, open(os.path.join(HERE, "minute_events.json"), "w"), indent=0)
    json.dump(summary, open(os.path.join(HERE, "minute_summary.json"), "w"), indent=1)
    print(json.dumps(summary, indent=1))


def main_coinbase():
    """Added 9 Oct 2026, same rules: the first @CoinbaseMarkets post per asset (roadmap, deposits or
    trading, whichever came first; data/coinbase_posts.json) is the announcement; price from Binance,
    OKX or Bybit 1-minute bars. Writes minute_coinbase.json."""
    posts = json.load(open(os.path.join(HERE, "data", "coinbase_posts.json")))["posts"]
    first = {}
    for p in posts:
        if p.get("t") and (p["symbol"] not in first or p["t"] < first[p["symbol"]]["t"]):
            first[p["symbol"]] = p
    rows, dropped = [], []
    for sym, p in sorted(first.items(), key=lambda kv: kv[1]["t"]):
        t = p["t"]
        ev = {"venue": "coinbase", "symbol": sym, "announced": datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d %H:%M"),
              "leak_24h_before": None}
        got = None
        for src in ("binance", "okx", "bybit"):
            c = SOURCES[src](sym, int(t) - 1800, int(t) + 3600)
            if c and any(x[0] + 60 <= t for x in c) and any(x[0] >= t + 600 for x in c):
                got = measure(ev, t, src, c)
                if got:
                    got["first_post_kind"] = p["kind"]
                    break
        if got:
            rows.append(got)
        else:
            dropped.append((sym, "no 1-minute bars around the post"))
    s = summarise(rows)
    s["by_first_post_kind"] = {k: summarise([r for r in rows if r["first_post_kind"] == k]) for k in ("roadmap", "deposits", "trading")}
    s["dropped"] = dropped
    json.dump(rows, open(os.path.join(HERE, "minute_coinbase.json"), "w"), indent=0)
    json.dump(s, open(os.path.join(HERE, "minute_coinbase_summary.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in s.items() if k != "by_first_post_kind"}, indent=1))
    print({k: (v.get("events"), (v.get("pess_3") or {}).get("median_pct")) for k, v in s["by_first_post_kind"].items()})


if __name__ == "__main__":
    main_coinbase() if sys.argv[1:] == ["coinbase"] else main()
