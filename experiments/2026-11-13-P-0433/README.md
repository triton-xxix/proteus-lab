# P-0433: "gaps fill 85% of the time", measured on our own daily bars

Trials, 13 Nov 2026. Deepen of P-0432, which found the win-rate selling sits on gap-fill videos, not
gap and go.

**The claim.** Nitro Trades, "85% Winrate Trading Strategy | Gap Fill Trading" (ieCrXvKLq3g), 17
seconds, 75 words. All of it: the strategy "has an 85% win rate"; when price drops and creates a gap
it comes back and fills it 85% of the time, same for the upside, "later on"; use it for price targets
only. No instrument, no timeframe, no horizon, no trade count, no stop.

**Shot.** works at 0.70: SPY same-day gap fill about 65% over all gaps; under 0.25% gaps fill 85% or
more, over 1% gaps 40% or less; fading every gap to the prior close makes a mean within 0.05% of
zero per trade, not distinguishable from luck.

**Rules, written before the run.** The source withholds everything but the 85%, so these are my
guesses, stated first:

- Data: daily OHLC already on disk in `sandbox/p0082/data/` (Yahoo, price only, unadjusted), the
  nine-ETF basket of P-0089: SPY QQQ DIA IWM EFA EEM EWU EWJ EWG. Whole history, and since 2009.
- Gap: today's open against yesterday's close, at least 0.05% either way. Buckets by size:
  0.05 to 0.25%, 0.25 to 0.5%, 0.5 to 1%, over 1%.
- Chart gap (what the Short draws): open above yesterday's high or below yesterday's low.
- Filled: price trades back to yesterday's close. Three horizons, because "later on" has none: the
  same day, within 5 trading days, within 20.
- The trade: fade at the open, target yesterday's close, out at the close if not filled. No stop
  (the source gives none). Cost 0.02% a round trip.
- Control one (no randomness): the mirror level. How often does price reach the same distance from
  the open in the other direction, away from yesterday's close? If that is hit about as often, the
  fill rate is volatility, not a pull towards the gap.
- Control two (luck): on the same gap days, a coin picks fade or follow (follow: target the mirror
  level, out at the close). 2,000 draws; p is the share of draws with a mean at least the fade's.
- Beside holding: the instrument's mean open-to-close on all days.

## Results (after the run)

`gapfill.py`, seeded, numbers in `results.json`. Bars end 6 Oct 2026.

| | gaps | fill same day | mirror same day | fill 5d | fill 20d | fade win | fade mean after cost | t | p v coin |
|---|---|---|---|---|---|---|---|---|---|
| SPY, 1993 on | 7,572 | 64.3% | 57.7% | 83.7% | 91.7% | 70.7% | +0.029% | 3.54 | 0.000 |
| SPY, 2009 on | 4,026 | 59.7% | 53.1% | 81.5% | 90.3% | 67.8% | +0.029% | 2.85 | 0.012 |
| nine ETFs, all | 59,416 | 51.2% | 47.7% | 77.9% | 88.9% | 64.1% | +0.005% | 1.44 | 0.000 |
| nine ETFs, 2009 on | 37,362 | 47.8% | 45.1% | 76.4% | 88.1% | 62.4% | -0.009% | -2.39 | 0.076 |

By gap size, nine ETFs, 2009 on (SPY all-history in brackets):

| gap | gaps | fill same day | mirror | fill 5d | fill 20d | fade mean |
|---|---|---|---|---|---|---|
| 0.05 to 0.25% | 10,317 | 79.5% (81.6%) | 76.8% | 92.4% | 96.5% | -0.008% |
| 0.25 to 0.5% | 9,505 | 55.2% (62.7%) | 51.7% | 82.9% | 91.5% | -0.006% |
| 0.5 to 1% | 10,099 | 32.1% (47.1%) | 30.5% | 70.2% | 85.5% | -0.019% |
| over 1% | 7,441 | 15.8% (35.2%) | 12.5% | 54.1% | 76.0% | +0.002% |
| chart gaps (beyond yesterday's range) | 19,700 | 32.5% (51.9%) | 29.5% | 67.7% | 83.6% | -0.003% |

Per symbol since 2009, fade mean after cost: SPY +0.029, IWM +0.010, EWG -0.002, EWJ -0.004,
EWU -0.004, EFA -0.014, QQQ -0.019, DIA -0.026, EEM -0.047 (percent a trade). Seven of nine negative.
The worst single fade in the pooled set lost 13.1%.

## Reading

- **85% is a horizon, not a rule.** No slice reaches 85% the same day. SPY gets to 83.7% in five
  days and 91.7% in twenty; the pooled basket needs twenty days to pass 85 (88.9%). Chart gaps, the
  kind the Short draws, fill 32.5% the same day and 83.6% in twenty. "Later on" does the work.
- **Most of the fill rate is just price moving.** The mirror level, the same distance the other way,
  is hit 45.1% of the time against 47.8% for the fill (pooled, 2009 on). The pull towards
  yesterday's close is about three points, not eighty-five.
- **A high win rate and no money.** Fading every gap wins 62% of the time across the basket and
  makes -0.009% a trade after a 0.02% cost since 2009, seven of nine symbols negative. Small gaps
  fill 80% of the time and lose, because the win is the size of the gap and the loss is the day.
- **SPY is the exception and I did not call it.** +0.029% a trade after cost, t 2.85 since 2009,
  p 0.012 against the coin. It is one symbol of nine, it rests on the over-1% bucket (+0.198% on 443
  gaps), and 0.029% is about one tick of slippage at the open. I would not trade it on this.
- Beside holding: SPY's open-to-close on all days since 2009 averages +0.025% a day, so the fade's
  +0.029% on gap days is no better than just being long the session.

## Against the shot

SPY same-day fill: called about 65%, measured 64.3%. Over 1%: called 40% or less, measured 35.2%.
Under 0.25%: called 85% or more, measured 81.6%, a miss by three points. Fade mean within 0.05% of
zero: yes (+0.029%). "Not distinguishable from luck": wrong on SPY (p 0.000), right on the basket
since 2009 (p 0.076). And I called the verdict works; by the luck-test rule it is not-worth-it.

## Caveats

- Price-only bars: an ex-dividend open counts as a small gap down. Not removed.
- The open and the target are assumed filled at the printed price. Real opens slip.
- No stop, because the source gives none; a stop would change every number here.
- Early Yahoo bars for the country ETFs are thin and some opens look stale; the 2009-on rows are the
  ones to read.
- Daily bars only. A gap "filled" on day one may have filled in the last minute.
- The 0.05% floor and the four buckets are my choices, made before the run and not swept.

## Not done

The neurotrader permutation of the retired skill: the coin control on the same days answers the same
question here more directly, and there was no time for both. No walk-forward, since no parameter was
searched. The SPY over-1% bucket on its own, with a stop and open slippage, is the only thread worth
pulling, and it is 443 trades in 17 years.

