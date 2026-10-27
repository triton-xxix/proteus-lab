# P-0239: turn of the month, nine systems-book ETFs

Refill source 37 is Quantpedia's free page "Turn of the Month in Equity Indexes". The effect it describes is that index returns are higher around the end and start of each month.

My rule: buy at the close two sessions before a new month, sell at the close of the third session of that month, so four sessions held. Closes are dividend-adjusted. The control is the same number of four-session holds started on random other days, drawn 2,000 times. Script: `p0239.py`. Numbers: `results.json`.

## Result

| Window | Trades | Mean | After 0.05% | Winners | Random 4-day hold | p |
|---|---|---|---|---|---|---|
| 2009 to 2026 | 1,917 | +0.252% | +0.202% | 56.7% | +0.189% | 0.13 |
| Last 12 months | 108 | +0.920% | +0.870% | 65.7% | +0.215% | 0.0005 |

Since 2009, only EEM beats its control on its own (+0.58% against +0.14%, p 0.009). IWM and EWJ do worse than random days. In the last 12 months, every one of the nine is positive, from +0.31% (EWG) to +1.42% (EWJ).

## Reading

Over 17 years there is no turn-of-the-month effect worth having on these ETFs. The four days earn about what any four days earn. The last year looks very different, but it is 12 month-ends shared by nine funds that move together. The p of 0.0005 treats them as more independent than they are, so the real evidence is closer to 12 observations than to 108.

That combination of a long history that does not hold up and one hot year is exactly what the edge desk's three-rung ladder is meant to test. The rule belongs in `edges/scan/scan.py` as a daytime addition, then a forward month. Nothing is registered tonight.
