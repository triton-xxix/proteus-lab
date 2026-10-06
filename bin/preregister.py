#!/usr/bin/env python3
"""The nightly's two sweep commits, limited to the files the nightly owns.

    python3 /Users/triton/PROTEUS/bin/preregister.py pre   [--date YYYY-MM-DD] [--dry-run]
    python3 /Users/triton/PROTEUS/bin/preregister.py close [--date YYYY-MM-DD] [--dry-run]

Until 7 Oct 2026 steps 4 and 7 ran `git add -A`. On 6 Oct that swept an interactive session's
experiment, REFILL-SOURCES.md and three Skool prompts into "nightly: pre-register", and a Skool
survey into the close. The pre-register commit is the proof that predictions came before outcomes,
so it now holds desk data only:

  pre    data files (.csv .json .jsonl) under grinder/, pitch/, exchange/, plus state/runs/*.md
  close  the pre set, plus games/, field-notes/drafts/, field-notes/SEEN.md, the research desk's
         working files (state/research/, state/agents/research/; narrative.py commits only the copy),
         field-notes/vault-threads.json and the desks' RULES.md files (kill-check verdicts)

Everything else that is dirty is left alone, listed on stdout and in one run-log line, so the
session that made it can commit it. The commit names its paths (`git commit -- paths`), so anything
an interactive session staged stays out too. Pushes after committing. Under HALT it does nothing.
"""
import argparse
import os
import subprocess
import sys
from datetime import datetime

ROOT = "/Users/triton/PROTEUS"
HALT = ROOT + "/HALT"
DESKS = ("grinder/", "pitch/", "exchange/")
DATA_EXT = (".csv", ".json", ".jsonl")
CLOSE_PREFIXES = ("games/", "field-notes/drafts/", "state/research/", "state/agents/research/")
CLOSE_FILES = ("field-notes/SEEN.md", "field-notes/vault-threads.json")


def git(args, check=True, timeout=120):
    r = subprocess.run(["git", "-C", ROOT] + args, capture_output=True, text=True, timeout=timeout)
    if check and r.returncode != 0:
        raise RuntimeError("git %s: %s" % (" ".join(args[:2]), (r.stderr or r.stdout).strip()[:300]))
    return r.stdout


def dirty():
    """Every changed, deleted or untracked path, relative to ROOT (ignored files excluded)."""
    out = git(["status", "--porcelain=v1", "-z", "-uall"])
    paths, items = [], out.split("\0")
    i = 0
    while i < len(items):
        it = items[i]
        i += 1
        if len(it) < 4:
            continue
        paths.append(it[3:])
        if it[0] in "RC":  # rename/copy: the next item is the old path, which is gone
            paths.append(items[i])
            i += 1
    return paths


def owned(path, mode):
    if path.startswith(DESKS) and path.endswith(DATA_EXT):
        return True
    if path.startswith("state/runs/") and path.endswith(".md"):
        return True
    if mode == "close":
        if path.startswith(CLOSE_PREFIXES) or path in CLOSE_FILES:
            return True
        if path.startswith(DESKS) and os.path.basename(path) == "RULES.md":
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("pre", "close"))
    ap.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if os.path.exists(HALT):
        print("HALT set: nothing staged, nothing committed")
        return 0
    paths = dirty()
    take = [p for p in paths if owned(p, a.mode)]
    left = [p for p in paths if not owned(p, a.mode)]
    label = "pre-register" if a.mode == "pre" else "close"

    if a.dry_run:
        print("would commit %d: %s" % (len(take), ", ".join(take) or "-"))
        print("would leave %d: %s" % (len(left), ", ".join(left) or "-"))
        return 0

    if take:
        present = [p for p in take if os.path.exists(os.path.join(ROOT, p))]
        gone = [p for p in take if p not in present]
        if present:
            git(["add", "--"] + present)
        if gone:
            git(["rm", "-q", "--cached", "--ignore-unmatch", "--"] + gone)
        git(["commit", "-q", "-m", "nightly: %s %s" % (label, a.date), "--"] + take)
        h = git(["rev-parse", "--short", "HEAD"]).strip()
        git(["push", "-q", "origin", "main"], check=False, timeout=90)
        result = "%s, %d files" % (h, len(take))
        if git(["rev-parse", "HEAD"]).strip() != git(["rev-parse", "origin/main"], check=False).strip():
            result += ", push failed"
    else:
        result = "nothing to commit"
    print("%s: %s" % (label, result))

    line = "- %s %s commit: %s" % (datetime.now().strftime("%H:%M"), label, result)
    if left:
        shown = ", ".join(left[:8]) + (" and %d more" % (len(left) - 8) if len(left) > 8 else "")
        line += "; left dirty for the session that made them (%d): %s" % (len(left), shown)
        print("left dirty (%d): %s" % (len(left), ", ".join(left)))
    os.makedirs(ROOT + "/state/runs", exist_ok=True)
    with open(ROOT + "/state/runs/%s.md" % a.date, "a") as fh:
        fh.write(line + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
