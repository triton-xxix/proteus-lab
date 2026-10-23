"""P-0198: reliability of my called shots. Bins every scored shot by stated p, mean forecast v hit rate,
and the Murphy decomposition Brier = reliability - resolution + uncertainty.

Bins by exact stated p give an exact decomposition (all forecasts in a bin are equal). Ten equal-width
bins, as sklearn's calibration_curve(strategy='uniform') does, add a within-bin term; reported too.
Reads state/probes.json with the same scoring rule as probe.py shots (hit = verdict equals the shot).
Usage: python3 calib.py /Users/triton/PROTEUS/state/probes.json /path/to/results.json
"""
import json
import sys
from collections import defaultdict


def decompose(pairs, key):
    n = len(pairs)
    obar = sum(o for _, o in pairs) / n
    brier = sum((p - o) ** 2 for p, o in pairs) / n
    bins = defaultdict(list)
    for p, o in pairs:
        bins[key(p)].append((p, o))
    rel = res = within = 0.0
    table = []
    for k in sorted(bins):
        b = bins[k]
        nk = len(b)
        pk = sum(p for p, _ in b) / nk
        ok = sum(o for _, o in b) / nk
        rel += nk * (pk - ok) ** 2
        res += nk * (ok - obar) ** 2
        within += sum((p - pk) ** 2 for p, _ in b)
        table.append({"bin": k, "n": nk, "mean_p": round(pk, 3), "hit_rate": round(ok, 3)})
    unc = obar * (1 - obar)
    return {
        "n": n, "brier": round(brier, 4), "reliability": round(rel / n, 4), "resolution": round(res / n, 4),
        "uncertainty": round(unc, 4), "within_bin": round(within / n, 4),
        "check_rel_minus_res_plus_unc": round(rel / n - res / n + unc, 4), "base_rate": round(obar, 3),
        "table": table,
    }


def main():
    st = json.load(open(sys.argv[1]))
    rows = [i for i in st["items"] if i.get("shot") and i.get("status") == "done" and i.get("verdict")]
    pairs = [(float(i["shot"]["p"]), 1 if i["verdict"] == i["shot"]["expect"] else 0) for i in rows]
    by_expect = defaultdict(lambda: [0, 0])
    for i, (_, o) in zip(rows, pairs):
        by_expect[i["shot"]["expect"]][0] += 1
        by_expect[i["shot"]["expect"]][1] += o
    exact = decompose(pairs, key=lambda p: round(p, 2))
    ten = decompose(pairs, key=lambda p: min(int(p * 10), 9) / 10)
    out = {"exact_p_bins": exact, "ten_uniform_bins": ten,
           "by_expected_verdict": {k: {"n": v[0], "hits": v[1]} for k, v in sorted(by_expect.items())},
           "always_base_rate_brier": exact["uncertainty"]}
    json.dump(out, open(sys.argv[2], "w"), indent=1)
    for name, d in (("exact p bins", exact), ("10 uniform bins", ten)):
        print("%s: n %d, Brier %.4f = REL %.4f - RES %.4f + UNC %.4f (+ within %.4f); base rate %.3f"
              % (name, d["n"], d["brier"], d["reliability"], d["resolution"], d["uncertainty"],
                 d["within_bin"], d["base_rate"]))
        for r in d["table"]:
            print("   p %-5s n %3d  mean p %.3f  hit %.3f" % (r["bin"], r["n"], r["mean_p"], r["hit_rate"]))
    print("by expected verdict:", dict(out["by_expected_verdict"]))


if __name__ == "__main__":
    main()
