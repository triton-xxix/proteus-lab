# Pass marks: the standard Proteus is judged against

Written 2026-09-24 by Proteus, two days after the charter was signed and before any paper position
or prediction existed. The charter says the week-8 review is keep, change or kill per desk on the
published numbers. It never said which numbers are good enough, which would have made the review a
vibe check on the one project built to stop those. This file is the pre-registered pass mark. The
commit timestamp is the proof that it was written with nothing to protect.

`bin/review.py` computes every numeric line below from the committed ledgers and prints the
verdicts. The eighth Field Notes carries that output verbatim. The verdicts are dictated by this
file, not discussed. Luke may overrule any verdict in one word; the overrule and his reason go in
the next Field Notes. Proteus does not ask, does not chase, and does not open a decision item.

## Changing this file

- A line may be tightened at any time, with a dated entry in the log at the bottom.
- A line may be loosened only while no row that it would judge exists. Once data exists, loosening
  a line is the same as failing it: the desk takes the verdict the old line gives.
- The constants at the top of `bin/review.py` must match this file. A change to one is a change to
  both, in the same commit.

## Dates

| What | When |
|---|---|
| Charter signed | Tue 22 Sep 2026 |
| Field Notes Sundays counted | W39 (27 Sep) to W46 (15 Nov 2026), eight of them |
| Week-8 review | The Field Notes of Sun 15 Nov 2026 |
| Second and last date for a desk that was inconclusive at week 8 | Sun 13 Dec 2026 |
| The Pitch edge test | 500 scored matches, or 31 May 2027, whichever comes first |

## Verdicts and what they do

- **KEEP**: the desk continues under the same rules. Next review eight weeks later, same file.
- **CHANGE**: one named fix, written as a dated note in the desk's `RULES.md` on the day of the
  review, and nothing else changes on that desk until the second date. A desk under CHANGE gets no
  new features. At the second date it is KEEP or KILL, never CHANGE again.
- **KILL**: the desk's steps come out of the nightly and weekly runs, the ledger is frozen and
  stays published in the same place, and the finding is written up in the next Field Notes with
  the numbers. Kill is not failure of the project. A desk was built to answer a question, and a
  clear no is an answer.
- **INCONCLUSIVE**: the sample floor was not met by the date. See "Inconclusive" below. It never
  rolls over silently.

## Rule changes and the clock

A plumbing fix (a feed, a fixtures source, a bug where code disagreed with the written rule) does
not touch the clock. A rule change (entry, exit, sizing, fee model, model version, edge threshold)
resets the sample for that desk: rows under the old rules stay published and are judged under their
own version, and do not count toward the new version's pass mark. `rule_version` in the ledger is
what `review.py` reads. A desk that changes its rules in week six has a week-six clock, and that is
the honest price of changing rules. The rules changelog note says which kind of change it is on the
day, not in hindsight.

## The Grinder

Question under test: pump.fun is a meat grinder for the people using it. The desk's product is the
answer, either way. A closed position is a ledger row with `pnl_gbp` filled, after the fees in
`grinder/RULES.md`.

| Criterion | Line |
|---|---|
| Sample floor for any verdict | 40 closed positions under one rule version |
| Sample after which INCONCLUSIVE is no longer available | 100 closed positions |
| KEEP | Expectancy at least +10% of the stake per position after costs (£0.50 at v0.1's £5, £10 at v0.2's £100), still at or above zero with the single best position removed, and at most 10% of positions logged as rugs |
| KILL | Expectancy at or below -10% of the stake per position at 40 or more positions; or anything below +10% at 100 or more positions |
| INCONCLUSIVE | Under 40 positions, or between the lines under 100 positions, or a KEEP condition missed under 100 positions |

The lines are stated as a share of the stake from 2026-09-25, when the stake moved from £5 to £100
(`grinder/RULES.md`, v0.2). At £5 they are the same numbers as before to the penny. Only rows under
the current rule version (`grinder/BOOKS.json`, `current`) are judged; each earlier version's rows
stay published as their own book and are judged under their own stake.

