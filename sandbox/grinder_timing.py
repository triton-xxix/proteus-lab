#!/usr/bin/env python3
"""What-if on the Grinder's closed v0.2 trades, from the minute candles already saved.
Entry delay, take-profit / stop-loss grid, trailing stop. Hindsight on 16 trades: descriptive only."""
import csv, statistics as st
L = "/Users/triton/PROTEUS/grinder/"
FEE = 0.019  # per side, calibrated so +100% nets about +92.6 and -50% about -52.7 on 100

def pnl(entry, exit_):
    return round(100 * ((1 - FEE) ** 2 * exit_ / entry - 1), 1)

rows = [r for r in csv.DictReader(open(L + "LEDGER.csv")) if r["rule_version"] == "v0.2" and r["exit_reason"]]
trades = []
for r in rows:
    try:
        c = [dict(ts=int(x["ts"]), h=float(x["h"]), l=float(x["l"]), c=float(x["c"]), o=float(x["o"]))
             for x in csv.DictReader(open(L + "candles/%s.csv" % r["id"]))]
    except FileNotFoundError:
        continue
    trades.append((r, c))

print("closed v0.2 trades with candles:", len(trades))
print("\nid       token       exit          pnl   minutes  peak%%  peak@min  low-before-peak%%  low24h%%  last%%")
for r, c in trades:
    e = float(r["entry_price_usd"])
    pk = max(range(len(c)), key=lambda i: c[i]["h"])
    lowb = min(x["l"] for x in c[:pk + 1])
    print("%-8s %-10s %-12s %6s %8d %6.0f %8d %12.0f %11.0f %6.0f" % (
        r["id"], r["token"][:10], r["exit_reason"], r["pnl_gbp"], len(c), 100 * (c[pk]["h"] / e - 1), pk,
        100 * (lowb / e - 1), 100 * (min(x["l"] for x in c) / e - 1), 100 * (c[-1]["c"] / e - 1)))

def sim(c, delay, tp, sl, trail=None, hold=24 * 60):
    if delay >= len(c):
        return None
    e = c[delay]["o"]; top = e
    for x in c[delay:delay + hold]:
        if x["l"] <= e * (1 + sl):
            return pnl(e, e * (1 + sl))
        if trail is not None and x["l"] <= top * (1 - trail) and top > e:
            return pnl(e, top * (1 - trail))
        if tp is not None and x["h"] >= e * (1 + tp):
            return pnl(e, e * (1 + tp))
        top = max(top, x["h"])
    return pnl(e, c[min(len(c), delay + hold) - 1]["c"])

def line(name, f):
    res = [f(c) for _, c in trades]
    res = [x for x in res if x is not None]
    wins = sum(1 for x in res if x > 0)
    print("%-42s n=%2d  total %7.1f  mean %6.1f  wins %2d" % (name, len(res), sum(res), st.mean(res), wins))

print("\n-- as run: TP +100, SL -50, enter at snapshot")
line("baseline (sim)", lambda c: sim(c, 0, 1.0, -0.5))
print("\n-- entry delay, same exits")
for d in (15, 30, 60, 120, 240, 480):
    line("enter %d min later" % d, lambda c, d=d: sim(c, d, 1.0, -0.5))
print("\n-- exit grid, enter at snapshot")
for tp in (0.3, 0.5, 1.0, 2.0):
    for sl in (-0.2, -0.3, -0.5):
        line("TP +%d SL %d" % (tp * 100, sl * 100), lambda c, tp=tp, sl=sl: sim(c, 0, tp, sl))
print("\n-- trailing stop from the high, no TP, SL -50")
for t in (0.2, 0.3, 0.4):
    line("trail %d%%" % (t * 100), lambda c, t=t: sim(c, 0, None, -0.5, trail=t))
print("\n-- time stop only (hold N hours, no TP/SL)")
for h in (1, 4, 12, 24):
    line("hold %dh" % h, lambda c, h=h: sim(c, 0, None, -9.9, hold=h * 60))
