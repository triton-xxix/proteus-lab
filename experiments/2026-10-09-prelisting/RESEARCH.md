# Can you know a listing is coming? (9 Oct 2026)

Luke's idea, after P-0107 showed the listing pop is gone within five minutes: hold the coins most
likely to be announced on a major exchange, and sell two or three minutes after the announcement
into the pop. Paper only. This is the research half. The rules for the week of tracking are in
`RULES.md`; the tracker is `poller.py`.

## The short answer

1. **The pop is worth having if you already hold.** On 58 Upbit KRW listings of coins already
   trading elsewhere, holding at the announcement and selling at the worst price inside the minute
   that contains +3 minutes made a median **+15.8% after costs**, positive in 91%. Binance spot
   (8 events): +6.0%. Coinbase roadmap posts (16 events): +1.8%. Waiting is not the danger I
   expected: +10 minutes is still +16.8% on Upbit. The fade P-0107 found happens over hours and days.
2. **Some public events make a listing far likelier.** Against a 0.33% base rate (an average coin
   gets an Upbit KRW listing in the next 14 days a third of one percent of the time), a new Bybit
   spot listing precedes one 26% of the time, a Coinbase trading launch 20%, a Binance spot
   announcement 29%, a new Binance USD-M perpetual 12%. Lead time is about a week (median 6 to
   7 days), up to three weeks for Binance perps.
3. **It does not yet make money.** Holding the top 10 ranked coins every day beat 99% of random
   lists drawn from the same pool, so the ranking is real. But the coins it ranks are mostly newly
   launched tokens, and they fall: first half (fit, in-sample) **-42%**, second half (out of
   sample) **+9%**, against **+16%** for simply holding everything. Over the year, about **-37%**.
   The pops are real; there are not enough of them to pay for holding new tokens while they bleed.
4. **Coverage is the ceiling.** The top-10 list held 8 coins at the moment of their announcement
   out of 52 target listings in the test half (15%). Most Upbit listings show no public event in the fortnight before them that I can see
   keylessly.

So the honest framing for Luke: the ranking finds the right coins about ten times more often than
chance (7% of list members are announced within 14 days, against 0.7% for any of the three venues), and that is still a losing trade on its own, because "right coin" means "new coin" and new
coins go down. The week of tracking is there to check the plumbing and the detection speed, and to
start a forward record. It cannot settle the money question; that needs about 30 hits, which is
roughly 12 weeks.

## Data

All keyless except X. Window 9 Oct 2025 to 8 Oct 2026, look-back to 1 Jun 2025.

| Source | What | How |
|---|---|---|
| Upbit trade notices | 120 notices back to 18 Sep 2025 (the API stops there): 103 KRW listings or KRW additions, 15 BTC/USDT-only | `api-manager.upbit.com` |
| Binance catalogue 48 | 525 notices: 26 crypto spot listings, 206 futures launches | `bapi/composite` |
| Coinbase | 109 @CoinbaseMarkets posts (roadmap, deposits, trading), times from the post ids | xAI X search, 7 calls |
| Published listing times | Binance USD-M perps 658, OKX spot 411 and swap 485, Bybit perps 785, Gate 2,010, Binance Alpha 661 | exchange info endpoints |
| First trading day | Bithumb KRW 486 markets, Coinbase USD 492 products, Bybit spot 390, Binance spot 760 | daily candles |
| Turnover and closes | daily, Binance + OKX + Bybit spot, about 1,000 coins | daily candles |
| 1-minute bars | around each announcement | Binance, OKX, Bybit |

Notes. @CoinbaseAssets is silent; Coinbase now announces on @CoinbaseMarkets. Bithumb's notice API
returns only its latest five, so Bithumb listings are dated by their first candle. Gate keeps no
1-minute history that old.

## 1. What is visible before a listing, and how early

Precision = of coins showing the signal (not yet on the target), the share announced there within
14 days. Lift = precision over the base rate. Coverage = of the target's listings of coins with a
prior market, the share preceded by the signal within 14 days. Lead = median days from signal to
announcement (signals within 90 days). Full tables: `research.json`; every signal row: `signals.json`.

### Target: Upbit KRW (base rate 0.33% per coin per 14 days; 69 listings with a prior market)

