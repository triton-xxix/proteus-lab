"""P-0107: does a coin's price jump when Binance or Upbit announces a spot listing, and can a buyer
who acts after the announcement is public still make money? Luke's question, 9 Oct 2026.

Rules, fixed before the first run:
- Announcements, last 12 months to 9 Oct 2026, keyless:
  Binance "New Cryptocurrency Listing" catalogue, titles starting "Binance Will List" (spot listings;
  futures, Alpha, margin, earn, bStocks and collateral notices are excluded), ticker from the
  brackets. Upbit notices whose title says new trading support or a digital asset added to a KRW
  market. Coinbase and Crypto.com are not covered: neither publishes a keyless announcement feed
  with timestamps (Coinbase announces on X), so they would need a paid X search.
- Price: the coin's USDT spot market on another exchange that already traded it at the
  announcement (for Binance listings: OKX, Bybit, Gate; for Upbit listings: Binance, OKX, Bybit,
  Gate), 5-minute candles. No prior market, no row: a coin that only starts trading at the listing
  cannot be bought on the announcement.
- Entry: the open of the first 5-minute candle starting at least 5 minutes after the announcement
  (a script that polls the feed). A second, slower entry at +30 minutes (a person who sees it).
- Exits: the close at +1h, +4h, +24h and +7 days after entry. Costs 0.5% round trip.
- Also recorded, not tradable: the move in the 24 hours before the announcement (leak), and the
  highest price in the first 24 hours after entry (the "peak" nobody can know in advance).
Writes events.json and summary.json beside this file and prints the summary.
"""
import json
import os
import re
import statistics
import time
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0"}
NOW = time.time()
SINCE = NOW - 365 * 86400
COST = 0.005
M5 = 300


def get(url):
    for a in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.load(r)
        except Exception:
            time.sleep(2 * (a + 1))
    return None


def binance_announcements():
    out, page = [], 1
    while True:
        d = get("https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&catalogId=48&pageNo=%d&pageSize=50" % page)
        arts = (((d or {}).get("data") or {}).get("catalogs") or [{}])[0].get("articles") or []
        if not arts:
            break
        for a in arts:
            t = a["releaseDate"] / 1000
            if t < SINCE:
                return out
            title = a["title"]
            if not title.startswith("Binance Will List"):
                continue
            for sym in re.findall(r"\(([A-Z0-9]{2,12})\)", title):
                out.append({"venue": "binance", "t": t, "symbol": sym, "title": title})
        page += 1
        time.sleep(0.5)
    return out


def upbit_announcements():
    out, page = [], 1
    while True:
        d = get("https://api-manager.upbit.com/api/v1/announcements?os=web&page=%d&per_page=20&category=trade" % page)
        notes = ((d or {}).get("data") or {}).get("notices") or []
        if not notes:
            break
        for n in notes:
            t = datetime.fromisoformat(n["first_listed_at"]).timestamp()
            if t < SINCE:
                return out
            title = n["title"]
            if ("신규 거래지원" in title or "디지털 자산 추가" in title) and "KRW" in title:
                m = re.search(r"\(([A-Z0-9]{2,12})\)", title)
                if m:
                    out.append({"venue": "upbit", "t": t, "symbol": m.group(1), "title": title})
        page += 1
        time.sleep(0.4)
    return out


