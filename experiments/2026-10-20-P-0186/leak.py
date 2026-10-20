"""P-0186: is graph_insiders 0 a blank (missing report) or a real reading? Kaggle Learn's leakage lesson:
a feature that is 0 for one whole outcome class deserves a look at how it was recorded.
Run: python3 leak.py"""
import csv, glob, json, os, statistics
from datetime import datetime

ROOT = "/Users/triton/PROTEUS/"
HERE = os.path.dirname(os.path.abspath(__file__))

ins = {}  # (ts, mint) -> insider row
for f in sorted(glob.glob(ROOT + "grinder/insiders/*.jsonl")):
    for line in open(f):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        ins[(r["ts"], r["mint"])] = r

snap = {(r["ts"], r["mint"]): r for r in csv.DictReader(open(ROOT + "grinder/SNAPSHOTS.csv"))}

def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None

def blank(x):
    return x in (None, "", "None")

def profile(keys):
    out = {"n": len(keys)}
    if not keys:
        return out
    def share(fn):
        return round(sum(1 for k in keys if fn(k)) / len(keys), 2)
    out["holders_blank"] = share(lambda k: blank(snap.get(k, {}).get("holders")))
    out["top10_blank"] = share(lambda k: blank(snap.get(k, {}).get("top10_pct")))
    out["creator_blank"] = share(lambda k: blank(ins[k].get("creator")))
    out["creator_balance_blank"] = share(lambda k: blank(ins[k].get("creator_balance")))
    out["networks_0"] = share(lambda k: (ins[k].get("insider_networks_n") or 0) == 0)
    out["any_blank"] = share(lambda k: blank(snap.get(k, {}).get("holders")) or blank(snap.get(k, {}).get("top10_pct"))
                              or blank(ins[k].get("creator")))
    h = [fnum(snap.get(k, {}).get("holders")) for k in keys]
    h = [x for x in h if x is not None]
    out["median_holders"] = statistics.median(h) if h else None
    rs = [fnum(snap.get(k, {}).get("rug_score")) for k in keys]
    rs = [x for x in rs if x is not None]
    out["median_rug_score"] = statistics.median(rs) if rs else None
    return out

def bucket(n):
    return "0" if n == 0 else ("1-5" if n <= 5 else "over 5")

# A. every insider row the scanner ever wrote (all scanned tokens, not just positions)
allk = [k for k, r in ins.items() if r.get("graph_insiders") is not None]
A = {b: profile([k for k in allk if bucket(ins[k]["graph_insiders"]) == b]) for b in ("0", "1-5", "over 5")}
A["graph_insiders_null_rows"] = sum(1 for r in ins.values() if r.get("graph_insiders") is None)

# B. the 19 G-book positions from P-0013, at their entry snapshot
p13 = json.load(open(ROOT + "experiments/2026-10-20-P-0013/results.json"))["rows_first20"]
mint_of = {r["id"]: r["mint"] for r in csv.DictReader(open(ROOT + "grinder/LEDGER.csv"))}
pk = {b: [(x["snap_ts"], mint_of[x["id"]]) for x in p13 if bucket(x["graph_insiders"]) == b] for b in ("0", "over 5")}
B = {b: profile(v) for b, v in pk.items()}

# C. same positions, earliest snapshot of the mint taken 1h+ before entry: does the bucket hold?
def t(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
C = []
for x in p13:
    m = mint_of[x["id"]]
    early = sorted(k for k in allk if k[1] == m and (t(x["entered_at"]) - t(k[0])).total_seconds() >= 3600)
    if early:
        C.append({"id": x["id"], "at_entry": x["graph_insiders"], "early_ts": early[-1][0],
                  "early": ins[early[-1]]["graph_insiders"], "out": x["outcome_24h_pct"]})

res = {"A_all_scanned": A, "B_positions": B, "C_1h_before": C, "C_n": len(C),
       "C_bucket_changed": sum(1 for c in C if bucket(c["early"]) != bucket(c["at_entry"]))}
json.dump(res, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
