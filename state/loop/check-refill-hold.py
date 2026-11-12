"""Smith 12 Nov 2026: a `hold YYYY-MM-DD` in a refill row's `used` cell skips it that day only.

    python3 /Users/triton/PROTEUS/state/loop/check-refill-hold.py

Row 152 (YouTube captions) was offered twice in the 12 Nov Trials loop while the IP was blocked;
writing a date in `used` would have burnt the row, so the loop ended on the refill instead.
"""
import importlib.util
from datetime import timedelta

spec = importlib.util.spec_from_file_location("probe", "/Users/triton/PROTEUS/bin/probe.py")
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)

today = p.now().strftime("%Y-%m-%d")
yesterday = (p.now() - timedelta(days=1)).strftime("%Y-%m-%d")
TXT = "\n".join([
    "| # | Source | How to pull | A build it suggests | used |",
    "|---|---|---|---|---|",
    "| 1 | a | b | c | 2026-11-11 |",
    "| 2 | a | b | c | hold %s: IpBlocked |" % today,
    "| 3 | a | b | c | hold %s: IpBlocked |" % yesterday,
    "| 4 | ~~a~~ | b | c | |",
    "| 5 | a | b | c | |",
    "| 6 | a | b | c | 2026-11-11 (held over, hold on) |",
])
got = [r[0] for r in p.unused_refill_rows(TXT)]
CASES = [
    ("used row stays out", "1" not in got),
    ("held today is skipped", "2" not in got),
    ("held yesterday is back", "3" in got),
    ("struck row stays out", "4" not in got),
    ("empty row is offered", "5" in got),
    ("a dated note that merely contains the word hold stays used", "6" not in got),
    ("order kept, yesterday's hold first", got == ["3", "5"]),
]
bad = 0
for name, ok in CASES:
    print(("OK   " if ok else "FAIL ") + name)
    bad += 0 if ok else 1
live = [r[0] for r in p.unused_refill_rows()]
print("live list unused rows: %s" % ", ".join(live))
print("%d of %d OK" % (len(CASES) - bad, len(CASES)))
