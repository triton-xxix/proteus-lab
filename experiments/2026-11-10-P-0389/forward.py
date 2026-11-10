"""P-0185: score the skip-if-graph_insiders-is-0 filter forward on G and R01 entries after 20 Oct.
Pass if kept (insiders > 0) beats skipped (insiders == 0) by 20+ points mean 24h outcome over the next 20.
Reuses P-0013's join. Run: python3 forward.py (writes results.json beside it)."""
import csv, glob, json, os, statistics

ROOT = "/Users/triton/PROTEUS/"
HERE = os.path.dirname(os.path.abspath(__file__))
CUT = "2026-10-20T23:59:59"

snaps = {}
for f in sorted(glob.glob(ROOT + "grinder/insiders/*.jsonl")):
    for line in open(f):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if r.get("graph_insiders") is None:
            continue
        snaps.setdefault(r["mint"], []).append((r["ts"], r["graph_insiders"]))

paths = {r["id"]: r for r in csv.DictReader(open(ROOT + "grinder/PATHS.csv"))}

def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None

entries, rows = [], []
for led in ("LEDGER.csv", "LEDGER-R01.csv"):
    for r in csv.DictReader(open(ROOT + "grinder/" + led)):
        if r["entered_at"] <= CUT:
            continue
        entries.append((led, r["id"], r["entered_at"]))
        before = [s for s in snaps.get(r["mint"], []) if s[0] <= r["entered_at"]]
        if not before:
            continue
        ts, gi = max(before)
        p = paths.get(r["id"], {})
        out = fnum(r.get("score_24h"))
        src = "score_24h"
        if out is None:
            out = fnum(p.get("path_move_pct"))
            src = "path_move_pct"
        if out is None:
            continue
        rows.append({"id": r["id"], "book": led, "token": r["token"], "entered_at": r["entered_at"],
                     "graph_insiders": gi, "outcome_24h_pct": out, "outcome_src": src})

rows.sort(key=lambda x: (x["entered_at"], x["id"]))
seen, uniq = set(), []
for x in rows:
    if x["token"] in seen:
        continue
    seen.add(x["token"])
    uniq.append(x)

def grp(sel, keep):
    v = [x["outcome_24h_pct"] for x in sel if (x["graph_insiders"] > 0) == keep]
    return {"n": len(v), "mean": round(statistics.mean(v), 1) if v else None,
            "median": round(statistics.median(v), 1) if v else None}

first20 = uniq[:20]
res = {"cut": CUT, "entries_after_cut": len(entries), "scored_unique": len(uniq),
       "entries_by_book": {b: sum(1 for e in entries if e[0] == b) for b in ("LEDGER.csv", "LEDGER-R01.csv")},
       "last_entry": max((e[2] for e in entries), default=None),
       "first20_kept": grp(first20, True), "first20_skipped": grp(first20, False),
       "rows": first20}
k, s = res["first20_kept"]["mean"], res["first20_skipped"]["mean"]
res["gap_points"] = round(k - s, 1) if k is not None and s is not None else None
json.dump(res, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps({x: res[x] for x in res if x != "rows"}, indent=1))
