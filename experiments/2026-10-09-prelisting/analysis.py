"""Pre-listing research, step 1 analysis: which publicly visible events come before a listing on Upbit
KRW, Binance spot or Coinbase, how often, and how early.

Definitions, fixed before the first run (9 Oct 2026):
- Study window: signals from 9 Oct 2025 to 24 Sep 2026, so every one has 14 full days of follow-up
  inside the data (to 8 Oct 2026).
- Targets: Upbit KRW market announcement (new listing or KRW added to a BTC/USDT-only coin,
  cancellations dropped); Binance spot "Binance Will List"; Coinbase first @CoinbaseMarkets post
  for the asset (roadmap, deposits or trading), and where there is no post, its first USD candle.
  A coin already on the target venue before 9 Oct 2025 is out of that target's universe; a coin
  listed in the window leaves it at the announcement.
- Universe: coins with a USDT market on Binance (spot or USD-M perp), OKX (spot or swap) or Bybit
  (spot or perp) at the day in question. Coins delisted from all of them before today are missing
  (survivorship; noted, not fixed).
- A signal is the first time a coin shows the event in the window. Its time is when it was knowable:
  published listing times as published; daily-candle firsts at the end of that day; volume signals
  at the end of the day.
- Hit: the target announced in (signal, signal + 14 days]. Precision = hits / signals where the coin
  was not yet on the target. Base rate = the same 14-day hit chance for an average coin-day in the
  universe. Lift = precision / base rate.
- Coverage: of target events in the window whose coin had a prior market, the share preceded by the
  signal within 14 days, within 90 days; median lead time in days among those within 90.
- Volume surge: 3-day mean turnover (Binance + OKX + Bybit spot, USDT) at least 3x the mean of the 30
  days before that, at least $500k a day, at least 20 days of history. Rank jump: rank by 7-day
  turnover improved by 150 places or more against 14 days earlier and now inside the top 300. Both
  debounced to once per 14 days per coin.
- Size band (a stand-in for market cap, which has no keyless history): rank by 30-day turnover.
Writes signals.json (every signal row), research.json (the tables) and prints the tables.
"""
import glob
import json
import os
import statistics
from collections import defaultdict
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
DATA = os.path.join(HERE, "data")
DAY = 86400
SINCE = datetime(2025, 6, 1, tzinfo=timezone.utc).timestamp()
W0 = datetime(2025, 10, 9, tzinfo=timezone.utc).timestamp()
W1 = datetime(2026, 9, 24, tzinfo=timezone.utc).timestamp()
END = datetime(2026, 10, 9, tzinfo=timezone.utc).timestamp()
H = 14 * DAY
STABLE = {"USDT", "USDC", "USDE", "USDG", "PYUSD", "RLUSD", "FDUSD", "TUSD", "DAI", "USD1", "XAUT", "PAXG", "JPYC",
          "BFUSD", "U", "KGST", "EURC", "USDS", "USDD", "FRAX", "USDP", "EURI", "AEUR", "XUSD", "USTC", "BUSD"}


def load(name):
    return json.load(open(os.path.join(DATA, name)))


def cache_dir(tag):
    out = {}
    for p in glob.glob(os.path.join(CACHE, tag, "*.json")):
        out[os.path.basename(p)[:-5]] = json.load(open(p))
    return out


def first_candle(rows, lookback=0):
    """First daily candle's time if it starts inside the window (a new listing), else None."""
    if not rows:
        return None
    t = rows[0][0]
    return t if t > SINCE - lookback + 2 * DAY else None


