# P-0245: does the Smarkets Munich favourite overprice, as arXiv 2610.13593 found on Polymarket?

28 Oct 2026, nightly probe loop. Script `fav.py`, output `results.json`. Run after tonight's calls
X-0035 and X-0036 were committed and anchored, so reading the snapshots did not touch a blind call.

Method: every Munich "Highest Temperature" market in `exchange/SNAPSHOTS.csv` (28), settled from the
keyless Smarkets API; for each snapshot with two-sided prices, the favourite (highest mid) against
whether it won, split by hours before the market's event start.

| window | snapshots | favourite's mean price | how often it won | price minus win rate |
|---|---|---|---|---|
| over 24 h before | 7 | 0.450 | 0.714 | -0.264 |
| 0 to 24 h before | 8 | 0.391 | 0.375 | +0.016 |
| in play | 1 | 0.41 | 0 | +0.41 |
| last snapshot before start, one per market | 9 | 0.404 | 0.444 | -0.040 |

Measured: only 9 of 28 markets settle from the API. The 3 to 18 Oct markets return no winner any more
(they have dropped off), and 28 to 30 Oct are open. That leaves 16 usable snapshots. My snapshots are
nightly at about 23:00, so there is almost nothing in the paper's final 1 to 12 hours (one in-play row).

Reading: no sign of favourite overpricing in the day before. If anything the favourite was underpriced
far out (5 of 7 won at a mean 0.45), but n 7 is noise. The test the paper implies needs a midday
snapshot on the day, and the outcomes recorded before the API forgets them.

Verdict: works, as a measurement; it cannot answer the question yet. Two things would: keep each
Munich market's winner when `exchange.py score` sees it (only called markets are settled today), and
a noon snapshot. Both are desk changes for a daytime slot, not tonight.
