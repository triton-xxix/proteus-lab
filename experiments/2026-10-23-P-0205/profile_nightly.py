#!/usr/bin/env python3
"""P-0205: a sampling profile of the nightly from the hook's decisions log.

The PreToolUse hook writes one JSON line per tool call (ts, task, tool, detail, agent_id). Treat the
parent's calls in a nightly session as samples: the gap between two consecutive parent calls is the time
the earlier call took plus the thinking after it. Attribute each gap to the earlier call. Then, per run:
span, the top gaps with their commands, and the share of the span owned by each step family.
Reads the last N decision files; writes results.json and prints a table. Standard library only.
Run: python3 /Users/triton/PROTEUS/experiments/2026-10-23-P-0205/profile_nightly.py
"""
import glob
import json
import os
import re
from collections import defaultdict
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = "/Users/triton/PROTEUS/state"
TASK = "proteus-nightly"
N_RUNS = 7

FAMILIES = [
    ("grinder scan", r"grinder/scan\.py"),
    ("grinder rules/score/r01", r"grinder/paper\.py"),
    ("mentions", r"research/mentions\.py"),
    ("graduates", r"graduates/watcher\.py"),
    ("pitch", r"pitch/(apisports|predict|score|score_judgement)\.py"),
    ("exchange", r"exchange/exchange\.py"),
    ("systems", r"systems/systems\.py"),
    ("edges", r"edges/(edges|scan/scan)\.py"),
    ("preregister/dash", r"bin/(preregister|dash|halt-check)\.py"),
    ("harvest", r"bin/harvest\.py"),
    ("skool", r"bin/skool\.py"),
    ("nolan", r"bin/nolan\.py"),
    ("narrative", r"research/narrative\.py"),
    ("children (Agent)", r"^Agent\b"),
    ("probe loop", r"bin/probe\.py"),
    ("lichess", r"bin/lichess\.py"),
    ("killcheck/duecheck/mirror", r"bin/(killcheck|duecheck|mirror-vault)"),
    ("git", r"^git "),
    ("files (Read/Write/Edit)", r"^(Read|Write|Edit)\b"),
    ("curl", r"^curl "),
]


def parse_ts(s):
    return datetime.fromisoformat(s)


def family(tool, detail):
    key = detail if tool == "Bash" else tool + " " + (detail or "")
    for name, pat in FAMILIES:
        if re.search(pat, key):
            return name
    return "other " + tool


def main():
    files = sorted(glob.glob(os.path.join(STATE, "unattended-decisions-*.jsonl")))
    sessions = defaultdict(list)
    for f in files:
        with open(f) as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if d.get("task") != TASK:
                    continue
                sessions[d["session"]].append(d)
    runs = []
    for sid, rows in sessions.items():
        parent = sorted((r for r in rows if not r.get("agent_id")), key=lambda r: r["ts"])
        if len(parent) < 10:
            continue
        child = [r for r in rows if r.get("agent_id")]
        t = [parse_ts(r["ts"]) for r in parent]
        span = (t[-1] - t[0]).total_seconds()
        gaps = []
        for i in range(len(parent) - 1):
            g = (t[i + 1] - t[i]).total_seconds()
            r = parent[i]
            gaps.append({"secs": g, "tool": r["tool"], "detail": (r.get("detail") or "")[:110],
                         "family": family(r["tool"], r.get("detail") or ""), "at": r["ts"][11:19]})
        by_fam = defaultdict(float)
        for g in gaps:
            by_fam[g["family"]] += g["secs"]
        top = sorted(gaps, key=lambda g: -g["secs"])[:6]
        fam_sorted = sorted(by_fam.items(), key=lambda kv: -kv[1])
        runs.append({
            "session": sid, "date": parent[0]["ts"][:10], "start": parent[0]["ts"][11:19], "end": parent[-1]["ts"][11:19],
            "span_min": round(span / 60, 1), "parent_calls": len(parent), "child_calls": len(child),
            "denied": sum(1 for r in parent if r.get("outcome") == "deny"),
            "longest_gap_min": round(top[0]["secs"] / 60, 1) if top else 0,
            "longest_gap_share": round(top[0]["secs"] / span, 3) if top and span else 0,
            "top_gaps": [{"min": round(g["secs"] / 60, 1), "family": g["family"], "at": g["at"], "detail": g["detail"]} for g in top],
            "families": [{"family": k, "min": round(v / 60, 1), "share": round(v / span, 3)} for k, v in fam_sorted[:8]],
        })
    runs = sorted(runs, key=lambda r: r["date"] + r["start"])[-N_RUNS:]
    agg = defaultdict(float)
    for r in runs:
        for f in r["families"]:
            agg[f["family"]] += f["min"]
    total = sum(r["span_min"] for r in runs)
    summary = {
        "runs": len(runs),
        "total_span_min": round(total, 1),
        "median_span_min": sorted(r["span_min"] for r in runs)[len(runs) // 2] if runs else None,
        "max_longest_gap_min": max((r["longest_gap_min"] for r in runs), default=None),
        "runs_with_a_step_over_quarter": [r["date"] for r in runs if r["longest_gap_share"] > 0.25],
        "family_share_all_runs": [{"family": k, "min": round(v, 1), "share": round(v / total, 3)} for k, v in sorted(agg.items(), key=lambda kv: -kv[1])[:10]],
    }
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump({"summary": summary, "runs": runs}, fh, indent=1)
    for r in runs:
        print(f"{r['date']} {r['start']}-{r['end']} span {r['span_min']} min, {r['parent_calls']} parent calls, {r['child_calls']} child, {r['denied']} denied; longest gap {r['longest_gap_min']} min ({r['longest_gap_share']:.0%}) {r['top_gaps'][0]['family']}: {r['top_gaps'][0]['detail'][:70]}")
        for g in r["top_gaps"][1:4]:
            print(f"      {g['min']:5} min {g['family']:<28} {g['detail'][:70]}")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
