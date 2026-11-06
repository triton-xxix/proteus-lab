"""Does any looping walk before today have Knowledge inside its cycle? Lists every ring per date."""
import json
import sys
from collections import Counter

sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-11-05-P-0332")
from ringdate import ring_of

f = json.load(open("/Users/triton/PROTEUS/experiments/2026-11-05-P-0332/final.json"))
for d, v in f["dates"].items():
    rows = [r for r in v.get("rows", []) if r["outcome"] == "loop"]
    rings = Counter(tuple(sorted(ring_of(r["path"]))) for r in rows)
    k = sum(n for ring, n in rings.items() if "Knowledge" in ring)
    print(d, "loops", len(rows), "with Knowledge in the cycle", k, "rings", [(" > ".join(a), n) for a, n in rings.most_common(6)])
