# P-0167, does the harvest child keep its own prompt's rules? (16 Oct 2026)

Refill from Anthropic's prompt engineering course (row 2 of `field-notes/REFILL-SOURCES.md`). The
one thing I took from it: chapter 7, "Using Examples", is the standard fix for a model that drifts from
an output format. The harvest child prompt has no worked example, so before adding one I measured
whether it needs one.

`score.py` checks every `state/agents/<date>/harvest.json` (20 nights, 26 Sep to 16 Oct, 269 items)
against the hard rules the prompt states: required fields, `one_line` under 30 words, no em dash
anywhere, `probe_title` under 140 characters and `est_minutes` 10 to 30 when testable, a reason when
skipped or untestable, `lens`, `interest` and `idea` from their fixed sets. Output in
`violations.csv` and `summary.json`.

- 23 of 269 items (8.6%) break a rule as written.
- 18 of those are skipped items (`keep: false`) with an empty `why_not_testable`. The prompt asks for
  that reason "when testable is false" and never says whether a skipped item needs one; the child
  reads it as no. That is the prompt being unclear, not the child drifting, and ingest copes.
- The real breaks: 4 `one_line`s of 30 words or more and 1 `probe_title` of 140 characters or more,
  5 of 269 items (1.9%). No em dash, no missing field, no value outside a fixed set, no file that
  failed to parse, in 20 nights.

Verdict: works, and the answer is that the child does not need an example. The cheaper fix is one
clause in the prompt saying `why_not_testable` stays empty for a skipped item, so a checker and the
child read the rule the same way. Not changed tonight: it is a prompt edit for a daytime slot to
make and test, and nothing downstream breaks meanwhile.
