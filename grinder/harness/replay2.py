#!/usr/bin/env python3
"""Round-2 replay: the entry-rule variants of grinder/harness/VARIANTS-2.md (E01-E06, M01-M09),
each at exits V01 (TP +100 / SL -50 / 24h) and V17 (hold 4h), over every snapshot row that
passed the v0.2 gates (plus the age-over-48h rows for E06), joined to grinder/research/MENTIONS.csv.

Pre-registered 30 Sep 2026; first run 8 Oct 2026. Seen variants (E01-E06, M05-M09) count only
snapshots at or after 2026-09-30T12:00Z; M01-M04 count everything. X variants count only rows
with an X measurement (after 30 Sep the X pull is capped at 8 tokens a night, so "no X row" is
unmeasured, not silent). Bar (VARIANTS-2.md, N = 59): n >= 40, expectancy >= +10, best-three
removed >= 0, and expectancy >= V01 on the same rows + 10 + 49.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/grinder/harness/replay2.py [--no-fetch]

Writes grinder/harness/REPLAY-2.md and REPLAY-2.csv.
"""
import csv
import os
import statistics as st
import sys
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import paper  # noqa: E402
import paths  # noqa: E402
import replay  # noqa: E402

MENTIONS = os.path.dirname(HERE) + "/research/MENTIONS.csv"
SEEN_FROM = replay.ts_of("2026-09-30T12:00:00Z")
N_TOTAL = 59
EXITS = ("V01", "V17")
f = paper.fnum


def population(now):
    """Gate-passers as replay.population, plus rows that fail only the age gate with age > 48h (E06)."""
    rows = list(csv.DictReader(open(paths.SNAPS)))
    nights = sorted({r["ts"] for r in rows})
    seen, out = set(), []
    for n in nights:
        if replay.ts_of(n) + (24 + 8) * replay.H > now:
            continue
        for r in rows:
            if r["ts"] != n or r["mint"] in seen:
                continue
            if paper.passes(r):
                seen.add(r["mint"]); r["_grp"] = "pass"; out.append(r)
            else:
                others = all(g(r) for k, g in paper.GATES.items() if k != "age")
                age = f(r.get("age_h"))
                if others and age is not None and age > paper.RULES["age_h_max"]:
                    seen.add(r["mint"]); r["_grp"] = "old"; out.append(r)
    return out


def mentions():
    m = {}
    for r in csv.DictReader(open(MENTIONS)):
        m.setdefault((r["mint"], r["night"]), {})[r["source"]] = r
    return m


def x_of(r, m):
    return m.get((r["mint"], r["ts"][:10]), {}).get("x")


def src_count(r, m, src):
    s = m.get((r["mint"], r["ts"][:10]), {}).get(src)
    return None if s is None else (f(s.get("count")) or 0)


def paid_before(r, m):
    s = m.get((r["mint"], r["ts"][:10]), {}).get("dexpaid")
    if s is None:
        return None
    return (f(s.get("paid")) or 0) > 0 or "paid-before-asof 0" not in (s.get("detail") or "paid-before-asof 0")


def e01(r): return (f(r.get("chg_h1")) or 0) <= 0
def e02(r): return not (r.get("rug_risks") or "").strip()
def e04(r):
    age, v1, liq = f(r.get("age_h")), f(r.get("vol_h1")) or 0, f(r.get("liq_usd")) or 0
    return age is not None and age >= 12 and v1 <= liq and e02(r)


def variants(m):
    """id -> (predicate(row) -> True/False/None (None = unmeasured, excluded), seen_only, group)."""
    def xa(r):
        x = x_of(r, m); return None if x is None else (f(x.get("authors")) or 0)
    def xs(r):
        x = x_of(r, m); return None if x is None else f(x.get("shill_share"))
    def xc(r):
        x = x_of(r, m); return None if x is None else (f(x.get("count")) or 0)
    def tg(r): return src_count(r, m, "telegram")
    def rd(r): return src_count(r, m, "reddit")
    def nn(v, pred): return None if v is None else pred(v)
    return {
        "E01": (e01, True, "pass"), "E02": (e02, True, "pass"), "E03": (lambda r: e01(r) and e02(r), True, "pass"),
        "E04": (e04, True, "pass"), "E05": (lambda r: e01(r) and e04(r), True, "pass"),
        "E06": (lambda r: True, True, "old"),
        "M01": (lambda r: nn(xa(r), lambda v: v >= 10), False, "pass"),
        "M02": (lambda r: nn(xa(r), lambda v: v <= 3), False, "pass"),
        "M03": (lambda r: nn(xs(r), lambda v: v <= 0.5), False, "pass"),
        "M04": (lambda r: nn(rd(r), lambda v: v >= 1), False, "pass"),
        "M05": (lambda r: nn(paid_before(r, m), lambda v: not v), True, "pass"),
        "M06": (lambda r: nn(xs(r), lambda v: v <= 0.5 and e01(r)), True, "pass"),
        "M07": (lambda r: nn(xc(r), lambda v: v >= 1), True, "pass"),
        "M08": (lambda r: None if xc(r) is None or tg(r) is None else (xc(r) >= 1 and tg(r) >= 1), True, "pass"),
        "M09": (lambda r: nn(tg(r), lambda v: v >= 1), True, "pass"),
    }


