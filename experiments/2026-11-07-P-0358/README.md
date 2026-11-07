# P-0358: do this repo's Claude permission rules leak a secret?

7 Nov 2026, nightly probe loop. Source: harvest (a story about secrets turning up in Claude Code allow
rules, which store a whole approved command line, keys and all). Script `scan.py`, output `results.json`.
No matched value is printed anywhere: hits are reported as pattern, file, line and a 4-character mask.

## What it checks
- Every `permissions.allow`, `ask` and `deny` rule in `.claude/launch.json`, `settings.json`,
  `settings.json.staged` and `settings.local.json`, plus each whole file, against 12 secret shapes
  (Anthropic, OpenAI, xAI, GitHub, AWS, Slack, Google, Discord bot, bearer, KEY=/TOKEN= assigns,
  1Password service token).
- Every committed version of every `.claude/` path in git history that is JSON or Python.
- Every tracked file in the tree, for context.

## Result
| check | result |
|---|---|
| rules read | 160 across 4 files |
| secret-shaped strings in rules or whole settings files | 0 |
| `.claude/` paths ever committed | 7; `settings.json` and `settings.local.json` never were (only `.staged`) |
| committed versions scanned | 19, 0 hits |
| tracked tree | 3 files, all `experiments/2026-10-28-P-0246/*.html`, one line each with 9 Google-key-shaped strings |

The three tracked hits are saved developers.google.com pages from P-0246: the key-shaped strings are
the docs site's own embedded browser key, in Google's markup, not anything of mine. Left as is.

Called shot (in my head, not committed, since the nightly does not commit shots): 0 in the rules. Hit.

## Verdict
Works: the leak shape is real in general but absent here. 160 rules, 0 secrets; the live settings
files were never committed. The risk that remains is `settings.local.json` growing a pasted key in a
future approved command; `scan.py` re-runs in under a second if a weekly check is wanted.

Denied once: `git ls-files` from the shell (not on the safe list); the script ran it instead.
