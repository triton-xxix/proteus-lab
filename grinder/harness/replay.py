#!/usr/bin/env python3
"""Replay the variants in grinder/harness/VARIANTS.md over every snapshot row that passed the v0.2
gates. In-sample: it can earn a variant a second paper book, never a result (PASS-MARKS.md).

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/grinder/harness/replay.py [--no-fetch]

Writes grinder/harness/REPLAY.md and REPLAY.csv. Candles are cached under grinder/harness/candles/.
"""
import csv
import os
import statistics as st
import sys
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import paper  # noqa: E402
import paths  # noqa: E402

CANDLES = HERE + "/candles/"
N_VARIANTS = 29
H = 3600
# id: (entry delay min, take-profit, stop, trail, time stop h). None = off.
VARIANTS = {
    "V01": (0, 1.00, -0.50, None, 24), "V02": (0, 0.30, -0.20, None, 24), "V03": (0, 0.30, -0.30, None, 24),
    "V04": (0, 0.30, -0.50, None, 24), "V05": (0, 0.50, -0.20, None, 24), "V06": (0, 0.50, -0.30, None, 24),
    "V07": (0, 0.50, -0.50, None, 24), "V08": (0, 1.00, -0.20, None, 24), "V09": (0, 1.00, -0.30, None, 24),
    "V10": (0, 2.00, -0.20, None, 24), "V11": (0, 2.00, -0.30, None, 24), "V12": (0, 2.00, -0.50, None, 24),
    "V13": (0, None, -0.50, 0.20, 24), "V14": (0, None, -0.50, 0.30, 24), "V15": (0, None, -0.50, 0.40, 24),
    "V16": (0, None, None, None, 1), "V17": (0, None, None, None, 4), "V18": (0, None, None, None, 12),
    "V19": (0, None, None, None, 24),
    "V20": (15, 1.00, -0.50, None, 24), "V21": (30, 1.00, -0.50, None, 24), "V22": (60, 1.00, -0.50, None, 24),
    "V23": (120, 1.00, -0.50, None, 24), "V24": (240, 1.00, -0.50, None, 24), "V25": (480, 1.00, -0.50, None, 24),
    "V26": (0, None, -0.20, 0.20, 24), "V27": (0, None, -0.20, 0.30, 24), "V28": (0, 0.50, -0.20, 0.20, 24),
    "V29": (0, 0.50, -0.20, None, 4),
}
assert len(VARIANTS) == N_VARIANTS


