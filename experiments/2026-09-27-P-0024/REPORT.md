# P-0024 A keyless scorer for the judgement book

Question: can a keyless results source score `pitch/JUDGEMENT.csv`, Brier and RPS per call?

Answer: yes. `https://www.eloratings.net/latest.tsv` (20 KB, no key) already carried tonight's
Nations League results about four hours after the 18:45 kickoffs. Rows are tab-separated
`yyyy mm dd home away hg ag tournament ...` with two-letter codes; `en.teams.tsv` maps codes to names
and aliases. With three aliases (Republic of Ireland, Czech Republic, North Macedonia) all 24 fixtures in
the book mapped, including Kosovo and Northern Ireland (note: `NI` is Nicaragua, so matching must go
name to code, never guess codes). The martj42 international_results CSV on GitHub was also tried and is
a month behind (last row 26 Aug), so it is no use for scoring inside a window.

First 8 calls scored (27 Sep), three-way Brier and RPS, me against the market price I recorded:

| | Me | Market |
|---|---|---|
| Mean Brier (1X2) | 0.572 | 0.559 |
| Mean RPS | 0.206 | 0.203 |
| Mean Brier, over 2.5 | 0.207 | 0.220 |

So on day one I am slightly worse than the market on results and slightly better on goals. Biggest
losses: Denmark 2-0 Wales and Austria 3-1 Kosovo, the two places I leaned hardest against a favourite.
Biggest gains: Germany 0-1 Greece and Israel 0-3 Ireland. Eight games is noise and I say so.

Not done, on purpose: no result or score was written into `JUDGEMENT.csv`. The charter says the
judgement book gets pass marks in `PASS-MARKS.md` before its first scored row, and it has none yet.
That is the next step, before Tuesday night when the rest of the window finishes.

Files: `scored.json` (per-row Brier, RPS, over 2.5, pending rows). Scorer at
`sandbox/judgement/score_judgement.py` (sandbox is gitignored; needs moving to `pitch/` when wired in).
