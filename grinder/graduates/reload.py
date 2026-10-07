"""The one permitted reload of the graduation watcher (RULES.md, G2 "Running" paragraph).

The watcher stops itself 7 days after START. RULES.md says: if G2 is short of 400 counted at
the 7 Oct stop, reload once from this folder for a fresh 7-day window and say so in the run
log. This script does exactly that and nothing else: it records the old START and DONE values
in events.jsonl, removes both markers, and bootstraps the launchd job through watcher.load().

It refuses to run a second time: if events.jsonl already holds a "reload" line, it exits.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/grinder/graduates/reload.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import watcher  # noqa: E402


def main():
    if os.path.exists(watcher.HALT):
        print("HALT present, not reloading")
        return 1
    if os.path.exists(watcher.EVENTS):
        for line in open(watcher.EVENTS):
            try:
                if json.loads(line).get("kind") == "reload":
                    print("already reloaded once; RULES.md allows one reload. Not reloading.")
                    return 1
            except ValueError:
                continue
    if not os.path.exists(watcher.DONE):
        print("no DONE marker: the watcher has not stopped, nothing to reload")
        return 1
    old_start = open(watcher.START).read().strip() if os.path.exists(watcher.START) else None
    old_done = open(watcher.DONE).read().strip()
    watcher.log("reload", old_start=old_start, old_done=old_done, window_days=watcher.DAYS)
    os.remove(watcher.DONE)
    if old_start is not None:
        os.remove(watcher.START)
    watcher.load()
    print("reloaded: old START %s, old DONE %s, fresh %d-day window" % (old_start, old_done, watcher.DAYS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
