"""P-0541: lead and tail of public attention on scheduled sky events (Wikimedia pageviews, keyless).

For each event page: baseline = median daily views from 90 to 61 days before the event. Lead = days
before the event from the start of the last unbroken run above twice baseline that reaches the event
day. Peak day and views. Tail = days after the peak until views first drop below twice baseline;
half-life = days after the peak until views first drop below half the peak.
"""
import json, statistics, urllib.parse, urllib.request
from datetime import date, timedelta
from pathlib import Path

OUT = Path(__file__).with_name("results.json")
EVENTS = [
    ("Solar_eclipse_of_April_8,_2024", date(2024, 4, 8)),
    ("Comet_Tsuchinshan–ATLAS", date(2024, 10, 12)),
    ("Perseids", date(2024, 8, 12)),
    ("Perseids", date(2025, 8, 12)),
    ("Solar_eclipse_of_August_12,_2026", date(2026, 8, 12)),
    ("Geminids", date(2025, 12, 14)),
]
API = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{}/daily/{}/{}"


def views(title, start, end):
    url = API.format(urllib.parse.quote(title, safe=""), start.strftime("%Y%m%d"), end.strftime("%Y%m%d"))
    req = urllib.request.Request(url, headers={"User-Agent": "proteus-probe (research; keyless)"})
    items = json.loads(urllib.request.urlopen(req, timeout=60).read())["items"]
    return {date(int(i["timestamp"][:4]), int(i["timestamp"][4:6]), int(i["timestamp"][6:8])): i["views"] for i in items}


res = []
for title, ev in EVENTS:
    row = {"page": title, "event": ev.isoformat()}
    try:
        v = views(title, ev - timedelta(days=90), ev + timedelta(days=45))
    except Exception as e:
        row["error"] = str(e)[:120]
        res.append(row)
        continue
    base = statistics.median([v.get(ev - timedelta(days=d), 0) for d in range(61, 91)])
    row["baseline"] = base
    lead = 0
    d = ev
    while v.get(d, 0) > 2 * base and lead < 89:
        lead += 1
        d -= timedelta(days=1)
    row["lead_days_above_2x"] = lead - 1 if lead else None  # days before the event day itself
    window = {k: x for k, x in v.items() if ev - timedelta(days=3) <= k <= ev + timedelta(days=3)}
    pk = max(window, key=window.get)
    row["peak_day_offset"] = (pk - ev).days
    row["peak_views"] = v[pk]
    row["peak_over_baseline"] = round(v[pk] / base, 1) if base else None
    tail = half = None
    for n in range(1, 46):
        x = v.get(pk + timedelta(days=n))
        if x is None:
            break
        if half is None and x < v[pk] / 2:
            half = n
        if tail is None and x < 2 * base:
            tail = n
            break
    row["half_life_days"] = half
    row["tail_days_to_below_2x"] = tail
    row["views_7d_before"] = v.get(ev - timedelta(days=7))
    row["views_7d_after"] = v.get(ev + timedelta(days=7))
    res.append(row)

OUT.write_text(json.dumps(res, indent=1, ensure_ascii=False))
print(json.dumps(res, indent=1, ensure_ascii=False))
