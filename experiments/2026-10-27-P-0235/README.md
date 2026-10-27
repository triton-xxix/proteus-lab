# P-0235: IBS, close fills against next-open fills

The question came from tonight's watched-it item. Quantified Strategies claims 0.79% a trade for IBS, and my P-0091 replay made +0.27%. How much of that gap is the fill alone?

The test takes P-0091's signals without its gate: buy when IBS is below 0.2 at the close, sell after a close above yesterday's high. That is one signal set across nine ETFs from 2009, giving 4,430 trades. Each trade is filled four ways. Prices are unadjusted, as in the live book. Script: `p0235.py`. Numbers: `results.json`.

| Fills (entry/exit) | Mean a trade | After 0.05% | Winners | t |
|---|---|---|---|---|
| next open / next open (my book) | +0.272% | +0.222% | 65.3% | 7.66 |
| close / close (the videos) | +0.377% | +0.327% | 69.2% | 11.03 |
| close / next open | +0.345% | +0.295% | 66.6% | 9.21 |
| next open / close | +0.303% | +0.253% | 70.6% | 9.52 |

Close fills add 0.105 points a trade, about 39% more edge. Most of it comes on entry: the overnight gap after an IBS signal averages +0.02% to +0.14%. The gap is largest on EWJ (+0.14%), QQQ (+0.11%) and EEM (+0.11%), where the open lands after the bounce has started. EWJ and EFA roughly double or treble at the close (EWJ +0.16% to +0.38%). DIA is the one market where the close does not help (+0.38% to +0.36%).

## Reading

The fill accounts for about a fifth of the gap: +0.27% becomes +0.38%, against a claimed +0.79%. The rest has to come from elsewhere. Their exit adds IBS above 0.9, their SPY history starts in 1993, and their numbers may be survivorship-picked. A buy at the close is also not free in practice. It needs a market-on-close order sent before the close is known, using an IBS estimated a few minutes early.

For the book: its rule is pre-registered and stays as it is. A close-fill shadow column could be scored beside it, but it would need its own pre-registration in a daytime slot, not tonight.
