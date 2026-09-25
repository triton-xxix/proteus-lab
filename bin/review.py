#!/usr/bin/env python3
"""Compute the week-8 review verdicts from the committed ledgers against PASS-MARKS.md.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/bin/review.py

Prints a markdown block per desk: every numeric criterion in PASS-MARKS.md, the value, and
PASS / FAIL / INCONCLUSIVE, then the verdict the pass marks dictate. Nothing here is typed by
hand. The checks marked MANUAL cannot be computed from the ledgers and are listed so they are not
forgotten. Thresholds live in PASS-MARKS.md; the constants below must match it, and a change to
either is a dated change to both.
"""
import csv
import glob
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone

ROOT = "/Users/triton/PROTEUS/"

# ---- Dates (PASS-MARKS.md, "Dates") -------------------------------------------------------------
REVIEW_DATE = datetime(2026, 11, 15, tzinfo=timezone.utc)      # eighth Sunday after signing
SECOND_DATE = datetime(2026, 12, 13, tzinfo=timezone.utc)      # week 12, the only extension
PITCH_EDGE_DEADLINE = datetime(2027, 5, 31, tzinfo=timezone.utc)
PITCH_COVERAGE_FROM = datetime(2026, 10, 1, tzinfo=timezone.utc)
FIELD_NOTES_WEEKS = [(2026, w) for w in range(39, 47)]         # W39 (27 Sep) to W46 (15 Nov)

# ---- Grinder (PASS-MARKS.md, "The Grinder") -----------------------------------------------------
G_FLOOR = 40            # closed positions before any verdict
G_FLOOR_FINAL = 100     # closed positions after which "inconclusive" is no longer available
# Expectancy lines are shares of the stake since 2026-09-25 (same pence at v0.1's £5 stake).
# Only rows under the current rule version in grinder/BOOKS.json are judged.
G_KEEP_EXP = 0.10       # share of stake per position after costs
G_KILL_EXP = -0.10
G_MAX_RUG = 0.10
G_EXEC_N = 200
G_EXEC_EXP = 0.20
G_EXEC_EXP_TRIMMED = 0.10   # after removing the best three positions
G_EXEC_MAX_RUG = 0.05

# ---- Pitch (PASS-MARKS.md, "The Pitch") ---------------------------------------------------------
P_MIN_COVERAGE = 0.80
P_MAX_LATE_SHARE = 0.05
P_EARLY_N = 80
P_EARLY_KILL_DIFF = 0.015   # model Brier minus market Brier, paired mean
P_EDGE_N = 500
P_EDGE_DIFF = -0.005
P_INGREDIENT_WEIGHT = 0.10

# ---- Field Notes (PASS-MARKS.md, "Field Notes") -------------------------------------------------
F_KILL_CONSECUTIVE = 3
F_KILL_OF_EIGHT = 4


def fnum(x):
    try:
        return float(x)
    except Exception:
        return None


def iso(s):
    try:
        d = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def mark(ok):
    return {True: "PASS", False: "FAIL", None: "INCONCLUSIVE"}[ok]


