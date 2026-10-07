#!/usr/bin/env python3
"""Build HOME.md: one page that says how Proteus stands today, for Luke to open in Obsidian.

    python3 /Users/triton/PROTEUS/bin/home.py

Every number is computed from the committed files at build time; nothing is typed by hand. Writes
/Users/triton/PROTEUS/HOME.md (gitignored, it changes every night); bin/mirror-vault.sh runs this and
copies the page to TRITON-CORE/Proteus/HOME.md, where the [[links]] resolve to the mirrored registers.
Standard library only, so it runs under the system python3 inside a scheduled run.
"""
import csv
import glob
import json
import os
import re
import statistics as st
import subprocess
from datetime import datetime, timedelta, timezone

ROOT = "/Users/triton/PROTEUS/"
OUT = ROOT + "HOME.md"
VENV = ROOT + ".venv/bin/python3"
GRINDER_START = {"v0.1": 100.0, "v0.2": 1000.0}


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def rows(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def money(x):
    return ("£%.2f" % x) if x >= 0 else ("-£%.2f" % -x)


def utc(s):
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return None


def grinder():
    led = rows(ROOT + "grinder/LEDGER.csv")
    out = ["## The Grinder (meme-coin paper desk)", ""]
    if not led:
        return out + ["No ledger yet.", ""]
    current = led[-1]["rule_version"]
    book = [r for r in led if r["rule_version"] == current]
    closed = [r for r in book if r["exit_at"]]
    pnl = [f(r["pnl_gbp"]) or 0.0 for r in closed]
    since = datetime.now(timezone.utc) - timedelta(hours=20)
    new = [r for r in led if (utc(r["entered_at"]) or since) > since]
    shut = [r for r in led if r["exit_at"] and (utc(r["exit_at"]) or since) > since]
    out += ["| Rules %s | |" % current, "|---|---|",
            "| Paper bankroll | %s (started %s) |" % (money(GRINDER_START.get(current, 0) + sum(pnl)), money(GRINDER_START.get(current, 0))),
            "| Opened / closed / open | %d / %d / %d |" % (len(book), len(closed), len(book) - len(closed)),
            "| Expectancy per closed position | %s |" % (money(st.mean(pnl)) if pnl else "n/a"),
            "| Hit rate | %s |" % (("%d%%" % round(100 * sum(p > 0 for p in pnl) / len(pnl))) if pnl else "n/a"),
            "| Rugged | %d |" % sum(r.get("rugged") == "1" for r in book), ""]
    if new or shut:
        out.append("Last 20 hours: entered %s; closed %s." % (
            ", ".join(r["token"] for r in new) or "none",
            ", ".join("%s %s %s" % (r["token"], r["exit_reason"].replace("_", " "), money(f(r["pnl_gbp"]) or 0)) for r in shut) or "none"))
        out.append("")
    try:
        g = subprocess.run([VENV, ROOT + "grinder/graduates/watcher.py", "summary"], capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        g = ["summary failed: %s" % type(e).__name__]
    if g:
        out += ["**Graduation book** (long-running paper job): " + "; ".join(g[:3]) + ".", ""]
    return out


def pitch():
    out = ["## The Pitch (football forecast desk)", ""]
    pred = rows(ROOT + "pitch/PREDICTIONS.csv")
    scored = [r for r in pred if f(r.get("brier")) is not None]
    out.append("- Model predictions committed: **%d**, scored %d%s." % (
        len(pred), len(scored),
        (", Brier %.4f v market %.4f" % (st.mean(f(r["brier"]) for r in scored),
                                         st.mean(f(r["market_brier"]) for r in scored if f(r["market_brier"]) is not None)))
        if scored and any(f(r["market_brier"]) is not None for r in scored) else ""))
    if not pred:
        out.append("  Nothing yet: `predict.py` only commits for fixtures inside an 8-day window on file. Check the run log's \"binding constraint\" line.")
    jb = rows(ROOT + "pitch/JUDGEMENT.csv")
    js = [r for r in jb if f(r.get("brier")) is not None and f(r.get("market_brier")) is not None]
    bl = [r for r in jb if f(r.get("blind_brier")) is not None and f(r.get("market_brier")) is not None]
    line = "- Judgement book: %d calls, %d scored" % (len(jb), len(js))
    if js:
        line += ", anchored minus market %+.4f" % st.mean(f(r["brier"]) - f(r["market_brier"]) for r in js)
    if bl:
        line += ", blind minus market %+.4f over %d" % (st.mean(f(r["blind_brier"]) - f(r["market_brier"]) for r in bl), len(bl))
    out += [line + " (negative beats the market).", ""]
    return out


def probes():
    d = json.load(open(ROOT + "state/probes.json"))
    items = d["items"]
    done = [p for p in items if p["status"] == "done"]
    counts = {}
    for p in done:
        counts[p["verdict"]] = counts.get(p["verdict"], 0) + 1
    killed = sum(p["status"] == "killed" for p in items)
    openq = [p for p in items if p["status"] == "open"]
    out = ["## Probes", "",
           "Verdicts %d: %s. Killed %d. Full register: [[PROBES]]." % (
               len(done), ", ".join("%s %d" % (k, v) for k, v in sorted(counts.items(), key=lambda kv: -kv[1])), killed), "",
           "**Last five**", ""]
    for p in sorted(done, key=lambda p: p.get("verdict_at") or "")[-5:][::-1]:
        out.append("- %s %s, **%s**: %s" % ((p.get("verdict_at") or "")[:10], p["id"], p["verdict"], p["note"][:230]))
    out += ["", "**Queue (%d open)**" % len(openq), ""]
    for p in openq:
        wait = ("waits for %s" % p["after"]) if p.get("after") else (("needs: %s" % p["needs"][:120]) if p.get("needs") else "ready")
        out.append("- %s %s (%s)" % (p["id"], p["title"][:110], wait))
    return out + [""]


def jobs():
    out = ["## Long-running jobs", ""]
    live = []
    for start in sorted(glob.glob(ROOT + "experiments/*/START")):
        d = os.path.dirname(start)
        if os.path.exists(d + "/DONE"):
            continue
        try:
            t0 = datetime.fromtimestamp(float(open(start).read().strip()), timezone.utc)
        except ValueError:
            continue
        polls = sum(1 for _ in open(d + "/polls.jsonl")) if os.path.exists(d + "/polls.jsonl") else 0
        live.append("- `%s`: started %s UTC, ends about %s UTC, %d polls so far." % (
            os.path.basename(d), t0.strftime("%d %b %H:%M"), (t0 + timedelta(hours=24)).strftime("%d %b %H:%M"), polls))
    return out + (live or ["None running."]) + [""]


def last_night():
    logs = sorted(glob.glob(ROOT + "state/runs/2*.md"))
    out = ["## Last nightly run", ""]
    for path in logs[::-1]:
        text = open(path).read()
        if "## Nightly run" in text:
            sec = text[text.rindex("## Nightly run"):].splitlines()
            out.append("%s (`state/runs/%s`). Probe lines are in [[PROBES]]." % (sec[0][3:], os.path.basename(path)))
            out.append("")
            for line in sec[1:]:
                if line.startswith("- ") and not line.startswith("- Probe P-") and not line.startswith("  Denied"):
                    out.append(line if len(line) < 260 else line[:257] + "...")
            return out + [""]
    return out + ["No nightly run logged yet.", ""]


def spend():
    text = open(ROOT + "SPEND.md").read() if os.path.exists(ROOT + "SPEND.md") else ""
    month = datetime.now().strftime("%B %Y")
    card = "no %s section yet, so nothing spent" % month
    m = re.search(r"## %s\n(.*?)(\n## |\Z)" % month, text, re.S)
    if m:
        totals = re.findall(r"£([0-9.]+) \|\s*$", m.group(1), re.M)
        card = "£%s spent" % (totals[-1] if totals else "0.00")
    xai = sum(float(x) for x in re.findall(r"^\| 20\d\d-\d\d-\d\d \|[^|]*\| ([0-9.]+) \|\s*$", text.split("## Luke's xAI account")[-1], re.M)) if "## Luke's xAI account" in text else 0.0
    logged = []
    for path in sorted(glob.glob(ROOT + "state/runs/2*.md"))[-7:]:
        logged += [float(x) for x in re.findall(r"x spend \$([0-9]+(?:\.[0-9]+)?)", open(path).read())]
    return ["## Money", "",
            "- Proteus card, %s: %s (cap £50 autonomous, £250 all-in). [[SPEND]]" % (month, card),
            "- Luke's xAI account: $%.2f in SPEND.md (updated Sundays); mentions spend logged this week $%.2f." % (xai, sum(logged)), ""]


def draft():
    week = datetime.now().strftime("%G-W%V")
    path = ROOT + "field-notes/drafts/%s.md" % week
    out = ["## This week's Field Notes (%s draft, ships Sunday)" % week, ""]
    if not os.path.exists(path):
        return out + ["No draft yet.", ""]
    secs = re.split(r"^## ", open(path).read(), flags=re.M)[1:]
    out.append(" · ".join("%s %s" % (s.splitlines()[0], "✓" if s.strip() != s.splitlines()[0].strip() else "·") for s in secs))
    return out + [""]


def main():
    now = datetime.now()
    halt = os.path.exists(ROOT + "HALT")
    head = ["# Proteus, today", "",
            "Built %s from the committed files by `bin/home.py`. Rebuilt after every nightly run; do not edit, it is overwritten." % now.strftime("%a %d %b %Y %H:%M"),
            "", "**Kill switch: %s.**" % ("HALT IS SET, no side effects" if halt else "clear"), ""]
    body = last_night() + grinder() + pitch() + jobs() + probes() + spend() + draft()
    foot = ["## Everything else", "",
            "[[TRACK-RECORD]] (audited score, rebuilt Sundays) · [[HARVEST]] · [[SEEN]] · [[BACKLOG]] · [[PASS-MARKS]] · [[USAGE]] · [[CHARTER]] · [[GRADUATES]]",
            "", "Public lab page, rebuilt Sundays: https://triton-xxix.github.io/proteus-lab/",
            "The record, a film and a page of the first sixteen nights: https://triton-xxix.github.io/proteus-lab/record/", ""]
    open(OUT, "w").write("\n".join(head + body + foot))
    print("home: %s (%d lines)" % (OUT, len(head + body + foot)))


if __name__ == "__main__":
    main()
