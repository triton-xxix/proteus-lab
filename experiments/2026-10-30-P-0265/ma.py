"""P-0265: does a 20/50 moving-average crossover beat buy and hold after fees on daily BTC?

Stdlib only, keyless. Binance spot BTCUSDT daily klines from the first day (17 Aug 2017), paged
1000 at a time. Rule: long when SMA20 > SMA50 at the close, else cash; the switch fills at the next
day's close (no look-ahead); 0.10% fee each way (Binance spot taker, no discounts). Buy and hold pays
0.10% once. Also 50/200 and 10/30 as neighbours, so the 20/50 result is not a lucky pair.
Writes RESULT.md beside this script.
"""
import json
import math
import os
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
URL = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=1000&startTime=%d"


def fetch():
    rows = []
    start = 1502928000000  # 2017-08-17 UTC
    while True:
        with urllib.request.urlopen(URL % start, timeout=30) as r:
            page = json.loads(r.read().decode())
        if not page:
            break
        rows.extend((int(k[0]), float(k[4])) for k in page)
        if len(page) < 1000:
            break
        start = page[-1][0] + 86400000
        time.sleep(0.3)
    # drop today's unfinished candle
    today = int(time.time() // 86400 * 86400 * 1000)
    rows = [r for r in rows if r[0] < today]
    return rows


def sma(xs, n):
    out = [None] * len(xs)
    s = 0.0
    for i, x in enumerate(xs):
        s += x
        if i >= n:
            s -= xs[i - n]
        if i >= n - 1:
            out[i] = s / n
    return out


def run(closes, fast, slow, fee=0.001, start=0):
    f, s = sma(closes, fast), sma(closes, slow)
    eq = 1.0
    pos = 0  # position held during day i (set from signal at i-1)
    trades = 0
    curve = []
    peak, mdd = 1.0, 0.0
    first = None
    for i in range(1, len(closes)):
        if i < start or s[i - 1] is None:
            continue
        if first is None:
            first = i - 1
            peak = 1.0
        want = 1 if f[i - 1] > s[i - 1] else 0
        if want != pos:
            eq *= (1 - fee)
            trades += 1
            pos = want
        if pos:
            eq *= closes[i] / closes[i - 1]
        curve.append(eq)
        peak = max(peak, eq)
        mdd = max(mdd, 1 - eq / peak)
    days = len(curve)
    cagr = eq ** (365.0 / days) - 1 if days else 0.0
    return {"multiple": eq, "cagr": cagr, "mdd": mdd, "trades": trades, "days": days, "first": first}


def hold(closes, first, fee=0.001):
    eq = (1 - fee) * closes[-1] / closes[first]
    peak, mdd = closes[first], 0.0
    for c in closes[first:]:
        peak = max(peak, c)
        mdd = max(mdd, 1 - c / peak)
    days = len(closes) - first - 1
    return {"multiple": eq, "cagr": eq ** (365.0 / days) - 1, "mdd": mdd, "days": days}


rows = fetch()
ts = [r[0] for r in rows]
closes = [r[1] for r in rows]
d0 = time.strftime("%Y-%m-%d", time.gmtime(ts[0] / 1000))
d1 = time.strftime("%Y-%m-%d", time.gmtime(ts[-1] / 1000))
L = ["# P-0265 result", "", "BTCUSDT daily closes, Binance spot, %s to %s, %d days. Fee 0.10%% a side." % (d0, d1, len(closes)), ""]
L += ["| window | rule | multiple | CAGR | max DD | trades | hold multiple | hold CAGR | hold max DD | rule minus hold (CAGR) |", "|---|---|---|---|---|---|---|---|---|---|"]
windows = [("all", 0), ("last 3 years", len(closes) - 3 * 365), ("last 1 year", len(closes) - 365)]
summary = {}
for wname, wstart in windows:
    for fast, slow in ((20, 50), (10, 30), (50, 200)):
        r = run(closes, fast, slow, start=max(wstart, slow))
        h = hold(closes, r["first"])
        L.append("| %s | %d/%d | %.2fx | %+.1f%% | %.0f%% | %d | %.2fx | %+.1f%% | %.0f%% | %+.1f pts |" % (
            wname, fast, slow, r["multiple"], 100 * r["cagr"], 100 * r["mdd"], r["trades"],
            h["multiple"], 100 * h["cagr"], 100 * h["mdd"], 100 * (r["cagr"] - h["cagr"])))
        summary[(wname, fast, slow)] = (r, h)
L += ["", "Rule: long when SMA(fast) > SMA(slow) at the close, else cash, filled at the next close. Hold pays the fee once at entry."]
open(os.path.join(HERE, "RESULT.md"), "w").write("\n".join(L) + "\n")
print("\n".join(L))
