# P-0526: Nations League draw rate by competition and matchday

Why: P-0518 found the judgement book holds 18 draws in 57 (32%) while the 2010-22 history it was
fitted on draws 21.9%. The book is mostly Nations League. Is the competition itself drawier?

## What I ran

`draws.py` on `sandbox/intl-results.csv` (martj42 results, last row 17 Nov 2026), no network.
NL group stage is NL matches June to November of even years 2018 to 2026; matchday is the rank of
a team's date within its edition. Qualifiers and friendlies are UEFA v UEFA only. `results.json`.

## Result

| Competition, 2018-26 | Matches | Draws |
|---|---|---|
| Nations League group stage | 768 | **25.3%** (se 1.6) |
| last matchday (either side's last) | 144 | 27.8% (se 3.7) |
| earlier matchdays | 624 | 24.7% (se 1.7) |
| NL finals and play-offs | 46 | 19.6% |
| World Cup qualifiers, UEFA v UEFA | 462 | 19.0% |
| Euro qualifiers | 501 | 17.0% |
| Friendlies, UEFA v UEFA | 479 | 26.3% |
| All non-friendlies 2010-22 (P-0518's base) | 8,132 | 21.9% |

By matchday 1 to 6: 22.8, 22.7, 29.2, 30.7, 19.6, 25.9%. No rise towards the end.

## What it means

Nations League group games draw about as often as friendlies and 6 to 8 points more than
qualifiers between the same teams. A model fitted on all competitive internationals underrates
NL draws by about 3.4 points before anything else. The last-matchday idea does not hold up: 3.1
points higher, under one standard error. The book's 32% is still above 25% (18 of 57 against an
expected 14.4; about a 1.2 se excess), so part of it is the competition and part looks like luck.

## Verdict

Works. Next, if the judgement book's blind column wants it: a competition-specific draw multiplier
(about 1.15 for NL group games) beside P-0518's 1.04, fitted on 2018-24 and scored on 2026.
