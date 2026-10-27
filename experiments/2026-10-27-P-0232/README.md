# P-0232: capture the ICON-EPS band before the day

**Question.** P-0231 could only score three days because the Open-Meteo ensemble API keeps about three
past days. To test the band properly it has to be captured ahead of time, every night, and committed.

**Method.** `capture.py` pulls the 39-member `icon_seamless` daily high for Munich (48.137, 11.575),
takes tomorrow's p10, p50, p90, min, max and control, and appends one row to
`exchange/icon_eps_band.jsonl`. A day already captured is skipped. `capture.py score` checks each
captured day DWD 03379 (Stadt) has observed: inside the raw band, inside the band shifted +0.5C (P-0225's
out-of-sample bias), and how many land above it.

Wired as step 3.4 of `tasks/nightly.md`, after the exchange snapshot, so the step 4 pre-registration
commit carries each row before its day.

**Numbers.**
- First row, captured 27 Oct 12:45 local for 28 Oct: p10 10.90, p90 13.14, **width 2.24C**, n 39.
- Re-run: "already captured 2026-10-28", nothing appended.
- `score`: 0 of 1 scored (28 Oct not observed yet), runs clean.

The band at about 1.5 days of lead is 2.24C wide, two and a half times P-0231's short-lead widths
(0.6 to 1.24C). So the past-day widths in P-0231 understate a real day-ahead band; the nightly capture
(about 23:00, under a day of lead) will sit somewhere between.

**What I did not do.** No score yet (needs 20 observed days), no Flughafen station, no change to how
exchange calls are made.

**Shot.** works at 0.75, expecting a 28 Oct row with width under 1.5C. Row came; width 2.24C.
