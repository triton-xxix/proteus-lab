"""P-0278: does the ICON ensemble's spread on the Munich high predict the size of my exchange-book miss?

Spread: p90 minus p10 across icon_seamless members for the day, from the ensemble API's past_days
archive (sandbox/om-ens-past14.json, the latest run per day, so a same-day spread, not the day-ahead
one; the nightly capture in exchange/icon_eps_band.jsonl holds the true day-ahead band from 27 Oct).
Miss: |called degree - settled winner degree| for every settled Munich call in exchange/BOOK.csv,
winners from exchange/munich_outcomes.jsonl plus the book's own winning calls.
"""
import csv
import json
import re
from datetime import datetime

ROOT = "/Users/triton/PROTEUS"
OUT = ROOT + "/experiments/2026-10-31-P-0278/results.json"

ens = json.load(open(ROOT + "/sandbox/om-ens-past14.json"))["daily"]
days = ens["time"]
member_keys = [k for k in ens if k.startswith("temperature_2m_max")]
spread = {}
for i, d in enumerate(days):
    vals = sorted(v for k in member_keys for v in [ens[k][i]] if v is not None)
    if len(vals) >= 10:
        p10, p90 = vals[int(0.1 * (len(vals) - 1))], vals[int(0.9 * (len(vals) - 1))]
        spread[d] = {"n": len(vals), "p10": p10, "p50": vals[len(vals) // 2], "p90": p90, "width": round(p90 - p10, 2),
                     "minmax": round(vals[-1] - vals[0], 2)}
band = {}
for line in open(ROOT + "/exchange/icon_eps_band.jsonl"):
    r = json.loads(line)
    band[r["day"]] = {"width": round(r["p90"] - r["p10"], 2), "n": r["n"]}

winners = {}
for line in open(ROOT + "/exchange/munich_outcomes.jsonl"):
    r = json.loads(line)
    d = datetime.strptime(r["event"].replace("st,", ",").replace("nd,", ",").replace("rd,", ",").replace("th,", ","), "%B %d, %Y").date().isoformat()
    winners[d] = int(re.match(r"-?\d+", r["winner"]).group())
calls = []
for r in csv.DictReader(open(ROOT + "/exchange/BOOK.csv")):
    if r["market"] != "Highest Temperature" or not r["outcome"]:
        continue
    d = r["event_start"][:10]
    m = re.match(r"-?\d+", r["contract"])
    if not m:
        continue
    deg = int(m.group())
    if r["outcome"] == "winner" and d not in winners:
        winners[d] = deg
    calls.append({"id": r["id"], "day": d, "called": deg, "p": float(r["p"]), "outcome": r["outcome"],
                  "lead_h": round((datetime.fromisoformat(r["event_start"].replace("Z", "+00:00")) -
                                   datetime.fromisoformat(r["committed_at"].replace("Z", "+00:00"))).total_seconds() / 3600, 1)})
rows = []
for c in calls:
    w = winners.get(c["day"])
    if w is None:
        continue
    miss = abs(c["called"] - w)
    rows.append({**c, "winner": w, "miss": miss, "same_day_spread": spread.get(c["day"], {}).get("width"),
                 "day_ahead_band": band.get(c["day"], {}).get("width")})
paired = [(r["same_day_spread"], r["miss"]) for r in rows if r["same_day_spread"] is not None]
paired_b = [(r["day_ahead_band"], r["miss"]) for r in rows if r["day_ahead_band"] is not None]


def corr(xy):
    n = len(xy)
    if n < 3:
        return None
    mx = sum(x for x, _ in xy) / n
    my = sum(y for _, y in xy) / n
    sxx = sum((x - mx) ** 2 for x, _ in xy)
    syy = sum((y - my) ** 2 for _, y in xy)
    if sxx == 0 or syy == 0:
        return None
    return round(sum((x - mx) * (y - my) for x, y in xy) / (sxx * syy) ** 0.5, 3)


res = {"ensemble_days_with_members": len(spread), "spread_by_day": spread, "day_ahead_band_days": len(band),
       "settled_calls": len(rows), "calls_with_same_day_spread": len(paired), "calls_with_day_ahead_band": len(paired_b),
       "corr_same_day_spread_v_miss": corr(paired), "corr_day_ahead_band_v_miss": corr(paired_b),
       "mean_miss": round(sum(r["miss"] for r in rows) / len(rows), 2) if rows else None,
       "miss_by_lead": {"under_24h": [r["miss"] for r in rows if r["lead_h"] < 24], "24h_plus": [r["miss"] for r in rows if r["lead_h"] >= 24]},
       "rows": rows}
json.dump(res, open(OUT, "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k not in ("rows", "spread_by_day")}, indent=1))
for r in rows:
    print(r["id"], r["day"], "called", r["called"], "winner", r["winner"], "miss", r["miss"], "lead", r["lead_h"], "spread", r["same_day_spread"], "band", r["day_ahead_band"])
