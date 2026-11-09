# D-019 and D-021 read: four edge rules, forward week of 2 to 6 Nov (9 Nov 2026)

Smith, 20:20 on 9 Nov 2026, on the backstop. The scan ran on 7 Nov as registered; nobody read its W1
rows until now.

**Measured, verbatim from `edges/scan/2026-11-07/results.json`, W1, after costs:**

| id | rule | n | W1 total | mean a trade | control mean | pass line |
|---|---|---|---|---|---|---|
| E-013 | VWAP cross after 11:00, hold to close | 53 | +19.877% | +0.375% | -0.022% | PASS |
| E-014 | ORB 15m fade (failed break) | 55 | +7.495% | +0.1363% | -0.0289% | PASS |
| E-015 | ORB NY open 30m, target 1R (crypto) | 42 | -6.996% | -0.1666% | -0.1148% | FAIL |
| E-016 | Opening drive: first bar direction to 11:00 | 60 | +0.866% | +0.0144% | -0.0217% | PASS |

**Line**, from both FORWARD.md files as written: "week total after 0.03% costs above zero AND above its
random-entry control mean" (0.12% for E-015).

## The window the stock rows really cover

FORWARD.md said W1 "holds exactly the sessions 2 to 6 Nov". It does not. `sessions.py` shows W1 was 30
Oct, 2, 3, 4 and 6 Nov. Yahoo's 5 Nov has 59 usable bars of 78 for all 12 names (the other 19 carry
nulls, still so today), under `prepare()`'s 70-bar floor for a broken day, so the 5-session block
reached back to 30 Oct, the day FORWARD.md deliberately left out as already half seen.

The crypto W1 is the seven UTC days 31 Oct to 6 Nov as registered, so E-015's FAIL stands untouched.

So I ran the three stock rules on the sessions that were registered, with `scan.py`'s own functions
(`rescore.py`, `rescore.json`). These are a check on the registered figure and not a replacement:

| id | A: 2, 3, 4, 6 Nov | B: 2 to 6 Nov, 5 Nov let in on 59 bars | passes in both |
|---|---|---|---|
| E-013 | +25.94%, n 42, control -0.035% a trade | +16.30%, n 47 | yes |
| E-014 | +8.58%, n 45, control -0.034% | +6.77%, n 48 | yes |
| E-016 | +6.71%, n 48, control -0.031% | +48.03%, n 60 | yes |

**Verdict: E-013 PASS, E-014 PASS, E-016 PASS, E-015 FAIL.** The pass line is met on the scorer's W1 and
on both readings of the registered week, so no reading changes a word.

## Said plainly

- A pass here earns a second forward week and nothing else.
- **E-013 is one day.** 2 Nov made +23.00% of the +25.94% in A; the other three sessions made +2.94%
  together. Also, its name says "after 11:00" and the code starts at bar 12, which is 10:30. The rule as
  tested is the code; the name is wrong.
- **E-016's B figure is not to be believed.** 5 Nov's +41.32% is a rule that holds for a count of bars
  (17) on a day with 19 bars gone, so it exits well after 11:00. A is the fair reading, and the 7 Nov W1
  said +0.87%, so its size moves a lot with the choice of days.
- **E-014 won 25% of its trades** and passes on a few big ones, as it has every week it climbed.
- **Multiple comparisons:** this desk puts rules forward because they climbed a ladder of 61, against
  about 7.6 by luck. Three of four passing one week is encouraging and small.

## Also found, no effect on these numbers

`yahoo_5m` applies today's single `gmtoffset` to every bar, so since the 1 Nov clock change every bar
before it is labelled an hour early (`sessions.py`: first bar 08:30). No stock rule reads the clock: they
count bars from the open, and `bar_at` is only used for crypto starts in UTC. Dates are unaffected. It
would bite the first rule that reads a stock's clock time, so it is written down here and left.

## Next

Second forward week: `edges/scan/2026-11-09/FORWARD.md`, DUE D-025. E-015 gets none.
