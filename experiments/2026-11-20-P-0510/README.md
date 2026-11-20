# P-0510: Elo plus Poisson on international results, scored on the 2022 World Cup

Question (harvest H-0709): does an Elo plus Poisson model beat uniform on the 2022 World Cup's
3-way Brier score?

Called shot (d61ff75d): works at 0.85, Brier about 0.58 against uniform 0.667.

## Method

`model.py`, standard library only. Data: martj42/international_results `results.csv` (keyless raw
GitHub, 3.8 MB). Elo in the eloratings.net style (K 60 World Cup, 50 continental finals and Nations
League, 40 qualifiers, 30 other, 20 friendlies; goal-difference multiplier; +100 home unless neutral)
over every match before 20 Nov 2022, then frozen. Goals per side from the Elo gap by Poisson
regression on 16,104 team-games (2010 to 2022, no friendlies): log mu = 0.187 + 0.769 x (gap/400).
Three-way probability from two independent Poissons. Scored on all 64 matches; the CSV's scores
include extra time, so a knockout level after 120 minutes counts as a draw.

## Numbers

| model | 3-way Brier, 64 matches |
|---|---|
| Elo plus Poisson | 0.617 |
| base rate (listed-home side, World Cups 1998 to 2018: 44% / 24% / 32%) | 0.646 |
| uniform | 0.667 |

Log loss 1.054. The favourite won 35 of 64. Elo before the tournament: Brazil 2231, Argentina 2196,
Netherlands 2110, Spain 2105, Italy 2066 (Italy did not qualify).

So it beats uniform by 0.050 and the base rate by 0.029. My called number (0.58) was too optimistic:
2022 had Saudi Arabia over Argentina, Japan over Germany and Spain, Morocco's run.

## Not done

No market comparison (no stored 2022 odds here), one tournament only, no draw inflation (independent
Poissons under-call draws), no tuning. Relevance: the judgement book (F-0104) has no international
model; this is a ready blind column for the March 2027 window if it earns one.
