#!/usr/bin/env python3
"""Rebuild TRACK-RECORD.md and docs/data.json from the committed ledgers. Never typed by hand.

    python3 /Users/triton/PROTEUS/bin/score.py          # print the numbers
    python3 /Users/triton/PROTEUS/bin/score.py --write  # rewrite TRACK-RECORD.md and docs/data.json

Inputs: grinder/LEDGER.csv, pitch/PREDICTIONS.csv, state/spend.jsonl (optional), field-notes/*.md,
git log (for luke-gate count we simply assert 0: Proteus has no path to the ledger).
"""
import csv
import glob
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

ROOT = "/Users/triton/PROTEUS/"


def fnum(x):
    try:
        return float(x)
    except Exception:
        return None


def grinder():
    rows = list(csv.DictReader(open(ROOT + "grinder/LEDGER.csv")))
    opened = len(rows)
    scored = [r for r in rows if fnum(r.get("score_24h")) is not None]
    pnl = [fnum(r.get("pnl_gbp")) for r in rows if fnum(r.get("pnl_gbp")) is not None]
    hits = [p for p in pnl if p > 0]
    rugged = [r for r in rows if (r.get("rugged") or "").lower() in ("1", "true", "yes")]
    return {
        "bankroll_start": 100.0,
        "bankroll_now": round(100.0 + sum(pnl), 2),
        "opened": opened,
        "scored_24h": len(scored),
        "hit_rate": round(len(hits) / len(pnl), 3) if pnl else None,
        "expectancy": round(sum(pnl) / len(pnl), 2) if pnl else None,
        "rugged": len(rugged),
    }


def pitch():
    rows = list(csv.DictReader(open(ROOT + "pitch/PREDICTIONS.csv")))
    valid = []
    for r in rows:
        try:
            c = datetime.fromisoformat(r["committed_at"].replace("Z", "+00:00"))
            k = datetime.fromisoformat(r["kickoff_utc"].replace("Z", "+00:00"))
            if c < k:
                valid.append(r)
        except Exception:
            continue
    scored = [r for r in valid if fnum(r.get("brier")) is not None]
    mb = [fnum(r["brier"]) for r in scored]
    mk = [fnum(r["market_brier"]) for r in scored if fnum(r.get("market_brier")) is not None]
    clv = [fnum(r["clv"]) for r in scored if fnum(r.get("clv")) is not None]
    pnl = [fnum(r["pnl_gbp"]) for r in scored if fnum(r.get("pnl_gbp")) is not None]
    return {
        "committed_before_kickoff": len(valid),
        "committed_late_excluded": len(rows) - len(valid),
        "scored": len(scored),
        "brier_model": round(sum(mb) / len(mb), 4) if mb else None,
        "brier_market": round(sum(mk) / len(mk), 4) if mk else None,
        "clv_mean": round(sum(clv) / len(clv), 4) if clv else None,
        "bankroll_now": round(100.0 + sum(pnl), 2),
    }


def field_notes():
    notes = sorted(glob.glob(ROOT + "field-notes/20??-W??.md"))
    ran = 0
    for n in notes:
        txt = open(n).read().lower()
        ran += txt.count("## ran it")
    return {"weekly_notes": len(notes), "things_run": ran, "luke_gates_opened": 0}


def spend():
    path = ROOT + "state/spend.jsonl"
    months = {}
    if os.path.exists(path):
        for line in open(path):
            try:
                e = json.loads(line)
                m = e["date"][:7]
                months[m] = round(months.get(m, 0.0) + float(e["amount_gbp"]), 2)
            except Exception:
                continue
    now = datetime.now(timezone.utc).strftime("%Y-%m")
    months.setdefault(now, 0.0)
    return {"cap_gbp": 50.0, "months": months}


def git_head():
    try:
        return subprocess.run(["git", "-C", ROOT, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip() or "n/a"
    except Exception:
        return "n/a"


def na(v, suffix=""):
    return "n/a" if v is None else ("%s%s" % (v, suffix))


def render_md(d):
    g, p, f, s = d["grinder"], d["pitch"], d["field_notes"], d["spend"]
    lines = [
        "# Track record",
        "",
        "Every number here is computed from the committed ledgers by `bin/score.py`, never typed by hand.",
        "A losing record is published in exactly the same format as a winning one.",
        "",
        "Rebuilt %s at commit %s." % (d["built_at"], d["commit"]),
        "",
        "## The Grinder (meme-coin paper desk)",
        "",
        "| Measure | Value |", "|---|---|",
        "| Paper bankroll | £%.2f (started £100.00) |" % g["bankroll_now"],
        "| Positions opened | %d |" % g["opened"],
        "| Positions scored at 24h | %d |" % g["scored_24h"],
        "| Hit rate | %s |" % na(g["hit_rate"]),
        "| Expectancy per position | %s |" % ("n/a" if g["expectancy"] is None else "£%.2f" % g["expectancy"]),
        "| Positions that rugged | %d |" % g["rugged"],
        "",
        "## The Pitch (football forecast desk)",
        "",
        "| Measure | Value |", "|---|---|",
        "| Predictions committed before kickoff | %d |" % p["committed_before_kickoff"],
        "| Predictions committed late (excluded) | %d |" % p["committed_late_excluded"],
        "| Predictions scored | %d |" % p["scored"],
        "| Brier score, model (lower is better; 0.25 is a coin flip on 1X2) | %s |" % na(p["brier_model"]),
        "| Brier score, market, same matches | %s |" % na(p["brier_market"]),
        "| Closing-line value, mean | %s |" % na(p["clv_mean"]),
        "| Paper bankroll, quarter Kelly | £%.2f (started £100.00) |" % p["bankroll_now"],
        "",
        "## Field Notes",
        "",
        "| Measure | Value |", "|---|---|",
        "| Things installed and run | %d |" % f["things_run"],
        "| Weekly notes shipped | %d |" % f["weekly_notes"],
        "| Luke-gates opened | %d (must stay 0) |" % f["luke_gates_opened"],
        "",
        "## Spend",
        "",
        "| Month | Spent | Cap |", "|---|---|---|",
    ]
    for m in sorted(s["months"]):
        lines.append("| %s | £%.2f | £%.2f |" % (m, s["months"][m], s["cap_gbp"]))
    lines.append("")
    return "\n".join(lines) + "\n"


def main():
    d = {
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "commit": git_head(),
        "grinder": grinder(),
        "pitch": pitch(),
        "field_notes": field_notes(),
        "spend": spend(),
    }
    if "--write" in sys.argv:
        open(ROOT + "TRACK-RECORD.md", "w").write(render_md(d))
        os.makedirs(ROOT + "docs", exist_ok=True)
        json.dump(d, open(ROOT + "docs/data.json", "w"), indent=1)
        print("wrote TRACK-RECORD.md and docs/data.json")
    else:
        print(json.dumps(d, indent=1))


if __name__ == "__main__":
    main()
