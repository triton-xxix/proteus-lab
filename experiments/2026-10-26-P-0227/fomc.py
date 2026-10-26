"""P-0227: parse scheduled FOMC meeting dates for 2023-2026 keyless from federalreserve.gov.

Called shot: 32 scheduled meetings (8 a year), unscheduled ones listed separately.
"""
import json
import re
import sys
import urllib.request

URL = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
OUT = "/Users/triton/PROTEUS/experiments/2026-10-26-P-0227/fomc.json"
MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"

req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (proteus probe)"})
html = urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")
print("bytes", len(html))

# Each year is a panel headed "<year> FOMC Meetings"; split on those headings.
parts = re.split(r'<h4[^>]*>\s*<a[^>]*>\s*(\d{4}) FOMC Meetings\s*</a>\s*</h4>', html)
if len(parts) < 3:
    parts = re.split(r'(\d{4}) FOMC Meetings', html)
years = {}
for i in range(1, len(parts) - 1, 2):
    year, body = int(parts[i]), parts[i + 1]
    if year in years:
        continue
    rows = re.findall(r'fomc-meeting__month[^>]*>\s*<strong>([^<]+)</strong>.*?fomc-meeting__date[^>]*>([^<]+)<', body, re.S)
    meetings = []
    for month, day in rows:
        month, day = month.strip(), day.strip()
        meetings.append({"month": month, "days": day,
                         "unscheduled": "unscheduled" in day.lower() or "notation" in day.lower()})
    years[year] = meetings

result = {}
total = 0
for y in (2023, 2024, 2025, 2026):
    ms = years.get(y, [])
    sched = [m for m in ms if not m["unscheduled"] and re.match(r"^\d", m["days"])]
    other = [m for m in ms if m not in sched]
    result[y] = {"scheduled": sched, "other": other}
    total += len(sched)
    print(y, "scheduled", len(sched), "other", len(other), [m["month"] + " " + m["days"] for m in sched])

print("years found on page", sorted(years))
print("total scheduled 2023-2026", total)
json.dump(result, open(OUT, "w"), indent=1)
sys.exit(0 if total == 32 else 1)
