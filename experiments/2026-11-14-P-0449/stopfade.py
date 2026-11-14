"""P-0449: P-0433's SPY big-gap fade (gaps of 1% or more, since 2009) with extra slippage and a stop.

Rules written before the run (README). Trade: at the open, fade the gap (short an up gap, buy a down gap).
Target: yesterday's close (the fill). Stop: the gap distance again beyond the open (so the stop sits twice
the gap from yesterday's close). Otherwise out at the close. Costs: P-0433's 0.02% round trip plus 0.05%
slippage at the open. Daily bars cannot say whether stop or target came first when the day's range touches
both: worst case takes the stop, best case the target. Vol split: prior 20-day realised vol of close-to-close
returns, terciles over the 443 gaps. Coin control as P-0433: fade or follow at random per gap, 2,000 draws,
for the worst case.
"""
import csv
import json
import math
import pathlib
import random
import statistics

HERE = pathlib.Path(__file__).parent
DATA = pathlib.Path("/Users/triton/PROTEUS/sandbox/p0082/data/SPY.csv")
COST, SLIP, MIN, FROM = 0.0002, 0.0005, 0.01, "2009-01-01"

d, o, h, l, c = [], [], [], [], []
for r in csv.DictReader(open(DATA)):
    try:
        v = [float(r[k]) for k in ("open", "high", "low", "close")]
    except ValueError:
        continue
    if min(v) <= 0:
        continue
    d.append(r["date"]); o.append(v[0]); h.append(v[1]); l.append(v[2]); c.append(v[3])

rows = []
for t in range(21, len(d)):
    if d[t] < FROM:
        continue
    pc = c[t - 1]
    g = o[t] / pc - 1
    if abs(g) < MIN:
        continue
    up = g > 0
    dist = abs(o[t] - pc)
    rets = [math.log(c[i] / c[i - 1]) for i in range(t - 20, t)]
    vol = statistics.pstdev(rets) * math.sqrt(252)
    if up:  # short at open; target pc below, stop o+dist above
        hit_t, hit_s = l[t] <= pc, h[t] >= o[t] + dist
        close_ret = (o[t] - c[t]) / o[t]
    else:   # long at open; target pc above, stop o-dist below
        hit_t, hit_s = h[t] >= pc, l[t] <= o[t] - dist
        close_ret = (c[t] - o[t]) / o[t]
    tgt, stp = dist / o[t], -dist / o[t]
    nostop = tgt if hit_t else close_ret
    worst = stp if hit_s else (tgt if hit_t else close_ret)
    best = tgt if hit_t else (stp if hit_s else close_ret)
    # follow side for the coin control (worst case for it too: its stop is the fill)
    f_worst = -tgt if hit_t else (dist / o[t] if hit_s else -close_ret)
    k = COST + SLIP
    rows.append({"date": d[t], "gap": g, "vol": vol, "both": bool(hit_t and hit_s), "stop_hit": bool(hit_s),
                 "nostop": nostop - k, "worst": worst - k, "best": best - k, "follow_worst": f_worst - k,
                 "nostop_p0433_cost": nostop - COST})


def m(key, rs):
    return round(100 * statistics.mean(r[key] for r in rs), 4) if rs else None


vs = sorted(r["vol"] for r in rows)
c1, c2 = vs[len(vs) // 3], vs[2 * len(vs) // 3]
terc = {"low": [r for r in rows if r["vol"] < c1], "mid": [r for r in rows if c1 <= r["vol"] < c2], "high": [r for r in rows if r["vol"] >= c2]}
rng = random.Random(449)
real = statistics.mean(r["worst"] for r in rows)
draws = [statistics.mean(r["worst"] if rng.random() < 0.5 else r["follow_worst"] for r in rows) for _ in range(2000)]
years = {}
for r in rows:
    years.setdefault(r["date"][:4], []).append(r)
out = {"gaps": len(rows),
       "replicate_p0433_cost_only": m("nostop_p0433_cost", rows),
       "nostop_with_slip": m("nostop", rows), "stop_worst": m("worst", rows), "stop_best": m("best", rows),
       "stop_touched": sum(r["stop_hit"] for r in rows), "both_touched": sum(r["both"] for r in rows),
       "win_worst": round(sum(r["worst"] > 0 for r in rows) / len(rows), 3),
       "t_worst": round(real / (statistics.stdev(r["worst"] for r in rows) / math.sqrt(len(rows))), 2),
       "coin_worst_mean": round(100 * statistics.mean(draws), 4), "p_worst_v_coin": round(sum(x >= real for x in draws) / 2000, 4),
       "vol_cuts_annualised": [round(c1, 3), round(c2, 3)],
       "by_vol": {k: {"n": len(v), "nostop": m("nostop", v), "worst": m("worst", v), "best": m("best", v)} for k, v in terc.items()},
       "years_positive_worst": sum(1 for v in years.values() if statistics.mean(r["worst"] for r in v) > 0), "years": len(years),
       "share_2020_2022_worst": round(sum(r["worst"] for r in rows if r["date"][:4] in ("2020", "2022")) / sum(r["worst"] for r in rows), 3)}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
