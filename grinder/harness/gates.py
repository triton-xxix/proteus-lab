#!/usr/bin/env python3
"""What each gate is worth: replay the tokens that failed exactly one v0.2 gate (near-misses), under
the current exits (V01) and a 24h hold (V19), and compare with the 58 that passed. Descriptive and
in-sample; a gate change still goes through VARIANTS.md and the replay bar.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/grinder/harness/gates.py [--max-fail 1]

Writes grinder/harness/GATES.md and GATES.csv. Candles cached with replay.py's.
"""
import csv
import os
import statistics as st
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import paper  # noqa: E402
import paths  # noqa: E402
import replay  # noqa: E402

MAXF = int(sys.argv[sys.argv.index("--max-fail") + 1]) if "--max-fail" in sys.argv else 1


def first_pass(now):
    rows = list(csv.DictReader(open(paths.SNAPS)))
    seen, out = set(), []
    for n in sorted({r["ts"] for r in rows}):
        if replay.ts_of(n) + 32 * 3600 > now:
            continue
        for r in rows:
            if r["ts"] == n and r["mint"] not in seen:
                seen.add(r["mint"]); out.append(r)
    return out


def main():
    rows = first_pass(time.time())
    pop = []
    for r in rows:
        failed = [g for g, fn in paper.GATES.items() if not fn(r)]
        if len(failed) <= MAXF and r.get("pair"):
            pop.append((r, failed))
    out = []
    for i, (r, failed) in enumerate(pop):
        c = replay.candles(r, True)
        print("candles %d/%d %s %s" % (i + 1, len(pop), r["symbol"], "ok" if c else "MISSING"), flush=True)
        if not c:
            continue
        e = paper.fnum(r["price_usd"]); t0 = replay.ts_of(r["ts"])
        rec = {"night": r["ts"][:10], "mint": r["mint"], "symbol": r["symbol"], "failed": "+".join(failed) or "passed"}
        for vid in ("V01", "V17", "V19"):
            d, tp, sl, tr, hold = replay.VARIANTS[vid]
            ts, fill, reason = paths.walk_rules(c, e, t0, time.time(), tp, sl, tr, hold)
            rec[vid] = paths.pnl_v02(e, fill, reason, 100.0, paper.fnum(r["liq_usd"]))
        hi = max(x[2] for x in c if x[0] < t0 + 24 * 3600)
        last = [x for x in c if x[0] < t0 + 24 * 3600][-1][4]
        rec["peak_pct"] = round(100 * (hi / e - 1), 1); rec["move24_pct"] = round(100 * (last / e - 1), 1)
        out.append(rec)
    groups = {}
    for x in out:
        groups.setdefault(x["failed"], []).append(x)
    L = ["# What each gate is worth", "",
         "Tokens that failed exactly %s of the v0.2 gates, replayed on their own minute candles at v0.2 costs, beside the ones that passed. In-sample, descriptive." % ("one" if MAXF == 1 else "up to %d" % MAXF), "",
         "| Group | n | V01 exp £ (TP+100/SL-50) | V17 exp £ (hold 4h) | V19 exp £ (hold 24h) | median 24h move | median peak | up at 24h |",
         "|---|---|---|---|---|---|---|---|"]
    for g, xs in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        L.append("| %s | %d | %.1f | %.1f | %.1f | %+.0f%% | %+.0f%% | %d |" % (
            g, len(xs), st.mean(x["V01"] for x in xs), st.mean(x["V17"] for x in xs), st.mean(x["V19"] for x in xs),
            st.median(x["move24_pct"] for x in xs), st.median(x["peak_pct"] for x in xs), sum(1 for x in xs if x["move24_pct"] > 0)))
    open(HERE + "/GATES.md", "w").write("\n".join(L) + "\n")
    with open(HERE + "/GATES.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
    print("\n".join(L))


if __name__ == "__main__":
    main()
