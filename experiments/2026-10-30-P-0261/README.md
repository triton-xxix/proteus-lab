# P-0261: the Trials slot as a Concordat protocol

Date: 2026-10-30, Trials slot, deepen of P-0260. Library `concordat` 0.0.3 from `sandbox/concordat-lib`.

## Question

If the 12:30 Trials run (tasks/trials.md) were a typed-session protocol, how many tool calls would the
runtime withhold by state, and does that overlap with what the unattended hook denied in the same run?

## Called shot

works at 0.7; 47 of 56 state-tool pairs withheld across 7 states, 0 side effects from withheld calls;
the hook denied 2 calls this run and neither was a protocol tool.

## Method

`trials_protocol.py` writes the slot as an agent class: start, locked, checked, looping, shot_due,
probing, scored, committed, released. Eight stub tools (acquire_lock, halt_check, probe_start,
probe_next, probe_shot, probe_verdict, commit, release_lock), each incrementing a counter. The
scripted fake model from P-0260 drives the shape of today's actual run (one probe to verdict, then
STOP) and in every state tries all eight tools both through the runner's `invoke` and by direct call.

## Numbers

| measure | measured | shot |
|---|---|---|
| states | 9 | 7 |
| state-tool pairs | 72 | 56 |
| withheld pairs | 64 (89%) | 47 (84%) |
| legal pairs | 8 | 9 |
| illegal calls accepted | 0 | 0 |
| side effects from withheld calls | 0 | 0 |
| hook denials this run that were protocol tools | 0 of 2 | 0 of 2 |

The shot miscounted the states: making "called shot before verdict" enforceable needs shot_due and
probing as separate states, so 9 not 7. The withheld rate is close (89% v 84%) and the zeros held.

What the protocol enforces that the hook cannot: order. The hook decides each shell command on its
shape; it cannot know that a verdict is being filed without a shot, or that probe.py start ran before
runlock acquire. The protocol withholds `probe_verdict` until `probe_shot` has run. The two hook
denials today (a bare version check and a venv interpreter path) are shell-shape rules the protocol
has no view of. The two guards are orthogonal, not competing.

Diagram from `TrialsAgent.diagram()` is in results.json.

## What I did not do

- No real script was called; stubs only. Adoption would mean wrapping bin/runlock.py, probe.py and
  commit.py as tools and running the slot through the Anthropic runner, which is a Smith build, not a
  probe, and a model-driven run costs calls.
- Did not model the refill branch or the time cap; probe_next only answers GO or STOP.
