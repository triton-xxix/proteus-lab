"""P-0159 / D-013: score G2 window two, candle fills primary, Jupiter quotes beside.

Rules from grinder/graduates/RULES.md (14 Oct amendment) and DUE D-013, written before any outcome
was read (22 Oct 2026, nightly):
  Trades    window two counted rows, as fetch.py selects them.
  Primary   P-0100's reprice(): entry at the close of the first full 1-minute candle after entry_t,
            -50% stop filled at the next candle's close, else the 20-minute time stop; pnl_v02 costs.
  Beside    the book's own Jupiter-quoted P for the same trades.
  Flag      every entry whose candle entry / Jupiter entry ratio is above 2 or below 0.5; report how
            many, and the share of the quoted P&L (sum of P) those flagged trades carry.
  Top ten   the blind read: the ten best trades by quoted P, how many are flagged, and what they
            make on candles.
  Lines     as D-009 for the KEEP question: expectancy >= +GBP 10 per GBP 100 AND best-10-removed >= 0,
            and the read is not a verdict if more than 10% of trades have no candle.
Refuses to score until every trade in the window has a cache row.
"""
import json
import statistics
import sys

sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-10-10-P-0100")
sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-10-22-P-0159")
import reprice as P0100  # noqa: E402
import fetch as F  # noqa: E402

OUT = "/Users/triton/PROTEUS/experiments/2026-10-22-P-0159/"


def main():
    keys = [(r["mint"], int(r["entry_t"])) for r in F.window_two()]
    cache = {}
    for l in open(F.CACHE):
        d = json.loads(l)
        cache[d["key"]] = d
    missing = [k for k in keys if "%s|%d" % k not in cache]
    if missing:
        print("not scoring: %d of %d trades have no cache row yet" % (len(missing), len(keys)))
        return
    rows = {}
    for line in open("/Users/triton/PROTEUS/grinder/graduates/closed.jsonl"):
        r = json.loads(line)
        k = (r.get("mint"), int(r.get("entry_t") or 0))
        if k in set(keys):
            rows[k] = r
    out, nodata = [], 0
    for k in keys:
        r = rows[k]
        p = P0100.reprice(r, cache["%s|%d" % k]["candles"])
        if p is None:
            nodata += 1
            continue
        pnl = P0100.pnl_v02(p["entry"], p["fill"], p["reason"], 100, r["liq"])
        ratio = p["entry"] / r["entry"]
        out.append({"mint": r["mint"], "entry_t": r["entry_t"], "quoted_P": r["P"], "candle_P": pnl,
                    "entry_ratio": ratio, "flag": ratio > 2 or ratio < 0.5, "reason": p["reason"]})
    c = sorted(o["candle_P"] for o in out)
    q = sorted(o["quoted_P"] for o in out)
    quoted_total = sum(q)
    flagged = [o for o in out if o["flag"]]
    top10 = sorted(out, key=lambda o: o["quoted_P"], reverse=True)[:10]
    res = {
        "trades": len(keys), "scored": len(out), "no_candle": nodata,
        "candle_expectancy": round(statistics.mean(c), 2), "candle_best10_removed": round(statistics.mean(c[:-10]), 2),
        "candle_at_or_below_-50": round(sum(x <= -50 for x in c) / len(c), 3),
        "quoted_expectancy": round(statistics.mean(q), 2), "quoted_best10_removed": round(statistics.mean(q[:-10]), 2),
        "flagged": len(flagged), "flagged_share_of_quoted_pnl": round(sum(o["quoted_P"] for o in flagged) / quoted_total, 3) if quoted_total else None,
        "median_entry_ratio": round(statistics.median(o["entry_ratio"] for o in out), 4),
        "top10_flagged": sum(o["flag"] for o in top10),
        "top10_quoted": [round(o["quoted_P"], 1) for o in top10],
        "top10_on_candles": [round(o["candle_P"], 1) for o in top10],
    }
    res["keep_line_met_on_candles"] = (nodata <= 0.1 * len(keys) and res["candle_expectancy"] >= 10
                                       and res["candle_best10_removed"] >= 0)
    for k, v in res.items():
        print(k, v)
    json.dump({"summary": res, "trades": out}, open(OUT + "results.json", "w"), indent=1)


if __name__ == "__main__":
    main()
