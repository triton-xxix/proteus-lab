# P-0082: five YouTube strategy claims, rebuilt and tested against luck

Run 7 Oct 2026, interactive, at Luke's request ("run P-0082 now"). The question: when the free
channels I chose to follow (field-notes/2026-10-07-skool-trading.md) state a strategy, do their
numbers come out the same when I rebuild it, and does the strategy beat a shuffled market?

## Method

- **Videos:** three from Quantified Strategies, two from Kevin Davey. Transcripts came keyless
  through youtube_transcript_api, about 5,000 words, which I read myself (too small to hand to a
  child model). They stay in `sandbox/p0082/` and are not committed.
- **Data:** daily bars from Yahoo's chart endpoint, keyless (`fetch_prices.py`). OHLC are scaled to
  total return unless I say "price only". Stooq now puts its CSV behind a proof-of-work bot check,
  so I did not use it.
- **Luck test:** neurotrader888's Monte Carlo permutation test (github.com/neurotrader888/mcpt, MIT),
  rewritten for numba in `p0082.py`. The gaps and the moves within each bar are shuffled
  separately, then the series is rebuilt. That keeps the drift and the size of the moves but
  destroys their order. Same rules, same scoring (profit factor of the daily strategy returns). p is
  the share of shuffles that do at least as well. Where the video chose a parameter from a sweep,
  every shuffle gets the same sweep and keeps its own best, so the search is paid for. 1,000 shuffles
  for fixed rules, 500 where a parameter was searched.
- **No costs or slippage**, as in the videos. On SPY that is small against average trades of 0.3%
  to 3%.

## Results

### 1. Quantified Strategies, "200 vs 222-Day Moving Average: A 33-Year SPY Backtest"

Rules given in full: close above the average, buy next open; close below, sell next open. SPY 1993 to 2026.

| | Their 200 | Mine 200 | Their 222 | Mine 222 |
|---|---|---|---|---|
| Trades | 111 | 109 | 98 | 106 |
| Profit factor (trades) | 3.20 | 3.96 | 3.84 | 3.90 |
| Max drawdown | 21.2% | 27.3% | 14.0% | 25.3% |
| Growth | 8.24x | 14.4x | 9.76x | 14.7x |

- **Partly replicates.** Trade counts match. On price-only data, 222 ranks 2nd of the 281 lengths
  and 190 to 230 is the strong zone, as they say. On total-return data the "best" length is
  wherever the search stops: growth climbs to 25x at 290 to 300.
- **Not shown in the video: every version made less than holding SPY.** Buy and hold was 32.4x
  total return (17.7x price only), with a 55% drawdown. The filter's value is the drawdown, about
  halved, not the return.
- **Luck test:** fixed 200, p = 0.057. Best of 281, p = 0.18. From 2009 on, p = 0.34. **Fails.**
  On this test, whether the length is 200 or 222 is noise.

### 2. Quantified Strategies, "This Simple RSI Strategy Grew 482% in Our Backtest"

Rules given in full: SPY above its 200-day average and RSI(5) below 30, buy at the close; RSI(5)
above 50, sell at the close. Double adds RSI falling three sessions in a row. Triple adds RSI below
60 three sessions earlier.

| | Trades (theirs / mine) | Growth (theirs / mine) | Luck test p, 1993 on | p, 2009 on |
|---|---|---|---|---|
| Simple | 199 / 211 | +482% / +598% | 0.001 | 0.037 |
| Double | 127 / 132 | +261% / +316% | 0.001 | |
| Triple | 90 / 93 | +202% / +251% | 0.001 | 0.029 |

Triple, theirs then mine: win rate 88.9% / 90.3%, average trade 1.25% / 1.38%, exposure 5.2% / 5.0%.
**Replicates.** Counts land within 6% and the ranking is the same: simple grows most, triple has
the best trades. Mine run a little higher, probably dividends or a slightly different date range.
None of the 1,000 shuffles matched it over the full period (0.001 is the floor). It still passes
from 2009 on, more weakly.

### 3. Quantified Strategies, "What Happens When You Backtest Every RSI Oversold Level?"

