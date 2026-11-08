"""Draws the blind sheet RULE.md describes from a digest.py --dump file.
python3 sample.py <dump.jsonl> <outdir>
Writes sheet.jsonl (id and text only) and key.jsonl (id, stratum, score, video, t)."""
import json
import os
import random
import sys

src, out = sys.argv[1], sys.argv[2]
rows = [json.loads(x) for x in open(src)]
rng = random.Random(20261108)
strata = {"flagged": [r for r in rows if r["flagged"]],
          "cut": [r for r in rows if not r["flagged"] and r["score"] >= 3],
          "below": [r for r in rows if r["score"] < 3]}
want = {"flagged": 60, "cut": 30, "below": 60}
picked = []
for name, pool in strata.items():
    for r in rng.sample(pool, min(want[name], len(pool))):
        picked.append(dict(r, stratum=name))
rng.shuffle(picked)
os.makedirs(out, exist_ok=True)
with open(os.path.join(out, "sheet.jsonl"), "w") as f:
    for i, r in enumerate(picked, 1):
        f.write(json.dumps({"id": i, "text": r["text"]}) + "\n")
with open(os.path.join(out, "key.jsonl"), "w") as f:
    for i, r in enumerate(picked, 1):
        f.write(json.dumps({"id": i, "stratum": r["stratum"], "score": r["score"], "video": r["video"], "t": r["t"]}) + "\n")
print({k: len(v) for k, v in strata.items()}, "| sheet", len(picked), {k: sum(1 for r in picked if r["stratum"] == k) for k in strata})
