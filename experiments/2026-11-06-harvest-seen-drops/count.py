#!/usr/bin/env python3
"""Owed since 5 Nov: how many of the harvest's seen-drops are vault threads, and do vault items earn their shortlist slots?

Reads state/harvest/<date>/candidates.json and shortlist.json and state/agents/<date>/harvest.json for the last
14 harvest nights. Prints candidates, seen-drops, shortlisted, kept and testable per source. Changes nothing.
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path("/Users/triton/PROTEUS/state")


def src(key):
    return "vault" if str(key).startswith("vault:") else str(key).split(":")[0]


dates = sorted(p.name for p in (ROOT / "harvest").iterdir() if (p / "shortlist.json").exists())[-14:]
tot = {k: Counter() for k in ("cand", "drop", "short", "kept", "testable")}
nights = []
for d in dates:
    wd = ROOT / "harvest" / d
    cand = json.loads((wd / "candidates.json").read_text())
    short = json.loads((wd / "shortlist.json").read_text())
    n = {k: Counter() for k in tot}
    for c in cand.get("candidates", []):
        n["cand"][src(c.get("key"))] += 1
    for x in short.get("dropped_seen", []):
        key = x.get("key") if isinstance(x, dict) else x
        n["drop"][src(key)] += 1
    for c in short.get("items", []):
        n["short"][src(c.get("key"))] += 1
    j = ROOT / "agents" / d / "harvest.json"
    if j.exists():
        try:
            for r in json.loads(j.read_text()):
                s = src(r.get("key"))
                if r.get("keep"):
                    n["kept"][s] += 1
                if r.get("testable"):
                    n["testable"][s] += 1
        except ValueError:
            pass
    for k in tot:
        tot[k].update(n[k])
    nights.append({"date": d, **{k: dict(v) for k, v in n.items()}})

out = {"nights": len(dates), "from": dates[0], "to": dates[-1], "totals": {k: dict(v) for k, v in tot.items()}, "by_night": nights}
Path(__file__).with_name("results.json").write_text(json.dumps(out, indent=1))
print(dates[0], "to", dates[-1], len(dates), "nights")
print(f"{'source':10}{'cand':>7}{'drop':>7}{'short':>7}{'kept':>7}{'test':>7}")
for s in sorted(tot["cand"], key=lambda x: -tot["cand"][x]):
    print(f"{s:10}{tot['cand'][s]:7}{tot['drop'][s]:7}{tot['short'][s]:7}{tot['kept'][s]:7}{tot['testable'][s]:7}")
