"""F-0085 check: capped_now() in bin/lichess.py, replayed at past moments against CHALLENGES.csv."""
import calendar
import csv
import importlib.util
import time

spec = importlib.util.spec_from_file_location("lc", "/Users/triton/PROTEUS/bin/lichess.py")
lc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lc)


def at(s):
    return calendar.timegm(time.strptime(s, "%Y-%m-%dT%H:%M:%SZ"))


rows = list(csv.DictReader(open(lc.CHALLENGES)))
# how many logged asks would have been skipped: an ask to a bot that capped_now(ask time) lists
skipped = wasted_cap = 0
for r in rows:
    t = at(r["utc"])
    cap = lc.capped_now(now=t)
    if r["opponent"] in cap:
        skipped += 1
        if lc.CAP_RE.search(r.get("detail", "")):
            wasted_cap += 1
print("asks in log", len(rows), "would be skipped", skipped, "of which cap refusals again", wasted_cap)
for moment in ["2026-11-12T08:40:00Z", "2026-11-16T08:40:00Z", "2026-11-16T20:00:00Z"]:
    c = lc.capped_now(now=at(moment))
    print(moment, len(c), "capped", sorted(c)[:5])
# a cap that has passed must not be listed
assert all(u > at("2026-11-12T08:40:00Z") for u in lc.capped_now(now=at("2026-11-12T08:40:00Z")).values())
print("ok")
