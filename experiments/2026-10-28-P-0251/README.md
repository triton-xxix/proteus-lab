# P-0251: Munich airport v city daily high

28 Oct 2026, nightly probe loop, refill row 43. `pair.py` reads DWD's keyless 10-minute air temperature
for 01262 Muenchen-Flughafen and 03379 Muenchen-Stadt (zips in `sandbox/dwd-01262/`, gitignored) the
same way as P-0241, over the last 60 complete local days both stations have (27 Aug to 27 Oct, two
gap days skipped). Output `results.json`, one row per day.

| measure | value |
|---|---|
| mean city minus airport high | +0.78C |
| city warmer | 81.7% of days |
| highs differ by 1C or more | 41.7% of days |
| same whole degree (rounded) | 35% of days |
| median hour of the high, city / airport | 15:10 / 15:40 |
| airport peaks later | 66.7% of days |

Reading: the station a Munich market settles on decides the degree on about two days in three. My calls
add about 1C to ICON for the city (0.3C for the airport); the measured gap of 0.78C between the two
stations fits that 0.7C difference. Any call that cannot name its station is guessing which of two
answers is wanted. The airport also peaks about half an hour later, which pushes the latest useful
forecast hour to around 16:30 if the airport is the source.