def main():
    fetch = "--no-fetch" not in sys.argv
    now = time.time()
    pop_rows = population(now)
    pop, missing = [], 0
    for i, r in enumerate(pop_rows):
        c = replay.candles(r, fetch)
        if not c:
            missing += 1
        pop.append((r, c))
        if fetch:
            print("candles %d/%d %s %s %s" % (i + 1, len(pop_rows), r["ts"][:10], r["symbol"], "ok" if c else "MISSING"), flush=True)
    m = mentions()
    # exits over the whole population, keyed by (mint, night)
    res = {}
    for ex in EXITS:
        for x in replay.run_variant(ex, pop):
            res[(ex, x["mint"], x["night"])] = x
    V = variants(m)
    lines = ["# Grinder replay, round 2: what gets bought", "",
             "Run %s. Pre-registered 30 Sep 2026 (`VARIANTS-2.md`), first run 8 Oct 2026. In-sample: earns a second book at most." % datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%MZ"),
             "", "Population: %d gate-passers and %d age-over-48h rows from %d nights, %d without candles; %d rows at or after 30 Sep 12:00Z. £100 stake, v0.2 costs and fill rule." % (
                 sum(1 for r in pop_rows if r["_grp"] == "pass"), sum(1 for r in pop_rows if r["_grp"] == "old"), len({r["ts"][:10] for r in pop_rows}), missing,
                 sum(1 for r in pop_rows if replay.ts_of(r["ts"]) >= SEEN_FROM)),
             "Bar: n >= 40, exp >= +10, best-3 removed >= 0, exp >= V01 on the same rows + %d. Rows: measured = the variant's signal exists for the row; n = rows the rule selects." % (10 + N_TOTAL - 10),
             "", "| Variant | Exit | Measured | n | Total £ | Exp £ | Exp less best 3 | Wins | Rugs | Up at 24h | V01 same rows | Bar | Qualifies |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    csvrows, qual = [], []
    for vid, (pred, seen_only, grp) in V.items():
        base_rows = [(r, c) for r, c in pop if c and r["_grp"] == grp and (not seen_only or replay.ts_of(r["ts"]) >= SEEN_FROM)]
        measured = [(r, c) for r, c in base_rows if pred(r) is not None]
        chosen = [(r, c) for r, c in measured if pred(r)]
        for ex in EXITS:
            sel = [res[(ex, r["mint"], r["ts"][:10])] for r, c in chosen if (ex, r["mint"], r["ts"][:10]) in res]
            same_v01 = [res[("V01", r["mint"], r["ts"][:10])] for r, c in chosen if ("V01", r["mint"], r["ts"][:10]) in res]
            s = replay.stats(sel)
            v01_exp = replay.stats(same_v01)["exp"] if same_v01 else 0
            bar = v01_exp + 10 + (N_TOTAL - 10)
            up = sum(1 for x in sel if x["reason"] == "time_stop" and x["move"] > 0) if ex == "V19" else None
            ok = s["n"] >= 40 and s["exp"] >= 10 and s["trim3"] >= 0 and s["exp"] >= bar
            if ok:
                qual.append((s["trim3"], vid + "/" + ex))
            lines.append("| %s | %s | %d | %d | %.1f | %.1f | %.1f | %d | %d | %s | %.1f | %.1f | %s |" % (
                vid, ex, len(measured), s["n"], s["total"], s["exp"], s["trim3"], s["win"], s["rug"], "-" if up is None else up, v01_exp, bar, "yes" if ok else "no"))
            csvrows.append(dict(variant=vid, exit=ex, measured=len(measured), **s, v01_same=v01_exp, bar=round(bar, 1), qualifies=ok))
        # the complement, for reading
        rest = [(r, c) for r, c in measured if not pred(r)]
        for ex in EXITS:
            sel = [res[(ex, r["mint"], r["ts"][:10])] for r, c in rest if (ex, r["mint"], r["ts"][:10]) in res]
            s = replay.stats(sel)
            lines.append("| %s not | %s | %d | %d | %.1f | %.1f | %.1f | %d | %d | - | - | - | - |" % (vid, ex, len(measured), s["n"], s["total"], s["exp"], s["trim3"], s["win"], s["rug"]))
    # baseline on the seen window
    for ex in EXITS:
        sel = [res[(ex, r["mint"], r["ts"][:10])] for r, c in pop if c and r["_grp"] == "pass" and replay.ts_of(r["ts"]) >= SEEN_FROM and (ex, r["mint"], r["ts"][:10]) in res]
        s = replay.stats(sel)
        lines.append("| all passers since 30 Sep | %s | %d | %d | %.1f | %.1f | %.1f | %d | %d | - | - | - | - |" % (ex, s["n"], s["n"], s["total"], s["exp"], s["trim3"], s["win"], s["rug"]))
    lines += ["", "Qualifying: %s." % (", ".join(v for _, v in sorted(qual, reverse=True)) or "none"),
              "Opens a second book: %s." % (max(qual)[1] if qual else "none")]
    open(HERE + "/REPLAY-2.md", "w").write("\n".join(lines) + "\n")
    with open(HERE + "/REPLAY-2.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(csvrows[0].keys())); w.writeheader(); w.writerows(csvrows)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
