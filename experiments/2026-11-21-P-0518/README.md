# P-0518: does a draw bump close P-0511's gap to the market?

**Question.** P-0511's Elo plus independent Poisson scored 0.043 Brier behind the market on the
judgement book. Independent Poissons are said to under-call draws. Fit one draw multiplier and
rescore: how much of the gap closes?

**Method.** `draw.py`: P-0511's Elo, Poisson fit and scoring unchanged. Draw probability times m,
renormalised; m fitted by 3-way log-likelihood over 8,132 non-friendly internationals 2010 to 2022
(Elo before each match), grid 0.80 to 2.00 in 0.02. Fixed the "Bosnia & Herzegovina" alias, so 57
of 57 scored rows are used now (P-0511 used 55). Data: `sandbox/intl-results.csv`, `pitch/JUDGEMENT.csv`
as of 21 Nov 2026.

**Called shot:** works at 0.70; the bump closes under a quarter of the gap, model Brier 0.570 to
0.580, still behind the market.

## Numbers

- **The Poisson barely under-calls draws**: it predicts 21.3% on the fit set, the actual rate is
  21.9%. The fitted multiplier is **1.04**.
- 57 rows, 3-way Brier: model **0.5889**, with the bump **0.5869**, me anchored 0.5536, market 0.5469.
- **Gap closed: 4.8%** (0.0020 of 0.0420).
- 33 blind rows: model 0.5922, bumped 0.5892, my blind 0.5682, market 0.5597.
- The book has 18 draws in 57 (32%), well above the 22% the history fits to. That is where the
  model loses, and a multiplier fitted on history cannot see it.

## Shot v measured

"Under a quarter of the gap": hit (4.8%). "Brier 0.570 to 0.580": miss, it landed at 0.587, because
with the alias fixed the base model sits at 0.589, not 0.581.

## What it says

The draw term is not the model's problem; the folklore that independent Poissons under-call draws
holds here only by half a point. The 0.04 gap is the model's ratings, not its shape. The book's draw
run (32%) looks like small-sample luck or Nations League dead rubbers; 57 rows cannot tell.

## What I did not do

- No Dixon-Coles low-score correction, only a flat multiplier.
- No tuning of K or home advantage, no market-implied Elo.
