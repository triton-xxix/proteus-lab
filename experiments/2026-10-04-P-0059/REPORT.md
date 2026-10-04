# P-0059: answer-me-with-html, Markdown to one-page HTML

Harvest H-0119. Repo QingYunA/answer-me-with-html v0.4.7, fetched as a tarball (`fetch_repo.py`) into
`sandbox/p0059/`. The skill ships a bundled single-file CLI, `skills/answer-me-with-html/scripts/am.mjs`
(306 KB), so no npm install was needed. Node only.

## What I ran

`run_probe.py` renders three drafts three times each with `am render ... -o ... --no-open`, AM_HOME
pointed into the sandbox: the repo's two examples and my own 91-word draft (`draft.md`) with a table
and a fenced `flow` block I wrote without reading the component docs.

| Draft | Words | Seconds (3 runs) | HTML bytes | SVG | External refs |
|---|---|---|---|---|---|
| tcp.en | 237 | 0.35, 0.35, 0.39 | 32,806 | 2 | 0 |
| architecture | 183 | 0.37, 0.35, 0.35 | 32,504 | 2 | 0 |
| my draft | 91 | 0.34, 0.35, 0.33 | 26,740 | 1 | 0 |

My flow block came out as a laid-out SVG with all four nodes. Every page is self-contained: no
`src` or `href` to any http URL.

## Verdict

Works. Under half a second per page, offline, zero external references, and a guessed diagram syntax
rendered first time. What I did not test: the README's 7.4x output-token claim, which needs model
calls on both arms. The mechanism (model writes ~100 words of Markdown, a deterministic renderer
writes ~30 KB of HTML) makes the direction obvious; the size of the saving depends on how much HTML
the model would otherwise type.

Denial on the way: `/usr/bin/time` is not on the safe list; timing moved into the Python harness.
