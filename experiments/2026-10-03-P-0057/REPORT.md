# P-0057: skill reference files over 100 lines without a contents list

Ran 2026-10-03, `sandbox/p0057/scan.py`, read-only over `~/.claude/skills`, `~/.claude/plugins` and
this repo's `.claude/`. Raw result `result.json` beside this file. Source: harvest H-0116, the skill
authoring guidance that a reference file over 100 lines should open with a contents list so a model
reading a partial preview still sees what is in it.

| Measure | Value |
|---|---|
| Skill folders with reference files | 31 |
| Reference markdown files (not SKILL.md) | 335 |
| Over 100 lines | 184 |
| Over 100 lines with no contents list in the first 40 lines | 170 (92%) |
| Median length of the long ones | 176 lines |

Worst: hyperframes-animation 58 files, hyperframes-creative 13, media-use, skill-creator and
command-development 8 each. Longest without one: media-use `media-treatment-recipes.md` 929 lines,
command-development `interactive-commands.md` 920.

Detector: a heading named contents, index or similar, or three or more `[..](#anchor)` lines, in the
first 40 lines. Heuristic, so the 92% is an upper bound; one flagged file (pdf `REFERENCE.md`, 612
lines) checked by eye and it has none.

What it does not tell me: whether a missing contents list actually changes what a model reads. That
would need a trigger test, not a count. None of these are Proteus's own files to edit except any
under this repo, and there are none among the long ones.
