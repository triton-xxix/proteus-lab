# P-0122: anatomy's dial-indicator example, rebuilt with no npm install

Date: 2026-10-10, nightly probe loop. Source: harvest H-0202 (github.com/wheresryan22/anatomy, a Claude
Code skill plus a zero-dependency SVG kit for interactive technical figures).

## Called shot
Builds and passes its own check with no install: yes, about 70 percent.

## What I ran
- `fetch.py`: tarball from codeload (2.84 MB, no git clone) into `sandbox/p0122-anatomy/`.
- Read the build script first: it imports only the repo's own `kit/` and `scripts/` and writes two
  HTML files beside itself. No network, no package.json, nothing to install.
- "Its own audit": `kit/audit.mjs` is a geometry library, not a command. The repo's real check is its
  CI job, which rebuilds every example on Node 22 and fails if any committed page changes. I ran the
  same check for this example: copied the committed pages aside, ran `build.mjs` and `build.mjs --light`,
  compared bytes (`compare.py`).

## Result
| Page | Committed | Rebuilt | Same? |
|---|---|---|---|
| dark | 136,488 B | 136,488 B | identical (sha256 2ba95d49a543) |
| light | 136,489 B | 136,489 B | identical (sha256 bc1810e340d9) |

On Node v25.6.0, against CI's pinned 22. Each page is one self-contained file: 354 SVG paths, its own
animation script, and two URL strings (namespace references, no fetched assets).

## Verdict
Works. The example rebuilds byte-for-byte on a newer Node with nothing installed, which is what the
repo claims. What I did not test: whether the skill itself produces a good figure from a new idea.
That needs a Claude Code session driving it, so it is a daytime job, not a probe.
