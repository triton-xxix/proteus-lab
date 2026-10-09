#!/usr/bin/env python3
"""One Proteus scheduled run at a time, and a marker per task.

Written 9 Oct 2026 for the daytime loop. Until then there was one marker file and one run a day,
so nothing stopped a second scheduled run from clobbering the first's binding (its calls would
fall back to prompting and hang) or racing its pushes. This is the first call every task makes:

  acquire TASK --minutes N   take the lock and write state/unattended/TASK.json (unbound); the
                             hook binds it to this session on the next tool call. Prints
                             ACQUIRED, or SKIP with who holds it (then the run logs one line and stops).
  release TASK               drop the lock and the task's marker. Safe to call twice.
  status                     who holds it, until when.

The lock is state/run.lock: {task, start, deadline}. It is stale, and taken over, once the holder's
deadline plus 15 minutes has passed, so a crashed run costs at most one slot. The nightly's legacy
marker (state/unattended-session.json, bound and under three hours old) also counts as held, so a
daytime slot cannot start inside a nightly that predates this script.
"""
import json
import os
import sys
import time

ROOT = "/Users/triton/PROTEUS/"
# PROTEUS_TEST_STATE moves everything into a temp folder, as in the hook (tests only).
STATE = (os.environ["PROTEUS_TEST_STATE"].rstrip("/") + "/") if os.environ.get("PROTEUS_TEST_STATE") else ROOT + "state/"
LOCK = STATE + "run.lock"
MARKER_DIR = STATE + "unattended/"
LEGACY = STATE + "unattended-session.json"
GRACE_S = 15 * 60
LEGACY_MAX_S = 3 * 3600
TASK_CHARS = set("abcdefghijklmnopqrstuvwxyz0123456789-")


def hhmm(t):
    return time.strftime("%H:%M", time.localtime(t))


def read_json(path):
    try:
        with open(path) as fh:
            return json.load(fh)
    except Exception:
        return None


def write_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(obj, fh)
    os.replace(tmp, path)


def holder(now):
    """(task, start, deadline) of a live holder, or None."""
    lock = read_json(LOCK)
    if lock and now <= float(lock.get("deadline", 0)) + GRACE_S:
        return lock.get("task"), float(lock.get("start", 0)), float(lock.get("deadline", 0))
    legacy = read_json(LEGACY)
    if legacy and legacy.get("session_id") not in (None, "closed"):
        bound_at = float(legacy.get("bound_at") or 0)
        if now - bound_at <= LEGACY_MAX_S:
            return legacy.get("task") or "legacy", bound_at, bound_at + LEGACY_MAX_S
    return None


def acquire(task, minutes):
    now = time.time()
    held = holder(now)
    if held and held[0] != task:
        print("SKIP: lock held by %s since %s, deadline %s. Log one line and stop." % (held[0], hhmm(held[1]), hhmm(held[2])))
        return 0
    if held and held[0] == task:
        print("NOTE: %s already held the lock (a crashed earlier run of the same task); taking it over." % task)
    os.makedirs(MARKER_DIR, exist_ok=True)
    deadline = now + minutes * 60
    write_json(LOCK, {"task": task, "start": now, "deadline": deadline, "pid": os.getppid()})
    write_json(MARKER_DIR + task + ".json", {"session_id": None, "task": task})
    print("ACQUIRED %s at %s, deadline %s (%d min). Marker state/unattended/%s.json binds on your next call."
          % (task, hhmm(now), hhmm(deadline), minutes, task))
    return 0


def release(task):
    lock = read_json(LOCK)
    if lock and lock.get("task") == task:
        os.remove(LOCK)
    try:
        os.remove(MARKER_DIR + task + ".json")
    except FileNotFoundError:
        pass
    print("RELEASED %s" % task)
    return 0


def status():
    held = holder(time.time())
    if held:
        print("HELD by %s since %s, deadline %s" % (held[0], hhmm(held[1]), hhmm(held[2])))
    else:
        print("FREE")
    return 0


def main(argv):
    if len(argv) >= 2 and argv[1] == "status":
        return status()
    if len(argv) >= 3 and argv[1] in ("acquire", "release"):
        task = argv[2]
        if not task or set(task) - TASK_CHARS:
            print("task names are lower-case letters, digits and hyphens")
            return 2
        if argv[1] == "release":
            return release(task)
        minutes = 40
        if "--minutes" in argv:
            minutes = int(argv[argv.index("--minutes") + 1])
        return acquire(task, minutes)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