A KILL here means the hypothesis is confirmed for this rule set. The paper book closes, the
result is published, and the scanner and its snapshots are free to become the rug-check CLI in the
backlog, which is a different artefact with a different purpose, not a reason to keep the book open.

**Executor bar** (the charter's "if the record earns it"): 200 closed positions under one unchanged
rule version, expectancy at least +20% of stake after costs, at least +10% of stake with the best
three positions removed, positive expectancy in each half of the sample, rug rate at most 5%, and
at least 20 of those positions filled at prices from a live quote at entry and exit, not the
nightly snapshot price. Nothing below this line gets an executor written.

**Why the stake moved, 2026-09-25, written before any v0.2 row.** Under v0.1's fee model a £5
position paid $3 flat plus 1% each way, about 46% round trip. A clean take-profit netted about
+£2.54 and a clean stop about -£4.88, so KEEP needed the take-profit to come first about 72% of the
time. A coin with no drift reaches +100% before -50% half the time, and this desk's hypothesis is
that these coins drift down. The line was unreachable by construction, and a KILL under it would
have measured the fee model, not the tokens. The $1.50 was also invented: a Solana swap's network
cost is cents. v0.2 drops it, keeps the 1% pool fee, adds price impact from the pool's own
liquidity and an execution slippage on every exit, and stakes £100 (inside the "£100 to £150 a
real trade would be" range Luke named). Round-trip cost falls to roughly 5 to 9% at the
liquidity gate. This is a rule change: the clock resets, v0.1's six rows stay published as their
own book. The cost model is lower than v0.1's, so on the cost line this is a loosening, and it is
logged as one. No pass line moved: every line is the same share of the stake it always was.

## The Grinder: rule candidates, the replay, and promotion

Written 2026-09-25, before the harness exists and before any candidate has been replayed.

**What the replay is, named honestly.** Replaying the snapshots since 22 Sep against rule variants
is in-sample fitting on the same weeks the live book trades. Its best variant will look better than
it is, by an amount that grows with the number of variants tried. So the replay can earn a variant
a trial, never a result. Only forward rows decide.

1. **Variants are listed before they run.** Every variant goes into `grinder/harness/VARIANTS.md`
   with its parameters, committed before the first replay. The count N is the number of rows in
   that file, including ones that later fail to run. Adding a variant after seeing results is
   allowed and costs: it increases N for every variant.
2. **Same costs, same fills.** A variant may change entry gates, the stop, the take-profit, the time
   stop, the check interval and the stake. It may not change the cost model, the fill rule or the
   candle record. A variant that only wins on cheaper assumptions has not won.
3. **Second paper book.** A variant earns one book beside the current rules if, on the replay: at
   least 40 replayed closed positions; expectancy at least +10% of stake; expectancy still at or
   above zero with its best three positions removed; and expectancy above the current rules'
   replay expectancy by at least 10 points of stake plus 1 point for every variant in N beyond ten.
   Only the single best qualifying variant by trimmed expectancy opens a book. One second book at a
   time, and never during a CHANGE window.
4. **Replacing the current rules.** Only on forward rows, closed after the second book opened, over
   the same nights for both books: at least 40 closed positions in each; the candidate's
   expectancy at least +10% of stake and at least 10 points above the incumbent's; the candidate's
   trimmed expectancy (best position removed) at or above zero. Replay rows never count here. A
   replacement is a rule change and resets the clock.
5. **Closing a second book.** If it has not met item 4 by 100 closed positions, or if it is at or
   below -10% of stake at 40, it closes and stays published as its own book.
6. **The record.** Exits are decided on the committed minute candles (RULES.md). If an hourly
   poller is ever added and it disagrees with the candles on a fill, the candles are the record and
   the disagreement is logged. At the executor rung this flips: a live quote that could have been
   traded beats any chart.

Why these lines. The fee model in `RULES.md` costs £5 positions about 46% round trip ($3 flat plus
1% each way on $6.50), so a position needs +49% just to break even and a flat exit at the time stop
loses £2.41. +£0.50 per position on top of that is a real edge, not a rounding error. The trimmed
mean is there because meme-coin returns are one big winner and a pile of losses, and a desk that
is only positive because of one position has not shown anything. The rug rate is a check on the
checks: a rug-check desk that gets rugged more than one time in ten has broken checks, whatever
the expectancy says. Forty is the smallest sample I am willing to call a result on with returns
this fat-tailed, and it is still small; that is why the KEEP band is one-sided and the executor bar
is five times larger.

**Horizon.** Eight weeks is the right horizon for the process and the wrong unit for the verdict.
The verdict is in positions, not weeks. At up to four new positions a night with a 24-hour time
stop, 40 closed positions is ten productive nights out of 56, and 100 is 25. Fewer than 40 by
15 Nov does not mean "needs more time"; it means the scanner spent most nights finding nothing that
passes the gates, which is what happened on the first three nights and is a feed problem already
in `BACKLOG.md`. That is a CHANGE with the second date, then KILL.

## The graduation book

Added 30 Sep 2026, before the watcher recorded any trade. Rules: `grinder/graduates/RULES.md`;
computed by `grinder/graduates/watcher.py summary`. Counted: primary-exit trades (-50% stop, else
sell at 20 minutes) with entry latency at most 120 seconds from the migration's block and Jupiter
liquidity of at least $5,000 at entry (amended 30 Sep 16:05 BST, before any trade closed: a tightening).

| Verdict | Line |
|---|---|
| KEEP | at 400 counted trades: expectancy at least +£10 per £100, at or above zero with the best 10 removed, at most 25% of trades at or below -50% |
| KILL | at 400: expectancy at or below zero; or at 200: at or below -£10 |
| CHANGE | anything else at 400: one written variant, a fresh 400 |

The lead it tests came from one day in-sample (`experiments/2026-09-30-launch-flip/`), so nothing
from that day counts here. Only trades closed after this section's commit count.

## The Pitch

Question under test: does a weekly-refit Dixon-Coles model beat the closing line on English
football, and if so, where. The market is the closing average odds from football-data with the
overround removed proportionally. The measure is the paired difference, per match, between the
model's 1X2 Brier and the market's, on the same matches, averaged. Negative means the model is
better. Only rows committed before kickoff count; `score.py` marks the rest LATE and excludes them.

**At week 8 (15 Nov 2026) the Pitch cannot pass. It can only fail or continue.** Eight weeks was
about 110 to 130 E0 and E1 matches when this was drafted; the desk widened to nine leagues the same
morning, so it is nearer 450 pooled across leagues, and the sample is pooled because the question
is whether the model beats closing prices anywhere, not per league. The per-match spread of Brier differences between two decent
forecasts makes a gap of one point in a hundred invisible at that sample. So the week-8 check is a
process check plus an early kill:

| Criterion | Line |
|---|---|
| Coverage | At least 80% of the matches kicked off from 1 Oct 2026 to the review, in every league the desk predicts (nine from 9 Oct 2026), have a row committed before kickoff |
| Late rows | At most 5% of all rows; none counted anywhere |
| Scored | At least 80 rows scored with both a model and a market Brier |
| Early KILL | 80 or more scored and the paired Brier difference is +0.015 or worse (model worse than the closing market by that much or more) |
| Coverage below 80% | CHANGE: fix the pipeline by 13 Dec 2026 or KILL |
| Otherwise | Continue to the edge test |

**The edge test** closes at 500 scored matches or 31 May 2027, whichever is first, with whatever
sample exists. Three tiers, checked in order:

| Tier | Line | Verdict |
|---|---|---|
| Edge | Paired Brier difference at or below -0.005 and the bootstrap 95% interval entirely below zero | KEEP, and the executor case opens |
| Ingredient | Not edge, but the model earns a log-opinion-pool weight of at least 0.10 chosen on the first half of the sample and lowering log loss on the second half | CHANGE: re-register a blend as the next version on a new clock |
| Nothing | Everything else, including "within noise of the market" | KILL: the finding is published and the desk stops |

Matching the closing market is not new knowledge; the papers already say a free model gets there.
The desk exists to find out whether it does better. If after a season it has not, the record is
the artefact and the desk stops. There is no tier for "close enough".

The paper bankroll is not a criterion at any date. Quarter-Kelly on a handful of bets is noise,
and the backtest already says the v0 betting rule loses. Closing-line value is in the executor bar
because it is the only fast signal a bettor has.

**Executor bar**: the Edge tier, plus at least 100 paper bets struck at a price captured live at
commit time (not the fixture file's average), mean closing-line value on those bets of at least
+2%, and positive paper return over them.

Why these lines. On 24 Sep the desk's own model was replayed on 2025-26 with `sandbox/clv_backtest.py`
(rerun today with four seasons of history in the cache): 930 matches, weekly walk-forward refit,
model Brier 0.6373 against the closing market's 0.6201, a paired gap of +0.017 against the model,
pool weight 0.00 against both pre-close and closing prices, and the paper rule down 23% over 308
bets. That is the starting position, and it is behind the market. The early-kill line at +0.015
sits just below where v0 already is, so a live desk that merely repeats its backtest is killed at
week 8 unless a v1 has been pre-registered by then. The per-match spread of that paired difference on the
same replay is 0.13, so at 80 to 120 matches the standard error is 0.012 to 0.015 and the early-kill
line is about one standard error. Said plainly: a v0 that truly matches the market has roughly a
one in seven chance of being killed at week 8 by bad luck, and a v0 that is truly as bad as its
backtest has a little under an even chance of surviving to the edge test. I accept both, because
matching the market is a kill at the edge test anyway. At 500 matches the standard error is 0.006,
so the interval condition in the Edge tier needs a gap of about one point in the model's favour; a
positive edge smaller than that cannot be shown inside a season by anyone, and I am not going to
pretend otherwise.

**Horizon.** Eight weeks is the wrong horizon for the Pitch on English football alone and I am
saying so now rather than at the review. 500 scored matches is the least that can carry a negative
verdict with any weight. On E0 and E1 that lands around February 2027; on nine leagues at about 90
matches a week it lands in late November, a week or two after the review, and 31 May 2027 is the
backstop if coverage falls short. The week-8 gates above still bind: a desk that cannot commit rows
before kickoff for four fifths of the matches in front of it does not get to the edge test.

## Field Notes

Field Notes is the only thing that reaches Luke. If it carries nothing, the desks are burning
tokens in private, and a persona built to bring artefacts back has stopped doing the one thing it
was for.

A Sunday **passes** when all of these hold:

1. The note shipped by Sunday 23:59, as the first commit of `field-notes/YYYY-WW.md`.
2. It has a `## Ran it` section with a verdict that came from running the thing.
3. It carries at least one thing that could not have been produced by reading: a number computed
   from data Proteus pulled itself, a public claim checked against that data, or an artefact a
   stranger could use. A note of summaries is a fail, however well written.
4. Luke did not say "nothing". One word in reply to the email, or at the review, is enough; it is
   recorded as the ISO week in `state/field-notes-vetoes.txt` and `review.py` counts it. He owes no
   reason and is never asked for one.

`review.py` checks 1, 2 and 4. Item 3 is judged by Proteus on the Sunday, honestly, and Luke's veto
is the backstop if it is not.

| Kill line | Effect |
|---|---|
| Three consecutive Sundays fail | Proteus stops as a whole: both scheduled runs deleted, `HALT` written, a last note says why |
| Four of the eight Sundays fail | Same |

A missed Sunday counts as a fail. There is no partial credit for a late note.

**Horizon.** Eight weeks is right for Field Notes. There is no sample problem: one note a week,
eight notes, and the bar is per note.

## The harvester

Written 2026-09-26, before the first harvest ran and before any entry existed. The harvester
(`bin/harvest.py`, design in `field-notes/HARVEST-DESIGN.md`) is a nightly intake: keyless pulls
from Hacker News, GitHub, arXiv, YouTube and awesome-list diffs, judged by a Sonnet sub-agent,
recorded in `field-notes/harvest.jsonl`, with testable items queued in `PROBES.md` under source
`harvest`. It exists because the probe queue ran dry within minutes on two nights running. It is
judged on whether it feeds verdicts, not on how many entries it writes. `bin/harvest.py review`
computes every line below from the register and `state/probes.json`; `bin/review.py` judges the
desks and does not judge this.

| Criterion | Line |
|---|---|
| Intake | At least 3 kept entries a night on at least 5 nights in every 7 |
| Conversion | Of items marked testable and queued, at least 50% reach a probe verdict within 14 days of being queued |
| Share | On the check date, at least a third of the probe verdicts reached in the trailing 28 days came from source `harvest` |
| Quality | Of harvest-sourced probe verdicts, at least a quarter are **works** |
| Check date | Sunday 25 Oct 2026 (2026-W43), four weeks after the first scheduled run, in that Sunday's Field Notes |
| KILL | Conversion, Share or Quality missed on the check date; or Intake missed in two consecutive weeks before it |

On a KILL the harvest step comes out of the nightly, the register is frozen and stays published,
and the finding goes in the next Field Notes with the numbers. There is no second date: a dead
intake is not worth a CHANGE window, and it can come back only as a Big Expedition from
`BACKLOG.md` with a different design.

Why these lines. Conversion is a test of the child's judgement, not of the probe loop: the loop
has spare capacity every night (it stopped for want of work on 24 and 25 Sep), so a harvest probe
that sits unrun for two weeks was not runnable and "testable" was wrong. Half is generous for a
first version and I will tighten it if the first fortnight beats it easily. Share is the reason the
harvester exists: the backlog, the persona and the desks produced twelve verdicts in two nights and
then nothing, so within a month harvest should be the largest single source; a third is the floor
below which it is cheaper for me to think of things myself. Quality guards the other failure, a
child that calls everything testable so the queue looks full and the loop grinds out blocked and
not-worth-it verdicts all night; one in four works is low, because the persona's own probes ran at
eight works in twelve, and I am allowing for the harvester finding harder things. Intake is a
plumbing alarm, not a quality line: two silent weeks means a fetch broke or the query list is dead,
and nobody should wait for the check date to find that out.

Cost is not a kill line. The charter's usage rule applies: if the harvest step takes more than a
fifth of the nightly's tokens in a week, Field Notes says so, and the cheapest cut is alternate
nights. The estimate before the first run and the measurement after it are in
`field-notes/HARVEST-DESIGN.md`.

## The judgement book

Written 2026-09-27 at about 23:50, which is late, and I say how late. The charter wants pass marks
before the first scored row. No row in `pitch/JUDGEMENT.csv` had been scored in the book, but I had
already scored the first eight privately tonight (P-0024, `experiments/2026-09-27-P-0024/`), so
I wrote these lines knowing that J-0001 to J-0008 came out Brier 0.572 against the market's 0.559.
Those eight are therefore **excluded from every line below**. They stay published as their own
"seen" book and are never counted toward a verdict. Everything from J-0009 on counts.

Question under test: when I call a match on judgement rather than a model, do I beat the market
price I wrote down beside the call? The measure is the paired difference, per call, between my 1X2
Brier and the recorded market's, averaged over calls. Negative means I am better. The over 2.5 Brier
difference is published beside it and is not a criterion. Only rows committed before kickoff count.
`pitch/score_judgement.py` computes it from eloratings.net results; `bin/review.py` does not judge
this book.

| Criterion | Line |
|---|---|
| Counted rows | J-0009 onwards, committed before kickoff, scored with both Briers |
| Sample floor for any verdict | 60 counted rows |
| KILL | At 60 or more counted rows, paired Brier difference of +0.010 or worse; or at 100 counted rows, anything not at or below -0.005 |
| KEEP | At 60 or more counted rows, paired difference at or below -0.005, on all counted rows and on the rows where my biggest lean was 0.03 or more |
| INCONCLUSIVE | Everything else under 100 counted rows |
| Horizon | 100 counted rows or 31 May 2027, whichever is first; at the horizon anything not KEEP is KILL |

On a KILL I stop making judgement calls, the book is frozen and published, and the finding goes in
Field Notes. On KEEP the book continues; it does not earn an executor on its own.

Why these lines. Matching the market is not knowledge, same as the Pitch, so there is no tier for
"close enough" at the horizon. The leaned subset is in the KEEP line because a book that only wins
where it agreed with the market has shown nothing. Sixty is two and a half international windows at
this window's 24 calls, and at that size I do not know the standard error: my probabilities sit
within about five points of the market, so the per-call spread of the difference should be well
under the Pitch's 0.13, but I have not measured it and will not pretend to. The eight seen rows are
excluded rather than included because a line written after seeing results has to cost something.

## Inconclusive

Inconclusive is the most likely result at eight weeks for both desks, and it is where projects
drift instead of deciding. So:

- Inconclusive means the sample floor was not met on the date. It is never "keep going and see".
- It converts on the day into **CHANGE** with three things written in the review: the binding
  constraint, named from the run logs (the Grinder's is already known: the gates and the feed do
  not fit); the one fix; and the second date, which is fixed here as 13 Dec 2026 for both desks.
- At the second date a desk still under its floor is **KILL**. There is no third date. Inconclusive
  twice is a result: the desk could not be made to produce its own evidence in twelve weeks.
- The Pitch is the exception in one respect only: its edge test has its own horizon above. Its
  week-8 gates are process gates, and an inconclusive process gate follows this section.
- During a CHANGE window the desk gets the named fix and nothing else. No new gates, no new
  markets, no v2 alongside v1, no widening the scanner to "get the numbers up".
- If a rule change resets a clock inside the eight weeks, the floor still applies at the review
  date to the rows under the new version. A reset does not buy time; it costs it.

## Disqualifiers

These are charter breaches. Any one of them is a kill on its own, before the numbers are read:

- A Flywheel card, luke-gate, Todoist task or any decision item opened for Luke by Proteus. This
  kills the persona, not a desk; it breaks the reason it exists.
- Spend over the monthly cap. Persona.
- An email to anyone other than Luke. Persona.
- An outcome column in either ledger rewritten after the outcome in the record's favour. Desk, and
  its whole record is void.
- A prediction committed at or after kickoff and counted in any average. Desk.

### The blind column (added 2026-09-29, before any blind row existed)

Luke's question of 28 Sep: were those predictions, or positions against the market? Positions. Every
number in J-0001 to J-0024 started from the price. From 29 Sep the book carries two columns. The
**blind** column is written and committed before any odds are pulled (`pitch/judgement.py blind`,
then commit, then `odds`), and the **anchored** column is written after the price is seen, as
before. A blind row counts only if its blind commit precedes `odds_seen_at` and kickoff.

Question under test: can I forecast a football match without seeing the price? Measure: paired
difference between the blind 1X2 Brier and the market's on the same rows. Published beside it, not
a criterion: blind minus anchored on rows that have both, which says whether seeing the price helps
or hurts.

| Criterion | Line |
|---|---|
| Counted rows | blind rows committed before odds and before kickoff, scored with both Briers |
| Sample floor for any verdict | 60 counted rows |
| KILL | At 60 or more counted rows, blind minus market of +0.020 or worse; or at 100 rows, anything above 0.000 |
| KEEP | At 60 or more counted rows, blind minus market at or below 0.000 |
| INCONCLUSIVE | Everything else under 100 counted rows |
| Horizon | 100 counted rows or 31 May 2027, whichever is first; at the horizon anything not KEEP is KILL |

A KILL on the blind column freezes the blind column only; the anchored book has its own lines above.

## Called shots (added 2026-10-09, before any shot existed)

Before each daytime probe the Trials slot commits a called shot: the verdict it expects (works,
broken, blocked, not worth it), how sure it is (p, 0 to 1), and the one number it expects the probe
to measure (`probe.py shot`). Scored at the verdict by `probe.py shots`: hit if the verdict matches,
Brier on p. Always saying 0.5 scores 0.250; always saying "works" at 0.77 (the share of works among
the first 77 verdicts, 59 of them) scores 0.766 x 0.234 = 0.179, so that is the bar a judgement has to beat, not the coin.

| Criterion | Line |
|---|---|
| Counted shots | committed before the probe's `next` GO, one per probe, verdict recorded |
| Sample floor | 40 scored shots |
| KEEP | Brier at or below 0.160 at 40 or more (beats the "always works" baseline) |
| KILL | Brier above 0.200 at 40 or more: the shots are noise, the habit stops and the slot saves the call |
| INCONCLUSIVE | Anything between, until 80 scored shots, then KILL unless KEEP |
| The number | Recorded and published beside the verdict, not scored until a rule for it is written here |

## Log of changes to this file

| Date | Change | Tightened or loosened | Rows it would have judged at the time |
|---|---|---|---|
| 2026-09-24 | Written | n/a | none: 0 positions, 0 predictions, 0 notes shipped |
| 2026-09-24 | Pitch coverage and sample pooled over every league the desk predicts, not E0 and E1 only, after the desk widened to nine leagues the same morning; the 500 floor is unchanged | Neither; the same bar over a larger feed | none: 0 predictions |
| 2026-09-25 | Grinder lines restated as a share of the stake (10% keep, -10% kill, executor 20% and 10% trimmed); only the current rule version is judged; the Grinder moves to v0.2 (stake £100, cost model replaced, exits on minute candles), which resets its clock | Pass lines: neither, same share of stake. Cost model: loosened (cheaper than v0.1's), logged as such | v0.1: 6 opened, 2 closed (G-0001 -£6.63, G-0002 +£3.45), judged as their own book. v0.2: none |
| 2026-09-25 | Rule candidates, replay and promotion section added, before the harness exists | Tightened: adds a bar where there was none | none: no candidate replayed |
| 2026-09-26 | Harvester section added: intake, conversion, share and quality lines with a kill on 25 Oct 2026, computed by `bin/harvest.py review` | Tightened: adds a bar where there was none | none: 0 harvest entries, 0 harvest-sourced probes |
| 2026-09-27 | Judgement book section added after eight rows had been scored privately; those eight are excluded from every line | Tightened: adds a bar where there was none | J-0001 to J-0008 seen (Brier 0.572 vs market 0.559) and excluded; J-0009 to J-0024 unplayed |
| 2026-09-29 | Blind column added to the judgement book: calls committed before any price is pulled, own KEEP and KILL lines | Tightened: adds a bar where there was none | none: 0 blind rows |
| 2026-09-30 | Graduation book section added before the watcher's first trade | Tightened: adds a bar where there was none | none: 0 trades |
| 2026-10-03 | Exchange book added (`exchange/RULES.md`): blind calls on Smarkets politics and current-affairs markets, me minus market by Brier; KILL +0.020 at 60 or above 0 at 100, KEEP at or below 0 at 60 | Tightened: adds a bar where there was none | none: 0 calls |
| 2026-10-03 | Graduation book judged KILL (2,252 counted, -£14.2, past the -£10 at 200 line). G2 registered in `grinder/graduates/RULES.md`: liquidity at least $50,000, counted from 2026-10-03T12:00Z only, the same lines, anything short of KEEP at 400 is KILL | Tightened: G2 has no CHANGE outcome | G2: none, counting starts after registration; the 241 trades the filter was found on never count |
| 2026-10-07 | Exchange book: a call with no two-sided price at its one anchor attempt is settled for the record but never counted, and never re-anchored (`exchange/RULES.md`, No anchor) | Neither: restates the existing Counted line | X-0001 and X-0002 (Quebec, unresolved): excluded from the count |
| 2026-10-09 | Called shots added for the daytime Trials slot: KEEP at Brier 0.160 or below at 40, KILL above 0.200 | Tightened: adds a bar where there was none | none: 0 shots |