def candles_binance(sym, start, end):
    rows = []
    t = int(start * 1000)
    while t < end * 1000:
        d = get("https://data-api.binance.vision/api/v3/klines?symbol=%sUSDT&interval=5m&limit=1000&startTime=%d" % (sym, t))
        if not d or not isinstance(d, list):
            break
        rows += [(r[0] / 1000, float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in d]
        if len(d) < 1000:
            break
        t = d[-1][0] + 1
    return rows


def candles_okx(sym, start, end):
    rows, after = [], int(end * 1000)
    for _ in range(25):
        d = get("https://www.okx.com/api/v5/market/history-candles?instId=%s-USDT&bar=5m&limit=100&after=%d" % (sym, after))
        data = (d or {}).get("data") or []
        if not data:
            break
        rows += [(int(r[0]) / 1000, float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in data]
        after = int(data[-1][0])
        if after / 1000 <= start:
            break
        time.sleep(0.12)
    return sorted(r for r in rows if r[0] >= start)


def candles_bybit(sym, start, end):
    rows, e = [], int(end * 1000)
    for _ in range(5):
        d = get("https://api.bybit.com/v5/market/kline?category=spot&symbol=%sUSDT&interval=5&limit=1000&start=%d&end=%d" % (sym, int(start * 1000), e))
        data = ((d or {}).get("result") or {}).get("list") or []
        if not data:
            break
        rows += [(int(r[0]) / 1000, float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in data]
        e = int(data[-1][0]) - 1
        if e / 1000 <= start:
            break
    return sorted(set(rows))


def candles_gate(sym, start, end):
    rows, s = [], int(start)
    while s < end:
        e = min(int(end), s + 999 * M5)
        d = get("https://api.gateio.ws/api/v4/spot/candlesticks?currency_pair=%s_USDT&interval=5m&from=%d&to=%d" % (sym, s, e))
        if not d or not isinstance(d, list):
            break
        rows += [(float(r[0]), float(r[5]), float(r[3]), float(r[4]), float(r[2])) for r in d]
        s = e + M5
    return sorted(rows)


def price_path(ev):
    start, end = ev["t"] - 86400 - M5, ev["t"] + 8 * 86400
    order = [("okx", candles_okx), ("bybit", candles_bybit), ("gate", candles_gate)]
    if ev["venue"] == "upbit":
        order = [("binance", candles_binance)] + order
    for name, fn in order:
        try:
            c = fn(ev["symbol"], start, end)
        except Exception:
            c = []
        # must have traded in the hour before the announcement
        if c and any(ev["t"] - 3600 <= x[0] < ev["t"] for x in c) and any(x[0] >= ev["t"] + 86400 for x in c):
            return name, c
    return None, None


def at_or_after(c, t):
    for x in c:
        if x[0] >= t:
            return x
    return None


def close_at(c, t):
    prev = None
    for x in c:
        if x[0] + M5 > t:
            return prev[4] if prev else x[1]
        prev = x
    return prev[4] if prev else None


def measure(ev, src, c):
    out = {"venue": ev["venue"], "symbol": ev["symbol"], "announced": datetime.fromtimestamp(ev["t"], timezone.utc).strftime("%Y-%m-%d %H:%M"),
           "price_source": src}
    before = close_at(c, ev["t"] - 86400)
    at = close_at(c, ev["t"])
    out["leak_24h_before"] = round(at / before - 1, 4) if before and at else None
    for name, delay in (("fast", 5 * 60), ("slow", 30 * 60)):
        e = at_or_after(c, ev["t"] + delay)
        if not e:
            continue
        entry, t0 = e[1], e[0]
        out[name + "_entry_vs_announce"] = round(entry / at - 1, 4) if at else None
        for lab, h in (("1h", 3600), ("4h", 4 * 3600), ("24h", 86400), ("7d", 7 * 86400)):
            px = close_at(c, t0 + h)
            if px and (t0 + h) <= c[-1][0] + M5:
                out["%s_%s" % (name, lab)] = round(px / entry - 1 - COST, 4)
        w = [x for x in c if t0 <= x[0] < t0 + 86400]
        if w:
            out[name + "_peak_24h"] = round(max(x[2] for x in w) / entry - 1, 4)
    return out


def summarise(rows, venue):
    s = {"events": len(rows)}
    for k in ("leak_24h_before", "fast_entry_vs_announce", "fast_1h", "fast_4h", "fast_24h", "fast_7d",
              "slow_1h", "slow_24h", "slow_7d", "fast_peak_24h"):
        xs = [r[k] for r in rows if r.get(k) is not None]
        if xs:
            s[k] = {"n": len(xs), "mean_pct": round(100 * statistics.mean(xs), 2),
                    "median_pct": round(100 * statistics.median(xs), 2),
                    "share_positive": round(sum(x > 0 for x in xs) / len(xs), 2)}
    return s


def main():
    anns = binance_announcements() + upbit_announcements()
    print("announcements:", sum(a["venue"] == "binance" for a in anns), "binance,", sum(a["venue"] == "upbit" for a in anns), "upbit")
    rows, skipped = [], []
    for a in anns:
        if a["t"] > NOW - 86400:
            skipped.append((a["symbol"], "too recent"))
            continue
        src, c = price_path(a)
        if not c:
            skipped.append((a["symbol"], "no prior USDT market found"))
            continue
        rows.append(measure(a, src, c))
    summary = {"binance": summarise([r for r in rows if r["venue"] == "binance"], "binance"),
               "upbit": summarise([r for r in rows if r["venue"] == "upbit"], "upbit"),
               "skipped": len(skipped), "skipped_examples": skipped[:15]}
    json.dump(rows, open(os.path.join(HERE, "events.json"), "w"), indent=0)
    json.dump(summary, open(os.path.join(HERE, "summary.json"), "w"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
