#!/usr/bin/env python3
"""The edge scanner: about 60 intraday rules, a three-week ladder, a random-entry control. Luke, 23 Oct 2026.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/edges/scan/scan.py [--tag 2026-10-23]

Luke's ask (voice note, 23 Oct 17:35 UTC): keep finding strategies, backtest each on the last week;
if it is positive, test the week before, then the week before that; try improved versions; dozens a
day. We are not looking for 20 years, only for what has been working lately.

Fixed before the run (23 Oct 2026, before any window was read):

  Data     Stocks and ETFs: Yahoo 5-minute regular-session bars, 60 days, keyless: SPY QQQ IWM TSLA
           NVDA META AMD AAPL AMZN MSFT GOOGL NFLX. Today's session (still open) is dropped.
           Crypto: Binance spot 5-minute klines, 35 UTC days, keyless: BTC ETH SOL BNB XRP DOGE
           (USDT pairs). Today's UTC day is dropped. A crypto "day" is the UTC day; every trade is
           flat by its day's last bar, as stock trades are flat at the close.
  Fills    Entry at the open of the bar after the signal bar. Stops and targets fill at their level,
           or at the bar's open if it gaps through. A stop and a target in the same bar is a stop.
           Otherwise the trade exits at the close of the bar its rule names, or the day's last bar.
  Costs    Round trip, taken off every trade: stocks 0.03%, crypto 0.12% (perp taker 0.05% a side
           plus a little slippage). Equal size every trade; a week's score is the sum of its trades.
  Weeks    Stocks: W1 = the last 5 complete sessions, W2 the 5 before, W3 the 5 before that.
           Crypto: W1 = the last 7 complete UTC days, W2 and W3 the 7-day blocks before.
           Also every earlier 5-session or 7-day block in the data, as a stability count.
  Ladder   Rung 1: W1 total net above zero. Rung 2: W2 above zero. Rung 3: W3 above zero. A rule
           that climbs all three is a survivor. Each week is scored separately, never pooled into the
           next, so W2 and W3 are fresh data for a rule picked on W1.
  Luck     For every trade, a random entry in the same day, long or short at random, same number of
           bars held (same-side draws were biased, see control_pool; found on synthetic data before
           any real run), 300 resamples; the permutation p is the share of 300 resamples whose mean is at least the rule's
           mean. Reported per week and pooled over W1 to W3. With about 60 rules and three
           independent coin-flip weeks, about 60/8 = 7.5 would survive the ladder by luck alone; the
           report prints that beside the count.
  After    Survivors with a pooled p below 0.10 go to a forward paper week, registered in
           edges/REGISTER.csv before the week starts. The ladder finds candidates; only the forward
           week admits them. Nothing here trades.

Noise benchmark (smoke.py, pure random walks shaped like the real data, run before any real window):
61 rules, 5 climbed all three rungs and 3 of those had a pooled p below 0.10. So the ladder plus the
pooled p still passes noise, which is why the forward week, not the ladder, is the admission.

Called shot (written before the run): between 4 and 12 rules survive the ladder, near the luck
figure, and 0 to 2 of them have a pooled p below 0.10. Confidence 0.6.

Writes edges/scan/<tag>/results.json and LADDER.md.
"""
import argparse
import json
import math
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

import numpy as np

ROOT = "/Users/triton/PROTEUS/edges/scan"
STOCKS = ["SPY", "QQQ", "IWM", "TSLA", "NVDA", "META", "AMD", "AAPL", "AMZN", "MSFT", "GOOGL", "NFLX"]
COINS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "DOGEUSDT"]
COST = {"stock": 0.0003, "crypto": 0.0012}
PERMS = 300
rng = np.random.default_rng(20261023)


# ---------- data ----------

def getj(url):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            return json.load(urllib.request.urlopen(req, timeout=40))
        except urllib.error.HTTPError as e:
            if e.code in (429, 418) and attempt < 3:
                time.sleep(6 * (attempt + 1))
                continue
            raise


def yahoo_5m(sym):
    r = getj("https://query1.finance.yahoo.com/v8/finance/chart/%s?range=60d&interval=5m" % sym)["chart"]["result"][0]
    q, off = r["indicators"]["quote"][0], r["meta"].get("gmtoffset", 0)
    rows = []
    for i, ts in enumerate(r["timestamp"]):
        vals = [q[k][i] for k in ("open", "high", "low", "close", "volume")]
        if None in vals:
            continue
        local = datetime.fromtimestamp(ts + off, tz=timezone.utc)
        rows.append((ts, local.date().isoformat(), local.hour * 60 + local.minute) + tuple(float(v) for v in vals))
    return rows


