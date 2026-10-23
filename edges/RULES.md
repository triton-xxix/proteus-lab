# The edge desk: rules

Written 19 Oct 2026 after Luke said long backtests are pointless because the market has changed a
hundred times, and short bursts are the game: if an edge ran for the last three weeks, assume we
have it for the next two, run it till it stops, then find another. Before this desk, 165 probe
verdicts carried 94 money findings and not one was ever traded, because every test demanded a
rule hold since 1993 or 2009, which rejects a temporary edge by design.

Paper only. The charter's execution ladder holds: paper with a public record first, then an
executor with caps in code, then Luke arms it. Nothing in this folder asks for real money.

## What an edge is

A mechanical rule: a trigger, an instrument, an entry, an exit, a cost model. No judgement calls
inside the rule. If I cannot write it so a script fills it, it is not an edge, it is an opinion.

## Admission

An edge is admitted to a forward paper test when it beats a **random-entry control** on a
**recent window**, costs in:

- The control: the same instrument, the same holding period, the same costs and funding, entries
  drawn at random over the window the events sit in (and never overlapping an event's own hold).
  At least 200 draws an instrument. Reported as the control's mean and median, where each event
  trade ranks among its own draws, and a pooled permutation p (2,000 permutations of one draw per
  event, the share whose pooled mean is at least the edge's).
- The window: about the last 21 days for an edge that triggers daily; for an event-driven edge
  the most recent N events, N stated, preferably 8 to 12, and the report says how far back N
  reaches. If the window is thin, the report says so in the first line.
- The line: mean net after costs above the control's mean, permutation p below 0.10, and at least
  five winners in eight (or the matching share of N). All three, or no admission.
- Decades of history are neither required nor wanted. A long backtest may be cited as background;
  it never admits an edge.

An edge found by **flipping the sign** of a failed one is a candidate, not an admission. Its window
starts the day the flip was written down; only events after that day count. The data that killed
the original cannot admit its mirror.

## Forward test

Admission goes straight into a forward paper test. Before the first forward trade is possible, the
edge's folder carries, committed:

- the rule, the venue, the fill (which bar, which price), the cost model;
- the **kill line**, concrete numbers, one line of justification each, for example: kill when the
  mean net of the last K closed trades is below zero (K at least six so one bad batch cannot do it
  alone); kill on M consecutive losses (M chosen so it is rare under the admission window's win
  rate); kill on any single loss past a floor that marks a regime change (a squeeze, a halt);
  retire, not kill, after D days with fewer than T trades (no flow is not a loss, it is an end).

Trades are filled by script from klines, never by hand, at a fixed delay after detection that the
watcher can actually achieve. The commit timestamp of each trade row is the proof it was decided
before its outcome. A trade the venue could not take (no perp, no market, settled) is recorded
as skipped, never filled from spot or from a venue that did not have it.

## Kill and retire

`edges.py status` reads every kill line every night. The first night an edge reads KILL, the
register row goes to `killed` with the numbers, the edge's REPORT.md gets a dated paragraph on
why, and the run log leads with it. A killed edge is not re-admitted on the same window; it can
come back as a new row on a new window. Retired edges (no flow) keep their watcher if it is cheap
and its data feeds another candidate.

## The register

`REGISTER.csv`, one row an edge: id, name, source probe, status (candidate, forward, killed,
retired), admitted date, window used, admission numbers, kill line, forward result so far.
`edges.py status` prints it. `edges.py score` fills whatever the watchers detected. Both run in the
nightly after the systems book; step 4's commit picks up `edges/` with the other desks.

## Standing order (Luke, 23 Oct 2026)

Keep testing. Any strategy found anywhere joins the register as a candidate the same day and gets a
recent-window admission test within a week. A rejected edge can be retested on a fresh window about
monthly, as a new reading on its row, never by reusing the window that rejected it.
