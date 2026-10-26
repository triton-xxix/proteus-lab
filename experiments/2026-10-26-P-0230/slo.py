"""P-0230: the nightly's own SLO, from git history (SRE workbook: SLI = good / valid, budget = 1 - SLO).

SLI: a night is good if both its pre-register commit and its close commit landed, each before 06:00
local on the morning after the run date. Valid nights: every run date from preregister.py's first use
to last night (tonight is still running and is left out). Also counts hook denials per night from
state/unattended-decisions-*.jsonl for the nightly's own session.

Called shot: about 85 percent good, so the 90 percent SLO is already over budget for the period.
"""
import collections
import datetime as dt
import glob
import json
import os
import re
import subprocess

ROOT = "/Users/triton/PROTEUS"
OUT = os.path.join(ROOT, "experiments/2026-10-26-P-0230")
TONIGHT = dt.date(2026, 10, 26)
SLO = 0.90

log = subprocess.run(["git", "-C", ROOT, "log", "--since=2026-09-20", "--format=%aI\t%s"],
                     capture_output=True, text=True, check=True).stdout.splitlines()
seen = collections.defaultdict(dict)  # run date -> {"pre-register": time, "close": time}
first = None
for line in log:
    when, subject = line.split("\t", 1)
    m = re.match(r"nightly: (pre-register|close) (\d{4}-\d{2}-\d{2})", subject)
    if not m:
        continue
    kind, day = m.group(1), dt.date.fromisoformat(m.group(2))
    t = dt.datetime.fromisoformat(when)
    seen[day].setdefault(kind, t)
    seen[day][kind] = min(seen[day][kind], t)
    first = day if first is None or day < first else first

days, rows = [], []
d = first
while d < TONIGHT:
    days.append(d)
    d += dt.timedelta(days=1)
for d in days:
    cutoff = dt.datetime.combine(d + dt.timedelta(days=1), dt.time(6, 0)).astimezone()
    pre, close = seen[d].get("pre-register"), seen[d].get("close")
    ok_pre = pre is not None and pre <= cutoff
    ok_close = close is not None and close <= cutoff
    rows.append({"date": str(d), "pre": pre.isoformat() if pre else None,
                 "close": close.isoformat() if close else None,
                 "good": ok_pre and ok_close, "pre_on_time": ok_pre, "close_on_time": ok_close})

# Denials per nightly session, by the decisions log of each date and the next (runs cross midnight).
den = {}
for d in days:
    n_den, sessions = 0, set()
    for f in (d, d + dt.timedelta(days=1)):
        p = os.path.join(ROOT, "state/unattended-decisions-%s.jsonl" % f)
        if not os.path.exists(p):
            continue
        for ln in open(p):
            try:
                r = json.loads(ln)
            except ValueError:
                continue
            if r.get("task") != "proteus-nightly":
                continue
            ts = r.get("ts") or r.get("at") or ""
            if f == d and ts[11:13] and ts[11:13] < "20":
                continue  # the morning's lines belong to the night before
            if f != d and ts[11:13] and ts[11:13] >= "12":
                continue
            sessions.add(r.get("session"))
            if r.get("outcome") == "deny":
                n_den += 1
    den[str(d)] = n_den if sessions else None
for r in rows:
    r["denials"] = den[r["date"]]

good = sum(r["good"] for r in rows)
n = len(rows)
sli = good / n
budget_nights = (1 - SLO) * n
spent = n - good
print("valid nights %d (%s to %s), good %d, SLI %.1f%%" % (n, days[0], days[-1], good, 100 * sli))
print("SLO %.0f%%: budget %.1f bad nights, spent %d, left %.1f" % (100 * SLO, budget_nights, spent, budget_nights - spent))
print("pre-register on time %d of %d; close on time %d of %d" %
      (sum(r["pre_on_time"] for r in rows), n, sum(r["close_on_time"] for r in rows), n))
oct_rows = [r for r in rows if r["date"] >= "2026-10-01"]
og = sum(r["good"] for r in oct_rows)
print("October: %d of %d good (%.1f%%); budget at 90%%: %.1f, spent %d" %
      (og, len(oct_rows), 100 * og / len(oct_rows), 0.1 * len(oct_rows), len(oct_rows) - og))
dn = [r["denials"] for r in rows if r["denials"] is not None]
if dn:
    print("denials a night (nightly task lines): mean %.1f, max %d, nights with data %d" % (sum(dn) / len(dn), max(dn), len(dn)))
print("bad nights:")
for r in rows:
    if not r["good"]:
        print("  %s pre %s close %s" % (r["date"], r["pre"] and r["pre"][:16], r["close"] and r["close"][:16]))
json.dump(rows, open(os.path.join(OUT, "nights.json"), "w"), indent=1)
