# P-0445: a morning fog code and the Munich forecast high

**Question.** Refill 168 found 9 Nov 2026 was freezing fog then stratus at 100 to 500 ft till noon, and ICON
lead 1 ran 3.5 C warm on the day high. Is that a pattern: over a year, do days with FG or FZFG in any EDDM
METAR from 00Z to 09Z show a warmer forecast error than days without?

**Method.** `fog.py`. P-0418's data and window (1 Nov 2025 to 31 Oct 2026): Iowa State EDDM METAR day high
(40+ reports), Open-Meteo previous-runs `icon_seamless` lead 1 at the city point, maxed per UTC day. Error =
METAR minus forecast (negative = forecast warm). Fog day = FG or FZFG in a report before 10Z (BCFG, MIFG,
PRFG left out). Because fog is seasonal and the bias is seasonal (P-0417), the permutation shuffles the fog
label within each calendar month, 10,000 times, one-sided.

**Called shot.** works at 0.75, gap -1.5 C.

## Numbers

| | days | mean error | MAE |
|---|---|---|---|
| fog morning | 58 | -0.49 | 1.19 |
| no fog | 307 | +0.30 | 1.02 |
| gap | | **-0.79** | |

- Within-month permutation p = 0.0038 (one-sided).
- Of the 17 days the forecast ran 2.5 C or more warm, 7 were fog mornings (41%, against 16% of all days).
- By month the fog days ran warmer than the rest in 8 of the 9 months with both kinds; November 2025 was
  the widest (-1.77 v -0.30, 9 fog days). October 2026 went the other way (+0.36 v -0.07, 11 fog days).

## What it means

The shot's direction held and the number missed: the gap is about half the -1.5 I called. A fog morning is
worth roughly a 0.8 C cold shift on the Munich lead-1 high, more in November, and it is known by 09Z, hours
before a daily high market settles. It does not fix every bad day: 10 of the 17 big warm misses had no fog code.

## What I did not do

- One station, one model, one year. No out-of-sample test: November 2026 (1 to 13 Nov) is the obvious one.
- No check of the airport point or the mean of points.
- Low stratus without a fog code (9 Nov after 08Z read BR) is not flagged; a cloud-base flag might catch more.
- No market prices: whether a 0.8 C shift moves a bucket price enough to trade is untested.
