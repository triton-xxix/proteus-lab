"""P-0184: is graphInsidersDetected 0 a fresh-token marker? Age at entry by insider bucket, R01 rows
counted, and a permutation test on the 0 v over-5 24h gap. Run: python3 age.py"""
import csv, glob, json, os, random, statistics

ROOT = "/Users/triton/PROTEUS/"
HERE = os.path.dirname(os.path.abspath(__file__))

snaps = {}
for f in sorted(glob.glob(ROOT + "grinder/insiders/*.jsonl")):
    for line in open(f):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if r.get("graph_insiders") is not None:
            snaps.setdefault(r["mint"], []).append((r["ts"], r["graph_insiders"]))

ages = {}
for r in csv.DictReader(open(ROOT + "grinder/SNAPSHOTS.csv")):
    try:
        ages[(r["ts"], r["mint"])] = float(r["age_h"])
    except (TypeError, ValueError):
        pass

paths = {r["id"]: r for r in csv.DictReader(open(ROOT + "grinder/PATHS.csv"))}

def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None

def bucket(n):
    return "0" if n == 0 else ("1-5" if n <= 5 else "over 5")

rows, r01_seen, r01_no_outcome = [], 0, 0
for led in ("LEDGER.csv", "LEDGER-R01.csv"):
    for r in csv.DictReader(open(ROOT + "grinder/" + led)):
        before = [s for s in snaps.get(r["mint"], []) if s[0] <= r["entered_at"]]
        if not before:
            continue
        ts, gi = max(before)
        if led == "LEDGER-R01.csv":
            r01_seen += 1
        out = fnum(r.get("score_24h"))
        if out is None:
            out = fnum(paths.get(r["id"], {}).get("path_move_pct"))
        if out is None and r.get("exit_price_usd"):
            # R01 has no 24h score; use its own entry-to-exit move, flagged
            ep, xp = fnum(r["entry_price_usd"]), fnum(r["exit_price_usd"])
            out = round((xp / ep - 1) * 100, 1) if ep and xp else None
            src = "ledger_exit_move"
        else:
            src = "24h"
        if out is None:
            r01_no_outcome += led == "LEDGER-R01.csv"
            continue
        rows.append({"id": r["id"], "book": led, "token": r["token"], "gi": gi, "bucket": bucket(gi),
                     "age_h": ages.get((ts, r["mint"])), "out": out, "src": src, "rugged": r.get("rugged")})

def med(v):
    v = [x for x in v if x is not None]
    return round(statistics.median(v), 1) if v else None

g = [x for x in rows if x["book"] == "LEDGER.csv"]
age_by = {b: {"n": sum(1 for x in rows if x["bucket"] == b),
              "median_age_h": med([x["age_h"] for x in rows if x["bucket"] == b]),
              "ages": sorted(x["age_h"] for x in rows if x["bucket"] == b and x["age_h"] is not None)}
          for b in ("0", "1-5", "over 5")}

# permutation test on the G book only (one outcome definition): mean(over 5) - mean(0)
a = [x["out"] for x in g if x["bucket"] == "0"]
b = [x["out"] for x in g if x["bucket"] == "over 5"]
obs = statistics.mean(b) - statistics.mean(a)
pool, k = a + b, len(a)
random.seed(20261020)
N, hits = 20000, 0
for _ in range(N):
    random.shuffle(pool)
    if statistics.mean(pool[k:]) - statistics.mean(pool[:k]) >= obs:
        hits += 1
res = {"age_by_bucket": age_by, "g_rows": len(g), "r01_rows": len(rows) - len(g), "r01_seen": r01_seen,
       "r01_no_outcome": r01_no_outcome, "gap_over5_minus_0": round(obs, 1),
       "perm_p_one_sided": round((hits + 1) / (N + 1), 4), "perm_N": N, "rows": rows}
json.dump(res, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1))
for x in rows:
    print(x["id"], x["bucket"], x["gi"], x["age_h"], x["out"], x["src"], x["rugged"])
