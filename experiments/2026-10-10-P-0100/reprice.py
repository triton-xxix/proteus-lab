"""P-0100 / DUE D-009: graduation G2 fill realism on the 403 counted at its KEEP (8 Oct 2026).

Fixed before any candle was fetched:
  Trades   G2 counted rows exactly as bin/killcheck.py counts them (latency <= 120 s, Jupiter liquidity at
           entry >= $50,000, block time >= 2026-10-03T12:00Z, P present), sorted by entry time, first 403.
  Candles  GeckoTerminal 1-minute OHLCV, keyless, in USD for the mint itself (token=<mint>), from the
           mint's top pool on Solana. A minute with no trades is absent; the last close carries forward.
  Entry    the close of the first full 1-minute candle starting after entry_t.
  Exit P   -50% stop, otherwise 20 minutes, as the book: from the candle after the entry candle, the
           first close at or below half the re-priced entry triggers; the fill is the NEXT candle's
           close (no candle: the trigger close). Otherwise the fill is the close of the first full
           candle starting after entry_t + 20 min.
  Costs    grinder/paths.pnl_v02 unchanged: stop_loss slippage on stops, time_stop on time exits,
           Jupiter liquidity at entry.
  No data  a trade with no candle at or after entry is reported and left out; if more than 10% have
           no data the test is not a verdict on the KEEP.
  Lines    KEEP stands only if expectancy >= +GBP 10 per GBP 100 AND best-10-removed >= 0 (D-009).

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/experiments/2026-10-10-P-0100/reprice.py
"""
import json
import os
import statistics
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, "/Users/triton/PROTEUS/grinder")
from paths import pnl_v02  # noqa: E402

OUT = "/Users/triton/PROTEUS/experiments/2026-10-10-P-0100/"
CACHE = OUT + "candles.jsonl"
G2_FROM = 1791028800
GT = "https://api.geckoterminal.com/api/v2/networks/solana/"
PAUSE = 2.2
_last = [0.0]


def get(url):
    for attempt in range(4):
        wait = PAUSE - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "proteus-p0100"})
            return json.loads(urllib.request.urlopen(req, timeout=30).read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(20 * (attempt + 1))
                continue
            if e.code == 404:
                return None
        except Exception:
            time.sleep(5)
    return None


def trades():
    rows = [json.loads(l) for l in open("/Users/triton/PROTEUS/grinder/graduates/closed.jsonl")]
    xs = [r for r in rows if r.get("latency_s") is not None and r["latency_s"] <= 120
          and (r.get("liq") or 0) >= 50000 and r["block_t"] >= G2_FROM and r.get("P") is not None]
    return sorted(xs, key=lambda r: r["entry_t"])[:403]


def fetch(r):
    pools = get(GT + "tokens/%s/pools?page=1" % r["mint"])
    if not pools or not pools.get("data"):
        return {"mint": r["mint"], "pool": None, "candles": []}
    pool = pools["data"][0]["attributes"]["address"]
    before = int(r["entry_t"]) + 20 * 60 + 5 * 60
    o = get(GT + "pools/%s/ohlcv/minute?aggregate=1&limit=40&before_timestamp=%d&token=%s&currency=usd"
            % (pool, before, r["mint"]))
    cs = (o or {}).get("data", {}).get("attributes", {}).get("ohlcv_list", []) if o else []
    return {"mint": r["mint"], "pool": pool, "candles": sorted(cs)}


def reprice(r, candles):
    after = [c for c in candles if c[0] >= int(r["entry_t"]) // 60 * 60 + 60]
    if not after:
        return None
    entry = after[0][4]
    if not entry:
        return None
    mark = (int(r["entry_t"]) + 1200) // 60 * 60 + 60
    path = after[1:]
    for k, c in enumerate(path):
        if c[0] >= mark:
            break
        if c[4] <= entry * 0.5:
            fill = path[k + 1][4] if k + 1 < len(path) else c[4]
            return {"entry": entry, "fill": fill, "reason": "stop_loss"}
    later = [c for c in after if c[0] >= mark]
    fill = later[0][4] if later else after[-1][4]   # no candle after the mark: last close carries forward
    return {"entry": entry, "fill": fill, "reason": "time_stop", "carried": not later}


def main():
    ts = trades()
    have = {}
    if os.path.exists(CACHE):
        for l in open(CACHE):
            d = json.loads(l)
            have[d["mint"]] = d
    with open(CACHE, "a") as fh:
        for i, r in enumerate(ts):
            if r["mint"] in have:
                continue
            d = fetch(r)
            have[r["mint"]] = d
            fh.write(json.dumps(d) + "\n")
            fh.flush()
            if i % 25 == 0:
                print("fetched", i, "of", len(ts), flush=True)
    out, nodata = [], 0
    for r in ts:
        p = reprice(r, have[r["mint"]]["candles"])
        if p is None:
            nodata += 1
            continue
        pnl = pnl_v02(p["entry"], p["fill"], p["reason"], 100, r["liq"])
        out.append({"mint": r["mint"], "orig_P": r["P"], "orig_entry": r["entry"], **p, "pnl": pnl,
                    "entry_ratio": p["entry"] / r["entry"]})
    xs = sorted(o["pnl"] for o in out)
    orig = sorted(o["orig_P"] for o in out)
    res = {"trades": len(ts), "repriced": len(out), "no_data": nodata,
           "expectancy": round(statistics.mean(xs), 2), "best10_removed": round(statistics.mean(xs[:-10]), 2),
           "at_or_below_-50_pct": round(sum(x <= -50 for x in xs) / len(xs), 3),
           "same_trades_original_expectancy": round(statistics.mean(orig), 2),
           "same_trades_original_best10_removed": round(statistics.mean(orig[:-10]), 2),
           "median_entry_ratio_candle_over_jupiter": round(statistics.median(o["entry_ratio"] for o in out), 4),
           "stops": sum(o["reason"] == "stop_loss" for o in out),
           "carried_forward_exits": sum(bool(o.get("carried")) for o in out)}
    res["keep_stands"] = (res["no_data"] <= 0.1 * len(ts) and res["expectancy"] >= 10 and res["best10_removed"] >= 0)
    for k, v in res.items():
        print(k, v)
    json.dump({"summary": res, "trades": out}, open(OUT + "results.json", "w"), indent=1)


if __name__ == "__main__":
    main()
