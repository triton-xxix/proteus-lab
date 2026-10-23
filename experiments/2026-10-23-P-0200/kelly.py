"""P-0200: what would my exchange calls have paid if staked? Full Kelly, half Kelly and flat stakes on
each settled call in exchange/BOOK.csv, my p against the market mid, in settlement order.

On each call I back whichever side I rate above its price: 'yes' at q if p > q, 'no' at 1-q if p < q.
Kelly fraction for backing a side I rate at P priced at Q: (P - Q) / (1 - Q). Flat stakes are 1 unit on
a 100 bank. No commission (Smarkets charges 2% of net winnings), no spread: the mid is not a fillable
price, so every line here is an upper bound. Settled = the same filter as killcheck.py.
The outcome is read back from brier = (p - y)^2.
Usage: python3 kelly.py BOOK.csv results.json
"""
import csv
import json
import sys


def main():
    rows = list(csv.DictReader(open(sys.argv[1])))
    s = [r for r in rows if r.get("brier") and r.get("market_brier") and r.get("mid_at") and r["committed_at"] < r["mid_at"]]
    s.sort(key=lambda r: r.get("settled_at") or "")
    banks = {"full": 100.0, "half": 100.0, "flat": 100.0}
    trail = []
    for r in s:
        p, q, b = float(r["p"]), float(r["market_mid"]), float(r["brier"])
        y = 1 if abs((1 - p) ** 2 - b) < abs(p ** 2 - b) else 0
        if p >= q:
            P, Q, won = p, q, y == 1
        else:
            P, Q, won = 1 - p, 1 - q, y == 0
        f = (P - Q) / (1 - Q) if Q < 1 else 0.0
        step = {"id": r["id"], "contract": r["contract"], "p": p, "mid": q, "y": y, "side": "yes" if p >= q else "no",
                "kelly_f": round(f, 3), "won": won}
        for name, frac in (("full", f), ("half", f / 2)):
            stake = frac * banks[name]
            banks[name] += stake * (1 - Q) / Q if won else -stake
            step[name] = round(banks[name], 2)
        if f > 0:
            banks["flat"] += (1 - Q) / Q if won else -1
        step["flat"] = round(banks["flat"], 2)
        trail.append(step)
    out = {"settled": len(s), "final": {k: round(v, 2) for k, v in banks.items()}, "trail": trail,
           "bets_won": sum(1 for t in trail if t["won"] and t["kelly_f"] > 0),
           "bets": sum(1 for t in trail if t["kelly_f"] > 0)}
    json.dump(out, open(sys.argv[2], "w"), indent=1)
    for t in trail:
        print("%s %-22s p %.2f mid %.3f y %d %-3s f %.3f %-5s full %8.2f half %7.2f flat %7.2f" % (
            t["id"], t["contract"][:22], t["p"], t["mid"], t["y"], t["side"], t["kelly_f"], t["won"],
            t["full"], t["half"], t["flat"]))
    print("settled %d, bets %d, won %d; final full %.2f, half %.2f, flat %.2f (start 100, not betting 100)" % (
        out["settled"], out["bets"], out["bets_won"], banks["full"], banks["half"], banks["flat"]))


if __name__ == "__main__":
    main()