def binance_5m(sym, days=35):
    end = int(time.time() * 1000)
    t, rows = end - days * 86400000, []
    while t < end:
        d = getj("https://api.binance.com/api/v3/klines?symbol=%s&interval=5m&startTime=%d&limit=1000" % (sym, t))
        if not d:
            break
        for k in d:
            u = datetime.fromtimestamp(k[0] / 1000, tz=timezone.utc)
            rows.append((k[0] // 1000, u.date().isoformat(), u.hour * 60 + u.minute) + tuple(float(k[j]) for j in (1, 2, 3, 4, 5)))
        t = d[-1][0] + 300000
        time.sleep(0.2)
    return rows


# ---------- indicators on the whole series ----------

def rsi(c, n):
    out = np.full(len(c), 50.0)
    d = np.diff(c, prepend=c[0])
    up, dn = np.where(d > 0, d, 0.0), np.where(d < 0, -d, 0.0)
    au = ad = None
    for i in range(1, len(c)):
        if au is None:
            if i >= n:
                au, ad = up[1:i + 1].mean(), dn[1:i + 1].mean()
        else:
            au, ad = (au * (n - 1) + up[i]) / n, (ad * (n - 1) + dn[i]) / n
        if au is not None:
            out[i] = 100.0 if ad == 0 else 100 - 100 / (1 + au / ad)
    return out


def rolling_mean_sd(c, n):
    mid, sd = np.full(len(c), np.nan), np.full(len(c), np.nan)
    for i in range(n - 1, len(c)):
        w = c[i - n + 1:i + 1]
        mid[i], sd[i] = w.mean(), w.std()
    return mid, sd


def adx(h, l, c, n=14):
    out = np.full(len(c), np.nan)
    tr = np.maximum(h[1:] - l[1:], np.maximum(abs(h[1:] - c[:-1]), abs(l[1:] - c[:-1])))
    pdm = np.where((h[1:] - h[:-1]) > (l[:-1] - l[1:]), np.maximum(h[1:] - h[:-1], 0), 0)
    ndm = np.where((l[:-1] - l[1:]) > (h[1:] - h[:-1]), np.maximum(l[:-1] - l[1:], 0), 0)
    atr = pp = nn = None
    dxs = []
    a = None
    for i in range(len(tr)):
        if i < n:
            continue
        if atr is None:
            atr, pp, nn = tr[:n].sum(), pdm[:n].sum(), ndm[:n].sum()
        atr, pp, nn = atr - atr / n + tr[i], pp - pp / n + pdm[i], nn - nn / n + ndm[i]
        pdi, ndi = 100 * pp / atr if atr else 0, 100 * nn / atr if atr else 0
        dx = 100 * abs(pdi - ndi) / (pdi + ndi) if pdi + ndi else 0
        dxs.append(dx)
        if len(dxs) == n:
            a = sum(dxs) / n
        elif len(dxs) > n:
            a = (a * (n - 1) + dx) / n
        if a is not None:
            out[i + 1] = a
    return out


def prepare(rows, kind):
    arr = np.array([r[3:] for r in rows])
    o, h, l, c, v = arr.T
    dates = [r[1] for r in rows]
    mins = np.array([r[2] for r in rows])
    s = {"o": o, "h": h, "l": l, "c": c, "v": v, "min": mins, "rsi2": rsi(c, 2)}
    # RSI(2) on 15-minute closes, readable only on the bar that closes each 15-minute block
    blk = [i for i in range(len(c)) if mins[i] % 15 == 10]
    r15 = np.full(len(c), np.nan)
    if blk:
        rr = rsi(c[blk], 2)
        r15[blk] = rr
    s["rsi2_15"] = r15
    s["bbm"], s["bbs"] = rolling_mean_sd(c, 20)
    s["adx"] = adx(h, l, c)
    days, start = [], 0
    for i in range(1, len(c) + 1):
        if i == len(c) or dates[i] != dates[start]:
            days.append((dates[start], start, i))
            start = i
    out = []
    today = datetime.now(timezone.utc).date().isoformat()
    for k, (d, a, b) in enumerate(days):
        if k == 0 or d >= today:
            continue
        if kind == "stock" and b - a < 70:  # half sessions and broken days
            continue
        if kind == "crypto" and b - a < 280:
            continue
        tp = (h[a:b] + l[a:b] + c[a:b]) / 3
        cum = np.cumsum(tp * v[a:b])
        cv = np.cumsum(v[a:b])
        vw = np.where(cv > 0, cum / np.maximum(cv, 1e-12), c[a:b])
        dev = c[a:b] - vw
        dsd = np.array([dev[:i + 1].std() if i >= 5 else np.nan for i in range(b - a)])
        out.append({"date": d, "a": a, "b": b, "n": b - a, "prev_close": c[days[k - 1][2] - 1],
                    "vwap": vw, "dsd": dsd, **{x: s[x][a:b] for x in s}})
    return out


# ---------- fills ----------

def run_exit(D, e, side, stop=None, target=None, last=None, until=None):
    """Enter at o[e]; walk bars e..last. until(j) -> True exits at c[j]. Returns (exit_bar, entry, exit)."""
    o, h, l, c = D["o"], D["h"], D["l"], D["c"]
    last = D["n"] - 1 if last is None else min(last, D["n"] - 1)
    ent = o[e]
    for j in range(e, last + 1):
        if stop is not None:
            if side > 0 and l[j] <= stop:
                return j, ent, min(o[j], stop) if j > e else stop
            if side < 0 and h[j] >= stop:
                return j, ent, max(o[j], stop) if j > e else stop
        if target is not None:
            if side > 0 and h[j] >= target:
                return j, ent, max(o[j], target) if j > e else target
            if side < 0 and l[j] <= target:
                return j, ent, min(o[j], target) if j > e else target
        if until is not None and until(j):
            return j, ent, c[j]
    return last, ent, c[last]


def bar_at(D, minute):
    idx = np.nonzero(D["min"] >= minute)[0]
    return int(idx[0]) if len(idx) else None


# ---------- rules: each returns a list of (entry_bar, side, exit_bar, entry_px, exit_px) ----------

def orb(D, k, tgt, start_min=None, fade=False):
    a = 0 if start_min is None else bar_at(D, start_min)
    if a is None or a + k + 1 >= D["n"]:
        return []
    hi, lo = D["h"][a:a + k].max(), D["l"][a:a + k].min()
    rng_w = hi - lo
    if rng_w <= 0:
        return []
    c = D["c"]
    for i in range(a + k, D["n"] - 1):
        if not fade:
            side = 1 if c[i] > hi else -1 if c[i] < lo else 0
            if side:
                stop = lo if side > 0 else hi
                target = None if tgt is None else D["o"][i + 1] + side * tgt * rng_w
                j, en, ex = run_exit(D, i + 1, side, stop, target)
                return [(i + 1, side, j, en, ex)]
        else:
            # a break that closes back inside the range: trade towards the other side
            if D["h"][i] > hi and lo < c[i] < hi:
                j, en, ex = run_exit(D, i + 1, -1, D["h"][i], lo)
                return [(i + 1, -1, j, en, ex)]
            if D["l"][i] < lo and lo < c[i] < hi:
                j, en, ex = run_exit(D, i + 1, 1, D["l"][i], hi)
                return [(i + 1, 1, j, en, ex)]
    return []


def vwap_revert(D, k, start=6, max_trades=3):
    out, i, c, vw, sd = [], start, D["c"], D["vwap"], D["dsd"]
    while i < D["n"] - 1 and len(out) < max_trades:
        if not np.isnan(sd[i]) and sd[i] > 0 and abs(c[i] - vw[i]) > k * sd[i]:
            side = 1 if c[i] < vw[i] else -1
            j, en, ex = run_exit(D, i + 1, side, until=lambda j: (c[j] - vw[j]) * side >= 0)
            out.append((i + 1, side, j, en, ex))
            i = j + 1
        else:
            i += 1
    return out


def vwap_trend(D, start=12, with_gap=False):
    c, vw = D["c"], D["vwap"]
    for i in range(max(start, 1), D["n"] - 1):
        for side in (1, -1):
            crossed = (c[i] - vw[i]) * side > 0 and (c[i - 1] - vw[i - 1]) * side <= 0
            if crossed and (not with_gap or (D["o"][0] - D["prev_close"]) * side > 0):
                j, en, ex = run_exit(D, i + 1, side)
                return [(i + 1, side, j, en, ex)]
    return []


def gap(D, g, go=False):
    gp = D["o"][0] / D["prev_close"] - 1
    if abs(gp) < g:
        return []
    side = (1 if gp > 0 else -1) * (1 if go else -1)
    target = None if go else D["prev_close"]
    j, en, ex = run_exit(D, 0, side, target=target)
    return [(0, side, j, en, ex)]


def rsi2(D, lvl, col="rsi2", hold=12, start=3, max_trades=4):
    out, i, r = [], start, D[col]
    while i < D["n"] - 1 and len(out) < max_trades:
        x = r[i]
        if not np.isnan(x) and (x < lvl or x > 100 - lvl):
            side = 1 if x < lvl else -1
            j, en, ex = run_exit(D, i + 1, side, last=i + hold,
                                 until=lambda j: not np.isnan(r[j]) and (r[j] - 50) * side > 0)
            out.append((i + 1, side, j, en, ex))
            i = j + 1
        else:
            i += 1
    return out


def boll(D, k, adx_max=None, hold=12, start=3, max_trades=4):
    out, i, c, m, s = [], start, D["c"], D["bbm"], D["bbs"]
    while i < D["n"] - 1 and len(out) < max_trades:
        if not np.isnan(m[i]) and s[i] > 0 and (adx_max is None or (not np.isnan(D["adx"][i]) and D["adx"][i] < adx_max)):
            side = 1 if c[i] < m[i] - k * s[i] else -1 if c[i] > m[i] + k * s[i] else 0
            if side:
                j, en, ex = run_exit(D, i + 1, side, last=i + hold, until=lambda j: (c[j] - m[j]) * side >= 0)
                out.append((i + 1, side, j, en, ex))
                i = j + 1
                continue
        i += 1
    return out


def intraday_mom(D, first_bars, last_bars):
    n = D["n"]
    r = D["c"][first_bars - 1] / D["prev_close"] - 1
    e = n - last_bars
    if r == 0 or e <= first_bars:
        return []
    side = 1 if r > 0 else -1
    j, en, ex = run_exit(D, e, side)
    return [(e, side, j, en, ex)]


def noon_mom(D):
    n = D["n"]
    e = n // 2
    r = D["c"][e - 1] / D["o"][0] - 1
    if r == 0:
        return []
    side = 1 if r > 0 else -1
    j, en, ex = run_exit(D, e, side)
    return [(e, side, j, en, ex)]


def drive(D, hold_bars, fade=False, first=1):
    r = D["c"][first - 1] - D["o"][0]
    if r == 0:
        return []
    side = (1 if r > 0 else -1) * (-1 if fade else 1)
    j, en, ex = run_exit(D, first, side, last=first + hold_bars - 1)
    return [(first, side, j, en, ex)]


def asian(D, tgt, fade=False):
    """Asian range 00:00 to 07:00 UTC; trade the London break (or its failure) up to 16:00 UTC."""
    a, b, z = 0, bar_at(D, 7 * 60), bar_at(D, 16 * 60)
    if b is None or z is None:
        return []
    hi, lo = D["h"][a:b].max(), D["l"][a:b].min()
    w, c = hi - lo, D["c"]
    for i in range(b, z):
        if not fade:
            side = 1 if c[i] > hi else -1 if c[i] < lo else 0
            if side:
                target = None if tgt is None else D["o"][i + 1] + side * tgt * w
                j, en, ex = run_exit(D, i + 1, side, lo if side > 0 else hi, target, last=z)
                return [(i + 1, side, j, en, ex)]
        else:
            if D["h"][i] > hi and lo < c[i] < hi:
                j, en, ex = run_exit(D, i + 1, -1, D["h"][i], lo, last=z)
                return [(i + 1, -1, j, en, ex)]
            if D["l"][i] < lo and lo < c[i] < hi:
                j, en, ex = run_exit(D, i + 1, 1, D["l"][i], hi, last=z)
                return [(i + 1, 1, j, en, ex)]
    return []


def coin_mom(D, look=48, thr=0.02, hold=48):
    out, i, c = [], look, D["c"]
    while i < D["n"] - 1:
        r = c[i] / c[i - look] - 1
        if abs(r) >= thr:
            side = 1 if r > 0 else -1
            j, en, ex = run_exit(D, i + 1, side, last=i + hold)
            out.append((i + 1, side, j, en, ex))
            i = j + 1
        else:
            i += 1
    return out


NY, LDN = 13 * 60 + 30, 7 * 60  # UTC, while the US is on EDT and the UK on BST (to 25 Oct, 1 Nov)

RULES = []
for k, label in ((1, "5"), (3, "15"), (6, "30")):
    for tgt in (1, 2, None):
        RULES.append(("stock", "ORB %sm, target %s" % (label, "%dR" % tgt if tgt else "close"), lambda D, k=k, t=tgt: orb(D, k, t)))
RULES += [
    ("stock", "ORB 15m fade (failed break)", lambda D: orb(D, 3, None, fade=True)),
    ("stock", "ORB 30m fade (failed break)", lambda D: orb(D, 6, None, fade=True)),
    ("stock", "VWAP reversion 1.5 sd", lambda D: vwap_revert(D, 1.5)),
    ("stock", "VWAP reversion 2 sd", lambda D: vwap_revert(D, 2.0)),
    ("stock", "VWAP reversion 2.5 sd", lambda D: vwap_revert(D, 2.5)),
    ("stock", "VWAP cross after 11:00, hold to close", lambda D: vwap_trend(D)),
    ("stock", "VWAP cross after 11:00 with the gap", lambda D: vwap_trend(D, with_gap=True)),
    ("stock", "Gap fade 0.5%", lambda D: gap(D, 0.005)),
    ("stock", "Gap fade 1%", lambda D: gap(D, 0.01)),
    ("stock", "Gap fade 2%", lambda D: gap(D, 0.02)),
    ("stock", "Gap and go 0.5%", lambda D: gap(D, 0.005, go=True)),
    ("stock", "Gap and go 1%", lambda D: gap(D, 0.01, go=True)),
    ("stock", "Gap and go 2%", lambda D: gap(D, 0.02, go=True)),
    ("stock", "RSI(2) 5m, 5/95", lambda D: rsi2(D, 5)),
    ("stock", "RSI(2) 5m, 10/90", lambda D: rsi2(D, 10)),
    ("stock", "RSI(2) 5m, 20/80", lambda D: rsi2(D, 20)),
    ("stock", "RSI(2) 15m, 5/95", lambda D: rsi2(D, 5, "rsi2_15", hold=24)),
    ("stock", "RSI(2) 15m, 10/90", lambda D: rsi2(D, 10, "rsi2_15", hold=24)),
    ("stock", "RSI(2) 15m, 20/80", lambda D: rsi2(D, 20, "rsi2_15", hold=24)),
    ("stock", "Bollinger 20/2 reversion", lambda D: boll(D, 2.0)),
    ("stock", "Bollinger 20/2.5 reversion", lambda D: boll(D, 2.5)),
    ("stock", "Bollinger 20/2 reversion, ADX under 20", lambda D: boll(D, 2.0, adx_max=20)),
    ("stock", "First 30m direction into last 30m", lambda D: intraday_mom(D, 6, 6)),
    ("stock", "First 60m direction into last 60m", lambda D: intraday_mom(D, 12, 12)),
    ("stock", "Morning direction into the afternoon", lambda D: noon_mom(D)),
    ("stock", "Opening drive: first bar direction to 11:00", lambda D: drive(D, 17)),
    ("stock", "Opening reversal: fade first 30m to 13:00", lambda D: drive(D, 36, fade=True, first=6)),
]
for start, sname in ((LDN, "London"), (NY, "NY")):
    for k, label in ((3, "15"), (6, "30")):
        for tgt in (1, None):
            RULES.append(("crypto", "ORB %s open %sm, target %s" % (sname, label, "1R" if tgt else "day end"),
                          lambda D, k=k, t=tgt, s=start: orb(D, k, t, start_min=s)))
RULES += [
    ("crypto", "VWAP (UTC day) reversion 1.5 sd", lambda D: vwap_revert(D, 1.5, start=12, max_trades=6)),
    ("crypto", "VWAP (UTC day) reversion 2 sd", lambda D: vwap_revert(D, 2.0, start=12, max_trades=6)),
    ("crypto", "VWAP (UTC day) reversion 2.5 sd", lambda D: vwap_revert(D, 2.5, start=12, max_trades=6)),
    ("crypto", "RSI(2) 5m, 5/95", lambda D: rsi2(D, 5, max_trades=8)),
    ("crypto", "RSI(2) 5m, 10/90", lambda D: rsi2(D, 10, max_trades=8)),
    ("crypto", "RSI(2) 5m, 20/80", lambda D: rsi2(D, 20, max_trades=8)),
    ("crypto", "RSI(2) 15m, 5/95", lambda D: rsi2(D, 5, "rsi2_15", hold=24, max_trades=8)),
    ("crypto", "RSI(2) 15m, 10/90", lambda D: rsi2(D, 10, "rsi2_15", hold=24, max_trades=8)),
    ("crypto", "RSI(2) 15m, 20/80", lambda D: rsi2(D, 20, "rsi2_15", hold=24, max_trades=8)),
    ("crypto", "Bollinger 20/2 reversion", lambda D: boll(D, 2.0, max_trades=8)),
    ("crypto", "Bollinger 20/2.5 reversion", lambda D: boll(D, 2.5, max_trades=8)),
    ("crypto", "Bollinger 20/2 reversion, ADX under 20", lambda D: boll(D, 2.0, adx_max=20, max_trades=8)),
    ("crypto", "Asian range break in London, target 1R", lambda D: asian(D, 1)),
    ("crypto", "Asian range break in London, to 16:00", lambda D: asian(D, None)),
    ("crypto", "Asian range sweep fade", lambda D: asian(D, None, fade=True)),
    ("crypto", "4h move over 2%, follow 4h", lambda D: coin_mom(D, 48, 0.02, 48)),
    ("crypto", "4h move over 2%, fade 4h", lambda D: coin_fade(D)),
]


def coin_fade(D):
    out, i, c = [], 48, D["c"]
    while i < D["n"] - 1:
        r = c[i] / c[i - 48] - 1
        if abs(r) >= 0.02:
            side = -1 if r > 0 else 1
            j, en, ex = run_exit(D, i + 1, side, last=i + 48)
            out.append((i + 1, side, j, en, ex))
            i = j + 1
        else:
            i += 1
    return out


# ---------- scoring ----------

def control_pool(D, side, hold, cost):
    """Every same-day entry with this hold, long and short both: entry bar open to exit bar close.

    Both sides, not the rule's side: on the synthetic smoke test a same-side pool inherited the day's
    drift (a reversion trade sits against the day's move, so its same-side random entries lose the move)
    and gave p 0.0 to reversion rules on a pure random walk. Both sides is the unbiased null."""
    n = D["n"]
    e = np.arange(0, n - hold + 1)
    r = D["c"][e + hold - 1] / D["o"][e] - 1
    return np.concatenate([r, -r]) - cost


def score(trades, cost):
    if not trades:
        return {"n": 0, "total_pct": 0.0, "mean_pct": None, "win_pct": None, "p": None}
    nets = np.array([t["net"] for t in trades])
    pools = [t["pool"] for t in trades]
    sims = np.array([[p[rng.integers(len(p))] for p in pools] for _ in range(PERMS)]).mean(axis=1)
    return {"n": len(nets), "total_pct": round(float(nets.sum() * 100), 3), "mean_pct": round(float(nets.mean() * 100), 4),
            "win_pct": round(float((nets > 0).mean() * 100), 1), "control_mean_pct": round(float(sims.mean() * 100), 4),
            "p": round(float((sims >= nets.mean()).mean()), 3)}


def blocks(dates, size):
    """Most recent first: lists of dates, size each, from the end."""
    out, ds = [], sorted(dates)
    while len(ds) >= size:
        out.append(set(ds[-size:]))
        ds = ds[:-size]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default=datetime.now(timezone.utc).date().isoformat())
    a = ap.parse_args()
    out_dir = os.path.join(ROOT, a.tag)
    os.makedirs(out_dir, exist_ok=True)

    days = {}
    for s in STOCKS:
        days[s] = prepare(yahoo_5m(s), "stock")
        time.sleep(0.5)
    for s in COINS:
        days[s] = prepare(binance_5m(s), "crypto")
    stock_blocks = blocks({D["date"] for s in STOCKS for D in days[s]}, 5)
    coin_blocks = blocks({D["date"] for s in COINS for D in days[s]}, 7)

    results = []
    for kind, name, fn in RULES:
        syms = STOCKS if kind == "stock" else COINS
        bl = stock_blocks if kind == "stock" else coin_blocks
        cost = COST[kind]
        per_block = [[] for _ in bl]
        for s in syms:
            for D in days[s]:
                bi = next((i for i, b in enumerate(bl) if D["date"] in b), None)
                if bi is None:
                    continue
                for e, side, j, en, ex in fn(D):
                    hold = j - e + 1
                    per_block[bi].append({"sym": s, "date": D["date"], "side": side, "hold": hold,
                                          "net": side * (ex / en - 1) - cost, "pool": control_pool(D, side, hold, cost)})
        weeks = [score(t, cost) for t in per_block]
        w3 = [t for b in per_block[:3] for t in b]
        rungs = 0
        for w in weeks[:3]:
            if w["n"] and w["total_pct"] > 0:
                rungs += 1
            else:
                break
        results.append({"kind": kind, "rule": name, "W1": weeks[0], "W2": weeks[1] if len(weeks) > 1 else None,
                        "W3": weeks[2] if len(weeks) > 2 else None, "rungs": rungs, "pooled_W1_W3": score(w3, cost),
                        "blocks_positive": sum(1 for w in weeks if w["n"] and w["total_pct"] > 0),
                        "blocks_with_trades": sum(1 for w in weeks if w["n"]),
                        "by_sym_W1_W3": {s: round(sum(t["net"] for t in w3 if t["sym"] == s) * 100, 3) for s in syms}})
        print("%-7s %-46s rungs %d  W1 %s" % (kind, name, rungs, weeks[0]))

    span = {"stock_weeks": [sorted(b)[0] + " to " + sorted(b)[-1] for b in stock_blocks[:3]],
            "coin_weeks": [sorted(b)[0] + " to " + sorted(b)[-1] for b in coin_blocks[:3]],
            "stock_blocks": len(stock_blocks), "coin_blocks": len(coin_blocks)}
    json.dump({"run_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "span": span, "rules": results},
              open(os.path.join(out_dir, "results.json"), "w"), indent=1)
    write_md(out_dir, span, results)


def write_md(out_dir, span, results):
    surv = [r for r in results if r["rungs"] == 3]
    strong = [r for r in surv if r["pooled_W1_W3"]["p"] is not None and r["pooled_W1_W3"]["p"] < 0.10]
    L = ["# Edge scanner ladder, %s" % os.path.basename(out_dir), "",
         "Rules tested: %d. Stock weeks (W1, W2, W3): %s. Crypto weeks: %s." % (len(results), "; ".join(span["stock_weeks"]), "; ".join(span["coin_weeks"])),
         "", "Climbed all three rungs: **%d** (luck alone would give about %.1f). Of those, pooled p below 0.10: **%d**." % (len(surv), len(results) / 8, len(strong)),
         "", "| rule | market | rungs | W1 total | W2 total | W3 total | trades W1-W3 | mean a trade | pooled p | earlier blocks positive |",
         "|---|---|---|---|---|---|---|---|---|---|"]

    def tot(w):
        return "-" if not w or not w["n"] else "%+.2f%%" % w["total_pct"]
    for r in sorted(results, key=lambda r: (-r["rungs"], -(r["pooled_W1_W3"]["total_pct"] or 0))):
        p = r["pooled_W1_W3"]
        L.append("| %s | %s | %d | %s | %s | %s | %d | %s | %s | %d of %d |" % (
            r["rule"], r["kind"], r["rungs"], tot(r["W1"]), tot(r["W2"]), tot(r["W3"]), p["n"],
            "-" if p["mean_pct"] is None else "%+.3f%%" % p["mean_pct"], "-" if p["p"] is None else "%.2f" % p["p"],
            r["blocks_positive"], r["blocks_with_trades"]))
    L += ["", "Totals are the sum of equal-size trades after costs (stocks 0.03%, crypto 0.12% round trip). "
          "Pooled p: share of 300 random-entry resamples (same day, side and hold) at or above the rule's mean over W1 to W3. "
          "The last column counts every 5-session (stock) or 7-day (crypto) block in the data, W1 to W3 included."]
    open(os.path.join(out_dir, "LADDER.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
