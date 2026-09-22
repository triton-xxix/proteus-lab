"""Nightly diagnostic: why did the Pitch commit zero predictions?

Reports what load_fixtures() actually returns: row count, divisions, how many
rows have a usable Kickoff, and the date span, so a silent NaT drop is visible.
Diagnostic only. It never writes to PREDICTIONS.csv.
"""
import sys
from datetime import datetime, timezone, timedelta

sys.path.insert(0, "/Users/triton/PROTEUS/pitch")
import data as D  # noqa: E402

fx = D.load_fixtures()
print("fixtures rows", len(fx))
print("columns", list(fx.columns)[:20])
if fx.empty:
    raise SystemExit("empty fixtures")

print("divisions", fx["Div"].value_counts().to_dict())

ko = fx["Kickoff"]
print("kickoff nat", int(ko.isna().sum()), "of", len(ko))
good = fx[ko.notna()]
if len(good):
    print("kickoff span", good["Kickoff"].min(), "->", good["Kickoff"].max())

now = datetime.now(timezone.utc)
print("now utc", now)
inwin = 0
for _, f in good.iterrows():
    k = f["Kickoff"].tz_localize("Europe/London").tz_convert("UTC")
    if now <= k <= now + timedelta(days=8):
        inwin += 1
print("in 8-day window", inwin)

print("first 5 rows:")
for _, f in fx.head(5).iterrows():
    print(" ", f.get("Div"), f.get("Date"), f.get("Time"), f.get("Kickoff"),
          f.get("HomeTeam"), "v", f.get("AwayTeam"), "AvgH", f.get("AvgH"))
