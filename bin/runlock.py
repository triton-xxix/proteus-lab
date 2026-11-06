#!/usr/bin/env python3
"""One Proteus scheduled run at a time, and a marker per task.

Written 9 Oct 2026 for the daytime loop. Until then there was one marker file and one run a day,
so nothing stopped a second scheduled run from clobbering the first's binding (its calls would
fall back to prompting and hang) or racing its pushes. This is the first call every task makes:

  acquire TASK --minutes N   take the lock and write state/unattended/TASK.json, bound to this
                             session (CLAUDE_CODE_SESSION_ID from the environment). Prints
                             ACQUIRED, WAIT with who holds it (then the run calls `wait`), or SKIP
                             (the wait ran out: the run logs one line and stops).
  wait TASK --minutes N      block up to 9 minutes for the lock, then ACQUIRED, WAIT or SKIP as above.
                             Needs a Bash timeout of 600000; acquire itself returns at once.
  release TASK               drop the lock and the task's marker. Safe to call twice.
  status                     who holds it, until when.

The lock is state/run.lock: {task, start, deadline}. It is stale, and taken over, once the holder's
deadline plus 15 minutes has passed, so a crashed run costs at most one slot. The nightly's legacy
marker (state/unattended-session.json, bound and under three hours old) also counts as held, so a
daytime slot cannot start inside a nightly that predates this script.

Waiting came in on 6 Nov 2026 (F-0073). When the Mac wakes, every missed slot fires inside a few
minutes; on 5 Nov a 33-minute nightly took the lock first and four slots skipped for good. A slot now
waits up to 150 minutes in all, tracked in state/lock-wait-TASK.json, so they run one after another.
There is no queue order: whichever polls first after a release goes next.
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
WAIT_CAP_S = 150 * 60
TESTING = bool(os.environ.get("PROTEUS_TEST_STATE"))
WAIT_CALL_S = 4 if TESTING else 9 * 60
POLL_S = 1 if TESTING else 20
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
    tmp = "%s.%d.tmp" % (path, os.getpid())
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


def wait_path(task):
    # Not under state/unattended/: the hook treats every .json there as a run marker.
    return STATE + "lock-wait-" + task + ".json"


def clear_wait(task):
    try:
        os.remove(wait_path(task))
    except FileNotFoundError:
        pass


def wait_or_skip(task, minutes, held, now):
    """The lock is someone else's: tell the run to keep waiting, or that the wait has run out."""
    since = (read_json(wait_path(task)) or {}).get("since")
    # A file older than the cap by an hour was left by a run that died; start again.
    if not since or now - float(since) > WAIT_CAP_S + 3600:
        since = now
        write_json(wait_path(task), {"since": since})
    since = float(since)
    if now - since >= WAIT_CAP_S:
        clear_wait(task)
        print("SKIP: lock held by %s since %s, deadline %s; gave up after waiting from %s. Log one line and stop."
              % (held[0], hhmm(held[1]), hhmm(held[2]), hhmm(since)))
        return 0
    print("WAIT: lock held by %s since %s, deadline %s. Run `python3 %sbin/runlock.py wait %s --minutes %d` with a "
          "Bash timeout of 600000, and again each time it prints WAIT. It gives up by itself at %s."
          % (held[0], hhmm(held[1]), hhmm(held[2]), ROOT, task, minutes, hhmm(since + WAIT_CAP_S)))
    return 0


def acquire(task, minutes):
    now = time.time()
    held = holder(now)
    if held and held[0] != task:
        return wait_or_skip(task, minutes, held, now)
    if held and held[0] == task:
        print("NOTE: %s already held the lock (a crashed earlier run of the same task); taking it over." % task)
    os.makedirs(MARKER_DIR, exist_ok=True)
    deadline = now + minutes * 60
    token = "%d-%f" % (os.getpid(), now)
    write_json(LOCK, {"task": task, "start": now, "deadline": deadline, "pid": os.getppid(), "token": token})
    # Waiting slots poll at once after a release, so two can write here together. The last write
    # stands: read it back after a beat and the loser goes on waiting.
    time.sleep(1)
    lock = read_json(LOCK)
    if not lock or lock.get("token") != token:
        return wait_or_skip(task, minutes, holder(time.time()) or ("another run", now, now), time.time())
    clear_wait(task)
    # Claude Code puts the session id in every Bash call's environment, so the marker is written
    # already bound to this run. An unbound marker could be taken by any session in the folder that
    # made a call first, Luke's included (the old single marker had a 15-minute window for that).
    sid = os.environ.get("CLAUDE_CODE_SESSION_ID")
    if sid:
        write_json(MARKER_DIR + task + ".json", {"session_id": sid, "task": task, "bound_at": now})
        how = "bound to session %s" % sid[:8]
    else:
        write_json(MARKER_DIR + task + ".json", {"session_id": None, "task": task})
        how = "unbound; binds on your next call"
    print("ACQUIRED %s at %s, deadline %s (%d min). Marker state/unattended/%s.json %s."
          % (task, hhmm(now), hhmm(deadline), minutes, task, how))
    if os.environ.get("CLAUDE_CODE_SESSION_ATTENDED") == "1":
        print("NOTE: this session is attended; from now on the hook answers its calls (allow or deny, "
              "no prompts) until `runlock.py release %s`." % task)
    return 0


def wait(task, minutes):
    """Block until the lock is free or this call's time is up, then answer as acquire does."""
    end = time.time() + WAIT_CALL_S
    while time.time() < end:
        held = holder(time.time())
        if not held or held[0] == task:
            return acquire(task, minutes)
        time.sleep(POLL_S)
    return acquire(task, minutes)


def release(task):
    clear_wait(task)
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
    if len(argv) >= 3 and argv[1] in ("acquire", "wait", "release"):
        task = argv[2]
        if not task or set(task) - TASK_CHARS:
            print("task names are lower-case letters, digits and hyphens")
            return 2
        if argv[1] == "release":
            return release(task)
        minutes = 40
        if "--minutes" in argv:
            minutes = int(argv[argv.index("--minutes") + 1])
        if argv[1] == "wait":
            return wait(task, minutes)
        return acquire(task, minutes)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
