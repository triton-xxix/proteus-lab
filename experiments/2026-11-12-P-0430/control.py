"""P-0430: P-0421's best-trades-removed cut, with a random-entry control.

For each registered rule (same windows as P-0421, imported from its script), every real trade is
matched 500 times with a random entry on the same symbol and day with the same hold, either side
(scan.control_pool, the scanner's own null). Two measures, rule against the 500 random lists:
  share of gross wins that the best ten trades supply (does not depend on the total)
  trades removed to reach zero, as a share of trades, among random lists that ended above zero
Usage: .venv/bin/python3 control.py /abs/path/results.json
"""
import json
import sys
import time

import numpy as np

sys.path.insert(0, "/Users/triton/PROTEUS/edges/scan")
sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-11-12-P-0421")
import scan  # noqa: E402
from all_rules import EDGES  # noqa: E402

N = 500
rng = np.random.default_rng(20261112)


def top10_share(nets):
    s = np.sort(nets)[::-1]
    wins = s[s > 0].sum()
    return float(s[:10].sum() / wins) if wins > 0 else float("nan")


def to_zero_share(nets):
    s = np.sort(nets)[::-1]
    run, k = s.sum(), 0
    while run > 0 and k < len(s):
        run -= s[k]
        k += 1
    return k / len(s)


def main(out_path):
    days = {}
    for s in scan.STOCKS:
        days[s] = scan.prepare(scan.yahoo_5m(s), "stock")
        time.sleep(0.5)
    for s in scan.COINS:
        days[s] = scan.prepare(scan.binance_5m(s, days=38), "crypto")
    rules = {(k, name): fn for k, name, fn in scan.RULES}
    out = {"n_random_lists": N, "rows": []}
    for eid, name, a, b, drop, reg_n, fwd in EDGES:
        kind = "crypto" if (("crypto", name) in rules and ("stock", name) not in rules) else "stock"
        fn, cost = rules[(kind, name)], scan.COST[kind]
        nets, pools = [], []
        for s in (scan.STOCKS if kind == "stock" else scan.COINS):
            for D in days[s]:
                if not (a <= D["date"] <= b) or D["date"] in drop:
                    continue
                for e, side, j, en, ex in fn(D):
                    nets.append(float(side * (ex / en - 1) - cost))
                    pools.append(scan.control_pool(D, side, j - e + 1, cost))
        nets = np.array(nets)
        sims = np.array([[p[rng.integers(len(p))] for p in pools] for _ in range(N)])
        r_share = np.array([top10_share(x) for x in sims])
        pos = sims[sims.sum(axis=1) > 0]
        r_zero = np.array([to_zero_share(x) for x in pos]) if len(pos) else np.array([])
        rule_share, rule_zero = top10_share(nets), to_zero_share(nets)
        row = {"id": eid, "rule": name, "n": len(nets), "matches_register": len(nets) == reg_n, "forward": fwd,
               "rule_total_pct": round(float(nets.sum() * 100), 2),
               "rule_top10_share_of_gross_wins": round(rule_share, 3),
               "random_top10_share_median": round(float(np.nanmedian(r_share)), 3),
               "random_top10_share_p10_p90": [round(float(np.nanpercentile(r_share, 10)), 3), round(float(np.nanpercentile(r_share, 90)), 3)],
               "share_of_random_lists_more_concentrated": round(float(np.nanmean(r_share >= rule_share)), 3),
               "rule_to_zero_share": round(rule_zero, 4),
               "random_lists_above_zero": int(len(pos)),
               "random_to_zero_share_median": round(float(np.median(r_zero)), 4) if len(r_zero) else None,
               "share_of_positive_random_lists_at_least_as_sturdy": round(float(np.mean(r_zero >= rule_zero)), 3) if len(r_zero) else None,
               "random_total_pct_median": round(float(np.median(sims.sum(axis=1)) * 100), 2),
               "share_of_random_totals_at_or_above_rule": round(float(np.mean(sims.sum(axis=1) >= nets.sum())), 3)}
        out["rows"].append(row)
        print("%s n %3d total %+6.2f%% top10 share %.2f v random %.2f [%.2f, %.2f] (more concentrated: %.0f%%) | to-zero %.1f%% v positive random %s%% (n %d, as sturdy: %s) | random total >= rule: %.1f%%" % (
            eid, row["n"], row["rule_total_pct"], rule_share, row["random_top10_share_median"], *row["random_top10_share_p10_p90"],
            100 * row["share_of_random_lists_more_concentrated"], 100 * rule_zero,
            None if row["random_to_zero_share_median"] is None else round(100 * row["random_to_zero_share_median"], 1),
            len(pos), row["share_of_positive_random_lists_at_least_as_sturdy"], 100 * row["share_of_random_totals_at_or_above_rule"]))
    json.dump(out, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
