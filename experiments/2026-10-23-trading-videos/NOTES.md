# Trading videos for the edge desk (23 Oct 2026)

Luke asked to "watch a couple vids on trading and day trading to see if we can line up any extra
strategy". Three videos, found with `sandbox/yt_search.py`, transcribed keyless through
`sandbox/skool_transcript.py` (YouTube captions, no whisper needed). Transcripts are in
`transcripts/` (local only, gitignored course-style text; commit this note, not them).

Nothing here was backtested. Claims are noted so the parent can check them.

## The videos

| # | Title | Channel | URL | Length | Age | Views | Transcript |
|---|---|---|---|---|---|---|---|
| V1 | I Backtested 1,178,668 Opening Range Breakout Trades. Here's the Data. | TOS Indicators | https://www.youtube.com/watch?v=MOG-DbgmzzI | 9:25 | about 7 mo (Mar 2026) | 36k | complete, captions, 1,695 words, last stamp 8:54 (about 180 wpm) |
| V2 | The ONLY Day Trading Strategy I'll use ALL 2026 (Backtested 1000 Times) | Trade with Pat | https://www.youtube.com/watch?v=E3McKlAp3qk | 12:19 | about 8 mo | 139k | complete, captions, 2,346 words, last stamp 11:47 (about 190 wpm) |
| V3 | Mean Reversion Trading Strategy Explained & Backtested (179% Profit) | Quant Tactics | https://www.youtube.com/watch?v=c9-SIpy3dEw | 8:01 | about 1 yr (2025) | 44k | complete, captions, 1,195 words, last stamp 7:24 (about 150 wpm) |

V2 and V3 are older than "last month" but within 2025-2026. Search ages are YouTube's relative
ages, not exact dates.

## Rules pulled out

### V1: ORB timeframe and target/stop study (TOS Indicators, a vendor selling a backtester)

Mechanical content is thin: it is a summary of results, but the rule is fully definable.

- Instrument: single US stocks (600 symbols, about 300 trading days, 1-minute candles).
- Trigger: opening range = high and low of the first N minutes after 09:30 ET, N in {5, 15, 30}.
- Entry: break of the range high (long) or low (short). Fill details not stated; assume first 1-min
  or 5-min close beyond the range, next bar open.
- Target and stop, as multiples of range width: (a) half-range target, full-range stop; (b) full
  target, half stop; (c) full target, full stop.
- Exit: target, stop, or end of day (3% of 5-min trades and 13% of 30-min trades still open at the
  close).

Claims to check, not believed: 5-min win rate 53.78%, 15-min 50.97%, 30-min 49.38%. 5-min with
half target and full stop: about 69% win. Full target and half stop: 39%. 15-min full/full: 46%
win but the best expectancy, about +4.4 cents a trade. TSLA 57% win on 5-min and best name; META
56% on 5-min but 37% on 15-min; SPY and QQQ about 50% everywhere ("no edge"). Shorts win slightly
more (54% v 53%), longs make about twice the profit a trade. The presenter flags the long/short split
is a 30-day window. Win rate is not profit: a 69% winner with half target, full stop needs a
payoff check. Costs are not mentioned anywhere.

### V2: "Displacement ORB" plus session analysis (Trade with Pat, sells a VIP room and a robot)

About half is discretionary (fair value gaps, order blocks, engulfing candles, "big candles").
The parts a script can fill:

- Step 1, range: first 15-minute candle of the NY cash open (09:30 to 09:45 ET) high and low.
- Step 1, trigger: on 5-min bars, a candle that CLOSES beyond the range (a wick does not count).
  The "big impulsive candles" requirement is not defined; leave out or use a body size filter
  fixed in advance.
- Step 1, entry: pullback to the demand zone (the last opposite-colour candle before the push)
  then enter, usually on the candle that closes back up (engulfing is "rare", often just enters when
  the zone holds). Not cleanly mechanical; a fallback is entry on the 5-min close beyond range.
- Stop: below the demand zone, or the range midline. Target: 1.5R to 1.6R, or about 2% to 2.2% on
  a strong day, or the Asian session high or low.
- Step 2, session filter: Asia ranges, London pushes, New York reverses. If London session is
  bearish, take only longs in New York, and vice versa. Skip (expect continuation) when London
  swept BOTH the Asian high and the Asian low.
- Sessions in UTC (not stated precisely; define before running): Asia about 00:00 to 07:00, London
  about 07:00 to 12:00 or 13:30, NY cash open 14:30 UTC (13:30 UTC in the US/UK gap weeks).
- Instruments shown: looks like index futures/CFD charts (the "2%" target hints at crypto or
  stock). Not stated.

Claim to check, not believed: 79.45% win rate over 1,000 backtested trades, with unknown rules.
Results from "community" prop-firm passes are unverifiable.

### V3: Bollinger, 4h RSI trend filter and ADX, crypto perps 1h (Quant Tactics, Freqtrade)

Fully mechanical, the cleanest of the three.

- Instrument: crypto perpetual futures, 1-hour bars (pairs not named; "near perpetual futures").
- Long entry, all true on the signal candle close: 4h RSI(14) above 55 (the RSI period is not
  stated, 14 assumed); ADX above 20 on 1h and above 25 on 4h; 1h close below the lower Bollinger
  band (default 20, 2.0). Enter at the next candle (open).
- Short: mirror (4h RSI below 45, same ADX, close above upper band).
- Exit long: 1h close above the upper band. Short: close below the lower band.
- Stop: below the signal candle low, further reduced by 4.5 x ATR from the signal close (the
  wording is ambiguous; read as stop = min(signal low, close - 4.5 x ATR(14))). Shorts mirror.
