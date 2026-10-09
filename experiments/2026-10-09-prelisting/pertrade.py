"""Exploratory, in-sample, written after the backtest (9 Oct 2026): per-signal trades instead of a
standing list. For every signal of a given kind in the window (coin not yet on the target), buy at
the close of the day the signal became knowable, hold until a target announcement (sell into the
pop: the coin's 1-minute +3 min result, else the venue median) or 14 days, whichever first. Costs
0.5% round trip on non-hit exits (hit results already carry costs). This is the shape the forward
rule would take if it holds up; it is NOT the pre-registered test. Writes pertrade.json.
"""
import json
import os
import statistics
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import backtest as B  # noqa: E402

DAY = A.DAY
HOLD = 14


def main():
    st, targets, before, avail, sig, turn, days, dix, close = A.build()
    ev_pop, med = B.pops()
    venue_of = {"upbit_krw": "upbit", "binance_spot": "binance", "coinbase": "coinbase"}
    fallback = {"upbit": 0.158, "binance": 0.06, "coinbase": 0.018}
    out = {}
    seen = set()
    rows = defaultdict(list)
    for x in sorted(sig, key=lambda x: x["t"]):
        s, name = x["symbol"], x["signal"]
        if not (A.W0 <= x["t"] <= A.W1) or (name, s) in seen or s in A.STABLE:
            continue
        seen.add((name, s))
        open_t = [t for t in targets if not A.on_target(s, x["t"], t, targets, before)]
        if not open_t:
            continue
        c = close.get(s, {})
        d0 = int(x["t"]) // DAY * DAY
        entry = c.get(d0)
        if not entry:
            continue
        ret, why = None, "time"
        for k in range(1, HOLD + 1):
            lo, hi = d0 + DAY + (k - 1) * DAY, d0 + DAY + k * DAY
            hit = [t for t in open_t if targets[t].get(s) and lo - DAY < targets[t][s] <= hi - DAY]
            if hit:
                v = venue_of[hit[0]]
                prev = c.get(d0 + (k - 1) * DAY) or entry
                ret = (prev / entry) * (1 + ev_pop.get((v, s), fallback[v])) - 1
                why = "hit " + hit[0]
                break
        if ret is None:
            last = None
            for k in range(HOLD, 0, -1):
                last = c.get(d0 + k * DAY)
                if last:
                    break
            if not last:
                continue
            ret = last / entry - 1 - 0.005
        rows[name].append({"symbol": s, "t": x["t"], "ret": round(ret, 4), "why": why})
    for name, rs in sorted(rows.items()):
        xs = [r["ret"] for r in rs]
        hits = [r for r in rs if r["why"] != "time"]
        out[name] = {"trades": len(xs), "hits": len(hits), "mean_pct": round(100 * statistics.mean(xs), 2),
                     "median_pct": round(100 * statistics.median(xs), 2), "share_up": round(sum(x > 0 for x in xs) / len(xs), 2),
                     "mean_hit_pct": round(100 * statistics.mean(r["ret"] for r in hits), 2) if hits else None,
                     "mean_nonhit_pct": round(100 * statistics.mean(r["ret"] for r in rs if r["why"] == "time"), 2) if len(hits) < len(rs) else None}
    json.dump({"summary": out, "trades": rows}, open(os.path.join(HERE, "pertrade.json"), "w"), indent=0)
    print("%-24s %6s %5s %8s %8s %6s %8s %8s" % ("signal", "trades", "hits", "mean%", "median%", "up", "hit%", "miss%"))
    for name, v in sorted(out.items(), key=lambda kv: -kv[1]["mean_pct"]):
        print("%-24s %6d %5d %8s %8s %6s %8s %8s" % (name, v["trades"], v["hits"], v["mean_pct"], v["median_pct"], v["share_up"], v["mean_hit_pct"], v["mean_nonhit_pct"]))


if __name__ == "__main__":
    main()
