# Lookahead audit, 13 Oct 2026

Interactive, on Luke's word ("do it"), after this afternoon's Workshop. The first draft of the luck
test's moving-average rule used each close's signal from that same bar's open. That turned a fail
(p 0.07) into a pass (p 0.03). A comparison caught it; reading the code had not. So the question
was whether the same kind of bug sits under anything already scored in public.

## Systems books (P-0082, P-0083, P-0091): clean

`audit.py` replays every vectorised backtest behind the two live books with a separate bar-by-bar
stepper. At each open it fills orders placed at an earlier close. At each close it decides using
indicator values at index t or earlier. RSI(5) and SMA(200) were also recomputed on the series cut
at 60 random bars per market, and none changed (worst difference 0).

| | Result |
|---|---|
| Checks (9 markets x 7 rule and fill combinations) | **63 of 63 match trade for trade**: same entry bar, exit bar and return |
| Trades compared | 12,876 (fewest in one check: 53) |
| Indicator causality, worst absolute difference | 0 |
| luck_test.py `sma` rule against the stepper, SPY | matches (total log return 2.51897 both) |
| Positive control: the bugged first draft | **flagged** (4.97978 against 2.51897) |

The control matters: a harness that cannot catch the known bug would make 63 matches meaningless.

What this covers: P-0082's RSI(5) close fills and 200-day filter, P-0083's RSI(5) next-open fills
(book 1), and P-0091's `books()` for both book 1 and gated IBS (book 2), run on each market's own
dates. The live `systems.py` was read, not stepped: it already logs each signal before the next open,
and on 7 Oct it was replayed against these backtests (P-0083, P-0091 READMEs).

## Grinder replay and R01 backfill: read, no lookahead found

- `grinder/harness/replay.py`: candles start at the first full minute after the snapshot. Within a
  candle, the stop is checked before the take-profit (pessimistic). The trailing level uses the high
  of earlier candles only, and delayed entries take the open of the first candle at or after the
  delay. Gates and the volume ranking use snapshot columns only.
- `experiments/2026-10-13-P-0139/backfill.py` calls `telegram_counts()` today for picks on 8 to 11
  Oct, which looked like a leak. It is not: `mentions.py` counts only posts in the 24 hours before
  each snapshot (`after <= t < before`, before = the snapshot time), keyed by (mint, night). The
  other R01 markers (`rug_risks`, `chg_h1`) are snapshot columns. Residual: a Telegram post deleted
  after the night and before the pull would be missed; that is not lookahead.
- Not lookahead, and already known: the Grinder enters at the snapshot price at a later time (fill
  realism, D-009).

## A correction to my own advice

At 17:10 I told Luke the IBS book had never been luck-tested. It had: P-0091, pooled p = 0.044, and
the result is in `systems/RULES.md`. I said it without checking.

## Reproduce

```
/Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 experiments/2026-10-13-lookahead-audit/audit.py
```

Writes `result.json` here. Data: `sandbox/p0082/data/`, as traded (not dividend-adjusted) for the
backtests, adjusted for the luck_test.py check, as each was published.
