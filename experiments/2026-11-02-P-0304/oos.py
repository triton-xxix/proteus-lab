"""P-0304: P-0292 out of sample. The same script, run on the meetings and trades it left out: MPC decisions
from 1997 to 2008 (P-0292 kept 2009 onwards). Everything else is unchanged: 5-day pre-window, RSI(5)
next-open trades, random-entry control, permutation test against trades outside any pre-window.
The source is read, three lines are swapped, and it runs; the swaps are asserted so a changed source fails.

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 -I experiments/2026-11-02-P-0304/oos.py
"""
SRC = "/Users/triton/PROTEUS/experiments/2026-11-02-P-0292/mpc_bucket_split.py"
EXP = "/Users/triton/PROTEUS/experiments/2026-11-02-P-0304"
code = open(SRC).read()
swaps = [
    ('OUT = "/Users/triton/PROTEUS/experiments/2026-11-02-P-0292/results.json"', 'OUT = "%s/results.json"' % EXP),
    ('MEET = "/Users/triton/PROTEUS/experiments/2026-11-02-P-0292/meetings.json"', 'MEET = "%s/meetings.json"' % EXP),
    ('        if r["date"] < dt.date(2009, 1, 1):\n            continue',
     '        if not dt.date(1997, 1, 1) <= r["date"] < dt.date(2009, 1, 1):\n            continue'),
    ('start = int(np.searchsorted(idx, np.datetime64("2009-01-01")))', 'start = 0'),
]
for old, new in swaps:
    assert old in code, old
    code = code.replace(old, new)
# trades after 2008 must not count: stop each symbol's walk at the first 2009 bar
old = "        rets, tid = rsi5_next_open_rp(o, c, 1)"
assert old in code
code = code.replace(old, old + '\n        end09 = int(np.searchsorted(idx, np.datetime64("2009-01-01")))')
old = "            if x == len(c) - 1 and rets[x] == np.log(c[x]) - np.log(c[x - 1]):"
assert old in code
code = code.replace(old, "            if e < 201 or x >= end09:\n                continue\n" + old)
old = "        for i in range(start, len(o) - 60):"
assert old in code
code = code.replace(old, "        for i in range(max(start, 200), min(len(o) - 60, end09)):")
code = code.replace('"meetings_since_2009"', '"meetings_1997_2008"')
exec(compile(code, SRC + " (P-0304 swaps)", "exec"))
