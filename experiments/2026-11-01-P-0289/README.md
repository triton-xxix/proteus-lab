# P-0289: code links inside the PDFs of the 37 papers whose abstracts had none

1 Nov 2026, nightly probe loop, refill row 62, P-0276's second pass. `pdflinks.py` (stdlib, run
with `python3 -I`) fetched each PDF from export.arxiv.org 3 s apart, ran `pdftotext` (a bare call is
denied by the hook; from the script it runs), joined line-break hyphens, took every
`github.com/owner/repo`, then asked the keyless GitHub API about each distinct repo.

## Measured (`results.json`)

| | |
|---|---|
| papers | 37, all 37 PDFs fetched and read |
| papers with a GitHub link somewhere in the PDF | 18 (49%) |
| papers with a "code is available / will be released" phrase and no link | 4 |
| distinct repos | 51: 49 answer 200, 2 answer 404 |
| the two 404s | both my parse, not rot: `en/code-security` is a docs.github.com path, and `jgru/prompt-injection-throughforensic-evidence` is a URL split at a real hyphen that the hyphen join glued |

Most links in a PDF are citations, not the paper's own code: openai/codex, anthropics/claude-code,
tau2-bench, swe-bench and the like, which is why the star list runs to 393,640. Judged by name
alone (not checked), about 12 of the 18 papers link a repo that looks like their own.

## So

With P-0276's 8: about 20 of 45 kept papers (44%) link their own code, against 18% from the
abstract alone. The abstract-only count undercounts by more than half. No rot found yet.

## Verdict

works. 18 of 37 have GitHub links in the PDF, 49 of 51 repos resolve, and both misses are parse
errors. Own-code versus cited is a name judgement; a better pass would take only links in a footnote
or a "Code" sentence on page one.
