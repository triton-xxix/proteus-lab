#!/usr/bin/env python3
"""Workshop 16 Nov 2026: what do Lichess's 400 refusals say? Scratch look before the ladder slice."""
import csv
import json
import re
from collections import Counter

CHALL = "/Users/triton/PROTEUS/games/lichess/CHALLENGES.csv"
rows = [c for c in csv.DictReader(open(CHALL)) if c["verdict"].startswith("refused")]
shapes = Counter()
for c in rows:
    d = c["detail"] or ""
    m = re.search(r'"error":"(.*)', d)
    t = m.group(1) if m else d
    t = re.sub(r"\d{4}-\d\d-\d\dT[\d:.]+Z", "<T>", t)
    t = re.sub(r"\b\d+\b", "<N>", t)
    t = re.sub(r"^\S+ ", "<BOT> ", t)
    shapes[(c["verdict"], t[:90])] += 1
for k, v in shapes.most_common():
    print(v, k)
