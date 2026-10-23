#!/usr/bin/env python3
"""Does Open-Meteo's ICON daily temperature_2m_max come from the day, or from the midnight hour?

Friday persona pick, 23 Oct 2026, interest 8 (checking whether published things are what they say).
Keyless: the historical-forecast archive for Munich city (48.137, 11.575), icon_seamless.
Writes results.json next to this file. Run:
  /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/experiments/2026-10-23-persona-daily-max/check.py
"""
import json
import os
import sys
import urllib.request
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
START, END = "2026-08-01", "2026-10-22"
URL = (
    "https://historical-forecast-api.open-meteo.com/v1/forecast"
    "?latitude=48.137&longitude=11.575"
    f"&start_date={START}&end_date={END}"
    "&hourly=temperature_2m&daily=temperature_2m_max"
    "&models=icon_seamless&timezone=Europe%2FBerlin"
)


def main():
    with urllib.request.urlopen(URL, timeout=60) as r:
        data = json.load(r)
    hours = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]
    daily_days = data["daily"]["time"]
    daily_max = data["daily"]["temperature_2m_max"]

    by_day = {}
    for t, v in zip(hours, temps):
        if v is None:
            continue
        d, h = t.split("T")
        by_day.setdefault(d, []).append((int(h[:2]), v))

    rows = []
    hour_of_max = Counter()
    for d, dmax in zip(daily_days, daily_max):
        hs = by_day.get(d)
        if not hs or dmax is None:
            continue
        full_max = max(v for _, v in hs)
        hmax = max(hs, key=lambda x: x[1])[0]
        day_max = max(v for h, v in hs if 7 <= h <= 21)
        rows.append({
            "date": d,
            "daily_field": dmax,
            "hourly_max": full_max,
            "hour_of_max": hmax,
            "daytime_max_07_21": day_max,
            "gap": round(full_max - day_max, 2),
            "rounds_differ": round(full_max) != round(day_max),
        })
        hour_of_max[hmax] += 1

    n = len(rows)
    field_matches_hourly = sum(abs(r["daily_field"] - r["hourly_max"]) < 0.051 for r in rows)
    night = sum(r["hour_of_max"] <= 6 or r["hour_of_max"] >= 22 for r in rows)
    differ = sum(r["rounds_differ"] for r in rows)
    gaps = sorted(r["gap"] for r in rows if r["gap"] > 0)
    summary = {
        "window": [START, END],
        "days": n,
        "daily_field_equals_hourly_max": field_matches_hourly,
        "max_at_night_22_to_06": night,
        "integer_rounding_differs": differ,
        "gap_when_positive_median": gaps[len(gaps) // 2] if gaps else 0,
        "gap_max": gaps[-1] if gaps else 0,
        "hour_of_max_histogram": dict(sorted(hour_of_max.items())),
        "night_days": [r for r in rows if r["hour_of_max"] <= 6 or r["hour_of_max"] >= 22],
    }
    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump({"summary": summary, "rows": rows}, f, indent=1)
    print(f"days {n}; daily field equals hourly max on {field_matches_hourly}")
    print(f"max fell at night (22h-06h) on {night} of {n}; integer rounding differs on {differ}")
    print(f"gap when positive: median {summary['gap_when_positive_median']}, max {summary['gap_max']}")
    print("hour of max:", summary["hour_of_max_histogram"])
    for r in summary["night_days"]:
        print(" ", r["date"], "field", r["daily_field"], "at", r["hour_of_max"], "h; daytime", r["daytime_max_07_21"], "differs" if r["rounds_differ"] else "")


if __name__ == "__main__":
    sys.exit(main())
