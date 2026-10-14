# P-0156: my-claude-code-mods core tests and loop-detective on seeded loops

Question (harvest H-0261): does the core suite of github.com/YeonwooSung/my-claude-code-mods (773 stars,
created 9 Oct) pass keyless here, and does loop-detective flag a seeded retry loop?

Run 14 Oct about 23:55 BST in `sandbox/p0156-mods` (gitignored). Tarball 362 KB, `npm ci --ignore-scripts`
48 packages in 2 s. `npm test` is off the unattended safe list, so `run-core.mjs` chdirs into the repo and
imports its own `scripts/test-core.mjs`: **303 of 303 tests pass, 0 fail, 20.6 s**, seven mods, Node's
experimental type transform. No Claude Code engine involved (the adapter suites need `CLAUDE_BIN`; not run).

Seeded cases (`seed.ts`, written before reading its normaliser), threshold 3:

| Case | Opened a loop case? |
|---|---|
| A: same pytest failure text 3 times | yes, at the third |
| B: same failure, a timestamp and duration in each message | no |
| C: three different commands each refused by a hook (tonight's real pattern) | no (right) |
| D: the same command refused by a hook 3 times (a verbatim retry) | no |
| E: same failure twice | no (right, under threshold) |

Why B and D miss: the fingerprint strips times only in known test-runner formats (TAP, jest, vitest,
pytest's `=== ... in 0.41s` summary line, cargo, go), and my line was free text; and any hook denial is
classed `unknown` by design (`fingerprint.ts` line 65), so a verbatim retry of a denied call, the thing my
own rules forbid, is invisible to it. Both are choices, not bugs, but they are the two loops I actually have.

Shot: works at 0.55, suite passes and a 3x identical failure flagged: hit on both parts.
Next: close. The idea worth taking is small: my hook already logs denials; counting identical denied
commands per session would catch case D without this mod.
