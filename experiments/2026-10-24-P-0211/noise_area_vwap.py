#!/usr/bin/env python3
"""P-0211: noise-area intraday momentum with the paper's VWAP trailing stop (deepen of P-0210).

Same 14-day band entry as experiments/2026-10-24-P-0210/noise_area.py (imported). The exit is the
day's VWAP instead of the band: a long exits when a bar's low reaches VWAP (fills at VWAP, or at the
bar's open if it gapped through), a short when a bar's high does; otherwise flat at the last bar.
One position at a time, re-entry allowed after an exit. Stocks only, scan.py's fills, costs, blocks,
control and p. Writes results.json beside this file.
"""
import json
import os
import sys
import time
from datetime import datetime, timezone

import numpy as np

sys.path.insert(0, "/Users/triton/PROTEUS/edges/scan")
sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-10-24-P-0210")
import scan  # noqa: E402
import noise_area as base  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def noise_area_vwap(D, fill="level"):
    """fill='level': exit at the bar's VWAP when its low (high) reaches it, as a stop. That VWAP is
    computed with the bar's own trade and can sit outside the bar's range, so it is a look-ahead.
    fill='close': exit at the close of the bar whose low (high) reached VWAP, the way scan.py's own
    VWAP rules exit (until -> c[j]). No look-ahead."""
    if D.get("up") is None:
        return []
    o, h, l, c, up, dn, vw, n = D["o"], D["h"], D["l"], D["c"], D["up"], D["dn"], D["vwap"], D["n"]
    out, i = [], 1
    while i < n - 1:
        if np.isnan(up[i]):
            i += 1
            continue
        side = 1 if c[i] > up[i] else -1 if c[i] < dn[i] else 0
        if not side:
            i += 1
            continue
        e = i + 1
        ent = o[e]
        j_exit, ex = n - 1, c[n - 1]
        for j in range(e, n):
            hit = (side > 0 and l[j] <= vw[j]) or (side < 0 and h[j] >= vw[j])
            if not hit:
                continue
            if fill == "close":
                j_exit, ex = j, c[j]
            elif side > 0:
                j_exit, ex = j, (min(o[j], vw[j]) if j > e else vw[j])
            else:
                j_exit, ex = j, (max(o[j], vw[j]) if j > e else vw[j])
            break
        out.append((e, side, j_exit, ent, ex))
        i = j_exit + 1
    return out


def ladder(days, fn):
    bl = scan.blocks({D["date"] for s in scan.STOCKS for D in days[s]}, 5)
    cost = scan.COST["stock"]
    per_block = [[] for _ in bl]
    for s in scan.STOCKS:
        for D in days[s]:
            bi = next((i for i, b in enumerate(bl) if D["date"] in b), None)
            if bi is None:
                continue
            for e, side, j, en, ex in fn(D):
                hold = j - e + 1
                per_block[bi].append({"sym": s, "date": D["date"], "side": side, "hold": hold,
                                      "net": side * (ex / en - 1) - cost,
                                      "pool": scan.control_pool(D, side, hold, cost)})
    weeks = [scan.score(t, cost) for t in per_block]
    w3 = [t for b in per_block[:3] for t in b]
    rungs = 0
    for w in weeks[:3]:
        if w["n"] and w["total_pct"] > 0:
            rungs += 1
        else:
            break
    by_sym = {s: {"W1": round(sum(t["net"] for t in per_block[0] if t["sym"] == s) * 100, 3),
                  "W1_W3": round(sum(t["net"] for t in w3 if t["sym"] == s) * 100, 3),
                  "trades_W1_W3": sum(1 for t in w3 if t["sym"] == s)} for s in scan.STOCKS}
    return {"stock_weeks": [sorted(b)[0] + " to " + sorted(b)[-1] for b in bl[:3]],
            "W1": weeks[0], "W2": weeks[1] if len(weeks) > 1 else None, "W3": weeks[2] if len(weeks) > 2 else None,
            "rungs": rungs, "pooled_W1_W3": scan.score(w3, cost),
            "blocks_positive": sum(1 for w in weeks if w["n"] and w["total_pct"] > 0),
            "blocks_with_trades": sum(1 for w in weeks if w["n"]),
            "by_sym": by_sym,
            "mean_hold_bars_W1_W3": round(float(np.mean([t["hold"] for t in w3])), 1) if w3 else None,
            "long_share_W1_W3": round(float(np.mean([t["side"] > 0 for t in w3])), 3) if w3 else None}


def main():
    days = {}
    for s in scan.STOCKS:
        days[s] = scan.prepare(scan.yahoo_5m(s), "stock")
        base.add_bands(days[s])
        time.sleep(0.5)
    # Count, per fill, how often the 'level' fill sits outside the exit bar's range (the look-ahead).
    outside = 0
    total = 0
    for s in scan.STOCKS:
        for D in days[s]:
            for e, side, j, en, ex in noise_area_vwap(D, "level"):
                if j < D["n"] - 1:
                    total += 1
                    if ex > D["h"][j] or ex < D["l"][j]:
                        outside += 1
    res = {"probe": "P-0211", "rule": "Noise area (14-day band) intraday momentum, VWAP trailing stop",
           "run_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "fill_level_look_ahead": ladder(days, lambda D: noise_area_vwap(D, "level")),
           "fill_close_no_look_ahead": ladder(days, lambda D: noise_area_vwap(D, "close")),
           "level_fills_outside_bar_range": {"outside": outside, "of_stop_exits": total}}
    json.dump(res, open(os.path.join(HERE, "results.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
