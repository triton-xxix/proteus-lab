"""P-0013: split the first 20 scored Grinder positions by graphInsidersDetected (0, 1-5, over 5)
and compare 24h outcomes. Run: python3 split.py (reads grinder/, writes results.json beside it)."""
import csv, glob, json, os, statistics

ROOT = "/Users/triton/PROTEUS/"
HERE = os.path.dirname(os.path.abspath(__file__))

# latest insider snapshot per mint, as a list of (ts, graph_insiders)
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

rows = []
for led in ("LEDGER.csv", "LEDGER-R01.csv"):
    for r in csv.DictReader(open(ROOT + "grinder/" + led)):
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
        rows.append({"id": r["id"], "token": r["token"], "entered_at": r["entered_at"], "snap_ts": ts,
                     "graph_insiders": gi, "outcome_24h_pct": out, "outcome_src": src,
                     "runup_pct": fnum(p.get("runup_pct")), "drawdown_pct": fnum(p.get("drawdown_pct")),
                     "rugged": r.get("rugged")})

rows.sort(key=lambda x: (x["entered_at"], x["id"]))
# one row per token (first entry) so the same coin in two books is not counted twice
seen, uniq = set(), []
for x in rows:
    if x["token"] in seen:
        continue
    seen.add(x["token"])
    uniq.append(x)

def bucket(n):
    return "0" if n == 0 else ("1-5" if n <= 5 else "over 5")

def summary(sel):
    out = {}
    for b in ("0", "1-5", "over 5"):
        v = [x["outcome_24h_pct"] for x in sel if bucket(x["graph_insiders"]) == b]
        out[b] = {"n": len(v), "mean": round(statistics.mean(v), 1) if v else None,
                  "median": round(statistics.median(v), 1) if v else None,
                  "share_below_-50": round(sum(1 for y in v if y <= -50) / len(v), 2) if v else None}
    return out

first20 = uniq[:20]
res = {"first20": summary(first20), "all": summary(uniq), "n_all": len(uniq),
       "outcome_sources": {s: sum(1 for x in first20 if x["outcome_src"] == s) for s in ("score_24h", "path_move_pct")},
       "rows_first20": first20}
json.dump(res, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps({k: res[k] for k in ("first20", "all", "n_all", "outcome_sources")}, indent=1))
