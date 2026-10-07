# Trading ideas register

Started 7 Oct 2026, after Luke asked for more ideas and frameworks from the YouTube channels we
follow. Four Sonnet readers went through 33 transcripts and ten GitHub repos and returned 100 ideas
and 31 methods. Their full output is in `state/agents/2026-10-07/yt-ideas-*.json`, merged in
`yt-ideas-merged.json`, with one digest each beside it. This file is the short list: what goes to
a probe, what does not, and why.

Every result is reported in three columns: does it make money, does it beat just holding, does it
beat luck (see P-0082 and P-0084).

## What was read

| Reader | Source | Ideas | With complete rules on free daily data | What it was mostly |
|---|---|---|---|---|
| A | Quantified Strategies, 16 videos | 44 | 23 | SPY and QQQ dip-buys sharing one exit |
| B | Kevin Davey and Perry Kaufman, 12 videos | 23 | 1 | Method; the strategy code is withheld for his book and masterclass |
| C | Algovibes, 5 videos | 15 | 0 | Intraday Nasdaq futures; the value is his debunking methods |
| D | neurotrader888, 10 GitHub repos | 18 | 5 | Code for patterns, volatility and walk-forward tests |

YouTube blocked transcript downloads from this Mac after about 30, so StatOasis, deltatrend, Top
Traders Unplugged, memlabs and neurotrader's own videos are still unread. They go to the next
interactive pull.

## Queued as probes

| Probe | Idea | Source | Why it goes first |
|---|---|---|---|
| P-0085 | The dip-buying family: Williams %R(7), slow stochastic, IBS, 5%-in-5-days, three lower closes, on SPY and the nine-ETF basket, each luck-tested, plus how often each trades on the same days as the RSI(5) book | A-03, A-04, A-16, A-22, A-24 | Reader A's best point: these are probably one trade seen ten ways. If so, they are not new edges, and the systems book already holds the trade. |
| P-0086 | Darvas box breakout on SPY: replicate 279 trades and profit factor 3.08, then luck test and basket | A-01 | The only complete breakout rule in the folder, with numbers to check |
| P-0087 | Calendar events on SPY since 1993: Fed decision days and the pre-Fed drift, jobs-report Fridays, the weak-Monday reversal, each against random days of the same length | C-05, C-06, A-05 | Nothing like it in our set; decades of events on free data against his 52 |
| P-0088 | Kaufman's efficiency ratio on the 28 ETFs: which markets trend, and does trading only the trendiest half (chosen on past data) improve P-0084? | B-01, B-11 | Feeds the one trend result we have, cheaply |
| P-0089 | A stricter luck test for the systems book: walk-forward permutation and a same-trade random-entry control on the RSI(5) basket | D framework, C framework | The book's backtest has passed the in-sample test only; these are the harder bars |
| P-0090 | Monthly timing models: Antonacci's global equities momentum and the Fabian 39-week model, replicated and luck-tested against 60/40 | A-13, A-12 | Complete rules, published records, one decision a month |

**Results so far.** P-0085 (7 Oct): their numbers replicated 5 for 5. The family is mostly the
RSI(5) trade again (75 to 97% overlap once the 200-day filter is added). The two "famous rules"
fail the luck test. IBS is the exception: its trades with no RSI(5) trade open average +0.51%.
The tradable version is queued as P-0091.
P-0091 (7 Oct): the tradable version passes narrowly (p 0.044 pooled, +0.27% a trade, US markets
only). The +0.51% was hindsight. Now systems book 2, judged after costs.

## Methods worth adopting (no probe needed, used from now on)

- **Same-trade random control** (Algovibes): run the identical trade on random days or entries many
  times and report where the real result sits. It complements the permutation test.
- **Freeze, then judge once** (Algovibes, Quantified Strategies): rank on the weaker of two periods,
  never retune on the judging period, and show the grid's median beside the winner.
- **Pessimistic fills** (Algovibes): when a bar touches both stop and target, count it a loss.
- **Only data after publication is clean out-of-sample** (Davey). That is why P-0082 split at 2009.
- **Joint multi-market permutation** (neurotrader): already used in P-0084.
- **Quit rules** (Kaufman and Davey: 12 months unprofitable, 1.5 times the backtest's worst
  drawdown). Not bolted onto the systems book, whose marks were fixed before its first trade.
  Kept for the next book.

## Parked, with the reason

- **Needs intraday data:** opening range breakout (C-01, C-02), jobs-report fade at 8:30 (C-04),
  Fed press-conference reversal (C-12), Davey's ES VWAP system (B-21), Kaufman entry timing (B-13).
  Free daily bars cannot test them; minute data costs money. Revisit only if a daily result points
  the same way.
- **Rules withheld:** Davey's 12-strategy micro portfolio (B-23), Quantified Strategies' Euro Stoxx
  exit (A-10) and their QSRSI formula (A-37).
- **Patterns** (head and shoulders, harmonics, flags: D-10, D-11, D-12): the code exists but has
  bugs reader D listed. Low priority.
- **RSI-PCA** (D-01): the code takes eigenvector rows where scipy returns columns, so it is not
  true PCA. Worth doing properly later, as an extension of the one survivor.

## Salesmanship, for the record

Every Quantified Strategies video ends on a pitch for their Skool group. Most Davey videos end on
his email list, book or masterclass, and "out-of-sample" in his titles means walk-forward on
developed data. Algovibes sells a research lab. None of that makes their numbers wrong. Quantified
Strategies' numbers have replicated three times out of three where the rules were given.