def build():
    st = json.load(open(os.path.join(CACHE, "static.json")))
    up = load("upbit_notices.json")
    bn = load("binance_notices.json")
    cbp = load("coinbase_posts.json")["posts"]

    # ---------- targets ----------
    targets = {"upbit_krw": {}, "binance_spot": {}, "coinbase": {}}
    for a in up:
        if "KRW" in a["markets"] and not a["cancelled"]:
            targets["upbit_krw"][a["symbol"]] = min(targets["upbit_krw"].get(a["symbol"], 1e12), a["t"])
    for a in bn:
        if a["kind"] == "spot" and a["symbol"]:
            targets["binance_spot"][a["symbol"]] = min(targets["binance_spot"].get(a["symbol"], 1e12), a["t"])
    cb_first = {}
    for pid, rows in cache_dir("coinbase").items():
        base = pid.split("-")[0]
        if rows:
            cb_first[base] = min(cb_first.get(base, 1e12), rows[0][0])
    for p in cbp:
        if p.get("t"):
            targets["coinbase"][p["symbol"]] = min(targets["coinbase"].get(p["symbol"], 1e12), p["t"])
    for base, t in cb_first.items():
        if t > SINCE + 2 * DAY and base not in targets["coinbase"]:
            targets["coinbase"][base] = t
    # listed before the window: out of the target universe for good
    before = {
        "upbit_krw": {m[4:] for m in st["upbit_markets"] if m.startswith("KRW-")} - set(targets["upbit_krw"]),
        "binance_spot": set(st["binance_spot_symbols"]) - set(targets["binance_spot"]),
        "coinbase": {b for b, t in cb_first.items() if t <= SINCE + 2 * DAY} - set(targets["coinbase"]),
    }

    # ---------- universe: when each coin first had a major USDT market ----------
    avail = defaultdict(lambda: 1e12)

    def seen(sym, t):
        avail[sym] = min(avail[sym], t)

    for k in ("binance_perp", "okx_spot", "okx_swap", "bybit_perp"):
        for s, t in st[k].items():
            seen(s, t)
    vol = {"bybit": cache_dir("bybit"), "okx": cache_dir("okx"), "binance": cache_dir("binance")}
    for venue, d in vol.items():
        for s, rows in d.items():
            if rows:
                seen(s, rows[0][0] if rows[0][0] > SINCE - 58 * DAY else 0)
    for s in st["binance_spot_symbols"] + st["bybit_spot_symbols"]:
        if s not in vol["binance"] and s not in vol["bybit"]:
            seen(s, 0)

    # ---------- daily turnover table ----------
    days = list(range(int(W0 - 60 * DAY) // DAY * DAY, int(END) // DAY * DAY + DAY, DAY))
    dix = {d: i for i, d in enumerate(days)}
    turn = defaultdict(lambda: [0.0] * len(days))
    close = {}
    for venue in ("bybit", "okx", "binance"):
        for s, rows in vol[venue].items():
            arr = turn[s]
            for r in rows:
                i = dix.get(int(r[0]) // DAY * DAY)
                if i is not None:
                    arr[i] += r[2]
            if s not in close or venue == "binance":
                close[s] = {int(r[0]) // DAY * DAY: r[1] for r in rows}

    # ---------- signals ----------
    sig = []

    def add(name, sym, t):
        if sym and sym not in STABLE and W0 - 90 * DAY <= t <= END:
            sig.append({"signal": name, "symbol": sym, "t": t})

    for name, k in (("binance_perp", "binance_perp"), ("binance_alpha", "binance_alpha"), ("okx_spot", "okx_spot"),
                    ("okx_swap", "okx_swap"), ("bybit_perp", "bybit_perp"), ("gate_spot", "gate_spot")):
        for s, t in st[k].items():
            if t > SINCE:
                add(name, s, t)
    for s, rows in vol["bybit"].items():
        t = first_candle(rows, 58 * DAY)
        if t:
            add("bybit_spot", s, t + DAY)
    for s, rows in vol["binance"].items():
        t = first_candle(rows, 58 * DAY)
        if t:
            add("binance_spot_trading", s, t + DAY)
    for m, rows in cache_dir("bithumb").items():
        t = first_candle(rows)
        if t:
            add("bithumb_krw", m[4:], t + DAY)
    firsts = {}
    for p in cbp:
        if p.get("t"):
            key = ("coinbase_roadmap" if p["kind"] == "roadmap" else "coinbase_post", p["symbol"])
            firsts[key] = min(firsts.get(key, 1e12), p["t"])
    for (name, s), t in firsts.items():
        add(name, s, t)
    for s, t in cb_first.items():
        if t > SINCE + 2 * DAY:
            add("coinbase_trading", s, t + DAY)
    for a in up:
        if "KRW" not in a["markets"] and not a["cancelled"]:
            add("upbit_btc_usdt_only", a["symbol"], a["t"])
    for s, t in targets["upbit_krw"].items():
        add("upbit_krw", s, t)
    for s, t in targets["binance_spot"].items():
        add("binance_spot_announce", s, t)

    # volume surge and rank jump
    last = {}
    rank_hist = {}
    for i, d in enumerate(days):
        if i < 7:
            continue
        r7 = sorted(((sum(turn[s][i - 6:i + 1]), s) for s in turn), reverse=True)
        rank_hist[d] = {s: n + 1 for n, (v, s) in enumerate(r7) if v > 0}
    for s, arr in turn.items():
        for i in range(34, len(days)):
            d = days[i]
            if d < W0 - 30 * DAY:
                continue
            prior = arr[i - 33:i - 3]
            if sum(1 for x in prior if x > 0) < 20:
                continue
            m3, m30 = sum(arr[i - 2:i + 1]) / 3, sum(prior) / 30
            if m3 >= 5e5 and m30 > 0 and m3 >= 3 * m30 and d + DAY - last.get(("surge", s), -1e12) > H:
                add("volume_surge", s, d + DAY)
                last[("surge", s)] = d + DAY
            r_now, r_then = rank_hist.get(d, {}).get(s), rank_hist.get(d - H, {}).get(s)
            if r_now and r_now <= 300 and (r_then is None or r_then - r_now >= 150) and r_then is not None \
                    and d + DAY - last.get(("rank", s), -1e12) > H:
                add("rank_jump", s, d + DAY)
                last[("rank", s)] = d + DAY
    return st, targets, before, avail, sig, turn, days, dix, close


def on_target(sym, t, tgt, targets, before):
    if sym in before[tgt]:
        return True
    tt = targets[tgt].get(sym)
    return tt is not None and tt <= t


def tables(targets, before, avail, sig, turn, days, dix):
    grid = [d for d in days if W0 <= d <= W1]
    out = {}
    for tgt in targets:
        # base rate over the universe
        num = den = 0
        band = defaultdict(lambda: [0, 0])
        for d in grid:
            i = dix[d]
            r30 = sorted(((sum(turn[s][max(0, i - 29):i + 1]), s) for s in turn), reverse=True)
            rk = {s: n + 1 for n, (v, s) in enumerate(r30)}
            for s, t0 in avail.items():
                if t0 > d or s in STABLE or on_target(s, d, tgt, targets, before):
                    continue
                tt = targets[tgt].get(s)
                hit = tt is not None and d < tt <= d + H
                num += hit
                den += 1
                r = rk.get(s, 9999)
                b = "top100" if r <= 100 else "101-300" if r <= 300 else "301+ or no volume"
                band[b][0] += hit
                band[b][1] += 1
        base = num / den if den else 0
        res = {"base_rate_14d": round(base, 5), "coin_days": den, "by_size_band": {b: {"rate_14d": round(h / n, 5), "lift": round(h / n / base, 2) if base else None, "coin_days": n} for b, (h, n) in sorted(band.items())}, "signals": {}}
        # precision per signal
        by = defaultdict(list)
        for x in sig:
            if W0 <= x["t"] <= W1 and not on_target(x["symbol"], x["t"], tgt, targets, before):
                tt = targets[tgt].get(x["symbol"])
                if x["signal"] == "upbit_krw" and tgt == "upbit_krw":
                    continue
                if x["signal"] == "binance_spot_announce" and tgt == "binance_spot":
                    continue
                by[x["signal"]].append(tt is not None and x["t"] < tt <= x["t"] + H)
        # coverage among target events with a prior market
        evs = [(s, t) for s, t in targets[tgt].items() if W0 <= t <= END and avail.get(s, 1e12) < t and s not in STABLE]
        firsts = defaultdict(dict)
        for x in sig:
            k = (x["signal"], x["symbol"])
            firsts[x["signal"]].setdefault(x["symbol"], []).append(x["t"])
        for name in sorted(set(by) | set(firsts)):
            hits = by.get(name, [])
            leads14 = leads90 = 0
            lead_days = []
            for s, t in evs:
                prior = [u for u in firsts[name].get(s, []) if u < t]
                if prior:
                    lead = (t - max(u for u in prior if u >= t - 90 * DAY)) / DAY if any(u >= t - 90 * DAY for u in prior) else None
                    if lead is not None:
                        leads90 += 1
                        lead_days.append(lead)
                        leads14 += lead <= 14
            res["signals"][name] = {
                "signals": len(hits), "hits_14d": sum(hits),
                "precision_14d": round(sum(hits) / len(hits), 4) if hits else None,
                "lift": round(sum(hits) / len(hits) / base, 1) if hits and base else None,
                "coverage_14d": round(leads14 / len(evs), 2) if evs else None,
                "coverage_90d": round(leads90 / len(evs), 2) if evs else None,
                "median_lead_days": round(statistics.median(lead_days), 1) if lead_days else None}
        res["target_events_with_prior_market"] = len(evs)
        out[tgt] = res
    return out


def xmention_pairs(targets, before, avail, turn, days, dix, n=9):
    """Cases and turnover-matched controls for xmentions.py (rules in its docstring)."""
    lo = datetime(2026, 3, 1, tzinfo=timezone.utc).timestamp()
    cases = sorted((t, s) for s, t in targets["upbit_krw"].items() if lo <= t <= W1 and avail.get(s, 1e12) < t and s not in STABLE)
    step = max(1, len(cases) // n)
    out = []
    for t, s in cases[::step][:n]:
        i = dix[int(t) // DAY * DAY - DAY]
        r30 = sorted(((sum(turn[x][max(0, i - 29):i + 1]), x) for x in turn), reverse=True)
        rk = {x: k for k, (v, x) in enumerate(r30)}
        if s not in rk:
            continue
        best = None
        for x, k in rk.items():
            tt = targets["upbit_krw"].get(x)
            if x == s or x in STABLE or avail.get(x, 1e12) > t or x in before["upbit_krw"] or (tt and abs(tt - t) < 90 * DAY):
                continue
            if best is None or abs(k - rk[s]) < abs(best[1] - rk[s]):
                best = (x, k)
        if best:
            out.append({"case": s, "control": best[0], "t": t, "case_rank": rk[s] + 1, "control_rank": best[1] + 1})
    json.dump(out, open(os.path.join(DATA, "xmention_pairs.json"), "w"), indent=0)
    return out


def main():
    st, targets, before, avail, sig, turn, days, dix, close = build()
    print("x pairs:", [(p["case"], p["control"]) for p in xmention_pairs(targets, before, avail, turn, days, dix)])
    json.dump(sorted(sig, key=lambda x: x["t"]), open(os.path.join(HERE, "signals.json"), "w"), indent=0)
    res = tables(targets, before, avail, sig, turn, days, dix)
    json.dump(res, open(os.path.join(HERE, "research.json"), "w"), indent=1)
    for tgt, r in res.items():
        print("\n== %s: base rate %.3f%% per coin per 14 days (%d coin-days), %d events with a prior market" % (
            tgt, 100 * r["base_rate_14d"], r["coin_days"], r["target_events_with_prior_market"]))
        print("   size bands:", {b: (round(100 * v["rate_14d"], 3), v["lift"]) for b, v in r["by_size_band"].items()})
        print("   %-24s %7s %5s %8s %6s %6s %6s %6s" % ("signal", "n", "hits", "prec%", "lift", "cov14", "cov90", "lead"))
        for name, v in sorted(r["signals"].items(), key=lambda kv: -(kv[1]["lift"] or 0)):
            print("   %-24s %7d %5d %8s %6s %6s %6s %6s" % (name, v["signals"], v["hits_14d"],
                  round(100 * v["precision_14d"], 2) if v["precision_14d"] is not None else "-", v["lift"],
                  v["coverage_14d"], v["coverage_90d"], v["median_lead_days"]))


if __name__ == "__main__":
    main()
