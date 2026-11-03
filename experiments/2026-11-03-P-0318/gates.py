"""P-0318: per night since 20 Oct 2026, how many Grinder candidates fail exactly one gate, and which gate.
Reads grinder/SNAPSHOTS.csv and imports paper.py's GATES and RULES unchanged (read-only)."""
import csv, json, sys, collections
sys.path.insert(0, "/Users/triton/PROTEUS/grinder")
import paper  # noqa: E402

rows = [r for r in csv.DictReader(open("/Users/triton/PROTEUS/grinder/SNAPSHOTS.csv")) if r["ts"] >= "2026-10-20"]
nights = collections.defaultdict(list)
for r in rows:
    nights[r["ts"]].append(r)
total_single = collections.Counter()
per_night = []
for ts in sorted(nights):
    snap = nights[ts]
    single = collections.Counter()
    passed = 0
    for r in snap:
        fails = [g for g, f in paper.GATES.items() if not f(r)]
        if not fails:
            passed += 1
        elif len(fails) == 1:
            single[fails[0]] += 1
    total_single.update(single)
    per_night.append({"ts": ts, "candidates": len(snap), "pass_all": passed, "one_gate_short": sum(single.values()),
                      "by_gate": dict(single)})
    print(ts, len(snap), "pass", passed, "one short", sum(single.values()), dict(single))
summ = {"nights": len(per_night), "candidates": len(rows), "pass_all": sum(n["pass_all"] for n in per_night),
        "one_gate_short": sum(total_single.values()), "by_gate": dict(total_single.most_common()),
        "rules": {k: v for k, v in paper.RULES.items() if isinstance(v, (int, float))}}
print(json.dumps(summ))
json.dump({"summary": summ, "nights": per_night}, open("/Users/triton/PROTEUS/experiments/2026-11-03-P-0318/results.json", "w"), indent=1)
