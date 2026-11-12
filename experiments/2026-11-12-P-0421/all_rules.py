"""P-0421: every registered edge rule (E-011 to E-019) with its best trades removed.

P-0410 did this for E-017 alone. Here each rule's trade list is rebuilt with the scanner's own
functions (edges/scan/scan.py, imported, not edited) on that rule's admission window, and the best
trades are taken away one at a time until the total is at or below zero.

Windows are the three ladder blocks each rule was admitted on, read from edges.py status and the
scanner's block logic (blocks of 5 sessions or 7 UTC days back from the day before the scan).
The trade count is compared with the count on the register as a check that the window is right.

Usage: .venv/bin/python3 all_rules.py /abs/path/results.json
"""
import json
import sys
import time

sys.path.insert(0, "/Users/triton/PROTEUS/edges/scan")
import scan  # noqa: E402

# id, rule name in scan.RULES, first day, last day, dropped days, trades on the register, forward result
EDGES = [
    ("E-011", "Morning direction into the afternoon", "2026-10-02", "2026-10-22", [], 179, "FAIL"),
    ("E-012", "ORB 30m, target 1R", "2026-10-02", "2026-10-22", [], 157, "FAIL"),
    ("E-013", "VWAP cross after 11:00, hold to close", "2026-10-07", "2026-10-27", [], 124, "PASS"),
    ("E-014", "ORB 15m fade (failed break)", "2026-10-07", "2026-10-27", [], 157, "PASS"),
    ("E-015", "ORB NY open 30m, target 1R", "2026-10-09", "2026-10-29", [], 126, "FAIL"),
    ("E-016", "Opening drive: first bar direction to 11:00", "2026-10-09", "2026-10-29", [], 179, "PASS"),
    ("E-017", "Gap and go 0.5%", "2026-10-19", "2026-11-09", ["2026-11-05"], 121, "pending"),
    ("E-018", "Opening reversal: fade first 30m to 13:00", "2026-10-19", "2026-11-09", ["2026-11-05"], 180, "pending"),
    ("E-019", "ORB 30m fade (failed break)", "2026-10-20", "2026-11-10", ["2026-11-05"], 145, "pending"),
]


def cut(nets):
    nets = sorted(nets, reverse=True)
    n, total = len(nets), sum(nets)
    wins = sum(x for x in nets if x > 0)
    run, k = total, 0
    while run > 0 and k < n:
        run -= nets[k]
        k += 1
    row = {"n": n, "total_pct": round(total, 3), "win_pct": round(100 * sum(1 for x in nets if x > 0) / n, 1) if n else None,
           "best_removed_to_reach_zero": k, "share_of_trades_removed": round(k / n, 4) if n else None,
           "best3_removed_total_pct": round(sum(nets[3:]), 3),
           "best10_removed_total_pct": round(sum(nets[10:]), 3),
           "best10_share_of_gross_wins": round(sum(nets[:10]) / wins, 3) if wins else None,
           "median_pct": round(sorted(nets)[n // 2], 4) if n else None,
           "worst3_removed_total_pct": round(sum(nets[:-3]), 3)}
    return row


def main(out_path):
    days = {}
    for s in scan.STOCKS:
        days[s] = scan.prepare(scan.yahoo_5m(s), "stock")
        time.sleep(0.5)
    for s in scan.COINS:
        days[s] = scan.prepare(scan.binance_5m(s, days=38), "crypto")
    rules = {(k, name): fn for k, name, fn in scan.RULES}
    out = {"rows": []}
    for eid, name, a, b, drop, reg_n, fwd in EDGES:
        kind = "crypto" if (("crypto", name) in rules and ("stock", name) not in rules) else "stock"
        fn = rules[(kind, name)]
        syms = scan.STOCKS if kind == "stock" else scan.COINS
        cost = scan.COST[kind]
        nets, sessions = [], set()
        for s in syms:
            for D in days[s]:
                if not (a <= D["date"] <= b) or D["date"] in drop:
                    continue
                sessions.add(D["date"])
                for e, side, j, en, ex in fn(D):
                    nets.append(float(side * (ex / en - 1) - cost) * 100)
        row = {"id": eid, "rule": name, "kind": kind, "window": [a, b], "sessions": len(sessions),
               "registered_n": reg_n, "forward": fwd, **cut(nets)}
        row["n_matches_register"] = row["n"] == reg_n
        out["rows"].append(row)
        print("%s %-44s n %3d (reg %3d) total %+7.2f%% win %4.1f%% to-zero %2d (%.1f%% of trades) best10 gone %+7.2f%% fwd %s" % (
            eid, name[:44], row["n"], reg_n, row["total_pct"], row["win_pct"], row["best_removed_to_reach_zero"],
            100 * row["share_of_trades_removed"], row["best10_removed_total_pct"], fwd))
    ks = sorted(r["best_removed_to_reach_zero"] for r in out["rows"])
    out["median_to_zero"] = ks[len(ks) // 2]
    for g in ("PASS", "FAIL", "pending"):
        rs = [r for r in out["rows"] if r["forward"] == g]
        out[g] = {"to_zero": [r["best_removed_to_reach_zero"] for r in rs],
                  "share": [r["share_of_trades_removed"] for r in rs],
                  "mean_share": round(sum(r["share_of_trades_removed"] for r in rs) / len(rs), 4)}
        print(g, out[g])
    print("median to zero", out["median_to_zero"])
    json.dump(out, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
