# P-0393: Sentinel-2 scene counts per day, 27 Oct to 9 Nov

**Question.** P-0385 found 3 of its 6 descending-pass misses lined up on Sentinel-2B about 3 Nov and
guessed at an outage. Worldwide, was 2B's 3 Nov a real drop below its own 14-day median?

**Shot.** works at 0.50 (called after seeing the 3 Nov 2B count of 5,108 in the refill test, not the
median): 2B on 3 Nov within 20 pct of its own 14-day median, no outage.

**Method.** `counts.py`: one keyless POST per platform per UTC day to Earth Search
(`sentinel-2-l2a`, limit 1), reading `numberMatched`. 42 calls, no errors.

**Numbers** (results.json). Median scenes a day: 2A 2,424, 2B 5,962, 2C 4,917. On 3 Nov: 2A 1,976
(0.82 of median, its 14-day low), 2B 5,108 (0.86, its 14-day low), 2C 5,108 (1.04). No platform has any
day below half its median.

2B alternates between about 5.1 to 5.4k and 6.0 to 6.7k from day to day (the orbit's repeat over land
and sea), and 3 Nov sits in the low group beside 2 Nov (5,178) and 31 Oct (5,300). It is the lowest of
the low days by 70 scenes.

**Answer.** No worldwide 2B outage on 3 Nov. P-0385's three misses are local (those cities' tiles, or
cloud filtering), not a dropped day. 2A dipped harder that day than 2B did.

**Caveats.** Counts are catalogued L2A granules, not acquisitions; a processing delay since filled
would not show. One catalogue.

**Not done.** I did not check the three missed tiles by name.
