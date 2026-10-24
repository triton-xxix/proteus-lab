"""D-013: graduation G2 window two, scored two ways (RULES.md amendment 14 Oct 2026).

Written by Smith 24 Oct 2026 before any candle was fetched. Same method as P-0100's reprice.py
(experiments/2026-10-10-P-0100), applied to the second window, with the flag the amendment asked for.

  Window   counted G2 rows (killcheck's count: latency <= 120 s, Jupiter liquidity at entry >= $50,000,
           P present) whose entry_t is at or after grinder/graduates/START (the 14 Oct 16:14:36Z reload)
           and whose block_t is at or before DONE (21 Oct 16:14:41Z). All of them, not a prefix.
  Candles  GeckoTerminal 1-minute OHLCV, keyless, USD for the mint, from the mint's top Solana pool.
  Entry    the close of the first full 1-minute candle starting after entry_t.
  Exit P   -50% stop (trigger on a close at or below half the re-priced entry; fill at the NEXT close),
           otherwise the close of the first full candle starting after entry_t + 20 min; no later
           candle: last close carries forward. Costs grinder/paths.pnl_v02 unchanged.
  Flag     entry_ratio = candle entry / Jupiter quoted entry; flagged when above 2 or below 0.5.
  Reads    primary: candles. Beside it: the same trades on Jupiter's quotes (P), comparable with
           window one. Top ten on Jupiter: how many are flagged and what they score on candles.
  Lines    the G2 KEEP lines as written 3 Oct: expectancy >= +GBP 10 per GBP 100, best-10-removed >= 0,
           at most 25% at or below -50%. Reported for both reads. G2 stays "KEEP withdrawn, nothing
           graduates" whatever they say (amendment 14 Oct); this read says whether window two on honest
           fills looks like window one did.
  No data  a trade with no candle at or after entry is reported and left out; above 10% no data the
           read is not a verdict.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/experiments/2026-10-24-D-013/window2.py [--count]

Resume cache candles.jsonl beside this file; a rerun skips every mint already fetched.
"""
import json
import os
import statistics
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

sys.path.insert(0, "/Users/triton/PROTEUS/grinder")
from paths import pnl_v02  # noqa: E402

OUT = "/Users/triton/PROTEUS/experiments/2026-10-24-D-013/"
CACHE = OUT + "candles.jsonl"
GRAD = "/Users/triton/PROTEUS/grinder/graduates/"
GT = "https://api.geckoterminal.com/api/v2/networks/solana/"
PAUSE = 2.2
_last = [0.0]


def window():
    start = float(open(GRAD + "START").read().strip())
    done = open(GRAD + "DONE").read().strip()
    end = datetime.strptime(done, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()
    return start, end


def get(url):
    for attempt in range(4):
        wait = PAUSE - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "proteus-d013"})
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
    start, end = window()
    rows = [json.loads(l) for l in open(GRAD + "closed.jsonl")]
    xs = [r for r in rows if r.get("latency_s") is not None and r["latency_s"] <= 120
          and (r.get("liq") or 0) >= 50000 and r.get("P") is not None
          and r["entry_t"] >= start and r["block_t"] <= end]
    return sorted(xs, key=lambda r: r["entry_t"])


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
    fill = later[0][4] if later else after[-1][4]
    return {"entry": entry, "fill": fill, "reason": "time_stop", "carried": not later}


def lines(xs):
    xs = sorted(xs)
    e = statistics.mean(xs)
    b10 = statistics.mean(xs[:-10]) if len(xs) > 10 else None
    tail = sum(x <= -50 for x in xs) / len(xs)
    return {"n": len(xs), "expectancy": round(e, 2), "best10_removed": None if b10 is None else round(b10, 2),
            "at_or_below_-50_pct": round(tail, 3),
            "keep_lines_met": bool(e >= 10 and b10 is not None and b10 >= 0 and tail <= 0.25)}


