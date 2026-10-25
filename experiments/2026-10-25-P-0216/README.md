# P-0216: partial pooling across Grinder entry-liquidity buckets

Refill from row 26 (Statistical Rethinking 2023, lecture 12, multilevel models). The idea: shrink each
bucket's mean toward the grand mean, the noisier the bucket the harder. Does it predict better than raw
bucket means?

**Shot:** works at 0.70, pooled MSE over raw MSE about 0.7. **Measured:** 1.17 on the headline setup. Miss.

## Method

- Data: `grinder/graduates/closed.jsonl`, counted rows (latency at most 120 s, Jupiter liquidity at least
  $5k), exit P (-50% stop, else 20 min), percent of stake. 14,887 rows, the same count the kill check uses.
  I used the stored P figure as is, without re-applying v0.2 costs; costs move every bucket alike.
- Split by entry time at the median: 7,443 first half, 7,444 second.
- Liquidity buckets (10 and 20) fixed on first-half quantiles.
- Empirical Bayes, normal-normal: tau^2 = var(bucket means) minus mean(se^2), weight tau^2/(tau^2+se^2).
- Score: MSE of first-half estimates against second-half bucket means. Also a shape score, each half's
  own grand mean removed, because the second half ran about 15 points better almost everywhere.
- Robustness: P winsorised at the 1st and 99th percentiles.

## Numbers (`results.json`)

| run | MSE raw | MSE pooled | ratio | shape raw | shape pooled | shape flat | shape ratio |
|---|---|---|---|---|---|---|---|
| raw %, 10 buckets (headline) | 333.5 | 390.9 | **1.172** | 130.0 | 143.3 | 330.3 | 1.102 |
| raw %, 20 buckets | 430.6 | 445.1 | 1.034 | 264.3 | 212.0 | 352.1 | 0.802 |
| winsor, 10 buckets | 384.3 | 375.8 | 0.978 | 120.9 | 112.5 | 157.7 | 0.930 |
| winsor, 20 buckets | 373.6 | 354.9 | 0.950 | 136.4 | 115.5 | 170.0 | 0.847 |

## What it says

- The bucket shape is real: raw bucket means beat a flat line in every run (shape 130 v 330 at 10 buckets).
  The top liquidity decile was positive in both halves (+24.4, then +35.2); the middle sat at -20 to -40,
  then -2 to -24.
- Pooling hurt at 10 buckets on raw returns because the lowest bucket's mean (-1.2) came from fat-tailed
  winners that recurred (+3.0 in the second half), and shrinkage pulled it to -15.7.
- Pooling helps only where buckets are thin (20 buckets) or once tails are trimmed: 5 to 20 percent less error.
- Most of the error is a level shift between halves (MSE 333 against mean se^2 of 91), which no pooling can fix.

## What I did not do

- No multiple random splits or rolling folds; one time split.
- No Bayesian fit (no Stan or PyMC); the closed-form empirical-Bayes estimate only.
- No look at G2's $50k floor separately. The book is KILL (G1) and KEEP withdrawn (G2), so nothing trades on this.
