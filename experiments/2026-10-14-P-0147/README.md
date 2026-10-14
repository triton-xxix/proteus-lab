# P-0147: a per-referee home-advantage offset in the Pitch's Dixon-Coles

Question (part two of P-0130, which found referees differ in cards but not, beyond chance, in home
wins): does a per-referee offset on the home side's scoring rate improve the model out of sample?

Rules are in `refterm.py`'s docstring, written before the run: ENG (E0, E1) and SCO (SC0), monthly
walk-forward from Aug 2023 (2022-23 as burn-in), plain desk objective v the same plus r[referee] on
log lambda_home with L2 2.0, unseen referees at 0; Brier on 1X2 and over 2.5, against Pinnacle's close.

Result (`result.json`), 3,664 test matches to Oct 2026, 98.8% with a referee already seen:

| | 1X2 Brier | over-2.5 Brier |
|---|---|---|
| plain | 0.61417 | 0.25411 |
| with referee offset | 0.61876 | 0.25694 |
| referee minus plain | +0.00459 (se 0.00129) | +0.00284 (se 0.00085) |
| on 2,818 rows with a close: plain / referee / market | 0.6104 / 0.6157 / 0.5867 | 0.2517 / 0.2550 / 0.2410 |

The offset makes the model worse, about 3.5 standard errors, in every division (E0 +0.0046, E1 +0.0059,
SC0 +0.0016). Even shrunk hard, a referee's past home margin is mostly noise, and fitting it moves the
team ratings too. This agrees with P-0130's permutation test (home-win rate p 0.048, borderline).

Shot said within plus or minus 0.001, no gain: the direction was right, the size was not; missed.
Side number: the plain model trails Pinnacle's close by 0.024 on 1X2 Brier here, which is the gap the
Pitch book lives with.

Next: close. Referee belongs on cards markets, which the desk does not trade.
