"""P-0410: E-017 (Gap and go 0.5%) with its best trades removed.

Rebuilds the trade list with the scanner's own functions (edges/scan/scan.py, imported, not edited) on
the 15 sessions E-017 was admitted on: 19 to 23 Oct, 26 to 30 Oct, and 2, 3, 4, 6, 9 Nov 2026.
"""
import json
import sys
import time

sys.path.insert(0, "/Users/triton/PROTEUS/edges/scan")
import scan  # noqa: E402

ADMIT = {"2026-10-19", "2026-10-20", "2026-10-21", "2026-10-22", "2026-10-23",
         "2026-10-26", "2026-10-27", "2026-10-28", "2026-10-29", "2026-10-30",
         "2026-11-02", "2026-11-03", "2026-11-04", "2026-11-06", "2026-11-09"}
COST = scan.COST["stock"]


def trades_for(g):
    out = []
    for s in scan.STOCKS:
        for D in DAYS[s]:
            for e, side, j, en, ex in scan.gap(D, g, go=True):
                out.append({"sym": s, "date": D["date"], "side": int(side), "gap_pct": round(float(D["o"][0] / D["prev_close"] - 1) * 100, 3),
                            "net_pct": round(float(side * (ex / en - 1) - COST) * 100, 4)})
    return out


def cut(trades):
    nets = sorted((t["net_pct"] for t in trades), reverse=True)
    n, total = len(nets), sum(nets)
    wins = sum(x for x in nets if x > 0)
    row = {"n": n, "total_pct": round(total, 3), "mean_pct": round(total / n, 4) if n else None,
           "win_pct": round(100 * sum(1 for x in nets if x > 0) / n, 1) if n else None,
           "gross_wins_pct": round(wins, 3)}
    for k in (1, 3, 5, 10):
        rest = nets[k:]
        row["best%d_removed_total_pct" % k] = round(sum(rest), 3)
        row["best%d_removed_mean_pct" % k] = round(sum(rest) / len(rest), 4) if rest else None
        row["best%d_share_of_total" % k] = round(sum(nets[:k]) / total, 3) if total else None
        row["best%d_share_of_gross_wins" % k] = round(sum(nets[:k]) / wins, 3) if wins else None
    # how many of the best trades must go before the total is at or below zero
    run, k = total, 0
    while run > 0 and k < n:
        run -= nets[k]
        k += 1
    row["best_removed_to_reach_zero"] = k
    row["worst3_removed_total_pct"] = round(sum(nets[:-3]), 3)
    return row


if __name__ == "__main__":
    DAYS = {}
    for s in scan.STOCKS:
        DAYS[s] = scan.prepare(scan.yahoo_5m(s), "stock")
        time.sleep(0.5)
    out = {"cost_round_trip": COST, "admission_sessions": sorted(ADMIT), "thresholds": {}}
    for g, label in ((0.005, "0.5%"), (0.01, "1%"), (0.02, "2%")):
        allt = trades_for(g)
        adm = [t for t in allt if t["date"] in ADMIT]
        out["thresholds"][label] = {"admission": cut(adm), "all_sessions_in_feed": cut(allt),
                                    "sessions_in_feed": len({t["date"] for t in allt})}
        if label == "0.5%":
            out["top10_admission_trades"] = sorted(adm, key=lambda t: -t["net_pct"])[:10]
            out["worst5_admission_trades"] = sorted(adm, key=lambda t: t["net_pct"])[:5]
            by_sym, by_day = {}, {}
            for t in adm:
                by_sym[t["sym"]] = round(by_sym.get(t["sym"], 0) + t["net_pct"], 3)
                by_day[t["date"]] = round(by_day.get(t["date"], 0) + t["net_pct"], 3)
            out["by_sym"], out["by_day"] = by_sym, by_day
    json.dump(out, open(sys.argv[1], "w"), indent=1)
    a = out["thresholds"]["0.5%"]["admission"]
    print("admission 0.5%:", json.dumps(a))
    print("all sessions 0.5%:", json.dumps(out["thresholds"]["0.5%"]["all_sessions_in_feed"]))
    print("top10:", json.dumps(out["top10_admission_trades"]))
    print("by_sym:", json.dumps(out["by_sym"]))
    print("by_day:", json.dumps(out["by_day"]))
