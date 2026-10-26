"""F-0056 check: which decisions-log dates the hook's spawn counter reads, old way and patched way.
Smith 26 Oct 2026. Pure date arithmetic, reads no logs.

    python3 /Users/triton/PROTEUS/state/loop/hook-patches/F-0056-check.py

Exit 0 when the old way shows the bug (same date twice on 25 Oct 2026) and the patched way gives two
distinct consecutive dates at every probe instant; exit 1 otherwise.
"""
import calendar
import os
import sys
import time

os.environ["TZ"] = "Europe/London"
time.tzset()


def old_days(t):
    return [time.strftime("%Y-%m-%d", time.localtime(d)) for d in (t - 86400, t)]


def new_days(t):
    now = time.localtime(t)
    yday = time.localtime(time.mktime((now.tm_year, now.tm_mon, now.tm_mday - 1, 12, 0, 0, 0, 0, -1)))
    return [time.strftime("%Y-%m-%d", d) for d in (yday, now)]


CASES = [
    ("2026-10-25 23:31:06", ("2026-10-24", "2026-10-25")),   # the night of F-0056, BST ended that morning
    ("2026-10-25 00:30:00", ("2026-10-24", "2026-10-25")),
    ("2026-03-29 23:30:00", ("2026-03-29", "2026-03-30")),   # BST began; 00:30 BST on the 30th, old way skips the 29th
    ("2026-03-01 00:10:00", ("2026-02-28", "2026-03-01")),   # month edge
    ("2027-01-01 12:00:00", ("2026-12-31", "2027-01-01")),   # year edge
    ("2026-10-26 20:05:00", ("2026-10-25", "2026-10-26")),
]

bad = 0
for utc, want in CASES:
    t = calendar.timegm(time.strptime(utc, "%Y-%m-%d %H:%M:%S"))
    o, n = old_days(t), new_days(t)
    ok = tuple(n) == want
    bad += not ok
    print("%s UTC  old %s  new %s  %s" % (utc, o, n, "OK" if ok else "WRONG, want %s" % (want,)))
bug = old_days(calendar.timegm(time.strptime("2026-10-25 23:31:06", "%Y-%m-%d %H:%M:%S")))
print("old way on F-0056's night reads the same file twice: %s" % (bug[0] == bug[1]))
sys.exit(0 if bad == 0 and bug[0] == bug[1] else 1)
