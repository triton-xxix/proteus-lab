# P-0532: Aurora pageviews as a storm detector

Do readers follow the sky? Refill row 221. NOAA's Kp file holds eight days, so the Kp history comes
from GFZ Potsdam's keyless JSON (CC BY 4.0).

## Method

`aurora.py`: GFZ three-hourly Kp, 1 Jan 2024 to 21 Nov 2026, reduced to the daily max; en Wikipedia
daily user views of `Aurora` (Wikimedia REST). A spike is views above twice the median of the 30 days
before. 1,056 days.

## Numbers

- Correlation of daily max Kp with views: 0.225 same day, 0.220 next day (0.242 against log views).
  Weak, because most storms pass unread and three (May 2024, Oct 2024, Nov 2025) dwarf everything.
- **Kp 7 or more: 28 days, 16 with a spike that day or the next (57%).** Kp 5 or more: 142 days, only 25
  with a spike (18%).
- Run the other way, as a detector: **39 spike days, 28 with Kp 5+ that day or the day before (72%),
  11 on calm days.** The biggest: 341,117 views on 11 May 2024 (Kp 9), about 100 times the median.
- The misses are night-time storms the press skipped: 28 Jun 2024 (Kp 7.7) drew fewer views than its
  median.

## What I did not do

No other languages or articles (`Geomagnetic storm` left out for time), no check of what the 11 calm
spikes were (eclipses, a viral photo?), no seasonality control (summer nights are too light to see).
