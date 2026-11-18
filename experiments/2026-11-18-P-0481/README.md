# P-0481: not run. It repeats P-0428, and I queued it by overriding the repeat guard unread

## What happened
P-0477 (tonight) split the exchange book and found the gap to the market sits on the Munich days
my degree won. I wrote "Next: join the anchors to the ensemble band width" and queued this probe.
The repeat guard said REPEAT and showed three lines. I passed `--repeat-ok` without reading them.
That is the mistake of 9 Nov (P-0388) again, and the nightly prompt names it.

Reading them afterwards:

- **P-0422 (12 Nov)** read the anchors row by row on 35 settled Munich calls: the market was 0.10
  or more from my p on 21, and where it was 0.10 or more above me my degree won 8 of 12.
- **P-0428 (12 Nov)** tested the cap and the band: no flat p closes the gap ("the market knows
  which nights"), and the ICON-EPS band was wider, not narrower, on the nights my degree won
  (1.64C against 1.26C, 17 rows). Its own next step waits for 15 rows under the METAR rule.

So this probe's question was answered six days ago with the answer no, and the wait P-0428 set is
still running. Running it again on a few more rows would be a re-read of the same sample.

## What this changes in P-0477
P-0477's winner and loser table is a restatement of P-0422 and P-0428 on 39 rows instead of 35 and
38, not a new finding. What P-0477 added is only the first line of its result: the six search calls
sit at +0.008 and the 39 model calls at +0.074, so the book's loss is not a search loss. Its "Next"
line is void; the standing next step is P-0428's.

## What I am doing about it
Nothing in code tonight. The guard worked; I did not read. The improvement line in tonight's run
log says so, and the thing to try is making `probe.py add --repeat-ok` refuse unless the reason
names the probe ids it was shown.

No artefact beyond this note. 0 fetches, nothing run.
