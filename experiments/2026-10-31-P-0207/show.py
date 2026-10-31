#!/usr/bin/env python3
"""Print claim, mechanism and the brief section for (date, n) pairs, to read the misses by hand.
Run: python3 .../show.py 2026-10-24:1 2026-10-24:6 ..."""
import importlib.util
import json
import sys

ROOT = "/Users/triton/PROTEUS/"
spec = importlib.util.spec_from_file_location("factcheck", ROOT + "experiments/2026-10-23-P-0206/factcheck.py")
fc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fc)

for arg in sys.argv[1:]:
    date, n = arg.split(":")
    n = int(n)
    with open(f"{ROOT}state/harvest/{date}/brief.md") as fh:
        secs = fc.sections(fh.read())
    with open(f"{ROOT}state/agents/{date}/harvest.json") as fh:
        item = json.load(fh)[n - 1]
    print(f"\n#### {date} item {n} {item.get('key')}")
    print("CLAIM:", item.get("claim"))
    print("MECH :", item.get("mechanism"))
    print("---- section ----")
    print(secs.get(n, "")[:2500])
