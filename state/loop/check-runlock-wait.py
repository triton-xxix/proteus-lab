#!/usr/bin/env python3
"""F-0073 check: bin/runlock.py waits for the lock instead of skipping. Temp state folder only.

Replays 5 Nov 2026: a nightly marker holds the lock, day slots fire, the nightly closes, the slots
run one after another. Exit 0 when every case holds.
"""
import json
import os
import subprocess
import sys
import tempfile
import threading
import time

SCRIPT = "/Users/triton/PROTEUS/bin/runlock.py"
state = tempfile.mkdtemp(prefix="runlock-check-")
env = dict(os.environ, PROTEUS_TEST_STATE=state, CLAUDE_CODE_SESSION_ID="check-session")
env.pop("CLAUDE_CODE_SESSION_ATTENDED", None)
fails = 0


def run(*args):
    return subprocess.run([sys.executable, SCRIPT] + list(args), env=env, capture_output=True, text=True).stdout.strip()


def case(name, ok, seen=""):
    global fails
    print(("OK   " if ok else "FAIL ") + name + ("" if ok else "  got: " + seen))
    if not ok:
        fails += 1


def write(name, obj):
    with open(os.path.join(state, name), "w") as fh:
        json.dump(obj, fh)


now = time.time()
write("unattended-session.json", {"session_id": "nightly", "task": "proteus-nightly", "bound_at": now})

out = run("acquire", "inspector", "--minutes", "40")
case("held by the nightly: WAIT, not SKIP", out.startswith("WAIT: lock held by proteus-nightly"), out)
case("WAIT names the wait command and the timeout", "runlock.py wait inspector --minutes 40" in out and "600000" in out, out)
case("wait file written outside the marker folder", os.path.exists(state + "/lock-wait-inspector.json"))
case("no lock taken while waiting", not os.path.exists(state + "/run.lock"))

t0 = time.time()
out = run("wait", "inspector", "--minutes", "40")
case("wait returns WAIT when its call time runs out", out.startswith("WAIT:") and 3 < time.time() - t0 < 10, out)

threading.Timer(1.5, lambda: write("unattended-session.json", {"session_id": "closed", "task": "proteus-nightly"})).start()
out = run("wait", "inspector", "--minutes", "40")
case("wait takes the lock once the nightly closes", out.startswith("ACQUIRED inspector"), out)
case("acquiring clears the wait file", not os.path.exists(state + "/lock-wait-inspector.json"))
case("acquiring writes the marker", os.path.exists(state + "/unattended/inspector.json"))

out = run("acquire", "trials", "--minutes", "40")
case("second slot waits behind the first", out.startswith("WAIT: lock held by inspector"), out)
run("release", "inspector")
out = run("wait", "trials", "--minutes", "40")
case("second slot goes after the release", out.startswith("ACQUIRED trials"), out)

write("lock-wait-workshop.json", {"since": time.time() - 151 * 60})
out = run("acquire", "workshop", "--minutes", "40")
case("past the 150-minute cap: SKIP", out.startswith("SKIP:"), out)
case("SKIP clears the wait file", not os.path.exists(state + "/lock-wait-workshop.json"))

write("lock-wait-workshop.json", {"since": time.time() - 300 * 60})
out = run("acquire", "workshop", "--minutes", "40")
case("a dead run's old wait file starts the wait again", out.startswith("WAIT:"), out)

run("release", "trials")
run("release", "workshop")
out = run("status")
case("free after the releases", out == "FREE", out)

# Two slots released at the same moment: exactly one gets the lock.
write("run.lock", {"task": "holder", "start": time.time(), "deadline": time.time() + 3600})
results = {}


def contender(task):
    results[task] = run("wait", task, "--minutes", "40")


threads = [threading.Thread(target=contender, args=(t,)) for t in ("smith", "trials")]
for th in threads:
    th.start()
time.sleep(1.2)
os.remove(state + "/run.lock")
for th in threads:
    th.join()
won = [t for t, o in results.items() if o.startswith("ACQUIRED")]
lost = [t for t, o in results.items() if o.startswith("WAIT")]
case("two polling together: one wins, one waits", len(won) == 1 and len(lost) == 1, str(results))

print("%d failed" % fails)
sys.exit(1 if fails else 0)
