"""P-0170: judgement book Brier gap (me minus market) split by lead time, fpp3 5.10 style.

Reads pitch/JUDGEMENT.csv, keeps settled rows with both briers, lead = kickoff_utc - committed_at
(hours). Splits at the median lead. Same for the blind column (lead from blind_committed_at).
Writes results.json beside this script.
"""
import csv, json, math, statistics, sys
from datetime import datetime
from pathlib import Path

LEDGER = Path("/Users/triton/PROTEUS/pitch/JUDGEMENT.csv")
OUT = Path(__file__).resolve().parent / "results.json"
SEEN = {f"J-{i:04d}" for i in range(1, 9)}  # results seen before commit, excluded by the scorer


def ts(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


def summary(gaps):
    n = len(gaps)
    if n == 0:
        return {"n": 0}
    m = statistics.fmean(gaps)
    se = statistics.stdev(gaps) / math.sqrt(n) if n > 1 else None
    return {"n": n, "mean_gap": round(m, 4), "se": round(se, 4) if se else None}


def split(rows, mine, committed):
    pts = []
    for r in rows:
        if not r["result"] or not r[mine] or not r["market_brier"] or not r[committed]:
            continue
        if mine == "brier" and r["id"] in SEEN:  # same exclusion as pitch/score_judgement.py
            continue
        lead = (ts(r["kickoff_utc"]) - ts(r[committed])).total_seconds() / 3600
        pts.append((lead, float(r[mine]) - float(r["market_brier"]), r["id"]))
    pts.sort()
    if not pts:
        return {"n": 0}
    med = statistics.median(p[0] for p in pts)
    near = [g for l, g, _ in pts if l <= med]
    far = [g for l, g, _ in pts if l > med]
    a, b = summary(near), summary(far)
    out = {"n": len(pts), "median_lead_h": round(med, 1),
           "lead_range_h": [round(pts[0][0], 1), round(pts[-1][0], 1)],
           "all": summary([p[1] for p in pts]), "near": a, "far": b}
    if a.get("se") and b.get("se"):
        diff = b["mean_gap"] - a["mean_gap"]
        se = math.sqrt(a["se"] ** 2 + b["se"] ** 2)
        out["far_minus_near"] = round(diff, 4)
        out["far_minus_near_se"] = round(se, 4)
        out["z"] = round(diff / se, 2)
    return out


def main():
    rows = list(csv.DictReader(LEDGER.open()))
    res = {"ledger_rows": len(rows),
           "anchored": split(rows, "brier", "committed_at"),
           "blind": split(rows, "blind_brier", "blind_committed_at")}
    OUT.write_text(json.dumps(res, indent=2) + "\n")
    json.dump(res, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
