"""P-0334: does the highest whole-degree METAR temperature at Munich airport explain the settled rows?

Usage: python3 -I metar_rule.py IEM.csv OUT.json
IEM.csv is Iowa Mesonet's asos.py output for EDDM with data=metar, tz=Etc/UTC, format=onlycomma.
Temperatures come from the raw METAR's TT/TdTd group, not from IEM's converted columns.
"""
import csv
import datetime as dt
import json
import re
import sys
import zoneinfo

BOOK = "/Users/triton/PROTEUS/exchange/BOOK.csv"
BERLIN = zoneinfo.ZoneInfo("Europe/Berlin")
TEMP = re.compile(r"\s(M?\d{2})/(M?\d{2})?\s")


def temp(raw):
    m = TEMP.search(" " + raw + " ")
    if not m:
        return None
    s = m.group(1)
    return -int(s[1:]) if s[0] == "M" else int(s)


reports, utc_day, local_day, skipped = 0, {}, {}, 0
for r in csv.DictReader(open(sys.argv[1], newline="")):
    t = temp(r["metar"])
    if t is None:
        skipped += 1
        continue
    reports += 1
    when = dt.datetime.strptime(r["valid"], "%Y-%m-%d %H:%M").replace(tzinfo=dt.timezone.utc)
    d_u, d_l = when.date().isoformat(), when.astimezone(BERLIN).date().isoformat()
    utc_day[d_u] = max(utc_day.get(d_u, -99), t)
    local_day[d_l] = max(local_day.get(d_l, -99), t)


def hit(contract, value):
    n = int(contract.split("°")[0])
    if "higher" in contract:
        return value >= n
    if "lower" in contract:
        return value <= n
    return value == n


book = [r for r in csv.DictReader(open(BOOK, newline=""))
        if r["market"] == "Highest Temperature" and "unich" in r["reason"]]
settled = [r for r in book if r["outcome"] in ("winner", "loser")]
res = {"reports": reports, "skipped": skipped, "first": min(utc_day), "last": max(utc_day), "rules": {}}
for name, days in (("utc_day", utc_day), ("local_day", local_day)):
    use = [r for r in settled if r["event_start"][:10] in days]
    bad = [{"id": r["id"], "day": r["event_start"][:10], "contract": r["contract"], "outcome": r["outcome"],
            "metar_high": days[r["event_start"][:10]]}
           for r in use if hit(r["contract"], days[r["event_start"][:10]]) != (r["outcome"] == "winner")]
    res["rules"][name] = {"rows": len(use), "agree": len(use) - len(bad), "wrong": bad}
res["unsettled"] = [{
    "id": r["id"], "day": r["event_start"][:10], "contract": r["contract"], "p": r["p"],
    "metar_high_local_day": local_day.get(r["event_start"][:10]),
} for r in book if r["outcome"] not in ("winner", "loser")]
json.dump(res, open(sys.argv[2], "w"), indent=1, ensure_ascii=False)
print(json.dumps(res, indent=1, ensure_ascii=False))
