# Charter v3.1: the quota diet, for Luke to sign

Drafted 27 Nov 2026 from Luke's decisions in a live chat that day (WF-0518). **Signed 28 Nov 2026** on Luke's word in an
interactive session ("Sign and load"): each change below was applied to `CHARTER.md` as written, the
signature block has a v3.1 paragraph, and the systems job was loaded the same day. This file stays as
the record, as `CHARTER-v3-DIFF.md` did for v3.

Already done without a charter change, because the charter lets any run edit task prompts and desk
code, and PASS-MARKS.md says what a KILL does: the Grinder and Pitch books closed with their final
numbers, their steps out of the nightly and weekly, the four side quests out of every task file, the
five daytime task files marked paused. The scheduled tasks themselves were switched off in another
session. What follows is the part the charter itself says, which no run may edit.

## 1. Cadence

Now:

> - Morning chess, 07:45, 40 minutes: rated Lichess bot games after the bots' daily caps reset.
> - Daytime loop, four slots of 40 minutes each (section below): Inspector 09:00, Trials 12:30,
>   Workshop 16:30, Smith 20:00.
> - Nightly expedition, 23:15, 90 minutes, on Opus, in this order: preflight; the desks update and
>   commit (scripted, short); one probe to a verdict, then the loop until its cap; one Field Notes
>   item, which may be the probe; run log. Saturday's probe slot goes to the Big Expedition.

Proposed:

> - Morning chess: stopped 27 Nov 2026 (the Lichess side quest is over). The task stays, switched off.
> - Daytime loop: paused 27 Nov 2026 (section below). Its five tasks stay, switched off, and come back
>   only on Luke's word.
> - Nightly expedition, Wednesday and Saturday at 23:15, 90 minutes, on Opus, in this order: preflight;
>   the Big Expedition's step while one is open (first, up to 45 minutes); the desks update and commit
>   (scripted, short); one Field Notes item; the probe loop until its cap; run log.
> - The systems book's daily step: Monday to Friday 22:30, a launchd job with no Claude session in it
>   (section 6 below).

The Sunday weekly, the fortnightly Big Expedition and the reviews are unchanged.

## 2. What Proteus must do

Now: "Take one probe to a verdict every night (Probes below), and record it in `PROBES.md`. The daytime
Trials slot runs more; the nightly one is still owed."

Proposed: "Take at least one probe to a verdict on every nightly run (Probes below), and record it in
`PROBES.md`. On a Big Expedition night the expedition's step may take the probe slot."

Now (judgement book): "Treat any book of calls made on judgement rather than by a model (the first is
`pitch/JUDGEMENT.csv`, ...) exactly like a desk ..."

Proposed: unchanged, plus one sentence: "The first judgement book closed with the Pitch on 27 Nov 2026,
short of its 60-row floor, unjudged."

## 3. The remit, a new paragraph under "Why Proteus exists"

> From 27 Nov 2026 the paper desks Luke handed over at the start are closed (the Grinder and the Pitch,
> on their week-8 KILLs) and the side quests that grew around them are stopped (Lichess, Nolan, sunspot
> and space weather, petitions). The remit stays broad: general R&D; Skool and course teardowns; tool
> vetting; and genuine quant trading and crypto edge research, through the edge desk, the exchange
> book, the systems book and the probe loop. A new desk or a new side quest needs a written reason
> in `BACKLOG.md` and a slot in a nightly that already runs; it does not get a scheduled task of its own.

## 4. The daytime loop

Proposed first line of the section: "Paused from 27 Nov 2026 to save Luke's shared Claude quota. The
text below describes the loop as it ran from 12 Oct to 27 Nov 2026 and as it would run again. Until
Luke switches it back on, the nightly carries the probe loop alone, the Sunday weekly rebuilds the
published numbers, and Smith's skill pruning waits."

## 5. What Proteus costs in Claude

Now: "The limit is time, not tokens: the nightly's 90 minutes plus 40 minutes for each daytime slot
and the morning chess job, about four and a half hours a day in all. `USAGE.md` is rebuilt every
morning by the Inspector and labels each slot, so the cost of the daytime loop is visible on its own."

Proposed: "The limit is time, not tokens: two nightlies of 90 minutes and the Sunday weekly's 60, about
four hours a week in all, against about thirty-five a week before 27 Nov 2026. `USAGE.md` is rebuilt every
Sunday by the weekly. If a week's scheduled usage is more than double the trailing four-week average,
Field Notes says which run or step did it; until four quieter weeks have passed, the average is the
old, higher one, so the alarm will not fire on the diet and Field Notes says the week's number plainly."

## 6. Long-running jobs (Probes), one added sentence

Now the clause allows background jobs only if each "stops itself at a fixed end time ... writes only
under its own experiment folder". The systems book's daily step meets neither: it runs until book 2's
verdict and writes `systems/` and a run-log line.

Proposed addition: "A desk's mechanical daily step may run the same way with no fixed end time, if its
rules file names it, it stops on HALT, it writes only its desk's data files and one run-log line, it
commits locally by named path and never pushes, and it ends when the desk reaches a verdict or Luke
switches it off. The first is `systems/daily.sh` (`com.proteus.systems`, 27 Nov 2026), ending at systems
book 2's verdict (DUE D-006, backstop 31 Dec 2027)."

Until this is signed the job is built and tested once by hand (27 Nov 2026 22:54, commit 434149c3) but
not loaded, and the nightly's catch-up keeps the book alive with rows logged after their fills on the
days between nightlies. Loading it is one command, for Luke or for an interactive session on his word:

```
launchctl bootstrap gui/502 /Users/triton/PROTEUS/systems/com.proteus.systems.plist
```

## 7. Signature, if signed

> Version 3.1, Luke Boyd, DD/MM/2026. Amended on Luke's word in an interactive session after he read
> `CHARTER-v3.1-DIFF.md`: the quota diet of 27 Nov 2026 (WF-0518). Version 3 otherwise stands.
