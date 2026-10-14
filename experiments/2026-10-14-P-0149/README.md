# P-0149: the 7 KOLs' trades against the Grinder's pick time

14 Oct 2026, Trials. Leg three of P-0128 (overlap), P-0134 (spam), P-0141 (re-count: 7 of 9 survive, all
51 in-window transactions KOL-signed). No RPC calls; everything comes from P-0141's results.json.

**Question.** Place each of the 51 KOL-signed trenchcat and Normie trades before or after the Grinder's
pick (G-0072, G-0074, both 11 Oct 22:28:10Z) and classify buy v sell from the token delta. How many of the 7
KOLs were net buyers before the pick and net sellers after it?

**Called shot.** works at 0.50; 1 of 7. A coin, called after seeing the deltas and first/last times in
P-0141.

## Method

`timing.py`: for each KOL token account, each in-window transaction's time against 22:28:10Z and its
balance delta (positive buy, negative sell). Net before, net after, net total inside the window.

## Numbers

| KOL | pick | trades | before pick | after pick | net before | net after | net in window | shape |
|---|---|---|---|---|---|---|---|---|
| Naruza | trenchcat | 8 | 8 | 0 | 0 | | 0 | round trip, out 20 min before the pick |
| CoCo | trenchcat | 3 | 3 | 0 | 0 | | 0 | round trip, out 21 min before |
| bandit | trenchcat | 4 | 4 | 0 | 0 | | 0 | round trip in 13 s, 23 min before |
| Gasp | Normie | 7 | 7 | 0 | -8.05m | | -8.05m | sold out in 12 s, 55 min before |
| West | trenchcat | 16 | 8 | 8 | +15.1m | -15.1m | 0 | **bought before, sold after** |
| Nyhrox | Normie | 11 | 6 | 5 | +4.35m | -13.6m | -9.29m | **bought before, sold after** |
| Yami | trenchcat | 2 | 0 | 2 | | 0 | 0 | round trip 20 to 24 min after |

- **2 of 7** (West, Nyhrox) were net buyers before the pick and net sellers after it. Shot said 1.
- 36 of the 51 trades were before the pick, 15 after. Four KOLs had finished trading 20 to 55 minutes
  before the Grinder picked, and all four left flat or short of the token. Only one KOL (Yami) started
  after the pick, and was flat again within four minutes.
- 5 of 7 are flat inside the window: in and out. Nobody was a net buyer across the two hours.
- West's 16 trades net to zero to the token unit: 15,148,115.38 in before, the same out after. Scripted.

## What it says

In this one batch the Grinder's pick landed after the KOL money had mostly left. Of the seven KOL accounts
that touched the two picks in the two hours, four were out before the pick, two sold into the half hour
after it, and none held at the end. If this repeats, KOL overlap is a sell signal for the Grinder's picks,
not a buy signal; one batch does not settle that.

## Caveats and not done

Window-only: positions held from before 21:23Z are invisible, so "flat" means flat inside the window.
"Net seller" is in tokens, not SOL; no prices here. One batch, two picks, seven wallets. Programs
(FLASHX8Dr, GMGNreQc, pAMMBay6, term9YPb) still not decoded. A second batch is queued.
