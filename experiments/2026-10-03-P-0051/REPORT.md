# P-0051: scoring P-0049, the pump.fun poller v3

Scored 2026-10-03 from `experiments/2026-10-01-P-0049/` (24 h, 1 Oct 22:55 to 2 Oct 22:53 UTC,
stopped itself, DONE written, job unloaded). Scorer `sandbox/p0051/score.py`, raw `result.json` here.

## The job

- 469 polls. 460 of them hit at least one HTTP 429 (1,700 error lines), almost all on the `pools/multi`
  lookups, but the retry held: 25,014 of 25,165 launches (99.4%) got their minute-five snapshot, 37
  `missed`, 114 never reached. So coverage is measured now and it is good.
- The last page was entirely new on 69 polls, so six pages still lose some launches in bursts.

## The numbers

| Measure | Value |
|---|---|
| Pools first seen | 35,083 |
| pump.fun launches (tokens) | 25,165 |
| pumpswap pools | 2,446 |
| Graduations matched by token address | 574 |
| Graduation rate by token | 2.28% |
| pumpswap pools whose launch I never saw | 1,872 |
| Graduates within 7 minutes of launch | 472 (82%) |
| Median launch-to-graduation | 0 min (same poll) |

25,165 launches in a day against P-0014's 7,326 seen and ~14,000 estimated: the floor moved again.
2.28% by token against P-0033's 0.65% name-matched floor. Still a floor, because 1,872 pumpswap pools
belong to launches outside what I saw.

## The minute-five screen, with the leak taken out

The naive profile says graduates look nothing like the rest at minute five, but most graduates had
already graduated by then (median reserve 0, the curve emptied). That is leakage. Taking only launches
still on the curve at minute five and graduating later (102 tokens), the base rate is 0.42%.

| Buyers in first 5 min | Picked | Late graduates | Precision | Recall |
|---|---|---|---|---|
| 5+ | 5,310 | 79 | 1.5% | 78% |
| 20+ | 1,754 | 54 | 3.1% | 53% |
| 50+ | 775 | 36 | 4.7% | 35% |

## What it says

Four in five graduations happen inside seven minutes, mostly in the same two-minute poll as the launch:
bought straight out of the curve, which a two-minute poller cannot act on. For the slow fifth, a buyer
count at minute five lifts the odds about elevenfold over base, from 0.4% to 4.7%, which is still
nineteen in twenty picks that never graduate. Graduation is not profit either; the graduation book's
KILL already says what buying graduates does.

Verdict: works, as a measurement. Not a strategy.