# =================================================================================================
def grinder():
    books = json.load(open(ROOT + "grinder/BOOKS.json"))
    cur = books["current"]
    stake = books["books"][cur]["stake_gbp"]
    rows = [r for r in csv.DictReader(open(ROOT + "grinder/LEDGER.csv")) if r.get("rule_version") == cur]
    closed = [r for r in rows if fnum(r.get("pnl_gbp")) is not None]
    n = len(closed)
    out = ["## The Grinder", "", "Rule version %s, stake £%.2f. Earlier versions are their own books and are not judged here." % (cur, stake), "",
           "| Criterion | Threshold | Value | Result |", "|---|---|---|---|"]
    if n == 0:
        out += ["| Closed positions | >= %d | 0 | INCONCLUSIVE |" % G_FLOOR, "",
                "**Verdict: INCONCLUSIVE.** No closed positions. Change with a deadline (PASS-MARKS.md, Inconclusive)."]
        return out, "INCONCLUSIVE"
    pnl = sorted((fnum(r["pnl_gbp"]) for r in closed), reverse=True)
    exp = sum(pnl) / n
    exp_trim1 = sum(pnl[1:]) / max(1, n - 1)
    exp_trim3 = sum(pnl[3:]) / max(1, n - 3)
    keep_l, kill_l, ex_l, ex3_l = G_KEEP_EXP * stake, G_KILL_EXP * stake, G_EXEC_EXP * stake, G_EXEC_EXP_TRIMMED * stake
    rugs = sum(1 for r in closed if (r.get("rugged") or "").lower() in ("1", "true", "yes"))
    rug_rate = rugs / n
    versions = sorted({r.get("rule_version", "") for r in closed})
    half = n // 2
    exp_first = sum(fnum(r["pnl_gbp"]) for r in closed[:half]) / max(1, half)
    exp_second = sum(fnum(r["pnl_gbp"]) for r in closed[half:]) / max(1, n - half)

    floor_ok = n >= G_FLOOR
    out.append("| Closed positions | >= %d | %d | %s |" % (G_FLOOR, n, mark(floor_ok)))
    out.append("| Rule versions in sample | 1 | %s | %s |" % (", ".join(v or "?" for v in versions), mark(len(versions) == 1)))
    out.append("| Expectancy per position, after costs | >= £%.2f keep, <= £%.2f kill | £%.2f | %s |"
               % (keep_l, kill_l, exp, mark(None if not floor_ok else (exp >= keep_l if exp >= keep_l or exp <= kill_l else None))))
    out.append("| Expectancy without the best position | >= £0.00 | £%.2f | %s |" % (exp_trim1, mark(None if not floor_ok else exp_trim1 >= 0)))
    out.append("| Rug rate | <= %.0f%% | %.1f%% (%d) | %s |" % (100 * G_MAX_RUG, 100 * rug_rate, rugs, mark(None if not floor_ok else rug_rate <= G_MAX_RUG)))
    out.append("| Executor: closed positions | >= %d | %d | %s |" % (G_EXEC_N, n, mark(n >= G_EXEC_N)))
    out.append("| Executor: expectancy | >= £%.2f | £%.2f | %s |" % (ex_l, exp, mark(exp >= ex_l if n >= G_EXEC_N else None)))
    out.append("| Executor: expectancy without best three | >= £%.2f | £%.2f | %s |" % (ex3_l, exp_trim3, mark(exp_trim3 >= ex3_l if n >= G_EXEC_N else None)))
    out.append("| Executor: both halves positive | > £0.00 each | £%.2f, £%.2f | %s |" % (exp_first, exp_second, mark((exp_first > 0 and exp_second > 0) if n >= G_EXEC_N else None)))
    out.append("| Executor: rug rate | <= %.0f%% | %.1f%% | %s |" % (100 * G_EXEC_MAX_RUG, 100 * rug_rate, mark(rug_rate <= G_EXEC_MAX_RUG if n >= G_EXEC_N else None)))

    if not floor_ok:
        verdict = "INCONCLUSIVE"
        why = "fewer than %d closed positions" % G_FLOOR
    elif len(versions) != 1:
        verdict = "INCONCLUSIVE"
        why = "the sample mixes rule versions; only positions under the current rules count"
    elif exp <= kill_l or (n >= G_FLOOR_FINAL and exp < keep_l):
        verdict = "KILL"
        why = "expectancy £%.2f over %d positions; the hypothesis is confirmed for this rule set, publish and close the paper book" % (exp, n)
    elif exp >= keep_l and exp_trim1 >= 0 and rug_rate <= G_MAX_RUG:
        verdict = "KEEP"
        why = "expectancy £%.2f over %d positions, survives removing the best position, rug rate %.1f%%" % (exp, n, 100 * rug_rate)
    else:
        verdict = "INCONCLUSIVE"
        why = "expectancy between the kill and keep lines, or a keep condition missed, with fewer than %d positions" % G_FLOOR_FINAL
    out += ["", "**Verdict: %s.** %s." % (verdict, why)]
    return out, verdict


# =================================================================================================
def _closing_probs(home, away, kickoff):
    """Closing 1X2 probabilities from the results cache, overround removed. None if not found."""
    try:
        sys.path.insert(0, ROOT + "pitch")
        import data as D  # noqa
        res = _closing_probs.res if hasattr(_closing_probs, "res") else D.load_results(getattr(D, "LEAGUES", D.DIVS))
        _closing_probs.res = res
    except Exception:
        return None
    day = kickoff.date()
    m = res[(res["HomeTeam"] == home) & (res["AwayTeam"] == away)]
    m = m[[abs((d.date() - day).days) <= 1 for d in m["Date"]]]
    if m.empty:
        return None
    r = m.iloc[0]
    try:
        inv = [1 / float(r["AvgCH"]), 1 / float(r["AvgCD"]), 1 / float(r["AvgCA"])]
    except Exception:
        return None
    s = sum(inv)
    return [x / s for x in inv]


