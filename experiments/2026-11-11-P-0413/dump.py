"""P-0413 step 1: print the 35 young works verdicts (P-0412) with their notes, for reading."""
import json

ROOT = "/Users/triton/PROTEUS"
rows = json.load(open(ROOT + "/experiments/2026-11-11-P-0412/results.json"))["rows"]
probes = {p["id"]: p for p in json.load(open(ROOT + "/state/probes.json"))["items"]}
young = [r for r in rows if r["age_days"] is not None and r["age_days"] < 14 and r["verdict"] == "works"]
print(len(young))
for r in young:
    p = probes[r["probe"]]
    print("%s | %s | age %d | %s\n  T: %s\n  N: %s" % (r["probe"], r["repo"], r["age_days"], r["queued"], p["title"][:150], (p.get("note") or "")[:330]))
