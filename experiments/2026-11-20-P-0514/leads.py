"""P-0514: ICON lead 1 v lead 2 on the settled Munich daily-high markets.

For each kept outcome in exchange/munich_outcomes.jsonl (winner is a bin like "9°C", "3°C or below",
"13°C or higher"), take Open-Meteo previous-runs icon_seamless hourly temperature_2m_previous_day1 and
_previous_day2 at 48.137,11.575, Europe/Berlin local day, max over the day, rounded half up to a whole
degree, nothing added (the nightly's recipe). Does each lead's degree land in the winning bin; when the
two leads differ, which one won? Writes results.json.
"""
import json
import math
import re
import sys
import urllib.request
from datetime import datetime

SRC, OUT = sys.argv[1], sys.argv[2]
outs = [json.loads(l) for l in open(SRC) if l.strip()]
outs = [o for o in outs if o.get("winner")]


def day_of(ev):
    ev = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", ev)
    return datetime.strptime(ev, "%B %d, %Y").date()


def in_bin(deg, w):
    n = int(re.search(r"-?\d+", w).group())
    if "below" in w:
        return deg <= n
    if "higher" in w:
        return deg >= n
    return deg == n


days = sorted({day_of(o["event"]) for o in outs})
url = ("https://previous-runs-api.open-meteo.com/v1/forecast?latitude=48.137&longitude=11.575"
       "&hourly=temperature_2m_previous_day1,temperature_2m_previous_day2&models=icon_seamless"
       f"&timezone=Europe/Berlin&start_date={days[0]}&end_date={days[-1]}")
h = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "proteus-lab-probe/1.0"}), timeout=60))["hourly"]
mx = {}
for t, a, b in zip(h["time"], h["temperature_2m_previous_day1"], h["temperature_2m_previous_day2"]):
    d = t[:10]
    m = mx.setdefault(d, [None, None])
    if a is not None:
        m[0] = a if m[0] is None else max(m[0], a)
    if b is not None:
        m[1] = b if m[1] is None else max(m[1], b)

rows = []
for o in outs:
    d = str(day_of(o["event"]))
    l1, l2 = mx.get(d, [None, None])
    if l1 is None or l2 is None:
        rows.append({"day": d, "winner": o["winner"], "missing": True})
        continue
    r1, r2 = math.floor(l1 + 0.5), math.floor(l2 + 0.5)
    rows.append({"day": d, "winner": o["winner"], "lead1": l1, "lead2": l2, "deg1": r1, "deg2": r2,
                 "hit1": in_bin(r1, o["winner"]), "hit2": in_bin(r2, o["winner"]), "differ": r1 != r2})
ok = [r for r in rows if not r.get("missing")]
dif = [r for r in ok if r["differ"]]
summary = {"outcomes": len(rows), "with_both_leads": len(ok), "hit_lead1": sum(r["hit1"] for r in ok),
           "hit_lead2": sum(r["hit2"] for r in ok), "differ": len(dif),
           "differ_lead1_won": sum(r["hit1"] for r in dif), "differ_lead2_won": sum(r["hit2"] for r in dif),
           "differ_neither": sum(1 for r in dif if not r["hit1"] and not r["hit2"]),
           "mean_abs_lead_gap": round(sum(abs(r["lead1"] - r["lead2"]) for r in ok) / len(ok), 2) if ok else None,
           "days": [str(days[0]), str(days[-1])]}
print(json.dumps(summary))
json.dump({"summary": summary, "rows": rows}, open(OUT, "w"), indent=1, ensure_ascii=False)
