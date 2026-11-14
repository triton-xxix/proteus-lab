# P-0449: the SPY big-gap fade with slippage and a stop

**Question.** P-0433 found fading SPY gaps of 1% or more since 2009 made +0.198% a trade after a 0.02%
round trip (443 gaps). With 0.05% slippage at the open and a stop at twice the gap, what is left, and is it
just the volatile years?

**Rules (before the run).** Fade at the open; target yesterday's close; stop the gap distance again beyond
the open; else out at the close. Costs 0.02% plus 0.05% slippage. When the day's range touches both stop and
target, daily bars cannot order them: worst case takes the stop, best case the target. Vol terciles on the
prior 20-day realised vol. Coin control as P-0433 (fade or follow at random, 2,000 draws). `stopfade.py`,
cached Yahoo daily bars, price only.

**Called shot.** works at 0.75; worst case +0.05%, best case about +0.17%.

## Numbers

| version | mean per trade |
|---|---|
| P-0433 cost only (replication) | +0.198% |
| + 0.05% slippage, no stop | +0.148% |
| + slippage + stop, best case | +0.160% |
| + slippage + stop, worst case | **+0.030%** (t 0.50, win 46.7%) |

- Stop touched on 82 of 443 days; stop and target both touched on 19.
- Worst case v coin: coin -0.132%, p 0.002, so the fade side still beats guessing, but its own t is 0.5.
- By prior vol tercile (no stop / worst / best): low (under 17% annualised) +0.135 / +0.096 / +0.129;
  mid +0.120 / +0.009 / +0.106; high (over 27%) +0.188 / -0.015 / +0.244.
- Worst case: 12 of 18 years positive, and 2020 plus 2022 carry 74% of the total.

## What it means

The stop does not help. At best it adds 0.01 points over no stop; at worst it takes the fade from +0.148% to
+0.030%, and it bites hardest in high-vol tape, exactly the years the edge came from. Without a stop the
fade is a short-volatility trade that earns most in 2020 and 2022; with one it is close to nothing. My shot
was close on both numbers (+0.05 and +0.17 called, +0.03 and +0.16 measured).

## What I did not do

- No intraday bars, so the 19 both-touched days stay unordered; the truth sits between the two rows.
- No other stop widths, no other ETFs (P-0433 found seven of nine lost even before costs).
- No borrow cost on the short side.
