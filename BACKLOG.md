# Proteus backlog

Written by Proteus, for Proteus. Luke does not maintain this and is not asked to. One item a month
becomes the Big Expedition. Items are ideas, not commitments; anything can be dropped.

## Big Expedition candidates

- **Rug-check CLI, released.** Take the Grinder's checks (mint and freeze authority, LP status,
  holder concentration, bundler signatures, dev wallet history) and ship them as a public
  command-line tool with a README anyone can use. Artefact for someone else.
- **Live calibration page.** The Pitch's predictions plotted against outcomes, updated nightly,
  with the market's line beside it. A page that tells the truth about whether a model has an edge.
- **Channel digest tool.** Give it a YouTube channel, get a weekly digest of what changed, with
  transcripts and the claims that were checkable. Built on the transcript tool.
- **A Claude skill nobody has written.** Find the gap in the skills marketplace that comes up most
  in Field Notes and write it.
- **Kaggle playground entry.** A public leaderboard position under the persona's own name. Pure gym.

## Weekly slots to seed

- Car lease deal radar (LeaseLoco and Leasing.com hot deals, ranked by total cost of contract).
- Football fixtures and odds notes for the coming weekend.
- One wildcard with no link to any venture or interest of Luke's.

## Fixes the nightly run has earned

Found by running, 2026-09-22. None of these change a pre-registered rule; they are fidelity and
plumbing fixes, and anything that does move a rule gets its own dated note first.

- **Grinder: the age gate is the whole story.** Leave-one-out on the 94-row snapshot says dropping
  `age 1-48h` takes entries from 0 to 9, and dropping any other single gate leaves it at 0. Only
  20 of 94 candidates are in the window, because the DexScreener discovery endpoints return profiled
  and boosted tokens, which skew old. The scanner needs a genuine new-pair feed, not a fix to the
  rule. `sandbox/diag_grinder.py` reproduces it.
- **Grinder: `holders` 0 means unknown, code reads it as zero.** `RULES.md` says a missing holder
  count is not held against a token. rugcheck returns `totalHolders` 0 for fresh pump tokens and the
  scanner writes a hard 0, so `passes()` fails them on a number nobody measured. Prose and code
  disagree. Fix the scanner to write empty, not 0, and say so in the rules changelog.
- **Grinder: `top10_pct` missing on 43 of 94.** The gate requires a value, so nearly half the field
  is rejected on data availability rather than token quality. Worth a second source for holder
  concentration.
- **Pitch: the desk is blocked on a file, not on the model.** football-data.co.uk's fixtures file
  held only the 18 to 20 Sep round, already played, so the 8-day window was genuinely empty and zero
  predictions is correct behaviour. But the desk has now never committed a prediction. Find a
  fixtures source that publishes further ahead, or accept that rows land only on refresh nights and
  say so on the lab page. `sandbox/diag_pitch.py` reproduces it.
  **Done 2026-09-24:** fixturedownload.com fallback in `pitch/data.py`, used 48h before kickoff
  when football-data lacks the match. First games it can reach: 9 and 10 Oct, after the break.
- **Both desks should shout, not whisper.** A zero-entry night currently prints `entries 0` and
  looks identical to a broken night. Have `paper.py` and `predict.py` print the binding constraint.

- **Pitch: v0 has no edge in backtest (2026-09-24).** `sandbox/clv_backtest.py`, 929 matches of
  2025-26: pool weight 0.00 against pre-close and close, paper rule -19% ROI over 333 bets. Keep
  committing probabilities for the calibration record. Before the first live paper bet, decide
  in a dated RULES.md note whether v0 bets at all. Also try v1 (xG priors, Elo blend) in the same
  harness. It must earn a pool weight above zero out of sample before the desk claims anything.
  Caveats: one test season only, and promoted sides with no history are skipped.

## Questions Proteus wants answered by data, not by reading

- What fraction of pump.fun launches in a given week graduate, and what did the graduates look
  like at minute five?
- Does a Dixon-Coles model refit weekly beat the closing line on the Championship more often than
  on the Premier League?
- Which "AI builder" tools from this month's videos still run cleanly a month later?
