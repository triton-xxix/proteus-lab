#!/usr/bin/env python3
"""P-0479: Voyager 1's distance from Earth, keyless, from JPL Horizons.

Asks the Horizons API for Voyager 1 (spacecraft id -31) as seen from the
Earth's centre (500@399), range (quantity 20) and one-way light time
(quantity 21), daily from 1 Oct 2026 to 31 Jan 2027. Compares each day's
range with one light-day and finds the first day at or past it.
Standard library only. Writes results.json and raw.txt beside itself.
"""
import json
import os
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
C_KM_S = 299792.458
LIGHT_DAY_KM = C_KM_S * 86400.0
AU_KM = 149597870.7

params = {
    "format": "text",
    "COMMAND": "'-31'",
    "OBJ_DATA": "'NO'",
    "MAKE_EPHEM": "'YES'",
    "EPHEM_TYPE": "'OBSERVER'",
    "CENTER": "'500@399'",
    "START_TIME": "'2026-10-01'",
    "STOP_TIME": "'2027-01-31'",
    "STEP_SIZE": "'1 d'",
    "QUANTITIES": "'20,21'",
    "RANGE_UNITS": "'KM'",
    "CSV_FORMAT": "'YES'",
}
url = "https://ssd.jpl.nasa.gov/api/horizons.api?" + urllib.parse.urlencode(params)
req = urllib.request.Request(url, headers={"User-Agent": "horizons-check/1.0"})
raw = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
with open(os.path.join(HERE, "raw.txt"), "w") as f:
    f.write(raw)

rows = []
inside = False
for line in raw.splitlines():
    if line.startswith("$$SOE"):
        inside = True
        continue
    if line.startswith("$$EOE"):
        break
    if not inside:
        continue
    parts = [p.strip() for p in line.split(",")]
    # date, (solar presence), (lunar presence), delta km, deldot km/s, light time minutes
    nums = []
    for p in parts[1:]:
        try:
            nums.append(float(p))
        except ValueError:
            pass
    if len(nums) < 3:
        continue
    km, rate, lt_min = nums[0], nums[1], nums[2]
    rows.append({
        "date": parts[0][:11],
        "km": km,
        "au": km / AU_KM,
        "rate_km_s": rate,
        "light_time_h": lt_min / 60.0,
        "of_light_day": km / LIGHT_DAY_KM,
    })

if not rows:
    raise SystemExit("no ephemeris rows parsed; see raw.txt")

today = next((r for r in rows if r["date"] == "2026-Nov-18"), rows[0])
first = next((r for r in rows if r["of_light_day"] >= 1.0), None)
# check the two columns against each other: range / c should equal the light time
check = max(abs(r["km"] / C_KM_S / 3600.0 - r["light_time_h"]) for r in rows)
out = {
    "source": "JPL Horizons API, keyless, COMMAND -31, CENTER 500@399",
    "rows": len(rows),
    "light_day_km": LIGHT_DAY_KM,
    "light_day_au": LIGHT_DAY_KM / AU_KM,
    "today": today,
    "today_pct_off_light_day": round((today["of_light_day"] - 1.0) * 100, 3),
    "within_2pct": abs(today["of_light_day"] - 1.0) <= 0.02,
    "first_day_at_or_past_one_light_day": first,
    "closest_and_farthest_in_window": [
        min(rows, key=lambda r: r["km"]), max(rows, key=lambda r: r["km"])],
    "range_over_c_v_light_time_max_diff_h": check,
    "range_going_down_days": sum(1 for r in rows if r["rate_km_s"] < 0),
}
with open(os.path.join(HERE, "results.json"), "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1))
