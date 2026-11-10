"""Grinder gate census, 21 Oct to 10 Nov 2026. Read-only: imports the desk's own GATES and RULES so
the lines are the registered ones, and changes nothing. A count, not a proposal.

Per night (last snapshot of each UTC date): rows, rows failing each gate, rows failing exactly one gate
(and which), and how many of those would pass if that one numeric line were eased by a quarter
(minimums x0.75, maximums x1.25). Then the same totals over the window.
"""
import csv, json, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, "/Users/triton/PROTEUS/grinder")
import paper  # noqa: E402

HERE = Path(__file__).resolve().parent
G, R, fnum = paper.GATES, paper.RULES, paper.fnum
START = "2026-10-21"

by_ts = defaultdict(list)
with open("/Users/triton/PROTEUS/grinder/SNAPSHOTS.csv", newline="") as f:
    for r in csv.DictReader(f):
        if r["ts"][:10] >= START:
            by_ts[r["ts"]].append(r)
last = {}
for ts in sorted(by_ts):
    last[ts[:10]] = ts


def eased(gate, r):
    v = lambda k: fnum(r.get(k))
    if gate == "liq":
        return (v("liq_usd") or 0) >= R["liq_usd_min"] * 0.75
    if gate == "vol_h24":
        return (v("vol_h24") or 0) >= R["vol_h24_min"] * 0.75
    if gate == "vol_h1":
        return (v("vol_h1") or 0) >= R["vol_h1_min"] * 0.75
    if gate == "top10":
        return v("top10_pct") is not None and v("top10_pct") <= R["top10_pct_max"] * 1.25
    if gate == "holders":
        return v("holders") is None or v("holders") >= R["holders_min"] * 0.75
    if gate == "lp":
        return v("lp_locked_pct") is None or v("lp_locked_pct") >= R["lp_locked_min"] * 0.75
    if gate == "age":
        return v("age_h") is not None and R["age_h_min"] * 0.75 <= v("age_h") <= R["age_h_max"] * 1.25
    return False  # authorities and price are yes/no, nothing to ease


nights, tot_fail, tot_one, tot_eased, tot_nfail = [], Counter(), Counter(), Counter(), Counter()
rows_all = passers = 0
for day, ts in sorted(last.items()):
    snap = by_ts[ts]
    fails = Counter()
    one = Counter()
    ease = Counter()
    npass = 0
    for r in snap:
        bad = [g for g, f in G.items() if not f(r)]
        tot_nfail[min(len(bad), 5)] += 1
        for g in bad:
            fails[g] += 1
        if not bad:
            npass += 1
        if len(bad) == 1:
            one[bad[0]] += 1
            if eased(bad[0], r):
                ease[bad[0]] += 1
    rows_all += len(snap)
    passers += npass
    tot_fail.update(fails); tot_one.update(one); tot_eased.update(ease)
    top = fails.most_common(1)[0] if fails else ("", 0)
    nights.append({"day": day, "rows": len(snap), "pass": npass, "top_gate": top[0], "top_fails": top[1],
                   "one_gate_away": sum(one.values()), "one_gate_by": dict(one), "pass_if_eased": dict(ease)})
    print(day, len(snap), "rows, pass", npass, "| top", top[0], top[1], "| one away", dict(one), "| eased", dict(ease))

res = {"window": [START, max(last)], "nights": len(nights), "rows": rows_all, "passers": passers,
       "fails_by_gate": dict(tot_fail.most_common()), "top_gate_by_night": dict(Counter(n["top_gate"] for n in nights)),
       "rows_by_gates_failed_capped_5": dict(sorted(tot_nfail.items())),
       "one_gate_away_by_gate": dict(tot_one.most_common()), "pass_if_that_gate_eased_25pct": dict(tot_eased.most_common()),
       "per_night": nights}
(HERE / "results.json").write_text(json.dumps(res, indent=1))
print(json.dumps({k: v for k, v in res.items() if k != "per_night"}))