def ts_of(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()


def population(now):
    rows = list(csv.DictReader(open(paths.SNAPS)))
    nights = sorted({r["ts"] for r in rows})
    seen, out = set(), []
    for n in nights:
        if ts_of(n) + (24 + 8) * H > now:          # window (incl. the 8h delay variant) not closed yet
            continue
        for r in rows:
            if r["ts"] == n and r["mint"] not in seen and paper.passes(r):
                seen.add(r["mint"]); out.append(r)
    return out


def candles(r, fetch):
    key = "%s_%s" % (r["mint"][:16], r["ts"][:10])
    p = CANDLES + key + ".csv"
    if os.path.exists(p):
        return [[float(x) for x in row] for row in list(csv.reader(open(p)))[1:]]
    if not fetch:
        return None
    t0 = ts_of(r["ts"])
    c = paths.fetch(r["pair"], (int(t0) // 60 + 1) * 60, t0 + (24 + 8) * H)
    if c is None:
        return None
    os.makedirs(CANDLES, exist_ok=True)
    with open(p, "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["ts", "o", "h", "l", "c", "v"]); w.writerows(c)
    return c


def walk(c, entry, t_entry, tp, sl, trail, hold_h):
    """paths.walk generalised: optional TP, fixed stop, trailing stop, time stop. Same pessimism."""
    horizon = t_entry + hold_h * H
    rug = entry * (1 + paths.RUG_DROP)
    top = entry
    for ts, o, h, l, cl, v in c:
        if ts < t_entry:
            continue
        if ts >= horizon:
            break
        stop, reason = None, "stop_loss"
        if sl is not None:
            stop = entry * (1 + sl)
        if trail is not None and top > entry:
            lvl = top * (1 - trail)
            if stop is None or lvl > stop:
                stop, reason = lvl, "trail_stop"
        if l <= rug and (stop is None or rug <= stop):
            stop_hit = True
        else:
            stop_hit = stop is not None and l <= stop
        if stop_hit or l <= rug:
            if l <= rug:
                lvl = stop if stop is not None else rug
                return ts, min(cl, o if o <= lvl else lvl), "rug"
            fill = o if o <= stop else stop
            return ts, fill, reason
        if tp is not None and h >= entry * (1 + tp):
            return ts, max(o, entry * (1 + tp)), "take_profit"
        top = max(top, h)
    last = [x for x in c if t_entry <= x[0] < horizon]
    return (last[-1][0], last[-1][4], "time_stop") if last else (horizon, entry, "time_stop")


def run_variant(vid, pop):
    delay, tp, sl, trail, hold = VARIANTS[vid]
    out = []
    for r, c in pop:
        if not c:
            continue
        t0 = ts_of(r["ts"]); entry = paper.fnum(r["price_usd"])
        if delay:
            after = [x for x in c if x[0] >= t0 + delay * 60]
            if not after:
                continue
            t0, entry = after[0][0], after[0][1]
        ts, fill, reason = walk(c, entry, t0, tp, sl, trail, hold)
        slip_reason = "stop_loss" if reason == "trail_stop" else reason
        pnl = paths.pnl_v02(entry, fill, slip_reason, 100.0, paper.fnum(r["liq_usd"]))
        out.append({"night": r["ts"][:10], "mint": r["mint"], "symbol": r["symbol"], "vol_h1": paper.fnum(r["vol_h1"]) or 0,
                    "reason": reason, "move": fill / entry - 1, "pnl": pnl})
    return out


def stats(res):
    p = sorted(x["pnl"] for x in res)
    if not p:
        return dict(n=0, total=0, exp=0, trim3=0, win=0, rug=0)
    trim = p[:-3] if len(p) > 3 else []
    return dict(n=len(p), total=round(sum(p), 1), exp=round(st.mean(p), 1), trim3=round(st.mean(trim), 1) if trim else 0,
                win=sum(1 for x in p if x > 0), rug=sum(1 for x in res if x["reason"] == "rug"))


def top_k(res, k):
    by = {}
    for x in res:
        by.setdefault(x["night"], []).append(x)
    return [x for n in by for x in sorted(by[n], key=lambda y: -y["vol_h1"])[:k]]


def main():
    fetch = "--no-fetch" not in sys.argv
    pop_rows = population(time.time())
    pop, missing = [], 0
    for i, r in enumerate(pop_rows):
        c = candles(r, fetch)
        if not c:
            missing += 1
        pop.append((r, c))
        print("candles %d/%d %s %s" % (i + 1, len(pop_rows), r["symbol"], "ok" if c else "MISSING"), flush=True)
    results = {v: run_variant(v, pop) for v in VARIANTS}
    base = stats(results["V01"])
    bar = base["exp"] + 10 + (N_VARIANTS - 10)
    lines = ["# Grinder replay", "",
             "Run %s. In-sample: earns a second book at most, never a result. Variants and rules: `VARIANTS.md`." % datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%MZ"),
             "", "Population: %d first-pass rows from %d nights; %d without candles. £100 stake, v0.2 costs and fill rule." % (
                 len(pop_rows), len({r['ts'] for r in pop_rows}), missing),
             "Bar for a second book (item 3): n at least 40, expectancy at least +10, best-three-removed at or above 0, and at least %.1f (V01 %.1f + 10 + %d)." % (bar, base["exp"], N_VARIANTS - 10),
             "", "| Variant | Params | n | Total £ | Exp £ | Exp less best 3 | Wins | Rugs | Top-4/night exp (n) | Top-8/night exp (n) | Qualifies |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    csvrows, qual = [], []
    for v, res in results.items():
        s = stats(res); s4 = stats(top_k(res, 4)); s8 = stats(top_k(res, 8))
        ok = s["n"] >= 40 and s["exp"] >= 10 and s["trim3"] >= 0 and s["exp"] >= bar
        if ok:
            qual.append((s["trim3"], v))
        d, tp, sl, tr, hold = VARIANTS[v]
        par = "delay %d, TP %s, SL %s, trail %s, %dh" % (d, "%+d%%" % (tp * 100) if tp else "-", "%d%%" % (sl * 100) if sl else "-", "%d%%" % (tr * 100) if tr else "-", hold)
        lines.append("| %s | %s | %d | %.1f | %.1f | %.1f | %d | %d | %.1f (%d) | %.1f (%d) | %s |" % (
            v, par, s["n"], s["total"], s["exp"], s["trim3"], s["win"], s["rug"], s4["exp"], s4["n"], s8["exp"], s8["n"], "yes" if ok else "no"))
        csvrows.append(dict(variant=v, params=par, **s, top4_exp=s4["exp"], top4_n=s4["n"], top8_exp=s8["exp"], top8_n=s8["n"], qualifies=ok))
    lines += ["", "Qualifying: %s." % (", ".join(v for _, v in sorted(qual, reverse=True)) or "none"),
              "Opens a second book: %s." % (max(qual)[1] if qual else "none")]
    # the population's shape, for the write-up
    b = results["V19"]
    if b:
        moves = sorted(x["move"] for x in b)
        lines += ["", "Hold-24h moves over the population: median %+.0f%%, quartiles %+.0f%% and %+.0f%%, %d of %d up." % (
            100 * st.median(moves), 100 * moves[len(moves) // 4], 100 * moves[3 * len(moves) // 4], sum(1 for m in moves if m > 0), len(moves))]
    open(HERE + "/REPLAY.md", "w").write("\n".join(lines) + "\n")
    with open(HERE + "/REPLAY.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(csvrows[0].keys())); w.writeheader(); w.writerows(csvrows)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
