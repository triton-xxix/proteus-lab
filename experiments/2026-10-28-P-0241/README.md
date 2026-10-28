# P-0241: by what local hour is Munich Stadt's daily high reached?

**Question.** Over the last 60 complete days, by what Europe/Berlin hour has DWD station 03379
(Muenchen-Stadt) already recorded its daily high on 90% of days? That is the latest hour a
day-of exchange call on the Munich high still has something left to forecast.

**Called shot.** works at 0.75, number 16:00 local. The verdict was right; the number was 20 minutes early.

**Method.** `hour_of_high.py` on the keyless DWD recent zip (`10minutenwerte_TU_03379_akt.zip`, file
`produkt_zehn_min_tu_20250426_20261027_03379.txt`). MESS_DATUM is UTC, converted to Europe/Berlin. High =
max TT_10 per local day; time = the first 10-minute stamp at that max. Days with under 140 of 144 slots skipped.
Window 29 Aug to 27 Oct 2026.

**Numbers.**
- 90th percentile: **16:20 local**. Median 15:10.
- Share of days with the high already in: 14:00 23%, 15:00 47%, 16:00 75%, 17:00 98%, 18:00 100%.
- By hour: 15:00 to 15:59 holds 21 days, 16:00 to 16:59 holds 15. Only one high after 17:00.
- 3 of 60 days (5 Sep, 9 Sep, 24 Oct) had their high at 00:00: warm night, then a cold front. On those days
  the high is set before the market day starts.

**Caveats, what I did not do.** One station, late summer into autumn only; summer highs and winter highs
will sit at different hours, and the clock change on 25 Oct shifts the local hour by one. TT_10 is a 10-minute
instantaneous value, not the true continuous max, so an exchange settling on a daily-max sensor can differ
by a few tenths. No exchange's settlement source checked here.

**Reading.** By 17:00 local the Munich high is in on 59 days of 60. An afternoon call after that is
a reading, not a forecast; a call made before about 14:00 still has three quarters of days open.
