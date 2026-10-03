#!/usr/bin/env python3
"""Every book with a pre-registered kill line, judged against it, one line each.

Written 3 Oct 2026 after the graduation book crossed its KILL line and the nightly only printed the
number. The point is the word: KILL, KEEP, CHANGE or RUNNING, said out loud every night.
Read-only. `--log` appends the lines to today's run log.

Books: the graduation book (closed, G1) and G2 (grinder/graduates/RULES.md), the judgement book's
anchored and blind columns (PASS-MARKS.md), the exchange book (exchange/RULES.md). The Grinder and the Pitch are judged at the week-8
review by bin/review.py, which has no nightly kill line to check.
"""
import csv
import json
import statistics
import sys
from datetime import date
from pathlib import Path

ROOT = Path("/Users/triton/PROTEUS")
G2_FROM = 1791028800  # 2026-10-03T12:00:00Z


def grad(rows, name, min_liq, since, closed_word=None):
    xs = sorted(r["P"] for r in rows
                if r.get("latency_s") is not None and r["latency_s"] <= 120
                and (r.get("liq") or 0) >= min_liq and r["block_t"] >= since and r.get("P") is not None)
    n = len(xs)
    if not n:
        return f"{name}: RUNNING, 0 counted"
    exp = statistics.mean(xs)
    less10 = statistics.mean(xs[:-10]) if n > 20 else float("nan")
    bad = sum(x <= -50 for x in xs) / n
    nums = f"{n} counted, expectancy £{exp:+.2f}, best-10 removed £{less10:+.2f}, at or below -50%: {bad:.0%}"
    if closed_word:
        return f"{name}: {closed_word} (closed). {nums}"
    if n >= 400:
        if exp >= 10 and less10 >= 0 and bad <= 0.25:
            word = "KEEP"
        else:
            word = "KILL"  # G2 has no CHANGE outcome
    elif n >= 200 and exp <= -10:
        word = "KILL"
    else:
        word = f"RUNNING ({400 - n} to the 400 floor)"
    return f"{name}: {word}. {nums}"


def judgement():
    rows = list(csv.DictReader(open(ROOT / "pitch/JUDGEMENT.csv")))
    out = []
    a = [r for r in rows if int(r["id"][2:]) >= 9 and r["brier"] and r["market_brier"]
         and r["committed_at"] < r["kickoff_utc"]]
    d = [float(r["brier"]) - float(r["market_brier"]) for r in a]
    lean = [float(r["brier"]) - float(r["market_brier"]) for r in a if r["lean_size"] and float(r["lean_size"]) >= 0.03]
    n = len(d)
    m = statistics.mean(d) if d else float("nan")
    ml = statistics.mean(lean) if lean else float("nan")
    if n >= 60 and m >= 0.010 or n >= 100 and not m <= -0.005:
        word = "KILL"
    elif n >= 60 and m <= -0.005 and lean and ml <= -0.005:
        word = "KEEP"
    else:
        word = f"RUNNING ({max(0, 60 - n)} to the 60 floor)"
    out.append(f"Judgement book, anchored: {word}. {n} counted, me minus market {m:+.4f} "
               f"(KILL at +0.010, KEEP at -0.005); leaned rows {len(lean)}, {ml:+.4f}")
    b = [r for r in rows if r["blind_brier"] and r["market_brier"] and r["blind_committed_at"]
         and r["blind_committed_at"] < (r["odds_seen_at"] or "9") and r["blind_committed_at"] < r["kickoff_utc"]]
    db = [float(r["blind_brier"]) - float(r["market_brier"]) for r in b]
    nb = len(db)
    mb = statistics.mean(db) if db else float("nan")
    if nb >= 60 and mb >= 0.020 or nb >= 100 and mb > 0:
        word = "KILL"
    elif nb >= 60 and mb <= 0:
        word = "KEEP"
    else:
        word = f"RUNNING ({max(0, 60 - nb)} to the 60 floor)"
    out.append(f"Judgement book, blind: {word}. {nb} counted, blind minus market {mb:+.4f} (KILL at +0.020, KEEP at 0.000)")
    return out


def exchange():
    p = ROOT / "exchange/BOOK.csv"
    rows = list(csv.DictReader(open(p))) if p.exists() else []
    s = [r for r in rows if r.get("brier") and r.get("market_brier") and r.get("mid_at") and r["committed_at"] < r["mid_at"]]
    n = len(s)
    m = statistics.mean(float(r["brier"]) - float(r["market_brier"]) for r in s) if s else float("nan")
    if n >= 60 and m >= 0.020 or n >= 100 and m > 0:
        word = "KILL"
    elif n >= 60 and m <= 0:
        word = "KEEP"
    else:
        word = f"RUNNING ({max(0, 60 - n)} to the 60 floor)"
    return f"Exchange book: {word}. {len(rows)} calls, {n} settled, me minus market {m:+.4f} (KILL at +0.020, KEEP at 0.000)"


def main():
    rows = [json.loads(l) for l in open(ROOT / "grinder/graduates/closed.jsonl")]
    lines = [grad(rows, "Graduation book G1", 5000, 0, closed_word="KILL"),
             grad(rows, "Graduation book G2 (liq >= $50k, from 3 Oct 12:00Z)", 50000, G2_FROM)]
    lines += judgement()
    lines.append(exchange())
    for l in lines:
        print(l)
    if "--log" in sys.argv:
        with open(ROOT / f"state/runs/{date.today().isoformat()}.md", "a") as f:
            f.write("- Kill check: " + " | ".join(lines) + "\n")


if __name__ == "__main__":
    main()