def main():
    ts = trades()
    start, end = window()
    if "--count" in sys.argv:
        print("window", datetime.fromtimestamp(start, timezone.utc).isoformat(), "to",
              datetime.fromtimestamp(end, timezone.utc).isoformat(), "counted trades", len(ts))
        return
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
            out.append({"mint": r["mint"], "orig_P": r["P"], "orig_entry": r["entry"], "no_data": True})
            continue
        pnl = pnl_v02(p["entry"], p["fill"], p["reason"], 100, r["liq"])
        ratio = p["entry"] / r["entry"]
        out.append({"mint": r["mint"], "orig_P": r["P"], "orig_entry": r["entry"], **p, "pnl": pnl,
                    "entry_ratio": ratio, "flagged": bool(ratio > 2 or ratio < 0.5)})
    priced = [o for o in out if not o.get("no_data")]
    top10 = sorted(priced, key=lambda o: o["orig_P"], reverse=True)[:10]
    res = {"trades": len(ts), "repriced": len(priced), "no_data": nodata,
           "window_start": datetime.fromtimestamp(start, timezone.utc).isoformat(),
           "window_end": datetime.fromtimestamp(end, timezone.utc).isoformat(),
           "candles": lines([o["pnl"] for o in priced]) if priced else None,
           "jupiter_same_trades": lines([o["orig_P"] for o in priced]) if priced else None,
           "jupiter_all_window": lines([r["P"] for r in ts]) if ts else None,
           "flagged": sum(o["flagged"] for o in priced),
           "median_entry_ratio_candle_over_jupiter": round(statistics.median(o["entry_ratio"] for o in priced), 4) if priced else None,
           "stops": sum(o["reason"] == "stop_loss" for o in priced),
           "carried_forward_exits": sum(bool(o.get("carried")) for o in priced),
           "top10_on_jupiter": {"flagged": sum(o["flagged"] for o in top10),
                                "jupiter_P": [round(o["orig_P"], 1) for o in top10],
                                "candle_pnl": [round(o["pnl"], 1) for o in top10]},
           "is_a_verdict": bool(ts) and nodata <= 0.1 * len(ts)}
    for k, v in res.items():
        print(k, v)
    json.dump({"summary": res, "trades": out}, open(OUT + "results.json", "w"), indent=1)
    c, j = res["candles"], res["jupiter_same_trades"]
    md = ["# D-013 window two: result (written by window2.py at %s)" % datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%MZ"),
          "", "Window %s to %s. Counted trades %d, re-priced %d, no data %d. %s" % (
              res["window_start"], res["window_end"], len(ts), len(priced), nodata,
              "A verdict." if res["is_a_verdict"] else "NOT a verdict (over 10 percent no data or no trades)."),
          ""]
    if c:
        md += ["| read | n | expectancy per GBP 100 | best 10 removed | at or below -50 pct | KEEP lines met |", "|---|---|---|---|---|---|",
               "| candles (primary) | %d | %+.2f | %s | %.1f%% | %s |" % (c["n"], c["expectancy"], c["best10_removed"], 100 * c["at_or_below_-50_pct"], c["keep_lines_met"]),
               "| Jupiter, same trades | %d | %+.2f | %s | %.1f%% | %s |" % (j["n"], j["expectancy"], j["best10_removed"], 100 * j["at_or_below_-50_pct"], j["keep_lines_met"]),
               "", "Flagged entries (quote more than 2x off the candle): %d of %d. Median candle over quote %.4f. Stops %d, carried-forward exits %d." % (
                   res["flagged"], len(priced), res["median_entry_ratio_candle_over_jupiter"], res["stops"], res["carried_forward_exits"]),
               "", "Top ten on Jupiter: %d of 10 flagged; Jupiter P %s; on candles %s." % (
                   res["top10_on_jupiter"]["flagged"], res["top10_on_jupiter"]["jupiter_P"], res["top10_on_jupiter"]["candle_pnl"]),
               "", "G2 stays KEEP withdrawn, nothing graduates (amendment 14 Oct). This read says whether window two on honest fills looks like window one: window one was -3.98 on candles against +45.75 on quotes (P-0100)."]
    open(OUT + "RESULT.md", "w").write("\n".join(md) + "\n")


if __name__ == "__main__":
    main()
