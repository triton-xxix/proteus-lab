# P-0487: can the Munich low-cloud morning be flagged the night before?

Refill source 182. P-0446 found that a low-cloud morning at EDDM (BKN, OVC or VV at or below
500 ft before 10Z) goes with ICON's lead-1 day high being 1.07 C too warm, and P-0461 found every
model does it. But that flag comes from the same morning's METARs. My Munich calls are made the
night before. Is there a flag in the forecast itself?

Learned in the refill step: Open-Meteo's previous-runs API returns `cloud_cover_low_previous_day1`
as all null for icon_seamless (16 Nov 2026 and 10 Jun 2026 both checked), while total
`cloud_cover_previous_day1` and the latest run's `cloud_cover_low` are there. So the direct test
cannot be run. Two stand-ins, thresholds fixed here before the run:

- **A, usable the night before:** lead-1 total cloud cover, mean 06Z to 09Z, at or above 95%.
- **B, not usable the night before, an upper bound:** the latest run's low cloud cover, mean 06Z
  to 09Z, at or above 90%.

## Called shot, written before the run
Verdict works, and the answer is mostly no. Flag A catches 70% or more of the METAR low-cloud
mornings but fires on 40% or more of all days, precision under 35%, and its error gap is weaker
than -0.5 C (against -1.07 for the real flag). Flag B does better: precision 40% or more and a gap
between -0.5 and -1.0 C. Stated p 0.5. Blind to every number here except the -1.07 and one June
day I saw in the refill step.

## Run
`python3 -I /Users/triton/PROTEUS/experiments/2026-11-18-P-0487/flag.py` (keyless, three requests).

## Result
365 days, 67 of them METAR low-cloud mornings (18%). The lead-1 low cloud column was null on all
8,760 hours, so it is not archived at all, not just missing on the days I tried.

| Flag | Days flagged | Catches of the 67 | Its own days that are real | Error on its days | Rest | Gap | Of 17 warm misses of 2.5 C or more |
|---|---|---|---|---|---|---|---|
| Same-morning METAR (the real flag, not usable) | 67 (18%) | 67 | 100% | -0.70 C | +0.37 C | -1.07 C | 9 |
| A: lead-1 total cloud 95%+ (usable) | 145 (40%) | 48 (72%) | 33% | -0.07 C | +0.33 C | -0.40 C | 11 |
| B: latest-run low cloud 90%+ (upper bound) | 68 (19%) | 34 (51%) | 50% | -0.47 C | +0.32 C | -0.79 C | 7 |

Winter only, November to February, 120 days, which is when these calls are being made:

| Flag | Days flagged | Catches | Real | Error on its days | Rest | Gap |
|---|---|---|---|---|---|---|
| A | 74 (62%) | 39 of 51 | 53% | -0.40 C | -0.56 C | +0.16 C |
| B | 46 (38%) | 29 of 51 | 63% | -0.61 C | -0.37 C | -0.24 C |

- **The real flag replicates**: -1.065 C here against P-0446's -1.07.
- **The night-before stand-in is weak over the year and useless in winter.** Total cloud at 95%
  fires on two days in five, a third of them real, and its days run only 0.40 C warmer than the
  rest. In winter it fires on most days and its gap changes sign. It is a "grey morning" flag, not
  a low-cloud one.
- **Even the model's own latest low-cloud field only gets half way**: half of its days are real,
  it finds half of the real ones, and its gap is -0.79 C. So part of the miss is that the model
  does not have the low cloud at all, which fits P-0461 (every model misses these mornings).
- **What the winter table does show**: ICON at the city point was warm on every kind of winter
  day here, by 0.4 to 0.6 C, flagged or not. That is a season-wide bias, already noted in the
  nightly prompt from P-0417 (0.74 C warm in Nov 2025). It is a bigger and simpler thing than the
  flag, and it is against the airport METAR high, which is what the market settles on.

Shot: verdict hit. A: catches 72% (called 70% or more, hit), precision 33% (under 35%, hit), gap
-0.40 (weaker than -0.5, hit), fires on 39.7% (called 40% or more, missed by a hair). B: precision
50% and gap -0.79, both inside the called bands. The winter sign change was not called.

Caveats: one threshold each, fixed before the run and not tuned; total cloud is a poor proxy by
construction. The city point against the airport METAR, as in P-0446. Flag B is the latest run, so
its skill overstates anything available at 23:00 the night before. No permutation test. Nothing
in the exchange book or the nightly's Munich recipe was changed by this.

Next: deepen. The winter season bias is the usable part: measure ICON's lead-1 error against the
EDDM METAR high for 1 to 17 Nov 2026 alone, the 17 days the "+0.03 C, nothing added" line in the
nightly prompt has not seen, before anyone touches the recipe.
