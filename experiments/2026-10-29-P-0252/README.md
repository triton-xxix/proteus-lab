# P-0252: does the RSI(5) book pay in VIX backwardation?

**Question.** Split the systems book's RSI(5) simple rule by VIX/VIX3M on the signal day (backwardation,
ratio at or above 1, is the stress state) and test each side against the P-0243 random-entry control.

**Rules** (unchanged from P-0243 and the book): close above its 200-day average and RSI(5) Wilder under 30
at the close; buy the next open; exit at the next open after RSI(5) closes above 50. Nine ETFs, 2009 on,
total-return scaled Yahoo OHLC from `sandbox/p0082/data`, no costs. VIX: FRED VIXCLS; VIX3M: FRED VXVCLS
(keyless, pulled 29 Oct 2026, from 2007-12-04, copied to `sandbox/fred/VXVCLS.csv`). Cut at 1, fixed in
the probe title before the run.

**Called shot.** works at 0.80, "backwardation under 10% of the 966 trades (about 70), its excess not
significant". Count missed: 164 trades (17%). Significance half hit, and harder than expected: the
excess is negative.

**Control.** Random signal days from the same symbol and bucket, 200-day filter, next-open entry, hold
drawn from that bucket's real trades, exit at an open. 2000 draws.

**Numbers.** Backwardation on 8.0% of days since 2009 (360 of 4481), but on 17% of signal days: the rule's
dips cluster there.

| VIX/VIX3M on signal day | trades | mean | win | control | excess | p |
|---|---|---|---|---|---|---|
| under 1 (contango) | 802 | +0.73% | 77% | +0.18% | +0.55% | 0.000 |
| 1 and over (backwardation) | 164 | +0.29% | 68% | +0.86% | -0.57% | 0.964 |

Pooled 966, as P-0243.

**Reading.** In backwardation a random long on a filtered day earns +0.86% over about six days, and the
RSI(5) entry earns a third of that. The whole edge of the book sits in contango. This sharpens P-0243's
"not when VIX is low": the tercile view hid that the stress days are where the signal is worst relative
to luck, because the luck there is so generous.

**What I did not do.** No costs (backwardation's +0.29% would lose about a third to a 0.1% round trip). No
out-of-sample halves and no count by year: backwardation comes in episodes, so a few of them may carry
the 164 trades (not measured). The control pool in backwardation is only 1110 symbol-days, about 120 distinct dates across
nine correlated ETFs, so its +0.86% is itself noisy. No skip rule tested as a live book.
