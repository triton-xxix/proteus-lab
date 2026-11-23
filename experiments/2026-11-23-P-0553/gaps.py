"""P-0553: Munich daily-high ladders with a whole degree missing inside their range.

Usage: python3 -I gaps.py SNAPSHOTS.csv munich_outcomes.jsonl OUT_JSON
A ladder is the union of contracts ever seen for a Munich market. Bins like
'-3°C or below' and '7°C or higher' are the open ends; the inside is every
whole degree strictly between them.
"""
import csv, json, re, sys
from collections import defaultdict

snaps, outs, out = sys.argv[1:4]
lad = defaultdict(set); name = {}
for r in csv.DictReader(open(snaps, encoding="utf-8")):
    if "Munich" not in r["market"] and "munich" not in r["event"].lower():
        continue
    if "Temperature" not in r["market"]:
        continue
    lad[r["market_id"]].add(r["contract"]); name[r["market_id"]] = r["market"]
win = {}
for line in open(outs, encoding="utf-8"):
    o = json.loads(line); win[o["market_id"]] = o["winner"]

def deg(c):
    m = re.match(r"(-?\d+)\s*°C(.*)", c)
    return (int(m.group(1)), m.group(2).strip().lower()) if m else (None, c)

rows = []
for mid, cs in lad.items():
    exact, lo, hi = [], None, None
    for c in cs:
        d, tail = deg(c)
        if d is None: continue
        if "below" in tail or "lower" in tail: lo = d
        elif "higher" in tail or "above" in tail: hi = d
        else: exact.append(d)
    if lo is None or hi is None: continue
    inside = set(range(lo + 1, hi))
    missing = sorted(inside - set(exact))
    w = win.get(mid)
    wd = deg(w)[0] if w else None
    rows.append({"market_id": mid, "market": name[mid], "low_bin": lo, "high_bin": hi,
                 "n_exact": len(set(exact)), "missing": missing, "winner": w,
                 "winner_in_gap": (wd in missing) if wd is not None else None})
rows.sort(key=lambda r: r["market"])
gappy = [r for r in rows if r["missing"]]
res = {"ladders": len(rows), "with_gap": len(gappy),
       "winners_known": sum(r["winner"] is not None for r in rows),
       "gappy_with_winner": sum(r["winner"] is not None for r in gappy),
       "winner_in_gap": [r for r in rows if r["winner_in_gap"]],
       "gappy": gappy}
json.dump(res, open(out, "w"), indent=1, ensure_ascii=False)
print("ladders", res["ladders"], "with a gap", res["with_gap"], "winners known", res["winners_known"],
      "gappy with winner", res["gappy_with_winner"], "winner in gap", len(res["winner_in_gap"]))
for r in gappy:
    print(" ", r["market"][-30:], "bins", r["low_bin"], "to", r["high_bin"], "missing", r["missing"], "winner", r["winner"])
