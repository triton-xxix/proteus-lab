# P-0090: two timing models, GEM and the Fabian 39-week plan, on free ETF data

Run 8 Oct 2026 00:02 BST, `p0090.py`, rules fixed in the docstring before the run, results in
`results.json`. Total-return ETF prices (Yahoo adjusted closes), index levels for the Fabian
confirmations, BIL as cash.

## GEM (Antonacci), June 2008 to October 2026, 220 months

| | GEM | SPY | 60/40 |
|---|---|---|---|
| CAGR | 8.5% | 12.4% | 8.7% |
| volatility | 12.5% | 15.5% | 9.6% |
| Sharpe | 0.72 | 0.83 | 0.92 |
| max drawdown | 21% | 42% | 25% |

Switches 1.85 a year (claimed about 1.5); 144 months in SPY, 39 in EFA, 37 in bonds. The claims
that free data can reach reproduce: the 21% drawdown (claimed 21.7%), the lag since 2010 (8.4% a
year against 14.2% for SPY; claimed about 9.5% against over 14%), and 2008 (+6.7% against -28.5%).
What the paper's 1971 start hides: 2018 was worse than SPY (-7.6% against -4.6%) and 2022 only
slightly better (-16.9% against -18.2%, in bonds while bonds fell). Joint monthly shuffle, 1,000
draws: p 0.13. On this span GEM does not beat luck, and 60/40 beats it on every risk-adjusted
line.

## Fabian three-index 39-week plan, 1993 to 2026, 1,720 weeks

| | Fabian | SPY | 60/40 (from 2002) |
|---|---|---|---|
| CAGR | 7.6% | 10.9% | 8.7% (Fabian 7.1% on the same span) |
| volatility | 10.6% | 17.1% | 10.1% |
| Sharpe | 0.75 | 0.69 | 0.88 (Fabian 0.71) |
| max drawdown | 25% | 55% | 31% (Fabian 19%) |

In the market 66% of weeks, 44 round trips in 33 years. It does what the video said: it misses
the worst drawdowns (25% against 55%) and gives up a third of the return for it. Joint weekly
shuffle of the three indices and SPY, 1,000 draws: p 0.041, so the 39-week filter is a real
trend signal on this span, narrowly. Against 60/40 on the same weeks it loses on Sharpe with the
same volatility, and wins only on drawdown.

## Verdict

**works** as replication: every checkable claim lands within a point or two. Neither model earns
a book: GEM fails the shuffle and both are beaten by a static 60/40 at the same risk. The one
thing either buys is a shallower worst drawdown, which is a preference, not an edge. Nothing
queued.
