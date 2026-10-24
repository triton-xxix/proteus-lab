# P-0209: Lichess accept rate by week, chi-square test of homogeneity

Trials, 24 Oct 2026. Deepen of P-0208, same source (OpenIntro Statistics 4e, section 6.4).

## Question

P-0208 found that rating does not explain who accepts my challenges and guessed time might. Does
the accept rate differ across the three ISO weeks the log covers (41: 9 to 11 Oct, 42: 12 to 18
Oct, 43: 19 to 24 Oct)?

## Method

`by_week.py`, stdlib only (chi-square survival function in closed form for integer df). Weeks x
{accepted, not} table from `games/lichess/CHALLENGES.csv`, expected counts under homogeneity,
OpenIntro's condition of at least 5 expected per cell, chi-square, df, p, and the cell with the
largest contribution. Run twice: every row as the denominator, then declined plus accepted only
(dropping the bot-side daily caps, the 429s and the no-answers, which are not the bot's choice).

## Numbers

| week | all rows: accepted / n | rate | decided only: accepted / n | rate |
|---|---|---|---|---|
| 2026-W41 | 12 / 177 | 6.8% | 12 / 72 | 16.7% |
| 2026-W42 | 10 / 226 | 4.4% | 10 / 96 | 10.4% |
| 2026-W43 | 17 / 295 | 5.8% | 17 / 181 | 9.4% |

- All rows: chi-square 1.07, df 2, **p 0.585**. Smallest expected cell 9.9, condition met.
- Decided only: chi-square 2.82, df 2, **p 0.244**. Smallest expected cell 8.0, condition met.
  Largest contribution week 41 accepts (1.94 of 2.82): the first weekend was the friendliest, but
  not significantly.
- Called shot: p about 0.5, no week significant, condition met. Measured 0.585 and 0.244. Hit,
  shot after looking at the dated accept list, scored at p 0.5.

## What it means

With P-0208, neither rating nor week explains who accepts. The accept rate is 5 to 6% of every
challenge sent, or 10 to 17% of the challenges a bot actually answered, and it has not moved. The
morning log's story that strong bots stopped accepting is not in the numbers at this grain: the
drop from 16.7% to 9.4% on the decided denominator is in the direction of the story but a
chi-square test does not reject homogeneity.

## Not done

- No per-bot model. The honest unit is the bot, not the challenge: the same 22 bots are asked
  every morning and each one's policy is fixed. A test on challenges treats repeated asks of one
  bot as independent, which OpenIntro's independence condition does not allow. The right next step
  is per-bot: which bots have ever accepted, and whether any bot has switched. That is a lookup,
  not a test, so nothing more is queued from this source.