def _matches_in_window(start, end):
    try:
        sys.path.insert(0, ROOT + "pitch")
        import data as D  # noqa
        res = D.load_results(getattr(D, "LEAGUES", D.DIVS))   # every league the desk predicts
        w = res[(res["Date"] >= start.replace(tzinfo=None)) & (res["Date"] <= end.replace(tzinfo=None))]
        return len(w)
    except Exception:
        return None


def _bootstrap_ci(d, k=4000, seed=1):
    import random
    random.seed(seed)
    n = len(d)
    means = sorted(sum(random.choice(d) for _ in range(n)) / n for _ in range(k))
    return means[int(0.025 * k)], means[int(0.975 * k)]


def _pool_weight_oos(model_p, market_p, ys):
    """Log-opinion-pool weight on the model, chosen on the first half, judged on the second half.
    Returns (weight, second-half log loss of pool, second-half log loss of market)."""
    import math
    n = len(ys)
    if n < 100:
        return None

    def ll(P, Y):
        return -sum(math.log(max(p[y], 1e-9)) for p, y in zip(P, Y)) / len(Y)

    def pool(w):
        out = []
        for m, k in zip(model_p, market_p):
            e = [math.exp(w * math.log(max(mi, 1e-9)) + (1 - w) * math.log(max(ki, 1e-9))) for mi, ki in zip(m, k)]
            s = sum(e)
            out.append([x / s for x in e])
        return out

    half = n // 2
    best_w, best = 0.0, None
    for i in range(0, 101):
        w = i / 100
        v = ll(pool(w)[:half], ys[:half])
        if best is None or v < best:
            best, best_w = v, w
    P = pool(best_w)
    return best_w, ll(P[half:], ys[half:]), ll(market_p[half:], ys[half:])


