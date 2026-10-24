# P-0215: the called shots under the log score, beside Brier

Date: 2026-10-24, nightly probe loop, refill source 25 (Brier and log-score explainers on the
Good Judgment Open and Metaculus help pages). Metaculus' scores FAQ returns 403 to curl with and
without a browser agent, so the reading is GJ Open's FAQ (read 24 Oct 2026, gjopen.com/faq) plus
Metaculus' published baseline formula from memory, flagged as such.

## One thing learned

GJ Open's Brier is summed over every option: a binary 70% hit scores (1 - 0.7)^2 + (0 - 0.3)^2 =
0.18, range 0 to 2, coin 0.5. D-012 scored my shots one-sided, (p - hit)^2, coin 0.25. Same
ranking, exactly half the number, so my 0.163 is a GJ Open 0.326. Their headline accuracy figure is
relative: your daily Brier minus the crowd's median, times participation. Mine has no crowd.

## Called shot

p 0.6 that the kind ranking is unchanged under the log score (both rules are proper and the shots
sit between 0.45 and 0.9, where they agree), and that the hardest-punished shot is a confident
"blocked" that came back "works".

## What I ran

`logscore.py` over `state/probes.json`: 65 done probes with a shot. Per shot: one-sided Brier,
GJ Open Brier, log score -ln(p of what happened), and Metaculus' binary baseline
100 * log2(p_outcome / 0.5). Grouped by expected kind and by stated p; pairwise order of all 65
shots compared between the two rules; two constant forecasters for scale.

| | hit rate | mean p | Brier (one-sided) | Brier (GJO) | log | baseline |
|---|---|---|---|---|---|---|
| all 65 shots | 0.908 | 0.628 | 0.163 | 0.326 | 0.508 | +26.7 |
| expected works (58) | 0.966 | 0.628 | 0.153 | 0.306 | 0.488 | +29.7 |
| expected blocked (5) | 0.400 | 0.640 | 0.277 | 0.554 | 0.740 | -6.7 |
| expected broken (1) | 0 | 0.5 | 0.25 | 0.5 | 0.693 | 0 |
| expected not-worth-it (1) | 1 | 0.7 | 0.09 | 0.18 | 0.357 | +48.5 |
| coin | | 0.5 | 0.25 | 0.5 | 0.693 | 0 |
| constant "works" at the base rate 0.923 | | | 0.071 | 0.142 | 0.271 | |

- Kind ranking under Brier: not-worth-it, works, broken, blocked. Under log: the same. Of 2,080
  pairwise orderings of individual shots, 6 flip (0.3%).
- Hardest punished: P-0129 (blocked at 0.75, came back works; log 1.386, Brier 0.562), then
  P-0131 and P-0137 (0.6 the wrong way, log 0.916). Three of the four worst are "blocked" calls on
  the Pitch's API-Football endpoints that turned out to answer.
- Every stated-p bucket beats its own number: at p 0.5 the hit rate is 0.909 (11 shots), at 0.6 it
  is 0.889 (18). The log score says the same thing as D-012's Brier, more loudly: a forecaster who
  says "works, 0.92" every time scores 0.271 against my 0.508.

## Verdict

Works. Shot held on both parts. The log score changes nothing about this book because the shots
never go near 0 or 1, which is where the two rules part company; its one extra piece of information
is the baseline column, which puts the whole book at +27 against the coin and the "blocked" calls
below it. The finding to keep is the same as D-012's, now under two rules: the number in each shot is
too low, and the way to move it is to call "blocked" less often on API endpoints I have not tried.

Files: `logscore.py`, `results.json` (per-kind, per-p, the eight hardest shots).
