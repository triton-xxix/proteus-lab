"""Live candidate scorer for the pre-listing week. The rule is RULES.md's, the same as backtest.py's,
with the per-signal probabilities fitted once on the full 12 months and frozen in scorer.json
(python3 score.py fit, run before the tracking starts and committed with RULES.md).

score.build(day) is called by poller.py once a day. Signals active in the last 14 days come from:
- signals.json (research history, to 9 Oct 2026);
- published listing times fetched fresh: Binance USD-M perps, Binance Alpha, OKX spot and swap, Bybit
  perps, Gate spot;
- new symbols on Bybit spot, Binance spot, Bithumb KRW and Coinbase USD products against the 9 Oct
  baseline (data/baseline.json), timed at first sight by the tracker (track/firstseen.json);
- notices the poller logged (track/feed.jsonl): Upbit BTC/USDT-only listings, Upbit KRW listings,
  Binance spot announcements, new Coinbase currencies (the keyless stand-in for a Coinbase post).
Coinbase roadmap posts are X-only and are not read live (no paid call per day).
"""
import json
import os
import sys
import time
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
TRACK = os.path.join(HERE, "track")
DAY = 86400
ACTIVE = 14 * DAY
SHRINK = 20
TOP_N = 25
LEFT_OUT = {"volume_surge", "rank_jump"}
TARGETS = ("upbit_krw", "binance_spot", "coinbase")
UA = {"User-Agent": "Mozilla/5.0 (proteus-prelisting)"}
sys.path.insert(0, HERE)


def get(url):
    for a in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.load(r)
        except Exception:
            time.sleep(2 * (a + 1))
    return None