def pitch():
    rows = list(csv.DictReader(open(ROOT + "pitch/PREDICTIONS.csv")))
    valid, late = [], 0
    for r in rows:
        c, k = iso(r.get("committed_at")), iso(r.get("kickoff_utc"))
        if c and k and c < k:
            valid.append(r)
        else:
            late += 1
    scored = [r for r in valid if fnum(r.get("brier")) is not None and fnum(r.get("market_brier")) is not None]
    n = len(scored)
    now = datetime.now(timezone.utc)
    cov_end = min(now, REVIEW_DATE)
    out = ["## The Pitch", "", "| Criterion | Threshold | Value | Result |", "|---|---|---|---|"]

    # Process gates
    played = _matches_in_window(PITCH_COVERAGE_FROM, cov_end)
    in_window = [r for r in valid if PITCH_COVERAGE_FROM <= iso(r["kickoff_utc"]) <= cov_end]
    coverage = (len(in_window) / played) if played else None
    late_share = late / len(rows) if rows else 0.0
    out.append("| Coverage of matches from 1 Oct, all leagues predicted | >= %.0f%% | %s (%d of %s) | %s |"
               % (100 * P_MIN_COVERAGE, "n/a" if coverage is None else "%.0f%%" % (100 * coverage), len(in_window), played,
                  mark(None if coverage is None else coverage >= P_MIN_COVERAGE)))
    out.append("| Late rows (excluded) as share of all rows | <= %.0f%% | %.1f%% (%d) | %s |" % (100 * P_MAX_LATE_SHARE, 100 * late_share, late, mark(late_share <= P_MAX_LATE_SHARE)))

    if n == 0:
        out += ["| Scored predictions with a market line | >= %d | 0 | INCONCLUSIVE |" % P_EARLY_N, "",
                "**Verdict: INCONCLUSIVE.** Nothing scored yet. Change with a deadline (PASS-MARKS.md, Inconclusive)."]
        return out, "INCONCLUSIVE"

    d = [fnum(r["brier"]) - fnum(r["market_brier"]) for r in scored]
    mean_d = sum(d) / n
    lo, hi = _bootstrap_ci(d)
    out.append("| Scored predictions with a market line | >= %d (week 8), >= %d (edge test) | %d | %s |" % (P_EARLY_N, P_EDGE_N, n, mark(n >= P_EARLY_N)))
    out.append("| Paired Brier, model minus market | early kill >= +%.3f; edge <= %.3f | %+.4f (95%% CI %+.4f to %+.4f) | %s |"
               % (P_EARLY_KILL_DIFF, P_EDGE_DIFF, mean_d, lo, hi,
                  mark(None if n < P_EARLY_N else (False if mean_d >= P_EARLY_KILL_DIFF else (True if (n >= P_EDGE_N and mean_d <= P_EDGE_DIFF and hi < 0) else None)))))

    # Pool weight, out of sample, needs closing probabilities matched from the results cache
    mp, kp, ys, unmatched = [], [], [], 0
    for r in scored:
        k = _closing_probs(r["home"], r["away"], iso(r["kickoff_utc"]))
        y = {"H": 0, "D": 1, "A": 2}.get(r.get("result"))
        if k is None or y is None:
            unmatched += 1
            continue
        m = [fnum(r["p_home"]), fnum(r["p_draw"]), fnum(r["p_away"])]
        s = sum(m)
        mp.append([x / s for x in m]); kp.append(k); ys.append(y)
    pw = _pool_weight_oos(mp, kp, ys)
    if pw:
        w, ll_pool, ll_mkt = pw
        ingredient = w >= P_INGREDIENT_WEIGHT and ll_pool < ll_mkt
        out.append("| Pool weight on model, fit first half, judged second half | >= %.2f and pool beats market | %.2f (pool %.4f v market %.4f; %d unmatched) | %s |"
                   % (P_INGREDIENT_WEIGHT, w, ll_pool, ll_mkt, unmatched, mark(ingredient if n >= P_EDGE_N else None)))
    else:
        ingredient = None
        out.append("| Pool weight on model, out of sample | >= %.2f | n/a (needs 100 matched rows; %d unmatched) | INCONCLUSIVE |" % (P_INGREDIENT_WEIGHT, unmatched))

    if n >= P_EARLY_N and mean_d >= P_EARLY_KILL_DIFF:
        verdict, why = "KILL", "model is worse than the closing market by %.4f Brier over %d matches; the early kill line is +%.3f" % (mean_d, n, P_EARLY_KILL_DIFF)
    elif n >= P_EDGE_N or now >= PITCH_EDGE_DEADLINE:
        if mean_d <= P_EDGE_DIFF and hi < 0:
            verdict, why = "KEEP", "edge: paired Brier %+.4f with the 95%% interval below zero over %d matches; the executor case opens" % (mean_d, n)
        elif ingredient:
            verdict, why = "CHANGE", "no edge alone, but the model earns pool weight %.2f out of sample; re-register a blend as the next version, new clock" % pw[0]
        else:
            verdict, why = "KILL", "no edge and no pool weight over %d matches; the finding is published and the desk stops" % n
    elif coverage is not None and coverage < P_MIN_COVERAGE and now >= REVIEW_DATE:
        verdict, why = "CHANGE", "coverage %.0f%% is below %.0f%%; fix the pipeline by %s or kill" % (100 * coverage, 100 * P_MIN_COVERAGE, SECOND_DATE.date())
    else:
        verdict, why = "INCONCLUSIVE", "%d of %d matches for the edge test; continue to the edge test unless a process gate fails" % (n, P_EDGE_N)
    out += ["", "**Verdict: %s.** %s." % (verdict, why)]
    return out, verdict


# =================================================================================================
def _first_commit_utc(path):
    try:
        r = subprocess.run(["git", "-C", ROOT, "log", "--diff-filter=A", "--format=%cI", "--", path],
                           capture_output=True, text=True)
        lines = [l for l in r.stdout.splitlines() if l.strip()]
        return iso(lines[-1]) if lines else None
    except Exception:
        return None


