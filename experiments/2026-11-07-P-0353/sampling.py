"""P-0353: how much of Heathrow's METAR-high gap is sampling alone?

From the cached October 10-minute SYNOPs for 03772 (sandbox/ogimet-03772-202610.txt), per day 06:00 to 18:00
UTC (P-0346's window): A = max of the tenths at :20 and :50 only (when METARs are issued), B = max of all
10-minute tenths, C = SYNOP TX from the 18 UTC 333 group (synop_highs.parse). Days used only where every
:20 and :50 slot and at least 90% of the 10-minute slots are present. Also A rounded, beside C, to set
against P-0346's 0.93 C.
Usage: python3 -I sampling.py OUT.json
"""
import json
import math
import re
import statistics as st
import sys
from collections import Counter, defaultdict

sys.path.insert(0, "/Users/triton/PROTEUS/docs/tools/synop-highs")
import synop_highs  # noqa: E402

out = sys.argv[1]
text = open("/Users/triton/PROTEUS/sandbox/ogimet-03772-202610.txt", encoding="latin-1").read()
tx, _, missing_tx = synop_highs.parse(text, "03772", "18")
day = defaultdict(dict)
minutes = Counter()
for line in text.splitlines():
    parts = line.strip().split(",", 6)
    if len(parts) < 7:
        continue
    _, y, mo, d, h, mi, rep = parts
    hh, mm = int(h), int(mi)
    if not (6 <= hh < 18 or (hh == 18 and mm == 0)):
        continue
    toks = rep.replace("=", "").split()
    for t in toks[5:]:
        if t == "333":
            break
        if re.fullmatch(r"1[01]\d{3}", t):
            v = int(t[2:]) / 10 * (-1 if t[1] == "1" else 1)
            day["%s-%s-%s" % (y, mo, d)][(hh, mm)] = v
            minutes[mm] += 1
            break

# The cache has no :50 reports at all (counts printed below), so the METAR-like half-hourly sample is taken at
# :00 and :30, the same density as EGLL's :20 and :50 METARs, and the "full" max is over the five slots there are.
SLOTS = [(h, m) for h in range(6, 18) for m in range(0, 50, 10)] + [(18, 0)]
METAR_SLOTS = [(h, m) for h in range(6, 18) for m in (0, 30)] + [(18, 0)]
rows, skipped = [], Counter()
for d, obs in sorted(day.items()):
    if d not in tx:
        skipped["no TX"] += 1
        continue
    if any(s not in obs for s in METAR_SLOTS):
        skipped["missing a :20 or :50 slot"] += 1
        continue
    if sum(s in obs for s in SLOTS) < 0.9 * len(SLOTS):
        skipped["under 90% of 10-minute slots"] += 1
        continue
    a = max(obs[s] for s in METAR_SLOTS)
    b = max(obs.values())
    rows.append({"day": d, "metar_slots_max": a, "ten_min_max": b, "synop_tx": tx[d],
                 "a_rounded": math.floor(a + 0.5)})

n = len(rows)
res = {"minute_counts_06_18": dict(sorted(minutes.items())), "days_used": n, "skipped": dict(skipped)}
if n:
    ab = [r["ten_min_max"] - r["metar_slots_max"] for r in rows]
    bc = [r["synop_tx"] - r["ten_min_max"] for r in rows]
    ac = [r["a_rounded"] - r["synop_tx"] for r in rows]
    res.update({
        "full_10min_max_minus_metar_slots_max": {"mean": round(st.mean(ab), 3), "sd": round(st.stdev(ab), 3) if n > 1 else None},
        "synop_tx_minus_full_10min_max": {"mean": round(st.mean(bc), 3), "sd": round(st.stdev(bc), 3) if n > 1 else None},
        "metar_slots_max_rounded_minus_tx": {"mean": round(st.mean(ac), 3), "sd": round(st.stdev(ac), 3) if n > 1 else None},
        "rows": rows,
    })
json.dump(res, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1))
