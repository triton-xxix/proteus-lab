# P-0479: Voyager 1 and one light-day, from JPL Horizons, keyless

Source: harvest H-0679 (Hacker News item 50548161), 18 Nov 2026.

## Called shot, written before the first fetch
Verdict works. Horizons answers keyless. Voyager 1 on 18 Nov 2026 is between 171.5 and 173.5 AU
from Earth, inside 2% of one light-day (173.14 AU), light time between 23 h 45 m and 24 h 05 m.
Stated p 0.7. Not blind to the size of the number: I know roughly where Voyager is. Blind to the
day it crosses and to which way Earth's own orbit is moving the range this month.

## Run
`python3 /Users/triton/PROTEUS/experiments/2026-11-18-P-0479/horizons.py`
Writes `raw.txt` (the API's answer) and `results.json`.

## Result
Run at about 23:40 UK on 18 Nov 2026, one request, no key, 123 daily rows (1 Oct 2026 to 31 Jan 2027).

- 18 Nov 2026 00:00 UTC, from the Earth's centre: 25,899,668,326 km, 173.129 AU, light time
  23.9978 hours. That is 0.009% short of one light-day (25,902,068,371 km, 173.145 AU). Inside 2%
  by a factor of about 200.
- The first daily row at or past one light-day is 20 Nov 2026 (24.0018 hours), so the crossing
  falls between 00:00 UTC on 19 Nov and 00:00 UTC on 20 Nov. I am writing this the night before.
- The range is growing at 25.6 km/s tonight, not Voyager's own 17 km/s: most of the month's change
  is the Earth moving away. The rate falls through zero on 21 Jan 2027, and for the last 11 days of
  the window the range shrinks. Whether it dips back under a light-day later in 2027 is outside the
  window and not measured.
- Check on the feed itself: range divided by the speed of light matches Horizons' own light-time
  column to within 5e-10 hours on every row, so the two columns are one number.

Shot: verdict hit, AU band hit (173.13 in 171.5 to 173.5), light-time band hit (23 h 59.9 m in
23 h 45 m to 24 h 05 m). The band was wide; the real finding is how close to the day it is.

Caveats: geocentric, not from a ground station (a station adds or removes up to 6,378 km, about
0.02 light-seconds, which cannot move the crossing by more than minutes). Daily steps, so the
crossing hour is not pinned. Horizons' Voyager trajectory is a prediction, not a tracked fix.
