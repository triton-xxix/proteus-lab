# P-0375: does Wikipedia interest in Nolan's films decay on one curve?

`decay.py` pulls daily English Wikipedia pageviews (users only) for Dunkirk, Tenet, Oppenheimer and The Odyssey. Day 0 is each film's peak day, days 7 and 30 are 7-day centred means. Leave-one-out: three films' mean day-30-over-day-7 ratio, times the fourth's day 7, predicts its day 30.

## Numbers

| Film | Peak date | Peak views | Day 30 over peak | Day 30 over day 7 | Power-law k, days 3 to 60 | Predicted day 30 | Actual | Error |
|---|---|---|---|---|---|---|---|---|
| Dunkirk | 23 Jul 2017 | 358,336 | 10.3% | 0.223 | -1.05 | 47,629 | 37,047 | +28.6% |
| Tenet | 29 Aug 2020 | 281,284 | 23.1% | 0.309 | -0.86 | 54,281 | 65,002 | -16.5% |
| Oppenheimer | 23 Jul 2023 | 1,362,922 | 10.9% | 0.289 | -0.92 | 136,210 | 148,800 | -8.5% |
| The Odyssey | 18 Jul 2026 | 1,199,464 | 12.9% | 0.262 | -1.01 | 162,210 | 155,266 | +4.5% |

3 of 4 within 25%. Day 30 is 22% to 31% of day 7, mean 0.271. All four sit near a power law with k about -1, so interest roughly halves each time the days since peak double.

## Reading

A single ratio works well enough for a rough day-30 number from day 7 on three of the four. The miss is Dunkirk, which fell faster. Tenet held up longest, and Tenet's peak is the smallest. It came out during the pandemic, so a slow staggered release may explain that, but I did not test it.

The Odyssey's fit is the tightest (+4.5%) and was left out of its own ratio, so it is a fair test.

## Called shot

Said 3 of 4 within 25%, day 30 about 12% of peak. Got 3 of 4, and 10.3 to 23.1% with a median of 11.9%. Right on both.

## Not done

Four films is a small sample and all are one director. The 25% line was chosen before the run. English Wikipedia only. Pageviews are interest, not tickets.
