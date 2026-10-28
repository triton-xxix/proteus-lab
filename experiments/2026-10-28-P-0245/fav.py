"""P-0245: does the Munich daily-high favourite on Smarkets settle as often as its price says?

For every Munich Highest Temperature market in exchange/SNAPSHOTS.csv, settle each contract from the
keyless Smarkets API, then for each snapshot take the favourite (highest two-sided mid) and compare its
price with whether it won. Split by hours before the market's event day ends (local). Writes results.json.
"""
import csv, json, sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/Users/triton/PROTEUS")
sys.path.insert(0, str(ROOT / "exchange"))
import exchange  # noqa: E402

OUT = Path(__file__).parent
rows = [r for r in csv.DictReader(open(ROOT / "exchange/SNAPSHOTS.csv")) if r["market"] == "Highest Temperature"]
by_market = defaultdict(list)
for r in rows:
    by_market[r["market_id"]].append(r)

results, snaps_out = {}, []
for mid, rs in sorted(by_market.items()):
    cs = exchange.get(f"/markets/{mid}/contracts/").get("contracts", [])
    winners = {c["id"] for c in cs if c.get("state_or_outcome") == "winner"}
    if not winners:
        results[mid] = {"event": rs[0]["event"], "settled": False}
        continue
    results[mid] = {"event": rs[0]["event"], "settled": True, "winner": [c["name"] for c in cs if c["id"] in winners]}
    end = datetime.fromisoformat(rs[0]["event_start"].replace("Z", "+00:00"))
    by_snap = defaultdict(list)
    for r in rs:
        if r["mid"] and r["bid"] and r["offer"] and float(r["bid"]) > 0:
            by_snap[r["snap_utc"]].append(r)
    for snap, cr in sorted(by_snap.items()):
        fav = max(cr, key=lambda r: float(r["mid"]))
        t = datetime.fromisoformat(snap.replace("Z", "+00:00"))
        total = sum(float(r["mid"]) for r in cr)
        snaps_out.append({"market": mid, "event": rs[0]["event"], "snap": snap,
                          "hours_to_start": round((end - t).total_seconds() / 3600, 1),
                          "fav": fav["contract"], "fav_p": float(fav["mid"]) / 10000,
                          "book_sum": round(total / 10000, 3),
                          "won": fav["contract_id"] in winners})

def summary(group):
    n = len(group)
    if not n:
        return {"n": 0}
    p = sum(s["fav_p"] for s in group) / n
    w = sum(s["won"] for s in group) / n
    return {"n": n, "mean_price": round(p, 3), "win_rate": round(w, 3), "overpricing": round(p - w, 3),
            "brier": round(sum((s["fav_p"] - s["won"]) ** 2 for s in group) / n, 4)}

bands = {"over 24 h before event_start": [s for s in snaps_out if s["hours_to_start"] > 24],
         "0 to 24 h before": [s for s in snaps_out if 0 <= s["hours_to_start"] <= 24],
         "after event_start (in play)": [s for s in snaps_out if s["hours_to_start"] < 0]}
out = {"markets": len(by_market), "settled": sum(1 for v in results.values() if v["settled"]),
       "snapshots": len(snaps_out), "all": summary(snaps_out),
       "bands": {k: summary(v) for k, v in bands.items()},
       "last_before_start": summary([max((s for s in snaps_out if s["market"] == m and s["hours_to_start"] >= 0),
                                         key=lambda s: -s["hours_to_start"], default=None)
                                     for m in {s["market"] for s in snaps_out}
                                     if any(s["market"] == m and s["hours_to_start"] >= 0 for s in snaps_out)]),
       "per_market": results, "rows": snaps_out}
json.dump(out, open(OUT / "results.json", "w"), indent=1, default=str)
print(json.dumps({k: out[k] for k in ("markets", "settled", "snapshots", "all", "bands", "last_before_start")}, indent=1))
