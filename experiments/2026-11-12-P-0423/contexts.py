"""P-0423, second pass: print the sentence around every not-run phrase in the flagged ran folders,
and around every install word, so the labels can be checked by reading. Read only."""
import json
import os
import re

ROOT = "/Users/triton/PROTEUS"
res = json.load(open(ROOT + "/experiments/2026-11-12-P-0423/results.json"))
PH = re.compile(r"(not|never|did not|didn't|without) (run|ran|execut|install)|not executed|was not run|read only", re.I)
for r in res["rows"]:
    if r["label"] != "ran" or not r["not_run_phrases"]:
        continue
    print("==", r["id"], "|", r["why"])
    seen = 0
    for f in r["folders"]:
        for d, _, fs in os.walk(os.path.join(ROOT, f)):
            for name in fs:
                if not name.lower().endswith((".md", ".txt")):
                    continue
                t = open(os.path.join(d, name), errors="replace").read().replace("\n", " ")
                for m in PH.finditer(t):
                    if seen >= 3:
                        break
                    print("   ...%s..." % t[max(0, m.start() - 130):m.end() + 90])
                    seen += 1
