# P-0158: the pairs laggard, out of sample, with a day-block shuffle

Question (deepen of P-0153): do P-0153's frozen rules still beat random holds of the same coin on the
90 days before its window, and does its in-sample p survive a shuffle that keeps overlapping trades
together?

Method: `pairs_oos.py`, the P-0153 rules copied unchanged. Out-of-sample window 18 Apr to 16 Jul 2026
(the 90 days ending the hour before P-0153's window), trading 18 May to 16 Jul. The in-sample window
re-run as a check. Two benchmarks of 2000 books: P-0153's per-trade random re-entry, and a day-block
shuffle (every trade entered on one day moved by the same random whole-day offset, hour kept). The pass
line was written in the docstring first: edge >= 0.3 pp and day-block p < 0.10.

Called shot: not-worth-it at 0.70, expecting the edge within 0.3 pp of random and day-block p above 0.2.

## Numbers (`results.json`)

| | out of sample | in sample re-check |
|---|---|---|
| pairs at corr >= 0.70 | 52 | 11 |
| trades | 735 | 144 |
| mean trade | -0.97% | +1.49% |
| random holds, same coins | -0.83% | +0.72% |
| edge | -0.14 pp | +0.78 pp |
| p, per-trade shuffle | 0.83 | 0.036 |
| p, day-block shuffle | 0.61 | 0.12 |
| win rate | 41% | 53% |

- Out of sample the rule loses to random entries on the same coins. It does not beat luck.
- The in-sample re-check reproduces P-0153 to the trade (144, +1.49%), so the code matches. The
  day-block shuffle's spread is 1.7 times the per-trade one there, and p moves from 0.036 to 0.12:
  the "nearly significant" in-sample result was mostly overlapping trades counted as independent.
- Out of sample 52 of 66 pairs passed the 0.70 correlation gate (a falling market where everything
  moved together), so the gate selected almost nothing. That is a weakness of the rule, not the data.

## Not done

No short leg, no cointegration test, no third window, no slippage beyond the 0.2% fee. None is worth
doing: the long-only laggard has one good 60-day window out of two and no edge once overlap is
respected.

Verdict: not-worth-it. Close.
