# P-0459: did the Munich market already price the low-cloud warm miss?

**Question.** P-0446 found that a cloud base at or below 500 ft before 10Z at EDDM marks a warm ICON
lead-1 miss (-1.07 C on the year, -1.28 C in early November). Did the Polymarket "Highest temperature in
Munich" market's 09Z prices already sit lower on those mornings, or was the shift there to take?

**Why Polymarket.** The source row (#176) pointed at `exchange/SNAPSHOTS.csv`, which holds one Munich
day (29 Oct), taken after close with empty prices. A Smarkets search hit Cloudflare. Polymarket's
daily events are keyless (gamma-api) and resolve on the EDDM METAR, the same airport as the flag.

**Method.** `market.py`: for 1 to 16 Nov 2026, every bucket's Yes price at or before 09:00Z
(clob prices-history, hourly), normalised to sum 1 (raw sums 0.98 to 1.10), gives an implied mean
high, with tail buckets counted at their edge degree. Truth is the bucket that resolved Yes. Error =
truth minus implied mean (negative = market warm). Flag as P-0446, pulled fresh from Iowa State.

**Numbers** (results.json, 16 days, none skipped).

| | days | mean error |
|---|---|---|
| low-cloud mornings | 5 | -0.32 C |
| other days | 11 | -0.08 C |
| **gap** | | **-0.24 C** |

- ICON's gap on the same flag: -1.07 C (year), -1.28 C (1 to 13 Nov). The market's is about a fifth
  of that.
- 11 Nov was flagged low cloud and came in **1.5 C above** the market; without it the flagged mean
  is -0.78 C. On 5 days one day decides the sign of the story.
- 9 Nov, the day that started the fog and cloud questions: market implied 6.53, resolved 5 (-1.53).
- Market favourite hit 5 of 16 (31%), 1 of 5 on low-cloud days. Mean |error| 0.70 C.
- 12 of 16 errors are negative: the market ran slightly warm most days, not only on cloudy ones.

**Reading.** Most of the ICON low-cloud miss is not there to take in the 09Z market: the market's own
gap is -0.24 C, inside the half-degree noise a whole-degree truth carries. What is left is a weak lean
on five days, one of which went the other way by 1.5 C.

**Called shot.** works at 0.60, "gap about -0.4 C, smaller than ICON -1.07". Measured -0.24, smaller
than ICON: the direction and the comparison held; the size was 0.16 C off.

**Not done.** No permutation test (5 flagged days is too few to mean much). No fees or spreads: the
mid at 09Z is not a fill. No other hour than 09Z. Tail buckets at their edge pull the implied mean
inward a little on tail-heavy days. No bets placed.
