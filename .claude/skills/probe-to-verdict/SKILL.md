---
name: probe-to-verdict
description: Take one Proteus probe from the queue to a measured verdict (works, broken, blocked, not worth it) with a called shot first and an artefact under experiments/. Use in the nightly probe loop, the daytime Trials slot, or any time a probe from state/probes.json is being run.
---

# Probe to verdict

A probe is one thing Proteus has not run before, taken to a verdict the same session. Reading about it
is not a verdict (CHARTER.md, Probes). Written 9 Oct 2026 from the nightly's step 6 and the 7 to 8 Oct
loops, which did six verdicts in 14 to 21 minutes each night.

## The loop

1. `python3 /Users/triton/PROTEUS/bin/probe.py next --refill` prints `GO P-00NN`, `REFILL`, or `STOP`.
   On STOP, stop. Never start a probe by hand after a STOP.
2. **Called shot, before touching the probe** (daytime Trials always; nightly when there is time):
   `python3 /Users/triton/PROTEUS/bin/probe.py shot P-00NN --expect works|broken|blocked|not-worth-it --p 0.7 --number "the one number I expect to measure"`
   Be honest with p. The bar is Brier 0.179 (always "works" at the base rate); see PASS-MARKS.md.
   Two ways this step went wrong under this skill, both in Trials:
   - **A "blocked" shot is a claim about this folder, not about the world.** On 12 Oct two probes
     were called blocked ("no key", "no fixtures till 17 Oct") without one grep; the key was in
     `pitch/apisports.py` and the fixtures were cached. Before calling blocked, grep the folder for the
     thing you say is missing (`grep -rl <name> /Users/triton/PROTEUS/pitch`); if it is there, call
     something else. Looking at what the folder already holds is not looking at the probe's result.
   - **A leg-two probe has no blind shot if you already read the thing it measures.** On 13 Oct P-0135's
     kickoff times were read before the shot, so the hit was free. Call it with `--p 0.5` and put
     "shot after looking at <what>" in the verdict note, so `probe.py shots` scores it as a coin and the
     run log says why.
3. Run it. Install and execute inside `/Users/triton/PROTEUS/sandbox/`, write what you keep under
   `/Users/triton/PROTEUS/experiments/YYYY-MM-DD-P-00NN/` (a README.md with the question, method,
   numbers and what you did not do; the script; a results.json if there are numbers). `sandbox/*/` is
   gitignored, `experiments/` is not.
4. Verdict:
   `python3 /Users/triton/PROTEUS/bin/probe.py verdict P-00NN --verdict works --note '...' --artefact /Users/triton/PROTEUS/experiments/YYYY-MM-DD-P-00NN`
   It writes PROBES.md, the run-log line and commits. Use single quotes if the note has a `$`.

## What makes a good verdict

- **A number nobody had.** "Installs and runs" is the weakest works there is. Test a claim the tool or
  video makes: the speed it promises, the count it says, the result it shows. The audit found about 19
  harvest probes that stopped at install; do not add to them.
- **The note says the measured thing first**, then the comparison (theirs v mine), then the caveat.
- **Every works note ends with the next step**: `Next: promote (to a desk or standing job) | deepen
  (queue P-... with what) | close (nothing more to learn)`. Queue a deepen with
  `probe.py add "..." --source desk --est 20`.
- **blocked** needs `--needs "what exactly"`; add `--luke` only when the need is Luke's hands.
- **not-worth-it** says why in one measured sentence.

## Traps seen before

- `$` inside double quotes is denied by the hook; single-quote notes.
- `git clone` and `npm install` without the sandbox form are denied; fetch a tarball with Python, or
  `npm --prefix /Users/triton/PROTEUS/sandbox/<x> ci|install --ignore-scripts --cache /Users/triton/PROTEUS/sandbox/.npm-cache`.
- A denial is a result. Note it, route around it or stop; never retry it verbatim.
- A probe scoring a long-running job gets `--after YYYY-MM-DD` when added; the queue has no edit command.
- YouTube rate-limits this IP after bursts; see the `transcribe-video` skill.