| Signal | Signals | Hits | Precision | Lift | Coverage 14d | Lead (days) |
|---|---|---|---|---|---|---|
| Binance spot announcement | 14 | 4 | 28.6% | 87 | 6% | 12.6 |
| New Bybit spot market | 42 | 11 | 26.2% | 80 | 16% | 6.3 |
| Coinbase post (deposits or trading) | 24 | 5 | 20.8% | 64 | 9% | 6.0 |
| Coinbase trading starts | 75 | 15 | 20.0% | 61 | 23% | 6.7 |
| Upbit BTC/USDT market only | 8 | 1 | 12.5% | 38 | 1% | 18.9 |
| New Binance USD-M perp | 90 | 11 | 12.2% | 37 | 16% | 24.1 |
| Coinbase roadmap post | 45 | 4 | 8.9% | 27 | 7% | 19.3 |
| New OKX spot market | 137 | 8 | 5.8% | 18 | 12% | 5.7 |
| Binance Alpha listing | 272 | 14 | 5.1% | 16 | 20% | 6.8 |
| New OKX perp | 260 | 12 | 4.6% | 14 | 17% | 11.7 |
| Bithumb KRW listing | 48 | 2 | 4.2% | 13 | 3% | 38.5 |
| New Bybit perp | 344 | 12 | 3.5% | 11 | 17% | 13.9 |
| New Gate market | 617 | 11 | 1.8% | 5 | 14% | 11.7 |
| Volume surge (3-day turnover 3x the month) | 1,698 | 10 | 0.6% | 1.8 | 16% | 22.4 |
| Turnover rank jump (150+ places) | 1,121 | 5 | 0.4% | 1.4 | 9% | 23.1 |

Bithumb before Upbit, which I expected to be the strongest, is weak: Bithumb usually lists the same
day as Upbit or after it, not before. The reverse is not much better (Upbit KRW to Binance spot,
6.8%).

### Target: Binance spot (base rate 0.16%; 20 listings with a prior market)

Best: Coinbase roadmap post 9.8% (lift 61, lead 8 days), new Binance perp 7.5% (lift 47, covers 30%
within 14 days and 75% within 90), Upbit KRW listing 6.8% (lift 42). Binance lists perps first and
spot later for most coins it spot-lists, but most perps never get spot.

### Target: Coinbase (base rate 0.23%; 41 listings with a prior market)

Best: Binance spot announcement 14% (1 of 7), new Binance perp 8.8% (lift 38). Coinbase listings
mostly come from nowhere I can see.

### Size

No keyless market-cap history, so the stand-in is rank by 30-day turnover. Top 100 coins (not yet
on the venue) get Upbit KRW listings at 5x the base rate, ranks 101 to 300 at 2.3x, the long tail at
0.4x. Same shape for Binance and Coinbase.

### X chatter (xAI)

Five Upbit KRW listings against five coins of matching turnover rank that were not listed, posts
with the cashtag counted in the two weeks before the announcement (B) and the two weeks before that
(A). The model does the counting and caps near 50, so these are estimates.

| Listed | A | B | B/A | Control | A | B | B/A |
|---|---|---|---|---|---|---|---|
| ICP | 9 | 30+ | 3.3+ | OPN | 42+ | 38+ | 0.9 |
| CC | 38 | 45 | 1.2 | ZBT | 35 | 22 | 0.6 |
| CHIP | 2 | 15 | 7.5 | CHESS | 12 | 8 | 0.7 |
| BLEND | 42 | 48 | 1.1 | HAEDAL | 32 | 17 | 0.5 |
| PROS | 25+ | 35+ | 1.4 | RDNT | 45 | 48 | 1.1 |

The listed coin's chatter grew more in 5 of 5 pairs (a coin-flip would do that 1 time in 32).
Median growth 1.4x against 0.7x. Encouraging and thin: five pairs, model-estimated counts, and part
of the rise is the run-up to a token launch. Korean-language posts on X were a handful either way.
Nine pairs were planned; the $10 cap stopped it at five.

### Not measured

Token unlocks (no keyless history), Korean community sites (no keyless source tried tonight),
real market-cap bands (turnover rank used instead).

## 2. Selling two or three minutes after the announcement

