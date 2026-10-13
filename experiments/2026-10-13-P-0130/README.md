# P-0130: do referees differ beyond chance, and would a referee term help the Pitch model?

Part one measured tonight. Part two (a referee term in the Dixon-Coles fit, scored by Brier and
over 2.5 against the closing line) not done: 30 minutes was the whole budget and the fit is a
separate build, queued as its own probe.

Called shot: works at 0.70, cards beyond chance (p under 0.01), home-win rate not (p above 0.1).
Measured: cards p under 0.0003 (0 of 4,000 draws), hit; home-win rate p 0.048, borderline, so the
second half of the shot missed.

## Method

`referees.py`: the Pitch desk's football-data cache, E0, E1 and SC0, seasons 2022-23 to 2026-27,
4,670 matches with a named referee; 68 referees with at least 20 games. Statistic: the
between-referee weighted sum of squares of each referee's mean (one-way ANOVA numerator).
Permutation test: referee labels shuffled across matches **within each division and season**, so
league and season levels cannot masquerade as referee effects; 4,000 draws; p is the share of draws
at or above the observed statistic. Four outcomes: cards a game (yellows plus reds), home-card bias
(home cards minus away cards), home win, over 2.5 goals. Output in `result.json`.

## Numbers

| Outcome | Stat | p | Top | Bottom |
|---|---|---|---|---|
| Cards a game | 705.3 | under 0.0003 | K Stroud 4.98, R Ricardo 4.72, E Bell 4.70 | A Kitchen 3.15, D Webb 3.15, S McLean 3.24 |
| Home-card bias | 271.4 | 0.034 | C Napier +0.40, E Bell +0.30 | A Muir -1.00, F Hallam -0.98 |
| Home-win rate | 21.9 | 0.048 | D Bond 0.59, K Clancy 0.55 | G Eltringham 0.28, L Doughty 0.28 |
| Over 2.5 goals | 22.0 | 0.49 | | |

## What it says

- Card counts are a referee trait: a 1.8-card spread between the strictest and most lenient
  referees over 20-plus games each, and no shuffle of 4,000 came near. That is the one number
  worth a card market, which the desk does not trade.
- Home-win rate differs at p 0.048 and home-card bias at p 0.034: real at the 5% line, weak, and
  with 68 referees a single such test proves little. Goals (over 2.5) show nothing.
- So a referee term in the goals model has little to find: the referee effect is on cards, not on
  goals or results. Part two is still owed, because "little" is not "none" and the Brier test is cheap
  once the fit exists.

## Not done

- Part two: the referee term in `pitch/models.py` (home advantage per referee), scored out of
  sample against the closing line. Queued.
- No correction for referees being assigned to particular kinds of match (big games to senior
  referees), which could produce a home-win difference without any referee effect.
