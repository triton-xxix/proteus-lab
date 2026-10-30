# P-0260: Concordat, does the typed-session library block every illegal tool call from a scripted fake model?

Date: 2026-10-30, Trials slot. Source: harvest H-0449, arXiv 2610.37461 (Sikaroudi, 27 Oct 2026).
Library: `concordat` 0.0.3 from PyPI (pure Python, Apache-2.0), repo github.com/miladsikaroudi/concordat.
Installed with `pip --target` into `sandbox/concordat-lib` plus pydantic for the runner module.
Python 3.14.6. No model, no key: the paper's claim is about the guard layer, which runs without one.

## Called shot

works at 0.55; 0 side effects from out-of-state tool calls, every illegal call rejected.

## Method

`fake_model.py` defines a four-state agent (start, asked, confirmed, done) with three tools and one
human step. Each tool increments a counter when its body runs. A scripted fake model walks the one legal
path and, in every state before and after each legal move, tries every tool in the catalogue plus an
unknown name, in two modes:

- A, direct method calls on the agent object (what in-process code can do);
- B, the runner's `invoke` over `allowed_tools()` (what a model-driven run goes through).

Also checked the two extra README claims: a subclass that adds a shortcut to the final state is
rejected when the class is defined, and the tool-call budget stops calls once spent. And one thing the
README does not claim: whether an in-process caller holding the raw function can skip the guard.

## Numbers

| measure | A direct | B runner |
|---|---|---|
| illegal calls tried (4 states) | 16 | 16 |
| rejected | 16 | 16 |
| accepted | 0 | 0 |
| side effects from illegal calls | 0 | 0 |
| side effects on the legal path | 1 per tool | 1 per tool |
| tools offered per state | start 1, asked 2, confirmed 1, done 0 | same |

- Mode A rejects with `ProtocolViolation` raised in the bound wrapper before the method body (agent.py:61).
- Mode B never offers the tool at all: `invoke` returns "'x' is not allowed in the current state." as an
  error string for the model to read, so the withheld set and the rejected set agree.
- Liskov: `FastBookingAgent` with a start-to-done shortcut raised `ProtocolError` at class definition,
  naming the parent's required path.
- Budget: `Budget(tool_calls=3)` allowed exactly 3 calls then raised `BudgetExceeded`; no body ran after.
- Bypass caveat: `type(agent)._steps["apply_change"].fn(agent, "B-9")` ran the body and fired the side
  effect with the session still in `start`. A model emitting tool names cannot reach this, so the paper's
  claim stands for model-driven runs, but the guard is at the method boundary, not around the function.

Shot v measured: expected 0 side effects from illegal calls, measured 0 of 32 tried. Hit.

## What I did not do

- No model-driven run (the tau-bench 13 of 50 v 0 result needs paid calls and the benchmark; out of
  scope here, and the paper's own RESULTS.md carries it).
- No test of the token budget or handoff split; tool-call budget only.
- Did not read the upstream test suite; this is my own harness, 32 illegal calls over 4 states.

## Why it matters here

The same pattern (offer only the legal tools, reject the rest before any side effect) is what the
unattended hook does for Proteus by denial after the fact. A protocol class per scheduled task would
let the runner withhold tools by state rather than deny them one call at a time.
