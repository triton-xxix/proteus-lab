#!/usr/bin/env python3
"""Every book with a pre-registered kill line, judged against it, one line each.

Written 3 Oct 2026 after the graduation book crossed its KILL line and the nightly only printed the
number. The point is the word: KILL, KEEP, CHANGE or RUNNING, said out loud every night.
Read-only. `--log` appends the lines to today's run log.

Books: the graduation book (closed, G1) and G2 (grinder/graduates/RULES.md), the judgement book's
anchored and blind columns (PASS-MARKS.md), the exchange book (exchange/RULES.md), the Grinder R01 shadow book (grinder/harness/VARIANTS-3.md), the systems book (systems/RULES.md). The Grinder and the Pitch are judged at the week-8
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


def grad(rows, name, min_liq, since, closed_word=None, withdrawn=None):
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
            # a later pre-registered check can withdraw a KEEP; the lines stay, the word says so (F-0002)
            word = f"KEEP withdrawn ({withdrawn}), nothing graduates" if withdrawn else "KEEP"
        else:
            word = "KILL"  # G2 has no CHANGE outcome
    elif n >= 200 and exp <= -10:
        word = "KILL"
    else:
        word = f"RUNNING ({400 - n} to the 400 floor)"
    return f"{name}: {word}. {nums}"


def se(xs):
    """Standard error of the mean, shown beside a Brier gap so a verdict near its line reads as noise
    when it is (W42 read-it, Foresight Arena power sum). Display only; no verdict uses it."""
    return statistics.stdev(xs) / len(xs) ** 0.5 if len(xs) > 1 else float("nan")


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
    out.append(f"Judgement book, anchored: {word}. {n} counted, me minus market {m:+.4f} (se {se(d):.4f}) "
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
    out.append(f"Judgement book, blind: {word}. {nb} counted, blind minus market {mb:+.4f} (se {se(db):.4f}) (KILL at +0.020, KEEP at 0.000)")
    return out


def exchange():
    p = ROOT / "exchange/BOOK.csv"
    rows = list(csv.DictReader(open(p))) if p.exists() else []
    s = [r for r in rows if r.get("brier") and r.get("market_brier") and r.get("mid_at") and r["committed_at"] < r["mid_at"]]
    n = len(s)
    d = [float(r["brier"]) - float(r["market_brier"]) for r in s]
    m = statistics.mean(d) if d else float("nan")
    if n >= 60 and m >= 0.020 or n >= 100 and m > 0:
        word = "KILL"
    elif n >= 60 and m <= 0:
        word = "KEEP"
    else:
        word = f"RUNNING ({max(0, 60 - n)} to the 60 floor)"
    return f"Exchange book: {word}. {len(rows)} calls, {n} settled, me minus market {m:+.4f} (se {se(d):.4f}) (KILL at +0.020, KEEP at 0.000)"


def r01():
    """The Grinder R01 shadow book (grinder/harness/VARIANTS-3.md, wired 13 Oct 2026 by P-0121), against
    v0.2's closed positions entered on the same nights. KILL at 20 if R01's rug rate is v0.2's or worse;
    at 40 KEEP only if rug rate is at most half v0.2's, expectancy at or above v0.2's and expectancy with
    the best three removed at or above zero; anything else at 40 is KILL. Read literally, as registered."""
    p = ROOT / "grinder/LEDGER-R01.csv"
    rows = [r for r in csv.DictReader(open(p)) if r.get("exit_at") and r.get("pnl_gbp")] if p.exists() else []
    nights = {r["entered_at"][:10] for r in rows}
    v02 = [r for r in csv.DictReader(open(ROOT / "grinder/LEDGER.csv"))
           if r.get("rule_version") == "v0.2" and r.get("exit_at") and r.get("pnl_gbp") and r["entered_at"][:10] in nights]
    n, nv = len(rows), len(v02)
    if not n:
        return "Grinder R01 shadow book: RUNNING (40 to the 40 mark). 0 closed"
    pnl = sorted(float(r["pnl_gbp"]) for r in rows)
    exp = statistics.mean(pnl)
    exp3 = statistics.mean(pnl[:-3]) if n > 3 else float("nan")
    rug = sum(r.get("rugged") == "1" for r in rows) / n
    exp_v = statistics.mean(float(r["pnl_gbp"]) for r in v02) if v02 else float("nan")
    rug_v = sum(r.get("rugged") == "1" for r in v02) / nv if nv else float("nan")
    if n >= 40:
        word = "KEEP" if (rug <= rug_v / 2 and exp >= exp_v and exp3 >= 0) else "KILL"
    elif n >= 20 and rug >= rug_v:
        word = "KILL (rug rate at 20)" + (", both rug rates 0: the line reads a tie as KILL" if rug == rug_v == 0 else "")
    else:
        word = f"RUNNING ({40 - n} to the 40 mark" + (f", {20 - n} to the 20 rug check)" if n < 20 else ")")
    return (f"Grinder R01 shadow book: {word}. {n} closed, expectancy £{exp:+.2f}, best-3 removed £{exp3:+.2f}, "
            f"rugs {rug:.0%} | v0.2 same nights: {nv} closed, expectancy £{exp_v:+.2f}, rugs {rug_v:.0%}")


def systems():
    """The systems book (systems/RULES.md, 7 Oct 2026). Its marks live beside its data in systems.py."""
    sys.path.insert(0, str(ROOT / "systems"))
    try:
        import systems as book
        return [book.verdict(), book.verdict2()]
    except Exception as e:
        return [f"Systems book: could not judge ({type(e).__name__}: {e})"]


def main():
    rows = [json.loads(l) for l in open(ROOT / "grinder/graduates/closed.jsonl")]
    lines = [grad(rows, "Graduation book G1", 5000, 0, closed_word="KILL"),
             grad(rows, "Graduation book G2 (liq >= $50k, from 3 Oct 12:00Z)", 50000, G2_FROM,
                  withdrawn="D-009 fill realism 11 Oct, RULES.md")]
    lines += judgement()
    lines.append(exchange())
    lines.append(r01())
    lines += systems()
    for l in lines:
        print(l)
    if "--log" in sys.argv:
        with open(ROOT / f"state/runs/{date.today().isoformat()}.md", "a") as f:
            f.write("- Kill check: " + " | ".join(lines) + "\n")


if __name__ == "__main__":
    main()
