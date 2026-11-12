"""P-0431: the systems book's RSI(5) simple trades so far, paired from systems/EVENTS.csv (read only),
and the binomial chance of so few winners if the backtest's 75% win rate held.
Returns here are gross, open to open; the desk's own score nets costs, so its mean is the one to quote."""
import csv
import json
import sys
from math import comb

ev = [r for r in csv.DictReader(open("/Users/triton/PROTEUS/systems/EVENTS.csv")) if r["strategy"] == "rsi5_simple"]
open_pos, trades = {}, []
for r in ev:
    if r["event"] == "buy_open":
        open_pos[r["market"]] = r
    elif r["event"] == "sell_open" and r["market"] in open_pos:
        b = open_pos.pop(r["market"])
        trades.append({"market": r["market"], "in": b["date"], "out": r["date"], "buy": float(b["price"]), "sell": float(r["price"]),
                       "gross_pct": round((float(r["price"]) / float(b["price"]) - 1) * 100, 2)})
n = len(trades)
w = sum(1 for t in trades if t["gross_pct"] > 0)


def tail(k, n, p):
    return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(0, k + 1))


out = {"trades": trades, "n": n, "gross_winners": w, "gross_mean_pct": round(sum(t["gross_pct"] for t in trades) / n, 3) if n else None,
       "still_open": sorted(open_pos), "event_kinds": sorted({r["event"] for r in ev}),
       "p_at_most_this_many_winners_if_75pct": round(tail(w, n, 0.75), 4) if n else None,
       "p_at_most_3_of_8_if_75pct": round(tail(3, 8, 0.75), 4),
       "p_at_most_3_of_8_if_65pct": round(tail(3, 8, 0.65), 4),
       "p_at_most_3_of_8_if_50pct": round(tail(3, 8, 0.50), 4)}
json.dump(out, open(sys.argv[1], "w"), indent=1)
for t in trades:
    print(t)
print({k: v for k, v in out.items() if k != "trades"})
