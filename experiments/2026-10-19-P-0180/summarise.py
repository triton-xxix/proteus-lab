#!/usr/bin/env python3
"""P-0180 summary from rows-v2.json: who counts as no-creator-buy, how many were touched at all, and the
seven shots with S3 and S5 also given on the launches that had any outside buy (S5 is true by default on
a launch nobody traded, since its last trade is the create at 0 s)."""
import json
import os
import statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(HERE + "/rows-v2.json"))
P = {"S1": 0.55, "S2": 0.40, "S3": 0.60, "S4": 0.15, "S5": 0.60, "S6": 0.15, "S7": 0.01}
ok = [r for r in rows if r.get("status") == "ok"]
nobuy = [r for r in ok if r["creator_buy_tokens"] == 0]
touched = [r for r in nobuy if r["buyers_total"] > 0]
out = {"read": len(rows), "ok": len(ok), "same_slot_creator_buy": len(ok) - len(nobuy), "no_creator_buy": len(nobuy),
       "touched_by_anyone": len(touched),
       "distinct_creators_all": len({r["creator"] for r in ok}), "distinct_creators_no_buy": len({r["creator"] for r in nobuy}), "median_age_at_read_s": st.median([r["age_s"] for r in nobuy]) if nobuy else None,
       "median_buyers_total_touched": st.median([r["buyers_total"] for r in touched]) if touched else None, "shots": []}
for sid, p in P.items():
    hits = [r["shots"][sid] for r in nobuy]
    row = {"shot": sid, "p": p, "hits": sum(hits), "n": len(hits),
           "brier": round(st.mean([(p - h) ** 2 for h in hits]), 4) if hits else None}
    if sid in ("S3", "S5") and touched:
        row["hits_touched"] = sum(r["shots"][sid] for r in touched)
        row["n_touched"] = len(touched)
    out["shots"].append(row)
if nobuy:
    out["mean_brier"] = round(st.mean(s["brier"] for s in out["shots"]), 4)
json.dump(out, open(HERE + "/summary.json", "w"), indent=1)
print(json.dumps(out, indent=1))
