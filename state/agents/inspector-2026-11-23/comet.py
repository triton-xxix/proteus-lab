"""P-0544: Comet C/2023 A3 (Tsuchinshan-ATLAS) pageviews under its 2024 title, P-0541's measures.

Tries candidate titles until one has views in Sep to Nov 2024. Event day 12 Oct 2024 (closest to Earth,
the evening-sky show); perihelion was 27 Sep. Same measures as P-0541 (baseline = median of days 90
to 61 before; lead = unbroken days above 2x ending on the event; half-life and tail after the peak),
but the peak is taken within 20 days of the event, since a comet's best night is not a fixed date.
"""
import json, statistics, urllib.parse, urllib.request
from datetime import date, timedelta
from pathlib import Path

OUT = Path(__file__).with_name("results.json")
EV = date(2024, 10, 12)
TITLES = ["C/2023_A3_(Tsuchinshan–ATLAS)", "C/2023_A3", "Comet_Tsuchinshan–ATLAS", "Tsuchinshan–ATLAS",
          "Tsuchinshan-ATLAS"]
API = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{}/daily/{}/{}"


def views(title):
    url = API.format(urllib.parse.quote(title, safe=""), (EV - timedelta(days=90)).strftime("%Y%m%d"),
                     (EV + timedelta(days=45)).strftime("%Y%m%d"))
    req = urllib.request.Request(url, headers={"User-Agent": "proteus-probe (research; keyless)"})
    items = json.loads(urllib.request.urlopen(req, timeout=60).read())["items"]
    return {date(int(i["timestamp"][:4]), int(i["timestamp"][4:6]), int(i["timestamp"][6:8])): i["views"] for i in items}


tried, v, used = {}, None, None
for t in TITLES:
    try:
        got = views(t)
        tried[t] = sum(got.values())
        if v is None or tried[t] > sum(v.values()):
            v, used = got, t
    except Exception as e:
        tried[t] = str(e)[:60]

res = {"titles_tried": tried, "title_used": used}
if v:
    base = statistics.median([v.get(EV - timedelta(days=d), 0) for d in range(61, 91)])
    lead, d = 0, EV
    while v.get(d, 0) > 2 * base and lead < 89:
        lead += 1
        d -= timedelta(days=1)
    win = {k: x for k, x in v.items() if abs((k - EV).days) <= 20}
    pk = max(win, key=win.get)
    half = tail = None
    for n in range(1, 46):
        x = v.get(pk + timedelta(days=n))
        if x is None:
            break
        if half is None and x < v[pk] / 2:
            half = n
        if tail is None and x < 2 * base:
            tail = n
            break
    top = sorted(v.items(), key=lambda kv: -kv[1])[:5]
    res.update({"baseline": base, "lead_days_above_2x": lead - 1 if lead else None,
                "peak_day": pk.isoformat(), "peak_offset_days": (pk - EV).days, "peak_views": v[pk],
                "peak_over_baseline": round(v[pk] / base, 1) if base else None,
                "half_life_days": half, "tail_days_to_below_2x": tail,
                "views_at_perihelion_27_sep": v.get(date(2024, 9, 27)),
                "top5_days": [(k.isoformat(), x) for k, x in top]})
OUT.write_text(json.dumps(res, indent=1, ensure_ascii=False))
print(json.dumps(res, indent=1, ensure_ascii=False))
