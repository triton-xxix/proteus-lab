# P-0211: noise-area momentum with the paper's VWAP trailing stop, and a fills lesson

Trials, 24 Oct 2026. Deepen of P-0210 (same entry, the exit the paper reports its numbers on).

## Question

P-0210's raw-band trailing stop whipsawed (16% wins). Does the paper's VWAP trailing stop turn the
noise-area entry into something that climbs the edges/scan ladder?

## Method

`noise_area_vwap.py` imports P-0210's band builder and scan.py's pull, fills, costs, blocks and
random-entry control. Exit when a bar's low (long) or high (short) reaches the day's VWAP. Two fills,
run side by side on the same trades:

- **level**: fill at that bar's VWAP, as a stop would. That VWAP is computed with the bar's own
  typical price and volume, so it is known only at the bar's close and can sit outside the bar's
  range. A look-ahead.
- **close**: fill at the close of the bar that touched VWAP, the way scan.py's own VWAP rules exit
  (`until -> c[j]`). No look-ahead.

## Numbers

| fill | W1 trades | W1 net | win % | W1 p | W2 net | W3 net | rungs | pooled W1 to W3 | pooled p |
|---|---|---|---|---|---|---|---|---|---|
| level (look-ahead) | 191 | **+15.08%** | 49.2 | 0.01 | +20.41% | +7.24% | **3** | +42.73% | 0.00 |
| close (honest) | 191 | **-7.71%** | 30.9 | 0.59 | +7.17% | +3.64% | **0** | +3.09% | 0.15 |

- The look-ahead fill landed outside the exit bar's range on **317 of 1442** stop exits (22%). Those
  are prices that never traded. Same 498 trades over W1 to W3, +42.7% with the bad fill, +3.1%
  without it.
- SPY W1 (honest): -1.78%. NFLX is the tell: +18.0% over 102 trades with the bad fill, -4.3% without.
- Called shot: W1 below zero, better than P-0210's -8.97%, win rate above 30%, rungs 0. Measured
  -7.71%, 30.9%, 0 rungs. All four held. The first run (level fill, before the check) would have
  scored the shot a miss on three of four; the check is what made it right.

## What it means

The paper's headline version does not climb the ladder either: a losing W1, a positive W2 and W3
that do not beat the control, pooled p 0.15. Together with P-0210 the noise-area family is not a
candidate for the forward week. Closed.

The bigger lesson is about fills. A stop whose level is computed from the bar it fires in is a
look-ahead, and it turned a losing rule into a 3-rung survivor with p 0.00. scan.py's own VWAP rules
already exit at the bar's close, so the ladder is not affected; any new rule with a path-dependent
stop (VWAP, a moving average, a band that updates each bar) must fill at the bar's close or at the
previous bar's level. Written here so the next scan rule does not repeat it.

## Not done

- Previous-bar VWAP as the stop level (a legitimate middle fill) not run; the honest version is
  bounded by the two above and neither climbs.
- Crypto set not run. Not added to scan.py.
