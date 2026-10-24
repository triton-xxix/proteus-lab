# P-0213: agent-usage-guard, does its hook warn on a stale cache with a large context?

Date: 2026-10-24, nightly probe loop. Source: harvest H-0391 (Show HN, 22 Oct 2026, 27 points).
Repo: https://github.com/rbartoli/agent-usage-guard (MIT), fetched as a tarball by `fetch.py`
into `sandbox/agent-usage-guard/` (60 files, 220 KB).

## Called shot

Works: the prompt gate asks "compact, then send" when the session has been idle an hour or more
and holds at least 150k context tokens; it stays quiet below either line.

## What it actually is

Not a classic stdin-JSON hook and it never reads a transcript file. It is a Claude Code mods plugin
(`hooks/hooks.json` names one module, `hooks/register.ts`, 34 KB) that subscribes to the mods
events `agent.spawn`, `prompt.submit`, `tool.call`, `turn.step` and `session.measure`. The context
figure is `input + cacheRead + cacheWrite` of the last API response the harness reports
(`core/observe.ts`, `contextOf`), and idle time is the gap since the session's last response. So the
probe's premise, a synthetic transcript, was wrong; the testable slice is the pure core
(`core/`, no I/O), which is exactly what the repo's own tests drive. Thresholds are env-driven
with defaults in `core/config.ts`: dormant at 3,600 s and 150,000 tokens, warn at 300k, hard ask
at 500k.

## What I ran

`harness.ts` (plain `node`, which here strips types; `bun` is not on the unattended safe list)
imports `promptGate` from the sandbox copy and calls it with crafted session states. Fourteen
cases, results in `results.json`:

| Case | Verdict |
|---|---|
| 160k context, 2 h idle, user present | ask [dormant], "Compact, then send / Send anyway / Cancel" |
| same, headless (claude -p), first then second resume | allow, then drop [dormant] (dormantMax 1 per 10 min per machine) |
| 149,999 context, 2 h idle | allow |
| 150,000 context, 2 h idle | ask [dormant] |
| 160k context, 59 min idle | allow |
| 160k context, 60 min idle | ask [dormant] |
| 350k context, 1 min idle | allow with a one-time note to Claude to keep the turn bounded |
| 600k context, 1 min idle, user | ask [prompt-context] |
| 600k context, headless | drop [prompt-context] |
| 160k, 2 h idle, source "other" (a notification) | allow, untouched |
| no context yet, 2 h idle | allow |
| tonight's real session, last usage 32 + 272,067 cache read + 486 cache write = 272,585 | ask at 2 h idle, allow at 1 min |

The gate itself is pure arithmetic: 76 microseconds a call, mean over 10,000 calls (first cold
call 423 µs), so it costs nothing a user would feel.

## Verdict

Works. Both boundaries sit exactly where the README says (150,000 and 3,600 s inclusive), the
notification path is never held, and headless sessions get one free heavy resume per machine per
window before a refusal. What this does not test: the adapter (`register.ts`) that feeds the core
from real Claude Code events, which needs an interactive session loading the plugin and
`claude plugin test`, neither of which runs unattended. The author's own numbers (the biggest
burst from 365 agent spawns to 27, requests over 500k from 14.5% to 0.6%) are his, over 75 days,
and not re-measured here.

## Relevance to Proteus

The scheduled runs here are headless, so the guard would refuse rather than ask: a 2 h gap on a
heavy session (the 17 Oct hang was 28 h) would have been dropped with a reason instead of
re-writing the cache. The nightly's own hook already caps spawns at four and depth one, which this
plugin does per machine (4 running, 12 starts per 10 min). Not installing it in a scheduled run: it
writes under `~/.claude/plugins/store/`, outside my write roots.
