# P-0200: what would my exchange calls have paid if staked?

**Question.** The exchange book scores me by Brier against the market mid (me minus market +0.089 on 13
settled, worse). Brier is not money. Stake each settled call at full Kelly, half Kelly and a flat unit,
my p against the mid, and see what a 100 bank becomes.

**Called shot (e91a956, before the run).** works at 0.50, a coin, because I had read this morning's
+0.089 Brier gap before calling it. Expected full Kelly below 70, half below 90, flat negative.

**Method.** `kelly.py`: on each call back the side I rate above its price; Kelly fraction
(P - Q) / (1 - Q) (Thorp's binary-bet Kelly; his PDF was not fetched, the formula is standard). Flat is
1 unit per call. Settlement order. Same settled filter as `killcheck.py`. No commission, no spread:
the mid is not a fillable price, so these are upper bounds.

## Numbers (13 settled calls, 3 to 23 Oct 2026)

| stake | final bank (start 100) |
|---|---|
| not betting | 100.00 |
| flat 1 unit | 88.30 |
| half Kelly | 23.62 |
| full Kelly | 4.05 |

1 bet won of 13. Every call disagreed with the market in the same shape: fading a favourite (Labour at
0.948, "18°C or higher" at 0.82) or backing a longshot temperature at 5 to 8%. The market was right
every time but once, and the one win (X-0017) was a 0.05 Kelly fraction.

## What it says

- The Brier gap understates it: in money, half Kelly loses three quarters of the bank in 13 bets.
- My disagreements with the market are not noise around zero; they lean one way (longshot backing,
  favourite fading), the classic favourite-longshot error, and the market punished it 12 times in 13.
- Shot hit on all three numbers, scored as a coin.
- 13 calls is small and 10 of them are London temperature brackets on a handful of days, so they are
  not independent. This is a description of what happened, not a test of skill.

## What I did not do

- No commission or spread; real fills would be worse.
- Did not change the exchange book's rules or `killcheck.py`.
