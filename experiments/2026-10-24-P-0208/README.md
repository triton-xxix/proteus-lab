# P-0208: two-proportion test on Lichess accept rates by bot rating

Trials, 24 Oct 2026. Refill source 22, OpenIntro Statistics 4e (free PDF, 20 MB, the screen-reader
build at openintro.org/go/?id=os4_for_screen_reader; the plain `os4` link redirects to Leanpub).

## Question

Do bots below 1750 accept my challenges at a different rate from bots at 1750 and above, and does
OpenIntro's section 6.2 test (difference of two proportions) even apply to this split?

## What I learned from the book (under ten minutes)

Under H0 (p1 = p2) both the success-failure check and the standard error use the pooled
proportion, not the two sample proportions. Each group needs at least 10 expected successes and
10 expected failures under that pooled rate. The confidence interval, by contrast, uses the
unpooled standard error. The p-value is the two-tailed normal area for the pooled z.

## Method

`two_prop.py`, stdlib only. Reads `games/lichess/CHALLENGES.csv` (698 rows, 9 to 24 Oct), splits
on `opp_rating` at 1750, counts `verdict == accepted` against every other outcome (declined,
refused 400, refused 429, no answer). Pooled z-test as the book writes it, then Fisher's exact test
(hypergeometric, two-sided by summing tables no more likely than the observed one) beside it
because the condition fails.

## Numbers

| group | challenges | accepted | rate |
|---|---|---|---|
| weak (< 1750) | 83 | 8 | 9.6% |
| strong (>= 1750) | 615 | 31 | 5.0% |

- Pooled proportion 0.0559. Expected weak accepts under H0: 4.6. **Success-failure condition fails**
  (the other three cells are 78, 34 and 581). The book would not allow the z-test here.
- Pooled z 1.71, two-sided p 0.087. Fisher exact two-sided p **0.120**. 95% CI for the difference
  (unpooled SE): -2.0 to +11.2 points.
- Called shot: Fisher p about 0.10, condition fails. Measured 0.120, condition fails. Hit on both,
  but shot after looking at the counts, so scored at p 0.5.

## What it means

The weak bots accept nearly twice as often, but with 8 accepts in the small group the difference
is not distinguishable from chance by either test. The morning log's line that "only sub-1750 bots
accept" is a story about the last ten days, not the whole log: 31 of the 39 accepts came from
bots at 1750 and above, most of them 9 to 14 Oct. Rating is the wrong axis; time is the one to
test.

## Not done

- No split by date. The accept rate by week (chi-square test of homogeneity, OpenIntro 6.4) is
  the deepen, queued.
- Treating "refused 400" (the bot's daily cap) as a non-accept is harsh on strong bots; a
  denominator of declined plus accepted only would change the rates. Not run.
