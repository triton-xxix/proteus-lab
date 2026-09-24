# P-0010: Wikipedia pageviews and Premier League results

**Verdict: works, and the spike follows the result, it does not precede it.** Pre-match attention says
nothing about whether a club beats its closing price (r = -0.015, CI -0.10 to +0.07, flat across quintiles),
so there is nothing here for the Pitch desk. After the match, views rise by a fifth on a loss and nearly two
fifths on a win (x1.21 v x1.38 the day after), and a shock win (two points or more over the price) nearly
doubles them (+0.67 log). Attention is a record of results, not a forecast of them.

Coverage caveat: only 14 of 20 clubs. The Wikimedia pageviews API returned 429 on the 15th to 20th call in
two runs, one with no pause and one with a one-second pause between calls, so it is a quota of about 14
per short window from this address, not a burst limit. Missing: Newcastle, Nottingham Forest, Sunderland,
Tottenham, West Ham, Wolves. Not rerun a third time. Rerunning later tonight or tomorrow should fill them.

14 club pages, 14 pageview calls in 24.4s, errors [('Newcastle', 'HTTP Error 429: Too Many Requests'), ("Nott'm Forest", 'HTTP Error 429: Too Many Requests'), ('Sunderland', 'HTTP Error 429: Too Many Requests'), ('Tottenham', 'HTTP Error 429: Too Many Requests'), ('West Ham', 'HTTP Error 429: Too Many Requests'), ('Wolves', 'HTTP Error 429: Too Many Requests')]. 569 team-matches from 1 Aug 2025 to 2026-09-20.

**Precede.** corr(abnormal views over the 3 days before, points minus closing-price expectation) = -0.015 (95% CI -0.097 to +0.068).

| pre-match attention quintile | n | mean abnormal log views | mean surprise (points) |
|---|---|---|---|
| 1 | 114 | -0.487 | +0.102 |
| 2 | 114 | -0.210 | -0.026 |
| 3 | 113 | -0.048 | +0.062 |
| 4 | 114 | +0.132 | -0.064 |
| 5 | 114 | +0.511 | +0.009 |

**Follow.** corr(abnormal views the day after, surprise) = +0.249 (95% CI +0.170 to +0.324).

| result | n | matchday abnormal | day-after abnormal (log) | day-after as a multiple |
|---|---|---|---|---|
| loss | 179 | +0.648 | +0.192 | x1.21 |
| draw | 162 | +0.539 | +0.145 | x1.16 |
| win | 228 | +0.602 | +0.325 | x1.38 |

Big surprises (|points - expected| >= 2, n=31): day-after abnormal +0.669 for shock wins, +0.194 for shock losses.
Median daily views across clubs: Man United 11864, Arsenal 10745, Chelsea 9294, Liverpool 9018, Man City 8248, lowest Burnley 1993, Fulham 2215, Brentford 2265.