def fit():
    """Fit p per (signal, target) on the whole study window and freeze it in scorer.json."""
    import analysis as A
    st, targets, before, avail, sig, turn, days, dix, close = A.build()
    res = json.load(open(os.path.join(HERE, "research.json")))
    p = {}
    for tgt in targets:
        base = res[tgt]["base_rate_14d"]
        by = defaultdict(lambda: [0, 0])
        for x in sig:
            if x["signal"] in LEFT_OUT or not (A.W0 <= x["t"] <= A.W1) or A.on_target(x["symbol"], x["t"], tgt, targets, before):
                continue
            if (x["signal"], tgt) in (("upbit_krw", "upbit_krw"), ("binance_spot_announce", "binance_spot")):
                continue
            tt = targets[tgt].get(x["symbol"])
            by[x["signal"]][0] += tt is not None and x["t"] < tt <= x["t"] + A.H
            by[x["signal"]][1] += 1
        for name, (h, n) in by.items():
            p["%s|%s" % (name, tgt)] = round((h + SHRINK * base) / (n + SHRINK), 5)
    baseline = {
        "bybit_spot": st["bybit_spot_symbols"], "binance_spot_trading": st["binance_spot_symbols"],
        "bithumb_krw": [m[4:] for m in st["bithumb_markets"] if m.startswith("KRW-")],
        "coinbase_trading": sorted({x["base"] for x in st["coinbase_products"] if x["quote"] == "USD"}),
        "upbit_krw": [m[4:] for m in st["upbit_markets"] if m.startswith("KRW-")],
        "taken_at": "2026-10-09",
    }
    json.dump(baseline, open(os.path.join(HERE, "data", "baseline.json"), "w"), indent=0, sort_keys=True)
    json.dump({"p": p, "shrink": SHRINK, "active_days": 14, "top_n": TOP_N, "left_out": sorted(LEFT_OUT),
               "fitted_on": "signals 2025-10-09 to 2026-09-24"}, open(os.path.join(HERE, "scorer.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps(dict(sorted(p.items(), key=lambda kv: -kv[1])[:25]), indent=1))


def live_sets():
    import collect
    st = collect.static_times()
    out = {"st": st}
    out["upbit_krw"] = {m[4:] for m in st["upbit_markets"] if m.startswith("KRW-")}
    out["binance_spot"] = set(st["binance_spot_symbols"])
    out["coinbase"] = {x["base"] for x in st["coinbase_products"] if x["quote"] == "USD"}
    out["universe"] = (set(st["binance_spot_symbols"]) | set(st["binance_perp"]) | set(st["okx_spot"]) | set(st["okx_swap"])
                       | set(st["bybit_spot_symbols"]) | set(st["bybit_perp"]))
    out["new_symbols"] = {
        "bybit_spot": set(st["bybit_spot_symbols"]), "binance_spot_trading": set(st["binance_spot_symbols"]),
        "bithumb_krw": {m[4:] for m in st["bithumb_markets"] if m.startswith("KRW-")}, "coinbase_trading": out["coinbase"]}
    return out


def prices():
    px = {}
    d = get("https://api.bybit.com/v5/market/tickers?category=spot") or {}
    for r in (d.get("result") or {}).get("list") or []:
        if r["symbol"].endswith("USDT"):
            px[r["symbol"][:-4]] = float(r["lastPrice"])
    d = get("https://www.okx.com/api/v5/market/tickers?instType=SPOT") or {}
    for r in d.get("data") or []:
        if r["instId"].endswith("-USDT") and r.get("last"):
            px[r["instId"][:-5]] = float(r["last"])
    d = get("https://data-api.binance.vision/api/v3/ticker/price")
    for r in d or []:
        if r["symbol"].endswith("USDT"):
            px[r["symbol"][:-4]] = float(r["price"])
    return px


def build(day):
    import analysis as A
    from poller import classify
    now = time.time()
    sc = json.load(open(os.path.join(HERE, "scorer.json")))
    p = sc["p"]
    base = json.load(open(os.path.join(HERE, "data", "baseline.json")))
    live = live_sets()
    sig = [x for x in json.load(open(os.path.join(HERE, "signals.json"))) if x["signal"] not in LEFT_OUT and now - ACTIVE <= x["t"] <= now]
    for name, key in (("binance_perp", "binance_perp"), ("binance_alpha", "binance_alpha"), ("okx_spot", "okx_spot"),
                      ("okx_swap", "okx_swap"), ("bybit_perp", "bybit_perp"), ("gate_spot", "gate_spot")):
        for s, t in live["st"][key].items():
            if now - ACTIVE <= t <= now:
                sig.append({"signal": name, "symbol": s, "t": t})
    fs_path = os.path.join(TRACK, "firstseen.json")
    fs = json.load(open(fs_path)) if os.path.exists(fs_path) else {}
    for name, cur in live["new_symbols"].items():
        for s in sorted(cur - set(base[name])):
            fs.setdefault(name, {}).setdefault(s, now)
    os.makedirs(TRACK, exist_ok=True)
    json.dump(fs, open(fs_path, "w"), indent=0, sort_keys=True)
    for name, d in fs.items():
        for s, t in d.items():
            if now - ACTIVE <= t <= now:
                sig.append({"signal": name, "symbol": s, "t": t})
    announced = defaultdict(set)
    feed = os.path.join(TRACK, "feed.jsonl")
    for line in open(feed) if os.path.exists(feed) else []:
        n = json.loads(line)
        kind, syms = classify(n)
        name = {"upbit_btc_usdt": "upbit_btc_usdt_only", "upbit_krw": "upbit_krw", "binance_spot": "binance_spot_announce",
                "coinbase_currency": "coinbase_post"}.get(kind)
        for s in syms:
            if kind == "upbit_krw":
                announced["upbit_krw"].add(s)
            if kind == "binance_spot":
                announced["binance_spot"].add(s)
            if kind in ("coinbase_currency", "coinbase_product"):
                announced["coinbase"].add(s)
            if name and now - ACTIVE <= n["t"] <= now:
                sig.append({"signal": name, "symbol": s, "t": n["t"]})
    on = {t: live[t] | announced[t] for t in TARGETS}
    by = defaultdict(list)
    for x in sig:
        by[x["symbol"]].append(x)
    rows = []
    for s in live["universe"]:
        if s in A.STABLE:
            continue
        q, used = 1.0, []
        for tgt in TARGETS:
            if s in on[tgt]:
                continue
            for x in by.get(s, []):
                k = "%s|%s" % (x["signal"], tgt)
                if k in p:
                    q *= 1 - p[k]
                    used.append(k)
        if q < 1:
            rows.append({"symbol": s, "score": round(1 - q, 4), "signals": sorted({(x["signal"], datetime.fromtimestamp(x["t"], timezone.utc).strftime("%Y-%m-%d %H:%M")) for x in by[s]}),
                         "open_targets": [t for t in TARGETS if s not in on[t]]})
    rows.sort(key=lambda r: (-r["score"], r["symbol"]))
    for i, r in enumerate(rows):
        r["rank"] = i + 1
    px = prices()
    return {"day": day, "built_at": datetime.fromtimestamp(now, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "rule": "RULES.md v1",
            "top_n": TOP_N, "candidates": rows[:TOP_N], "next_50": rows[TOP_N:TOP_N + 50], "pool_size": len(rows),
            "prices": {s: px[s] for s in sorted(live["universe"]) if s in px}}


if __name__ == "__main__":
    if sys.argv[1:] == ["fit"]:
        fit()
    else:
        print(json.dumps(build(datetime.now(timezone.utc).strftime("%Y-%m-%d")), indent=1)[:4000])
