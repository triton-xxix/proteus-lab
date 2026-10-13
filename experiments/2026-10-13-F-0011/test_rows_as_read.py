#!/usr/bin/env python3
"""F-0011 test, Smith 13 Oct 2026: does scan.py write SNAPSHOTS.csv rows as it reads them?

Runs scan.snapshot(limit=3) with every output path pointed at this folder (SNAPSHOTS.csv, cache,
watchlist, established.json, insiders), so the live record is untouched. Run it in the background and
read out/SNAPSHOTS.csv while it is still going: rows there before the process exits is the proof the
9825d44 fix gives a partial snapshot on a kill, not an empty one.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/experiments/2026-10-13-F-0011/test_rows_as_read.py
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__)) + "/"
OUT = HERE + "out/"
os.makedirs(OUT + "grinder/insiders", exist_ok=True)
sys.path.insert(0, "/Users/triton/PROTEUS/grinder")
import scan  # noqa: E402

scan.ROOT = OUT
scan.CACHE = OUT + "cache/"
scan.SNAP_CSV = OUT + "SNAPSHOTS.csv"
scan.WATCHLIST = OUT + "cache/watchlist.jsonl"
scan.EST_LIMIT = 3   # 3 fresh + 3 established, about a minute of rows

t0 = time.time()
print("start", time.strftime("%H:%M:%S"), flush=True)
rows = scan.snapshot(3)
print("done", time.strftime("%H:%M:%S"), "rows", len(rows), "in %.0f s" % (time.time() - t0), flush=True)
with open(OUT + "SNAPSHOTS.csv") as fh:
    lines = fh.read().splitlines()
live_header = open("/Users/triton/PROTEUS/grinder/SNAPSHOTS.csv").readline().rstrip("\n")
print("csv lines", len(lines), "header matches live:", lines[0] == live_header)
