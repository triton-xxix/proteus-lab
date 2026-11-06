"""Where do the dead ends in results.json stop, and do those pages really have no qualifying link?"""
import json
import sys
from collections import Counter

r = json.load(open("/Users/triton/PROTEUS/experiments/2026-11-05-P-0332/results.json"))
for d, v in r["dates"].items():
    rows = v.get("rows") or []
    if not rows:
        continue
    ends = Counter(x["path"][-1] for x in rows if x["outcome"] == "dead end")
    hops = Counter(x["hops"] for x in rows if x["outcome"] == "dead end")
    print(d, "dead ends", sum(ends.values()), "top ends", ends.most_common(8), "at hop 0:", hops.get(0, 0))
