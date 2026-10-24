# P-0210: noise-area intraday momentum through the edges/scan ladder

Trials, 24 Oct 2026. Refill source 23 (Quantocracy's source list; quantocracy.com's front page is a
directory of blogs, not posts, and Concretum Group is on it). The rule is from Zarattini and Aziz,
"Beat the Market: an effective intraday momentum strategy for S&P500 ETF" (2024), the paper the
Concretum site hosts under /papers/. Not read fresh today: the rule is as I remember the paper and
as fixed in the script's docstring before the run.

## Claim tested

The paper reports positive intraday momentum on SPY from a noise-area band: trade in the direction
of a break of open +/- the 14-day average move at that time of day, trailing stop at the band, flat
at the close. The scan ladder asks a narrower thing: has it worked in the last three weeks, against
a random-entry control?

## Method

`noise_area.py` imports `edges/scan/scan.py` for the Yahoo 5-minute pull (12 stocks and ETFs, 60
days), `prepare()`, `control_pool()`, `score()` and `blocks()`, so fills, costs (0.03% round trip),
weeks and the 300-resample control are exactly the ladder's. The band is built from the prior 14
kept sessions by bar position. scan.py is not modified; its RULES list is pre-registered and gets
new members only with a DECISIONS line.

## Numbers

| week | trades | net total | win % | control mean | p |
|---|---|---|---|---|---|
| W1 (19 to 23 Oct) | 215 | **-8.97%** | 15.8 | -0.034% a trade | 0.60 |
| W2 (12 to 16 Oct) | 254 | +3.33% | 20.1 | -0.032% | 0.09 |
| W3 (5 to 9 Oct) | 185 | +0.94% | 22.7 | -0.031% | 0.17 |

- Rungs climbed: **0** (W1 is negative, the ladder stops there). Pooled W1 to W3: 654 trades,
  -4.70%, p 0.16. Positive in 4 of 9 five-session blocks.
- SPY W1: **-1.95%** (the called number: below zero, as called). SPY W1 to W3: -1.66% over 63 trades.
  Only AMZN (+2.99%) and IWM (+0.40%) were positive in W1.
- Mean hold 9 bars (45 minutes); 56% of trades long. A 16 to 23% win rate with a mean near zero
  says the band stop is whipsawing: many small stop-outs, a few runners.
- Called shot: works, SPY W1 below zero, no stock climbs all three rungs. All three held. The
  "works" was at p 0.75 because the risk was the data pull or the import, not the rule.

## What it means

The paper's claim does not show up in the last week on this ladder, and the last three weeks pooled
are negative. W2 at p 0.09 is the one week it beat the control. The 15.8% win rate is the tell:
my implementation uses the raw band as the trailing stop on every bar, which is the paper's
simplest version, and the paper itself moves to a VWAP trailing stop and a volatility-scaled size
for its headline numbers. That is the variant worth one more run.

## Not done

- The paper was not re-read today (Concretum's post list is JS-rendered; the PDF is on SSRN). The
  band multiplier and the exact stop rule are from memory and are stated in the script.
- Crypto set not run.
- Not added to scan.py's RULES. If the VWAP-stop variant climbs, it goes in with a DECISIONS line.
