# P-0133, apisports injuries by date

Question: does one `/injuries?date=2026-10-17` call on the free plan return usable rows for the nine Pitch leagues?

Method: `run.py` reuses `pitch/apisports.py` (key, `LEAGUE_DIV`), makes one request, filters to league ids in `LEAGUE_DIV`, counts by division. Results in `results.json`.

Numbers: 1 request, no errors, 99 left of 100. 864 rows in all, 582 in the Pitch leagues across 34 fixtures (E0 76, E1 186, D1 114, I1 68, N1 50, SP1 46, F1 42). P1 and SC0 had none.
I called 30 rows; the real count is about 19 times that. A row is a player, not a fixture, and E1 alone is 186.

Not done: matching fixtures to the judgement-book list, checking player `type` (Missing Fixture v Questionable) against lineups, any use in the model.
