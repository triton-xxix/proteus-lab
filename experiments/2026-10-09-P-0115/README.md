# P-0115: founder-skill, do its Python unit-economics tools match a hand calculation? (9 Oct 2026)

Called shot: the arithmetic will be right; anything wrong will be in what it chooses to show.

Repo `jakeschincariol/founder-skill` (MIT) fetched as a tarball, unpacked to `sandbox/p0115-founder/`.
`skills/founder-cfo/unit_economics.py` is 270 lines of standard library, read in full before running.
I worked its own example (a matcha bar: 6.50 a cup, 1.74 variable, 26,540 fixed a month, 25,280
startup, ramp 140 to 292 cups a day) on paper, then ran the tool with `--json` (`compare.py`).

| field | tool | hand |
|---|---:|---:|
| contribution per cup | 4.76 | 4.76 |
| break-even cups a day | 185.85 (186) | 185.85 |
| margin at plan | 37.7% | 37.7% |
| year-1 revenue | 563,160 | 563,160 |
| year-1 operating profit | 93,926.40 | 93,926.40 |
| payback month | 8 | 8 |
| cash needed (deepest hole) | 34,092 | 34,092 |

8 of 8 match.

One thing to watch: "profit margin at your plan" uses `plan_per_day` (383 cups), but the year-1 ramp
in the same file never goes above 292. At 292 the margin is 26.6%, not 37.7%. The headline margin is
for a volume the business does not reach in the year being modelled, and the report does not say so.

Verdict: works. The calculator is correct and transparent; the board, CFO prose and the 100-persona
"consumer panel" are model guesses and were not part of this test.
