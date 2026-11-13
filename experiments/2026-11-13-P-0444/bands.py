"""P-0444: called-shot numbers against their own bands.
For each scored shot, parse the number text into a band (X to Y, between X and Y, at least X, under X,
about X), read the note's own hit/miss mark for the number (notes write "(shot: ..., hit)" or "shot ... missed"),
and split by stated p. Band width is (hi - lo) / midpoint for two-sided bands."""
import json, re
from collections import defaultdict

ROOT = "/Users/triton/PROTEUS/"
OUT = ROOT + "experiments/2026-11-13-P-0444/"
items = json.load(open(ROOT + "state/probes.json"))["items"]
NUM = r"(-?\d+(?:\.\d+)?)"
TWO = [re.compile(NUM + r"\s*%?\s*(?:to|-|–|and)\s*" + NUM), re.compile(r"between\s+" + NUM + r"\s*%?\s+and\s+" + NUM)]
ONE = re.compile(r"(at least|over|above|more than|under|below|fewer than|less than|at most|about|around|near)\s+" + NUM, re.I)
MARK = re.compile(r"shot[^.;]{0,120}?\b(hit|miss|missed|wrong|right)\b", re.I)


def band(text):
    t = text.lower()
    for rx in TWO:
        m = rx.search(t)
        if m:
            a, b = float(m.group(1)), float(m.group(2))
            if a < b:
                return "two", a, b
    m = ONE.search(t)
    if m:
        return m.group(1).lower(), float(m.group(2)), None
    return None, None, None


rows = []
for it in items:
    s = it.get("shot")
    if not s or it.get("status") != "done" or not it.get("verdict"):
        continue
    kind, lo, hi = band(s.get("number", ""))
    note = it.get("note") or ""
    mk = MARK.search(note)
    mark = None
    if mk:
        mark = "hit" if mk.group(1).lower() in ("hit", "right") else "miss"
    width = (hi - lo) / ((hi + lo) / 2) if kind == "two" and (hi + lo) > 0 else None
    rows.append({"id": it["id"], "p": s["p"], "expect": s["expect"], "verdict": it["verdict"], "verdict_hit": s["expect"] == it["verdict"],
                 "number": s.get("number", "")[:100], "kind": kind, "lo": lo, "hi": hi, "rel_width": None if width is None else round(width, 3),
                 "number_mark": mark})

by_p = defaultdict(lambda: {"n": 0, "banded": 0, "marked": 0, "number_hits": 0, "verdict_hits": 0, "widths": []})
for r in rows:
    k = "0.6 or less" if r["p"] <= 0.6 else "0.65 to 0.75" if r["p"] <= 0.75 else "0.8 and up"
    g = by_p[k]; g["n"] += 1; g["verdict_hits"] += r["verdict_hit"]
    if r["kind"]:
        g["banded"] += 1
    if r["kind"] and r["number_mark"]:
        g["marked"] += 1; g["number_hits"] += r["number_mark"] == "hit"
    if r["rel_width"] is not None:
        g["widths"].append(r["rel_width"])
summary = {}
for k, g in sorted(by_p.items()):
    w = sorted(g["widths"])
    summary[k] = {"shots": g["n"], "verdict_hit_rate": round(g["verdict_hits"] / g["n"], 2), "with_band": g["banded"],
                  "band_and_mark": g["marked"], "number_hit_rate": round(g["number_hits"] / g["marked"], 2) if g["marked"] else None,
                  "two_sided": len(w), "median_rel_width": w[len(w) // 2] if w else None}
tot_marked = sum(1 for r in rows if r["kind"] and r["number_mark"])
tot_hit = sum(1 for r in rows if r["kind"] and r["number_mark"] == "hit")
res = {"scored_shots": len(rows), "with_band": sum(1 for r in rows if r["kind"]), "band_and_mark": tot_marked,
       "number_hits": tot_hit, "number_hit_rate": round(tot_hit / tot_marked, 2) if tot_marked else None,
       "mean_p": round(sum(r["p"] for r in rows) / len(rows), 2) if rows else None, "by_p": summary, "rows": rows}
json.dump(res, open(OUT + "results.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1))
