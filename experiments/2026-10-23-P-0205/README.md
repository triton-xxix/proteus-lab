# P-0205: a sampling profile of the nightly, from the hook's own log

Refill build, 23 Oct 2026, from REFILL-SOURCES row 20 (MIT Missing Semester, Debugging and Profiling).
The lecture's one idea I took: a sampling profiler does not instrument anything, it looks at where the
program is every so often and attributes time to whatever was on the stack. The PreToolUse hook already
writes one timestamped line per tool call (`state/unattended-decisions-YYYY-MM-DD.jsonl`), so the nightly
has had a sampling profile all along and nobody read it.

## Called shot

works at 0.60; the longest gap in the last seven nightlies is a desk script or child wait under 12
minutes, and no step owns over a quarter of a run. Commit fbb0d28.

## Method

`profile_nightly.py` groups the log by session (a run crosses midnight), keeps the parent's calls for
task `proteus-nightly`, and treats the gap to the next parent call as the time the earlier call took plus
the thinking after it. Gaps are attributed to the earlier call and bucketed into step families by the
command. Seven runs: 16, 17, 19 (the 03:27 catch-up and the 23:23 run), 20, 22 and 23 Oct (tonight, read
live to 23:47). Standard library only, under a second.

## Numbers

| run | span | parent calls | child calls | longest gap | after |
|---|---|---|---|---|---|
| 16 Oct | 17.7 min | 190 | 26 | 1.7 min (10%) | grinder paper.py |
| 17 Oct | 12.7 min | 88 | 24 | 1.5 min (12%) | grinder paper.py |
| 19 Oct 03:27 | 42.5 min | 129 | 23 | 21.8 min (51%) | a Read of a background job's output file |
| 19 Oct 23:23 | 23.4 min | 133 | 48 | 4.8 min (20%) | pitch predict.py |
| 20 Oct | 23.3 min | 157 | 39 | 4.3 min (18%) | `tail -5 MENTIONS.csv` |
| 22 Oct | 25.5 min | 197 | 46 | 7.0 min (27%) | `date -u` |
| 23 Oct (to 23:47) | 23.2 min | 139 | 61 | 1.1 min (5%) | harvest.py run |

Across all seven (168 minutes of span): "other Bash" 29%, file reads and writes 27%, pitch 7%, probe
loop 7%, exchange 5%, grinder rules 4%, curl 2%, harvest 2%, narrative 2%, Agent spawns 1%.

## Reading

The long gaps are not scripts. A 7-minute gap after `date -u` and a 4-minute gap after a `tail` are the
parent sitting idle for a background job (mentions.py, the scan) to send its notification; the 21.8-minute
gap on 19 Oct is the same thing after the browser-hang night. The desk scripts the task file worries about
(scan, pitch refit, exchange snapshot) together take well under a fifth. So the shot's number missed: two
runs had a single gap over a quarter, both waits, not steps.

The other number that fell out: a nightly's parent activity spans 13 to 26 minutes, against a 90-minute
budget and a probe loop meant to run to the deadline. The hook log is the cheapest way to see that, and
`probe_nightly.py` can be re-run any morning.

## Not done

Gaps attribute thinking time to the previous call, so a long gap after a cheap command can be the model
composing, not the command; the log cannot separate the two. Children's calls were counted, not timed.
The Inspector, Trials, Workshop and Smith sessions were not profiled; the task filter would take them.
