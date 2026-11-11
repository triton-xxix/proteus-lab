"""P-0416: UTC day against Berlin day for Munich's ICON day high and low.

One keyless pull per window from Open-Meteo previous-runs (icon_seamless, 48.137,11.575, timezone=UTC,
padded a day each side), then both day definitions are cut from the same hourly series here: P-0407
showed the API's own timezone parameter is the same series shifted. Lead 0 (temperature_2m) and lead 1
(temperature_2m_previous_day1). A day counts only with all 24 hours present under both definitions.
"""
import json
import pathlib
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

HERE = pathlib.Path(__file__).parent
BERLIN = ZoneInfo("Europe/Berlin")
WINDOWS = {"july_2026": ("2026-07-01", "2026-07-31", "2026-06-30", "2026-08-01"),
           "nov_2025_to_feb_2026": ("2025-11-01", "2026-02-28", "2025-10-31", "2026-03-01")}


def pull(a, b):
    url = ("https://previous-runs-api.open-meteo.com/v1/forecast?latitude=48.137&longitude=11.575"
           f"&hourly=temperature_2m,temperature_2m_previous_day1&start_date={a}&end_date={b}&timezone=UTC&models=icon_seamless")
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "research-script/1.0"}), timeout=120).read())["hourly"]


def cut(times, vals, local):
    d = defaultdict(list)
    for t, v in zip(times, vals):
        if v is None:
            continue
        u = datetime.fromisoformat(t).replace(tzinfo=timezone.utc)
        k = u.astimezone(BERLIN) if local else u
        d[k.date().isoformat()].append((v, k.hour))
    return {day: v for day, v in d.items() if len(v) == 24}


out = {}
for name, (start, end, pa, pb) in WINDOWS.items():
    h = pull(pa, pb)
    block = {}
    for lead, var in ((0, "temperature_2m"), (1, "temperature_2m_previous_day1")):
        key = var if var in h else var + "_icon_seamless"
        u, b = cut(h["time"], h[key], False), cut(h["time"], h[key], True)
        days = sorted(x for x in set(u) & set(b) if start <= x <= end)
        res = {"days": len(days)}
        for what, f in (("high", max), ("low", min)):
            diffs = []
            for x in days:
                uu, bb = f(u[x])[0], f(b[x])[0]
                if abs(uu - bb) > 1e-9:
                    diffs.append({"day": x, "utc": uu, "berlin": bb, "berlin_minus_utc": round(bb - uu, 1),
                                  "utc_hour": f(u[x])[1], "berlin_hour": f(b[x])[1],
                                  "whole_degree_differs": round(uu) != round(bb)})
            a = [abs(d["berlin_minus_utc"]) for d in diffs]
            res[what] = {"differ": len(diffs), "share": round(len(diffs) / len(days), 3) if days else None,
                         "whole_degree_differs": sum(d["whole_degree_differs"] for d in diffs),
                         "berlin_higher": sum(d["berlin_minus_utc"] > 0 for d in diffs),
                         "mean_abs_c": round(sum(a) / len(a), 2) if a else None, "max_abs_c": max(a) if a else None,
                         "half_degree_or_more": sum(x >= 0.5 for x in a), "one_degree_or_more": sum(x >= 1.0 for x in a),
                         "rows": diffs}
        block["lead%d" % lead] = res
        print(name, "lead", lead, "days", len(days), {w: {k: v for k, v in res[w].items() if k != "rows"} for w in ("high", "low")})
    out[name] = block
(HERE / "results.json").write_text(json.dumps(out, indent=1))
