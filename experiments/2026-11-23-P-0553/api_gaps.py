"""P-0553 part 2: ladders of the last twelve settled Munich markets, from the Smarkets API contracts call.

Usage: python3 -I api_gaps.py contracts.json munich_outcomes.jsonl OUT_JSON
"""
import json, re, sys
from collections import defaultdict
src, outs, out = sys.argv[1:4]
cs = json.load(open(src))["contracts"]
win = {}; ev = {}
for line in open(outs, encoding="utf-8"):
    o = json.loads(line); win[o["market_id"]] = o["winner"]; ev[o["market_id"]] = o["event"]
lad = defaultdict(list)
for c in cs:
    lad[str(c["market_id"])].append(c["name"])
rows = []
for mid, names in lad.items():
    exact, lo, hi = set(), None, None
    for n in names:
        m = re.match(r"(-?\d+)\s*°C(.*)", n)
        if not m: continue
        d, t = int(m.group(1)), m.group(2).lower()
        if "below" in t or "lower" in t: lo = d
        elif "higher" in t or "above" in t: hi = d
        else: exact.add(d)
    miss = sorted(set(range(lo + 1, hi)) - exact) if lo is not None and hi is not None else None
    w = win.get(mid); wd = int(re.match(r"-?\d+", w).group()) if w else None
    rows.append({"market_id": mid, "event": ev.get(mid), "n_contracts": len(names), "low_bin": lo,
                 "high_bin": hi, "missing": miss, "winner": w,
                 "winner_in_gap": (wd in miss) if miss is not None and wd is not None else None,
                 "winner_at_open_end": (wd is not None and lo is not None and hi is not None and (wd <= lo or wd >= hi))})
rows.sort(key=lambda r: r["market_id"])
json.dump(rows, open(out, "w"), indent=1, ensure_ascii=False)
print("markets", len(rows), "with a gap", sum(bool(r["missing"]) for r in rows),
      "winner in gap", sum(bool(r["winner_in_gap"]) for r in rows),
      "winner at an open end", sum(r["winner_at_open_end"] for r in rows))
for r in rows:
    print(" ", r["event"], r["low_bin"], "to", r["high_bin"], "missing", r["missing"], "winner", r["winner"], r["n_contracts"])