def field_notes():
    vetoes = set()
    vp = ROOT + "state/field-notes-vetoes.txt"
    if os.path.exists(vp):
        vetoes = {l.strip() for l in open(vp) if l.strip() and not l.startswith("#")}
    now = datetime.now(timezone.utc)
    out = ["## Field Notes", "", "| Week | Sunday | Shipped by Sunday | Ran it, with verdict | Luke said nothing | Result |", "|---|---|---|---|---|---|"]
    results, pending = [], 0
    for (y, w) in FIELD_NOTES_WEEKS:
        sunday = datetime.fromisocalendar(y, w, 7).replace(tzinfo=timezone.utc)
        deadline = sunday + timedelta(hours=23, minutes=59)     # 23:59 UTC is after 23:59 London in Nov and on the same day in Sep/Oct
        tag = "%d-W%02d" % (y, w)
        path = ROOT + "field-notes/%s.md" % tag
        if now < deadline:
            pending += 1
            out.append("| %s | %s | pending | pending | %s | pending |" % (tag, sunday.date(), "yes" if tag in vetoes else "no"))
            continue
        exists = os.path.exists(path)
        first = _first_commit_utc("field-notes/%s.md" % tag) if exists else None
        on_time = bool(first and first <= deadline)
        txt = open(path).read().lower() if exists else ""
        ran = "## ran it" in txt and "verdict" in txt.split("## ran it", 1)[1].split("\n## ", 1)[0]
        veto = tag in vetoes
        ok = exists and on_time and ran and not veto
        results.append(ok)
        out.append("| %s | %s | %s | %s | %s | %s |" % (tag, sunday.date(), "yes" if on_time else ("late" if exists else "no"), "yes" if ran else "no", "yes" if veto else "no", mark(ok)))
    fails = [not r for r in results]
    run, longest = 0, 0
    for f in fails:
        run = run + 1 if f else 0
        longest = max(longest, run)
    total = sum(fails)
    out += ["", "Fails so far: %d of %d judged (%d pending). Longest run of consecutive fails: %d. Kill at %d consecutive or %d of eight."
            % (total, len(results), pending, longest, F_KILL_CONSECUTIVE, F_KILL_OF_EIGHT)]
    if longest >= F_KILL_CONSECUTIVE or total >= F_KILL_OF_EIGHT:
        verdict, why = "KILL", "the weekly note failed its own bar %d times in a row or %d of eight; Proteus stops as a whole" % (longest, total)
    elif pending:
        verdict, why = "INCONCLUSIVE", "%d Sundays still to come" % pending
    else:
        verdict, why = "KEEP", "eight Sundays judged, below both kill lines"
    out += ["", "**Verdict: %s.** %s." % (verdict, why)]
    return out, verdict


# =================================================================================================
def disqualifiers():
    out = ["## Disqualifiers (charter breaches; any one is a kill on its own)", ""]
    spent = 0.0
    sp = ROOT + "state/spend.jsonl"
    if os.path.exists(sp):
        for line in open(sp):
            try:
                e = json.loads(line)
                if e["date"][:7] == datetime.now(timezone.utc).strftime("%Y-%m"):
                    spent += float(e["amount_gbp"])
            except Exception:
                continue
    out.append("- Spend this month £%.2f against the £50.00 cap: %s." % (spent, mark(spent <= 50.0)))
    out.append("- Luke-gates, Flywheel cards or Todoist items opened by Proteus: MANUAL, must be 0.")
    out.append("- Email to anyone other than Luke: MANUAL, must be none (bin/send-field-notes.sh is the only path).")
    out.append("- Ledger or prediction outcome columns rewritten after the outcome in the record's favour: MANUAL, check `git log -p` on the two ledgers.")
    out.append("- Predictions committed after kickoff and counted in an average: %s (score.py excludes them; see the late-row line above)." % mark(True))
    return out


def main():
    g, gv = grinder()
    p, pv = pitch()
    f, fv = field_notes()
    lines = ["# Week-8 review, computed %s at commit %s" % (datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"), _head()),
             "", "Standard: PASS-MARKS.md. Review date %s. Second and last date for an inconclusive desk %s." % (REVIEW_DATE.date(), SECOND_DATE.date()),
             ""] + g + [""] + p + [""] + f + [""] + disqualifiers() + [
             "", "## Summary", "", "| Desk | Verdict |", "|---|---|",
             "| The Grinder | %s |" % gv, "| The Pitch | %s |" % pv, "| Field Notes | %s |" % fv, ""]
    print("\n".join(lines))


def _head():
    try:
        return subprocess.run(["git", "-C", ROOT, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip() or "n/a"
    except Exception:
        return "n/a"


if __name__ == "__main__":
    main()
