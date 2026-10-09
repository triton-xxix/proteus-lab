#!/usr/bin/env python3
"""Which desks have gone quiet: days since each last committed a new row, against a threshold.

    python3 /Users/triton/PROTEUS/bin/silence.py            # print the table
    python3 /Users/triton/PROTEUS/bin/silence.py --findings # also add each SILENT desk to the findings register

Written 9 Oct 2026 for the Inspector. The audit found the Pitch model had committed one prediction
in seventeen nights, the judgement book nothing since 1 Oct, Lichess nothing since 6 Oct and the
intel lane nothing since 3 Oct, and no step had noticed any of it. "Last new row" is read from git:
the newest commit that ADDED lines to the desk's file (or any file under its folder), so a script
that rewrites a file without adding to it does not count as activity. Read-only apart from --findings.
"""
import subprocess
import sys
import time

ROOT = "/Users/triton/PROTEUS"
# desk, path, days allowed without a new row, why the threshold
DESKS = [
    ("grinder-snapshot", "grinder/SNAPSHOTS.csv", 2, "nightly scan, every night"),
    ("grinder-ledger", "grinder/LEDGER.csv", 4, "entries can pause a few nights"),
    ("graduation-book", "grinder/graduates/closed.jsonl", 2, "launchd watcher, continuous"),
    ("pitch-model", "pitch/PREDICTIONS.csv", 4, "league weekends at least weekly"),
    ("judgement-book", "pitch/JUDGEMENT.csv", 7, "interactive calls, weekly at least"),
    ("exchange-book", "exchange/BOOK.csv", 4, "up to two blind calls a night"),
    ("systems-book", "systems/SIGNALS.csv", 5, "a row per close"),
    ("lichess", "games/lichess/GAMES.csv", 2, "morning job, daily"),
    ("nolan", "sites/nolan/films", 4, "one film a night until done"),
    ("intel", "intel", 10, "one write-up a fortnight at least"),
    ("probes", "state/probes.json", 2, "nightly loop"),
    ("field-notes-draft", "field-notes/drafts", 3, "one item a night"),
    ("harvest", "state/harvest", 2, "nightly harvest"),
]


def adding_commits(path):
    """Unix times, newest first, of recent commits that added at least one line under path."""
    r = subprocess.run(["git", "-C", ROOT, "log", "--format=@%ct", "--numstat", "-n", "200", "--", path],
                       capture_output=True, text=True)
    out, t = [], None
    for line in r.stdout.splitlines():
        if line.startswith("@"):
            t = int(line[1:])
            continue
        parts = line.split("\t")
        if t is not None and len(parts) == 3 and parts[0] not in ("0", "-") and (not out or out[-1] != t):
            out.append(t)
    return out


def main():
    add = "--findings" in sys.argv
    now = time.time()
    silent = []
    # days since the last adding commit, and how many adding commits in the last 7 days: a desk that
    # adds one row every four days passes the first and shows up in the second
    print("%-18s %-34s %6s %4s %4s  %s" % ("desk", "path", "days", "max", "7d", "state"))
    for desk, path, limit, why in DESKS:
        ts = adding_commits(path)
        t = ts[0] if ts else None
        week = sum(1 for x in ts if now - x <= 7 * 86400)
        days = (now - t) / 86400 if t else None
        state = "never" if t is None else ("SILENT" if days > limit else "ok")
        print("%-18s %-34s %6s %4d %4d  %s" % (desk, path, "-" if days is None else "%.1f" % days, limit, week, state))
        if state != "ok":
            silent.append((desk, path, days, limit, why))
    if add and silent:
        for desk, path, days, limit, why in silent:
            ev = "%s: no new row committed for %s days (allowed %d: %s)" % (
                path, "ever" if days is None else "%.1f" % days, limit, why)
            subprocess.run([sys.executable, ROOT + "/bin/findings.py", "add", "--source", "silence",
                            "--desk", desk, "--severity", "med", "--title", "desk silent", "--evidence", ev])
    print("%d silent of %d" % (len(silent), len(DESKS)))


if __name__ == "__main__":
    main()
