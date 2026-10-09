#!/usr/bin/env python3
"""Commit named paths and push, the one way scheduled runs commit since 9 Oct 2026.

    python3 /Users/triton/PROTEUS/bin/commit.py -m "message" PATH [PATH ...]

Why not plain git: with a daytime loop beside the nightly and Luke's own sessions, three things went
or could go wrong. A bare `git commit` takes whatever another session staged (6 Oct). `git add -A`
sweeps another session's files into a commit that is meant to prove timing. And a push rejected
because someone else pushed first was left for the next commit to carry.

So: only the named paths are staged and committed (deleted ones are removed from the index), the
commit names them (`git commit -- paths`), and a rejected push fetches and MERGES origin/main, then
pushes once more. Merge, never rebase: a rebase rewrites the committer date, and that date is the
pre-registration proof. If another session has files staged, git refuses the merge; the commit then
stays local, untouched, and the next commit's push carries it (tested 9 Oct). Under HALT nothing is
staged or committed. Prints one line:
COMMITTED <hash> <n> files [pushed|push failed] or NOTHING or HALT.
"""
import os
import subprocess
import sys

ROOT = os.environ.get("PROTEUS_TEST_ROOT") or "/Users/triton/PROTEUS"   # override: tests only


def git(args, timeout=120):
    r = subprocess.run(["git", "-C", ROOT] + args, capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout + r.stderr).strip()


def rel(p):
    p = os.path.abspath(p)
    return os.path.relpath(p, ROOT) if p.startswith(ROOT + "/") else None


def commit(paths, msg):
    if os.path.exists(ROOT + "/HALT"):
        return "HALT set: nothing staged, nothing committed"
    rels = [rel(p) for p in paths]
    outside = [p for p, r in zip(paths, rels) if r is None]
    if outside:
        return "REFUSED: outside %s: %s" % (ROOT, ", ".join(outside))
    present = [r for r in rels if os.path.exists(os.path.join(ROOT, r))]
    gone = [r for r in rels if r not in present]
    if present:
        rc, out = git(["add", "--"] + present)
        if rc:
            return "FAILED add: " + out[-200:]
    if gone:
        git(["rm", "-q", "--cached", "-r", "--ignore-unmatch", "--"] + gone)
    rc, out = git(["diff", "--cached", "--quiet", "--"] + rels)
    if rc == 0:
        return "NOTHING to commit in those paths"
    rc, out = git(["commit", "-q", "-m", msg, "--"] + rels)
    if rc:
        return "FAILED commit: " + out[-200:]
    _, h = git(["rev-parse", "--short", "HEAD"])
    _, n = git(["diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"])
    files = len([x for x in n.splitlines() if x])
    rc, out = git(["push", "-q", "origin", "main"], timeout=90)
    if rc:
        git(["fetch", "-q", "origin", "main"], timeout=90)
        mrc, mout = git(["merge", "-q", "--no-edit", "origin/main"])
        if mrc:
            git(["merge", "--abort"])
            return "COMMITTED %s %d files, push failed and merge refused (%s); next commit carries it" % (h, files, mout[-120:])
        rc, out = git(["push", "-q", "origin", "main"], timeout=90)
    return "COMMITTED %s %d files, %s" % (h, files, "pushed" if rc == 0 else "push failed: " + out[-120:])


def main(argv):
    if "-m" not in argv or argv.index("-m") + 1 >= len(argv):
        print(__doc__)
        return 2
    i = argv.index("-m")
    msg = argv[i + 1]
    paths = argv[1:i] + argv[i + 2:]
    if not paths:
        print("name at least one path")
        return 2
    print(commit(paths, msg))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