`minute.py`, rules committed (10dff27) before the run. P-0107's 68 events re-measured on 1-minute
bars: 66 measured (2 had no minute bars). Holding price is the close of the last full minute before
the announcement. Each exit is the bar containing announcement + k minutes, never the announcement's
own minute. Pessimistic = that bar's low; typical = its close. 0.5% round trip off every exit.

| Exit | Upbit (58) median | Upbit share up | Upbit 25th pct | Binance (8) median |
|---|---|---|---|---|
| +1 min, pessimistic | +14.3% | 90% | +5.5% | +6.9% |
| +2 min, pessimistic | +16.5% | 91% | +6.7% | +5.8% |
| +3 min, pessimistic | **+15.8%** | 91% | +5.5% | **+6.0%** |
| +5 min, pessimistic | +16.8% | 91% | +4.7% | +6.1% |
| +10 min, pessimistic | +16.8% | 88% | +5.7% | +4.9% |
| +3 min, typical (close) | +18.6% | 91% | +7.4% | +7.5% |
| Highest high in 30 min (hindsight) | +32.7% | 100% | +17.5% | +14.5% |

The top of the first 30 minutes falls in the announcement's own minute in half the Upbit events,
and 69% of tops come within the first three minutes. The six that lost were all stablecoins (USDG,
PYUSD, RLUSD, XAUT, USDE), which no ranking would hold. Holding through the day before added a median +1.7%
(the coin usually drifts up slightly into the announcement; the mean is skewed by a few leaks).

Coinbase (`minute.py coinbase`, the first @CoinbaseMarkets post per asset): 16 measurable, median
+1.8% at +3 minutes pessimistic, 81% up. 47 had no prior market on Binance, OKX or Bybit; many are
Base-chain tokens.

## 3. Does holding a ranked list pay? (`backtest.py`)

Rules committed before the run (506bf49, then cd0861e dropped the two volume signals for lift
under 2). The score for a coin is the chance of any target listing in 14 days, combining its active
signals with probabilities fitted on the first half only (Oct to Mar). Hold the top N each day,
equal weight, sell into the pop at +3 minutes when a target announces, 0.25% a side on every list
change. Benchmarks: every coin in the universe equal weight, and 200 random lists of the same size
drawn from coins with any active signal.

| List | Half | List | Universe | Random median | Random beaten | Hits |
|---|---|---|---|---|---|---|
| Top 10 | Oct to Mar (fit, in-sample) | -42.3% | -62.5% | -57.2% | 92% | 20 |
| Top 10 | **Apr to Sep (out of sample)** | **+9.0%** | **+15.7%** | -42.7% | 99% | 9 |
| Top 25 | Apr to Sep | +6.7% | +15.7% | -26.6% | 100% | 12 |
| Top 50 | Apr to Sep | +4.1% | +15.7% | -5.5% | 98% | 12 |

Three columns, as Luke asked for them: **makes money**: out of sample yes (+9%), over the year no;
**beats holding**: no; **beats luck**: yes, clearly. The universe benchmark is noisy (equal weight
over about 800 small coins, rebalanced daily); I would not lean on its exact size.

Exploratory, written after the backtest and in-sample (`pertrade.py`): trading each strong signal
on its own, entry at the day's close, out at the pop or after 14 days. Coinbase trading launch: 36
trades, mean +21%, median -4%. Binance Alpha listing: 45 trades, mean +10%, median -4%. Every signal
has a negative median; the means are carried by a few big Upbit pops. A lottery ticket profile, and
survivorship flatters it (coins delisted since are missing from the price data).

## What would change the answer

- **A faster or earlier signal.** If X chatter really doubles before a listing (5 of 5 pairs), it is
  a better filter than "is new". That needs a cheaper way to count posts than $0.40 a coin.
- **Less time held.** Most of the loss is drift while waiting. Entering only in the days just before
  typical lead time, or only on the three strongest signals, cuts exposure; it also cuts hits.
- **Going short the losers is not available** (UK retail, no derivatives).

## Files

`collect.py` sources, `analysis.py` signal tables, `minute.py` the 1-minute study, `backtest.py`
the list backtest, `pertrade.py` the exploratory per-signal trades, `xmentions.py` and
`coinbase_x.py` the two xAI pieces (ledger `xai-calls.jsonl`, $9.95 of the $10), `score.py` and
`scorer.json` the live rule, `poller.py` the tracker.
