#!/usr/bin/env python3
"""Print 80 chars of context around each hit of a pattern in a brief. Run: find.py FILE PATTERN [PATTERN...]"""
import re
import sys

text = open(sys.argv[1]).read()
for pat in sys.argv[2:]:
    hits = [m.start() for m in re.finditer(pat, text, re.I)]
    print(f"== {pat}: {len(hits)} hits")
    for h in hits[:6]:
        print("   ", text[max(0, h - 80):h + 80].replace("\n", " "))
