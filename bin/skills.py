#!/usr/bin/env python3
"""Proteus's own skills: what exists, how often scheduled runs used each, and retiring the unused.

    python3 /Users/triton/PROTEUS/bin/skills.py list            # name, age, uses in the last 14 days
    python3 /Users/triton/PROTEUS/bin/skills.py retire NAME     # move it to state/retired-skills/, dated

Written 9 Oct 2026 for the Smith slot, which writes a skill when a procedure has been done by hand
twice and retires any skill no scheduled run used in 14 days. Uses come from the hook's decisions
logs (tool "Skill", the skill name in `detail` since 9 Oct), so interactive use is not counted.
Retiring moves the folder rather than deleting it: Smith cannot run `rm`, and a retired skill can be
moved back by hand. Commit both paths afterwards with bin/commit.py.
"""
import glob
import json
import os
import shutil
import subprocess
import sys
import time

ROOT = "/Users/triton/PROTEUS/"
SKILLS = ROOT + ".claude/skills/"
RETIRED = ROOT + "state/retired-skills/"
WINDOW_DAYS = 14


def uses(days=WINDOW_DAYS):
    counts = {}
    cutoff = time.strftime("%Y-%m-%d", time.localtime(time.time() - days * 86400))
    for path in glob.glob(ROOT + "state/unattended-decisions-*.jsonl"):
        if path[-16:-6] < cutoff:
            continue
        with open(path) as fh:
            for line in fh:
                if '"Skill"' not in line:
                    continue
                try:
                    rec = json.loads(line)
                except ValueError:
                    continue
                if rec.get("tool") == "Skill" and rec.get("outcome") == "allow" and not str(rec.get("session", "")).startswith("t"):
                    name = str(rec.get("detail") or "").split(":")[-1]
                    counts[name] = counts.get(name, 0) + 1
    return counts


def created(name):
    r = subprocess.run(["git", "-C", ROOT, "log", "--diff-filter=A", "--format=%ct", "--", ".claude/skills/%s/SKILL.md" % name],
                       capture_output=True, text=True)
    ts = [int(x) for x in r.stdout.split()]
    return min(ts) if ts else None


def cmd_list():
    c = uses()
    names = sorted(n for n in os.listdir(SKILLS) if os.path.isfile(SKILLS + n + "/SKILL.md")) if os.path.isdir(SKILLS) else []
    print("%-28s %8s %6s  %s" % ("skill", "age d", "uses", "state"))
    for n in names:
        t = created(n)
        age = (time.time() - t) / 86400 if t else 0
        u = c.get(n, 0)
        state = "RETIRE" if age > WINDOW_DAYS and u == 0 else "ok"
        print("%-28s %8.1f %6d  %s" % (n, age, u, state))
    print("%d skills; uses counted from scheduled runs in the last %d days" % (len(names), WINDOW_DAYS))


def cmd_retire(name):
    src = SKILLS + name
    if not os.path.isdir(src) or "/" in name:
        sys.exit("no skill %s" % name)
    os.makedirs(RETIRED, exist_ok=True)
    dst = RETIRED + "%s-%s" % (time.strftime("%Y-%m-%d"), name)
    shutil.move(src, dst)
    print("RETIRED %s -> %s; commit both paths with bin/commit.py" % (src, dst))


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "list":
        cmd_list()
    elif len(sys.argv) == 3 and sys.argv[1] == "retire":
        cmd_retire(sys.argv[2])
    else:
        print(__doc__)
