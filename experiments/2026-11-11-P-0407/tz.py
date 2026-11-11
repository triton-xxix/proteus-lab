"""P-0407: does Open-Meteo's previous-runs endpoint honour the timezone parameter?

Munich city point 48.137, 11.575, icon_seamless, 1 to 7 Nov 2026, temperature_2m and
temperature_2m_previous_day1, pulled three times: timezone=UTC, Europe/Berlin, Pacific/Kiritimati
(UTC+14). For each: the offset the reply reports, the slot shift that lines its hourly series up
with the UTC pull (by absolute instant), and how many local-day maxima differ from the UTC-day maxima.
"""
import json
import pathlib
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta

HERE = pathlib.Path(__file__).parent
UA = {"User-Agent": "proteus-research/1.0"}
ZONES = ["UTC", "Europe/Berlin", "Pacific/Kiritimati"]
VARS = ["temperature_2m", "temperature_2m_previous_day1"]


def pull(tz):
    url = ("https://previous-runs-api.open-meteo.com/v1/forecast?latitude=48.137&longitude=11.575"
           "&hourly=" + ",".join(VARS) + "&start_date=2026-11-01&end_date=2026-11-07&models=icon_seamless"
           "&timezone=" + urllib.parse.quote(tz, safe=""))
    d = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
    (HERE / ("om-" + tz.replace("/", "_") + ".json")).write_text(json.dumps(d))
    return d


def daymax(d, var):
    m = defaultdict(list)
    for t, v in zip(d["hourly"]["time"], d["hourly"][var]):
        if v is not None:
            m[t[:10]].append(v)
    return {k: max(v) for k, v in sorted(m.items()) if len(v) >= 23}


def best_shift(a, b):
    """Slots s such that b[i + s] == a[i] on the most overlapping slots."""
    best = None
    for s in range(-20, 21):
        pairs = [(a[i], b[i + s]) for i in range(len(a)) if 0 <= i + s < len(b) and a[i] is not None and b[i + s] is not None]
        if len(pairs) < 24:
            continue
        same = sum(1 for x, y in pairs if x == y)
        if best is None or same / len(pairs) > best[1] / best[2]:
            best = (s, same, len(pairs))
    return {"shift_slots": best[0], "equal": best[1], "compared": best[2]}


pulls = {}
for tz in ZONES:
    pulls[tz] = pull(tz)
    time.sleep(2)

base = pulls["UTC"]
out = {"probe": "P-0407", "zones": {}}
for tz in ZONES:
    d = pulls[tz]
    off = d.get("utc_offset_seconds")
    row = {"utc_offset_seconds": off, "timezone": d.get("timezone"), "abbreviation": d.get("timezone_abbreviation"),
           "first_time": d["hourly"]["time"][0], "last_time": d["hourly"]["time"][-1], "slots": len(d["hourly"]["time"])}
    # the same instant by the reply's own clock: local label minus offset should be a UTC label
    t0 = datetime.fromisoformat(d["hourly"]["time"][0]) - timedelta(seconds=off or 0)
    row["first_slot_as_utc"] = t0.isoformat(timespec="minutes")
    for var in VARS:
        blk = {}
        if tz != "UTC":
            blk["against_utc_pull"] = best_shift(base["hourly"][var], d["hourly"][var])
        mine, ref = daymax(d, var), daymax(base, var)
        common = sorted(set(mine) & set(ref))
        blk["full_days"] = len(mine)
        blk["day_max"] = mine
        blk["days_compared_with_utc"] = len(common)
        blk["day_max_differs_from_utc_days"] = sum(1 for k in common if mine[k] != ref[k])
        blk["largest_difference_c"] = round(max([abs(mine[k] - ref[k]) for k in common], default=0), 1)
        row[var] = blk
    out["zones"][tz] = row
    print(tz, json.dumps({k: v for k, v in row.items()}, indent=1))

(HERE / "results.json").write_text(json.dumps(out, indent=1))
