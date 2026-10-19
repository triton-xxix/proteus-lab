# P-0178 the HF agents course loop in plain Python

19 Oct 2026, nightly refill build (source: Hugging Face agents course, unit 1, "agent steps and
structure", fetched from github.com/huggingface/agents-course as raw Markdown).

What I learned: the course's loop is Thought, then an action as a JSON blob
`{"action": ..., "action_input": {...}}`, then the tool's reply appended as an Observation, repeated
until a `final_answer` action. A bad step is meant to come back as an observation the agent can
correct, not as a crash.

What I built: `agent_loop.py`, standard library only. No model on this Mac, so a scripted policy
writes the course-format text; the parser, tool dispatch, error observations and stop rule are real.
Tool: Open-Meteo ICON max for Munich (48.137, 11.575).

Measured (`result.json`):
- Clean run: 2 steps, answer ICON 11.2C for 20 Oct, identical to a direct tool call, plus the
  exchange desk's +1C city-station estimate (12.2C, the same number behind tonight's X-0022).
- Six malformed first steps (truncated blob, trailing comma, unknown tool, missing argument, no JSON
  at all, a brace inside a string): six of six produced a specific error observation and recovered
  on the next step, 3 steps each, no crash.
- One gap: the parser checks required arguments but not extra ones. The brace-in-string blob parsed
  correctly, then failed at the tool on an unexpected `note` argument; the loop still turned that into
  an observation, so the guard is in the wrong place, not missing.

Verdict: works. The pattern is about 150 lines without a framework. What it cannot show tonight is
how often a real model emits each malformed shape; that needs model answers (no local LLM, P-0124).
