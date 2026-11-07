# P-0352: does Heathrow's METAR round or truncate? (7 Nov 2026)

Refill row 111, from P-0346, which found Heathrow's whole-degree METAR daily high 0.93 C under its SYNOP
maximum. Question: matched minute by minute, does the METAR temperature equal the SYNOP tenths reading
rounded, floored, or neither?

Shot: works at 0.75, rounded at 85% of matched minutes, floored at about 50%.

## Method

`rounding.py`: one Iowa Mesonet curl, EGLL October 2026, 1,488 METARs (routine and specials). Ogimet's
10-minute SYNOPs for 03772 from the cache, 3,668 minutes with a 1sTTT group. 738 METARs share a minute with a
SYNOP; 750 do not (the cache holds about half the :50 slots).

## Numbers (`results.json`)

| | shot | measured |
|---|---|---|
| METAR = tenths rounded half up | 85% | **66.5%** |
| METAR = tenths floored | 50% | **46.9%** |
| neither | | 17.9% |
| excluding x.0 readings (where both agree): rounded v floored | | 51% v 23% |
| x.5 readings: half up v half down | | 35 v 45 |
| mean METAR minus tenths | | **-0.02 C** (sd 0.56) |

## What it says

Not truncation: truncation would put the METAR about 0.45 C under the tenths on average, and the mean is
-0.02. Rounding wins over flooring two to one where they differ, but 18% of minutes match neither and the
spread is 0.56 C, so the METAR is not the same reading rounded: it is a different sample of the air
(likely a different averaging window or sensor), unbiased at the same minute. So P-0346's 0.93 C gap is not
in how the number is written. The obvious remaining cause is that half-hourly METARs miss the peak a
continuous SYNOP maximum catches; that is untested here.

## Not done

Only matched minutes, half the METARs. October only. The peak-sampling explanation is a guess.
