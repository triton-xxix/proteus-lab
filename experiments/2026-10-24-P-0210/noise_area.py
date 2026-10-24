#!/usr/bin/env python3
"""P-0210: noise-area intraday momentum (Zarattini and Aziz 2024, "Beat the Market", Concretum Group,
found through Quantocracy's source list) run through the edges/scan ladder on the stock set.

Rule, as the paper describes it and as fixed here before the run:
  band_t   = day open * (1 +/- sigma_t), sigma_t = mean over the prior 14 kept sessions of
             |close at bar position t / that day's open - 1|
  entry    long at the next bar's open when a 5m close is above the upper band; short when below the
             lower band; one position at a time, re-entry allowed after an exit (the paper flips)
  exit     trailing stop at the band (long: a bar's low at or under the upper band fills at the band,
             or at the bar's open if it gapped through); otherwise flat at the session's last bar
  costs    scan.py's 0.03% round trip; fills, blocks, control and p exactly scan.py's

Imports scan.py for the Yahoo pull, prepare(), control_pool(), score() and blocks(). Pulls stocks
only. Writes results.json and LADDER-LINE.md beside this file. scan.py is not modified.
"""
import json
import os
import sys
import time
from datetime import datetime, timezone

import numpy as np

sys.path.insert(0, "/Users/triton/PROTEUS/edges/scan")
import scan  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
LOOKBACK = 14


def add_bands(days):
    """Attach 'up' and 'dn' arrays to each day dict, from the prior LOOKBACK kept days."""
    for k, D in enumerate(days):
        if k < LOOKBACK:
            D["up"] = D["dn"] = None
            continue
        n = D["n"]
        sig = np.full(n, np.nan)
        for t in range(n):
            moves = []
            for P in days[k - LOOKBACK:k]:
                if t < P["n"]:
                    moves.append(abs(P["c"][t] / P["o"][0] - 1))
            if moves:
                sig[t] = float(np.mean(moves))
        op = D["o"][0]
        D["up"] = op * (1 + sig)
        D["dn"] = op * (1 - sig)


def noise_area(D):
    if D.get("up") is None:
        return []
    o, h, l, c, up, dn, n = D["o"], D["h"], D["l"], D["c"], D["up"], D["dn"], D["n"]
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
            band = up[j] if side > 0 else dn[j]
            if np.isnan(band):
                continue
            if side > 0 and l[j] <= band:
                j_exit, ex = j, (min(o[j], band) if j > e else band)
                break
            if side < 0 and h[j] >= band:
                j_exit, ex = j, (max(o[j], band) if j > e else band)
                break
        out.append((e, side, j_exit, ent, ex))
        i = j_exit + 1
    return out


def main():
    days = {}
    for s in scan.STOCKS:
        days[s] = scan.prepare(scan.yahoo_5m(s), "stock")
        add_bands(days[s])
        time.sleep(0.5)
    bl = scan.blocks({D["date"] for s in scan.STOCKS for D in days[s]}, 5)
    cost = scan.COST["stock"]
    per_block = [[] for _ in bl]
    for s in scan.STOCKS:
        for D in days[s]:
            bi = next((i for i, b in enumerate(bl) if D["date"] in b), None)
            if bi is None:
                continue
            for e, side, j, en, ex in noise_area(D):
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
    res = {"probe": "P-0210", "rule": "Noise area (14-day band) intraday momentum, trailing stop at the band",
           "run_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "stock_weeks": [sorted(b)[0] + " to " + sorted(b)[-1] for b in bl[:3]],
           "W1": weeks[0], "W2": weeks[1] if len(weeks) > 1 else None, "W3": weeks[2] if len(weeks) > 2 else None,
           "rungs": rungs, "pooled_W1_W3": scan.score(w3, cost),
           "blocks_positive": sum(1 for w in weeks if w["n"] and w["total_pct"] > 0),
           "blocks_with_trades": sum(1 for w in weeks if w["n"]),
           "by_sym": by_sym,
           "mean_hold_bars_W1_W3": round(float(np.mean([t["hold"] for t in w3])), 1) if w3 else None,
           "long_share_W1_W3": round(float(np.mean([t["side"] > 0 for t in w3])), 3) if w3 else None}
    json.dump(res, open(os.path.join(HERE, "results.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
