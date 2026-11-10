"""P-0388 (number from the GO line): where does Heathrow's SYNOP TX to METAR high gap come from?

Ogimet's 03772 files carry 10-minute reports with group 1snTTT. Ladder, per day, Sep and Oct 2026:
  TX     the 18 UTC 333 1snTxTxTx (06 to 18 UTC max, tenths)
  ten    the highest 10-minute reading, 06 to 18 UTC
  metset the highest of the readings at minutes 20 and 50 only (METAR's own sampling times), tenths
  round  metset rounded to whole degrees, as a METAR reports
  metar  the actual EGLL METAR high from Iowa State
Each rung's mean difference shows what that step costs.
"""
import json
import pathlib
from collections import defaultdict

ROOT = "/Users/triton/PROTEUS"
HERE = pathlib.Path(__file__).parent

tx, ten, met = {}, defaultdict(list), defaultdict(list)
rows_seen = 0
for name in ("202609", "202610"):
    for line in open(f"{ROOT}/sandbox/ogimet-03772-{name}.txt", encoding="latin-1"):
        p = line.strip().split(",")
        if len(p) < 7 or p[0] != "03772":
            continue
        rows_seen += 1
        day = f"{p[1]}-{p[2]}-{p[3]}"
        hh, mm = int(p[4]), int(p[5])
        groups = p[6].replace("=", "").split()
        if len(groups) < 6:
            continue
        # first group 1snTTT in section 1, after the station and iihVV/Nddff groups
        sec1 = groups[groups.index("333")] if False else None
        cut = groups.index("333") if "333" in groups else len(groups)
        s1 = groups[3:cut]
        g = next((x for x in s1[2:] if len(x) == 5 and x[0] == "1" and x[1] in "01" and x[2:].isdigit()), None)
        if g and 6 <= hh <= 18:
            t = int(g[2:]) / 10 * (-1 if g[1] == "1" else 1)
            if hh < 18 or mm == 0:
                ten[day].append(t)
                if mm in (20, 50):
                    met[day].append(t)
        if hh == 18 and mm == 0 and "333" in groups:
            sec = groups[groups.index("333") + 1:]
            if "555" in sec:
                sec = sec[:sec.index("555")]
            x = next((y for y in sec if len(y) == 5 and y[0] == "1" and y[1] in "01" and y[2:].isdigit()), None)
            if x:
                tx[day] = int(x[2:]) / 10 * (-1 if x[1] == "1" else 1)

iem = defaultdict(list)
for line in (pathlib.Path(f"{ROOT}/experiments/2026-11-09-P-0383/iem-EGLL.csv")).read_text().splitlines()[1:]:
    q = line.split(",")
    if len(q) >= 3 and q[2]:
        try:
            iem[q[1][:10]].append(float(q[2]))
        except ValueError:
            pass
metar = {k: max(v) for k, v in iem.items() if len(v) >= 12}

days = sorted(d for d in tx if d in ten and len(ten[d]) >= 40 and d in met and len(met[d]) >= 15 and d in metar)
res = {"synop_rows": rows_seen, "days": len(days), "first_last": [days[0], days[-1]] if days else None, "steps": {}}


def mean(xs):
    return round(sum(xs) / len(xs), 3)


if days:
    teneth = {d: max(ten[d]) for d in days}
    ms = {d: max(met[d]) for d in days}
    rd = {d: float(round(ms[d])) for d in days}
    res["steps"] = {
        "TX minus 10-minute max": mean([tx[d] - teneth[d] for d in days]),
        "10-minute max minus METAR-minute max": mean([teneth[d] - ms[d] for d in days]),
        "METAR-minute max minus rounded": mean([ms[d] - rd[d] for d in days]),
        "rounded minus actual METAR high": mean([rd[d] - metar[d] for d in days]),
        "TX minus actual METAR high (the whole gap)": mean([tx[d] - metar[d] for d in days]),
    }
    res["share_days_ten_above_tx"] = round(sum(teneth[d] > tx[d] for d in days) / len(days), 3)
    res["share_metar_rounding_up"] = round(sum(rd[d] > ms[d] for d in days) / len(days), 3)
(HERE / "results.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