- Note the exit (upper band) makes holds long, perhaps days, so event count is low.
- The parameters shown (BB period/width, RSI and ADX thresholds, ATR multiple) were hyper-optimised
  on 8 months, tested on 4 months out of sample, so the numbers above are the defaults the video
  describes; the tuned values are behind a paywall.

Claims to check: +179% in one year, market -66%, max drawdown 19.3%, no trade count, fee model or
leverage given.

## Overlap check: new or already covered

| Rule | Status |
|---|---|
| RSI(5) dip, IBS, Williams %R, stochastic, 3 lower closes | Not in these videos. Already covered by the systems book and P-0085 (daily bars). V3's "buy the dip below the lower band in an uptrend" is the same family idea but on 1h crypto, with a 4h trend filter: new instrument and timeframe, and the dip-buying family collapsed into RSI(5) on daily ETFs (P-0085), so expect overlap of idea, not of data. |
| Opening range breakout (any form) | NEW to the desk. TRADING-IDEAS.md C-01 and C-02 list it as "needs intraday data" and it was never run. grep of experiments/, systems/, grinder/ and state/probes.json found no ORB probe. Not in REGISTER.csv (E-001 to E-007). |
| London push then NY reversal session filter | NEW. Not found anywhere. E-005 is BTC range expansion after US releases, which is a different trigger. |
| Bollinger lower band + ADX + 4h RSI long, crypto 1h | NEW. No Bollinger, ADX or hourly-crypto probe in probes.json or experiments/. Overlaps conceptually with E-006 only in using Binance data. |
| VWAP, gap fill | Not in these three videos (V-searches turned up VWAP videos from 2024 or older; not used). Davey's ES VWAP system is already in TRADING-IDEAS.md B-21 as needing intraday data. |

## Ranked shortlist for the edge desk

All three are keyless. Yahoo intraday history limits: 5-minute bars about 60 days, 1-hour about 730
days, both through the chart endpoint. Binance klines are free with deep history.

### 1. Five-minute ORB on liquid single stocks, fixed 1R/1R (from V1)

- Rule to freeze before running: range = first 5-min bar (09:30 to 09:35 ET) high/low; enter on the
  first 5-min close beyond the range, fill at the next bar's open; stop at the opposite side of the
  range, target one range width away; flat at 15:55 ET if neither hit; one trade a day per
  symbol; symbols fixed in advance (TSLA, META, NVDA, AMD, AAPL, AMZN, plus SPY and QQQ as the
  claimed no-edge control). Do not use the 69% half-target variant as the headline (win rate is the
  trap); report 0.5R/1R and 1R/1R both but pre-register 1R/1R.
- Admission test: daily-triggering, so the last 21 sessions. N events about 21 per symbol, about
  100 to 150 pooled over the basket. Data: Yahoo 5-min bars (60 days), keyless. Control: random
  same-day entry times with the same stop and target and hold, 200+ draws per symbol, costs about
  0.05% round trip assumed plus a slippage line. The 60-day cap also allows a second, earlier
  window for a split.
- Reason: it is the most testable claim (a presenter-sold backtester says 5-min wins most often and
  that TSLA and META carry it), it is cheap, and the desk has never touched intraday stocks.

### 2. Crypto 1h Bollinger/ADX/4h-RSI dip-buy and rally-fade (from V3)

- Rule: as described above, run long and short separately; basket of Binance USDT perps fixed in
  advance (BTC, ETH, SOL, BNB, XRP, DOGE, ADA, AVAX, LINK, LTC). Fill at next 1h open, taker fee
  0.05% a side plus funding.
- Admission test: event-driven, so the most recent 8 to 12 closed trades across the basket,
  stating how far back that reaches (probably 3 to 6 weeks; the ADX gates make events rare). Data:
  Binance klines 1h and 4h, keyless. Control: same instrument, same hold time, random entries over
  the same window, 200+ draws.
- Reason: fully mechanical and the video claims it was tuned on 8 months then tested out of sample,
  so a short recent window is a fair, cheap check of whether defaults still work now.

### 3. Fade the London move at the NY open, 15-min ORB filter (from V2)

- Rule: define London direction = close at 13:30 UTC minus open at 07:00 UTC on a fixed instrument
  (BTCUSDT and/or NQ=F; both keyless); skip the day if London swept both the Asian high and low
  (Asia 00:00 to 07:00 UTC). At NY open take the 15-min ORB break only in the direction opposite
  to London; stop at the range midline, target 1.5R; flat at NY close. All fair value gap and
  demand-zone logic dropped as not mechanical, so this is a test of the session filter, not of
  Pat's full method.
- Admission test: daily-triggering on filtered days only. Last 21 weekdays gives maybe 8 to 12
  events, which is enough per the "most recent N events" rule. Data: Binance 5-min klines (BTC) or
  Yahoo 5-min NQ=F; keyless. Control: same direction-free random 15-minute entries in the same
  NY window with the same stop and target.
- Reason: the "London pushes, NY reverses" claim is a cheap, testable one; the 79.45% win rate is
  unverifiable and the rule is weakest of the three because most of the video's edge is discretionary.

## Blockers and notes

- No blocks. YouTube captions worked on all three, no whisper, no IP block.
- Titles here are mostly sales funnels (a backtester, a VIP room and robot, a Freqtrade file).
  Only the mechanical rules above are taken from them.
- I did not find recent VWAP or gap-fill videos with concrete rules; the VWAP results were 2024 or
  older, so none was transcribed.
- The ORB in V1 depends on an intraday trade fill rule the video never states (first close beyond or
  first touch). Whoever codes it must write that down before looking at data.
