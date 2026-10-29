"""Smith 29 Oct 2026, F-0051: check `probe.py next` without opening a loop or touching the queue.

The refill count cap is gone; a refill needs 25 minutes left and a reserve of REFILL_RESERVE unused
rows in REFILL-SOURCES.md, and at the reserve `next` prints SOURCES instead of STOP. Every side
effect (loop file, run log, git) is patched out. Prints one line per case; exit 1 on any failure.

    python3 /Users/triton/PROTEUS/state/loop/check-refill-cap.py
"""
import argparse
import importlib.util
import io
import sys
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone

spec = importlib.util.spec_from_file_location("probe", "/Users/triton/PROTEUS/bin/probe.py")
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)

ROW = ["47", "GitHub REST API", "curl", "re-count stars"]


def run(left, unused_n, refills=3, no_refill=False, probes=7):
    lp = {"key": "test", "deadline": (datetime.now(timezone.utc) + timedelta(minutes=left)).strftime("%Y-%m-%dT%H:%M:%S+0000"),
          "max_probes": 10, "max_calls": 150, "probes": ["P-%04d" % i for i in range(probes)], "refills": refills}
    p.current_loop = lambda: lp
    p.load_state = lambda: {"items": []}
    p.budget_lines = lambda lp_: (left, 50, "budget: test")
    p.halted = lambda: False
    p.save_loop = lambda lp_: None
    p.stop_loop = lambda lp_, reason, st=None: print("STOP: " + reason)
    p.runnable = lambda st, left_: ([], {"needs": [{"id": "P-0025", "needs": "vim"}], "after": [], "cull": [], "fit": []}, [{"id": "P-0025"}])
    p.unused_refill_rows = lambda txt=None: [ROW] * unused_n
    buf = io.StringIO()
    with redirect_stdout(buf):
        p.cmd_next(argparse.Namespace(no_refill=no_refill))
    return buf.getvalue(), lp


CASES = [
    # name, kwargs, must contain, must not contain
    ("4th refill with 53 min left and 7 unused rows (the 28 Oct night)", dict(left=53, unused_n=7), "REFILL 4 tonight", "STOP"),
    ("refill allowed down to the reserve (4 unused, 3 stay)", dict(left=40, unused_n=4), "REFILL 4 tonight", "STOP"),
    ("LOW printed when under 6 rows remain after this one", dict(left=40, unused_n=5), "LOW: 4 unused", "STOP"),
    ("at the reserve: SOURCES, not STOP", dict(left=53, unused_n=3), "SOURCES:", "STOP"),
    ("list dry: SOURCES, not STOP", dict(left=53, unused_n=0), "has 0 unused row(s)", "STOP"),
    ("under the 25-minute floor: STOP as before", dict(left=20, unused_n=7), "under the 25 needed", "REFILL"),
    ("--no-refill: STOP as before", dict(left=53, unused_n=7, no_refill=True), "STOP: nothing runnable", "refill"),
]

bad = 0
for name, kw, must, must_not in CASES:
    out, lp = run(**kw)
    ok = must in out and must_not not in out
    print(("OK   " if ok else "FAIL ") + name + ("" if ok else "\n" + out))
    bad += 0 if ok else 1
out, lp = run(left=53, unused_n=7)
if lp["refills"] != 4:
    print("FAIL refills counter did not advance (%r)" % lp["refills"])
    bad += 1
print("%d of %d cases pass" % (len(CASES) + 1 - bad, len(CASES) + 1))
sys.exit(1 if bad else 0)