RSI(2) below a threshold, SPY above its 200-day average, buy next open. **The video never states
the exit.** I tried four. "Close above yesterday's high" reproduces their table:

| Threshold | Theirs: trades, PF | Mine: trades, PF |
|---|---|---|
| RSI < 1 | 13, 6.56 | 15, 7.22 |
| RSI < 9 | 233, 2.59 (win 76.8%, avg 0.59%) | 235, 2.62 (win 77.0%, avg 0.55%) |
| RSI < 30 | 613, 1.84 (avg 0.33%) | 624, 1.77 (avg 0.29%) |

**Replicates.** Luck test, 1993 on: RSI < 30 fixed, p = 0.017. Best of 50 thresholds with at least
100 trades, p = 0.032. That picks RSI < 9, the same as theirs. **From 2009 on it fails:** RSI < 9,
p = 0.21; RSI < 30, p = 0.10. Larry Connors published RSI(2) in 2008. Their own video says the
edge weakened after 2005 and moved to higher thresholds.

### 4 and 5. Kevin Davey, "Does The Golden Cross Actually Work?" and "I Tested The RSI On 220 Markets"

He tested 44 futures markets on five intraday bar sizes with walk-forward testing in TradeStation,
which I cannot get free. My version is his entry and his exit on daily bars. The exit sells when
open profit falls a multiple of ATR below its peak. I ran it on 12 ETFs standing in for his
futures, 2007 to 2026. Each market gets the best of 48 parameter sets, and the luck test pays for
that search.

| | His verdict | Mine: markets with p < 0.05 | Closest |
|---|---|---|---|
| Golden cross | "Absolutely pass": 12 of 220 good, none very good, stock indices among the worst | 1 of 12 (USO, p 0.014); about 0.6 expected by luck | SPY 0.70, IWM 0.95 |
| RSI crossover | "Meh": a slight edge only in stock indices | 0 of 12 | SPY 0.062, the only one near |

**His verdicts replicate** on a different test. The golden cross has nothing to speak of, and
stock indices do badly with it. The RSI crossover's only hint is in the S&P 500. With fixed middle
settings, 10 of 12 RSI markets lost money. The golden cross grid (fast 25 to 100, slow 150 to 300)
is my guess at his 48. The RSI grid is his exactly.

### The fifth Quantified Strategies video I dropped

"This Russell 2000 Strategy Beat Buy and Hold Since 1995": "This time we won't show you the exact
trading rules." Rules for members only, so it cannot be checked. I swapped in video 3.

## What it means

- **Both channels are worth following.** Quantified Strategies' numbers came out the same three
  times out of three when rules were given (once I had to recover the exit). Davey's two negative
  verdicts held up. Neither oversold.
- **What has survived so far:** short-term mean reversion in SPY after a fall, inside an uptrend.
  The RSI(5) version passes the luck test before and after 2009. The RSI(2) version passes before
  and fails after, which is what you would expect from an edge that became famous.
- **Multiple tests.** I ran 36 luck tests here: 12 on the Quantified Strategies rules and 24 on Davey's. At that count, the post-2009
  p-values of 0.03 to 0.04 are suggestive, not proof. The full-period 0.001s are proof that 1993 to 2008 had the
  effect.
- **What failed:** trend filters on SPY as a way to make more money. They cut drawdown and lose
  return. The golden cross and RSI crossover failed as stand-alone systems on daily bars.
- **Next:** paper-track RSI(5) simple and triple on SPY forward, each signal committed before the
  open. That is the only test that cannot be fitted.

## Reproduce

```
/Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 experiments/2026-10-07-P-0082/fetch_prices.py SPY QQQ DIA IWM GLD SLV USO UNG TLT IEF FXE FXY
/Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 experiments/2026-10-07-P-0082/p0082.py
```

The scripts write to `sandbox/p0082/data/` and to `results.json` here. The full run took 212 s on
the Intel Mac. The 2009-on checks are in `results.json` under `post_publication_2009_on`. They came
from a one-off call to the same functions, with shuffles that start in 2009 and leave the earlier
bars real. Trade counts group adjacent bars, so an exit followed by an entry the next day counts as
one trade. That undercounts slightly.
