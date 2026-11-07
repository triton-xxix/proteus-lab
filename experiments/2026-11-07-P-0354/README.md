# P-0354: does Heathrow's METAR run cold at the warm part of the day? (7 Nov 2026)

Deepen of P-0353, which left about 0.6 C of P-0346's 0.93 C METAR-high gap unexplained by sampling.
Question: split P-0352's matched minutes (METAR minus SYNOP tenths, same minute) by UTC hour.

Shot: works at 0.60; about -0.3 C at 12 to 15 UTC against about +0.1 C at night.

## Method

`byhour.py`: P-0352's match again (one Iowa Mesonet curl, the cached Ogimet 10-minute SYNOPs), 738 matched
minutes, all at :20 since the cache has no :50. Per hour of day; the day's three warmest hours by the SYNOP
hourly mean; and the METAR at the day's warmest matched minute.

## Numbers (`results.json`)

| | shot | measured |
|---|---|---|
| 12 to 15 UTC | -0.3 | **-0.16 C** |
| 00 to 05 UTC | +0.1 | **+0.06 C** |
| coldest hours of the gap, 10 to 12 UTC | | -0.30 C each |
| day's three warmest hours (90) v the rest (648) | | -0.17 v 0.00 C (sd 0.58, se about 0.06) |
| at the day's warmest matched minute (31) | | -0.45 C, inflated by selection |

The gap has a daily cycle: positive all evening and night (+0.1 to +0.25), negative from 07 UTC, worst
10 to 12 UTC, easing by 14. The METAR runs cold while the air warms, warm while it cools: it lags. That
reads like a slower sensor or a longer averaging window than the SYNOP's, not a fixed offset.

## What it says for the gap

Sampling and rounding gave about 0.33 C (P-0353). The METAR's lag at the warm hours adds about 0.2 to 0.3.
Together roughly 0.5 to 0.6 of P-0346's 0.93; the rest is unexplained, and P-0346 covered Sep to Oct while
this is October only.

## Caveats

The -0.45 at the warmest minute is picked on the SYNOP's own high, so noise pushes it negative; do not quote
it as the lag. One month, :20 minutes only.
