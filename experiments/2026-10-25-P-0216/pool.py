"""P-0216: partial pooling of graduation-book trades across entry-liquidity buckets.

Question: does an empirical-Bayes (normal-normal) shrinkage of per-bucket mean return, fitted on the
first half of the book by time, predict the second half's bucket means better than the raw means?
Data: grinder/graduates/closed.jsonl, counted rows (latency <= 120 s, liq >= $5k), exit P (-50% stop,
else 20 min), as percent of stake. Run: python3 -I pool.py <closed.jsonl> <out.json>
"""
import json
import statistics as st
import sys


def load(path):
    rows = []
    with open(path) as f:
        for line in f:
            r = json.loads(line)
            if r.get("P") is None or r.get("latency_s") is None or r.get("liq") is None:
                continue
            if r["latency_s"] > 120 or r["liq"] < 5000:
                continue
            rows.append((r["entry_t"], r["liq"], float(r["P"])))
    rows.sort()
    return rows


def edges_for(liqs, k):
    s = sorted(liqs)
    return [s[int(len(s) * i / k)] for i in range(1, k)]


def bucket(liq, edges):
    for i, e in enumerate(edges):
        if liq < e:
            return i
    return len(edges)


def by_bucket(rows, edges, k):
    out = [[] for _ in range(k)]
    for _, liq, y in rows:
        out[bucket(liq, edges)].append(y)
    return out


def pooled(groups):
    means = [st.mean(g) for g in groups]
    se2 = [st.variance(g) / len(g) for g in groups]
    n = sum(len(g) for g in groups)
    grand = sum(sum(g) for g in groups) / n
    tau2 = max(0.0, st.variance(means) - st.mean(se2))
    est = []
    for m, v in zip(means, se2):
        w = tau2 / (tau2 + v) if tau2 + v > 0 else 0.0
        est.append(grand + w * (m - grand))
    return means, est, grand, tau2, se2


def mse(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) / len(a)


def winsor(rows, lo, hi):
    ys = sorted(y for _, _, y in rows)
    a, b = ys[int(len(ys) * lo)], ys[int(len(ys) * hi) - 1]
    return [(t, l, min(max(y, a), b)) for t, l, y in rows]


def run(rows, k):
    half = len(rows) // 2
    first, second = rows[:half], rows[half:]
    edges = edges_for([l for _, l, _ in first], k)
    g1, g2 = by_bucket(first, edges, k), by_bucket(second, edges, k)
    raw, pool, grand, tau2, se2 = pooled(g1)
    target = [st.mean(g) for g in g2]
    # shape only: each half's own grand mean removed, so a level shift between halves does not count
    g2_grand = sum(sum(g) for g in g2) / len(second)
    d_raw = [x - grand for x in raw]
    d_pool = [x - grand for x in pool]
    d_target = [x - g2_grand for x in target]
    return {
        "shape_mse_raw": round(mse(d_raw, d_target), 2),
        "shape_mse_pooled": round(mse(d_pool, d_target), 2),
        "shape_mse_flat": round(mse([0.0] * k, d_target), 2),
        "shape_ratio_pooled_raw": round(mse(d_pool, d_target) / mse(d_raw, d_target), 3),
        "k": k,
        "n_first": len(first),
        "n_second": len(second),
        "grand_first": round(grand, 2),
        "tau2": round(tau2, 2),
        "mean_se2": round(st.mean(se2), 2),
        "mse_raw": round(mse(raw, target), 2),
        "mse_pooled": round(mse(pool, target), 2),
        "mse_grand": round(mse([grand] * k, target), 2),
        "ratio_pooled_raw": round(mse(pool, target) / mse(raw, target), 3),
        "raw": [round(x, 2) for x in raw],
        "pooled": [round(x, 2) for x in pool],
        "target": [round(x, 2) for x in target],
    }


def main():
    rows = load(sys.argv[1])
    out = {"n": len(rows), "runs": {}}
    for label, data in (("raw_pct", rows), ("winsor_1_99", winsor(rows, 0.01, 0.99))):
        for k in (10, 20):
            out["runs"][f"{label}_k{k}"] = run(data, k)
    with open(sys.argv[2], "w") as f:
        json.dump(out, f, indent=1)
    for name, r in out["runs"].items():
        print(name, "n", r["n_first"], r["n_second"], "tau2", r["tau2"], "se2", r["mean_se2"],
              "mse raw", r["mse_raw"], "pooled", r["mse_pooled"], "grand", r["mse_grand"],
              "ratio", r["ratio_pooled_raw"], "| shape raw", r["shape_mse_raw"], "pooled",
              r["shape_mse_pooled"], "flat", r["shape_mse_flat"], "ratio", r["shape_ratio_pooled_raw"])


main()
