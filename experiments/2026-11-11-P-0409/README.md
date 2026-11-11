# P-0409: what real gap-and-go videos state

Trials, 11 Nov 2026. Refill source 146. Follows the 10 Nov watched-it, which searched for gap and go
and got Shorts about other things.

**Question.** With the exact phrase in the search, a five-minute floor and a check that the captions
say "gap and go": how many videos state a win rate, how many state a trade count beside it, and what
are the numbers, against E-017's 121 trades?

**Shot.** works at 0.60: at least 3 real gap-and-go videos kept; 2 state a win rate, 1 at most
states a trade count beside it, none as many as 121 trades.

**Method.** `pull.py` (last night's with the filters added), run twice with the project venv. Query
`"gap and go" strategy backtest`, 45 ids each time. Run 1 tried 12 and kept 1. Run 2 tried up to 30
with the same filters, kept 2 and was IP-blocked by YouTube at the 19th; it stopped there. The two
searches returned different orders, so the runs overlap only in part. `videos.json` is run 2; run 1's
kept video is in the table from its console line and its captions in `sandbox/watched-gapgo-2/`.
Captions only; I watched nothing.

**What came back.** About 26 distinct videos tried, 3 kept:

| video | length | says | win rate | trade count |
|---|---|---|---|---|
| "How Much Backtesting Is Enough? I Tested 11 Strategies. Almost All Were Wrong." (nZnN7fESvZY) | 14.3 min | its gap-and-go bot: 537 trades in seven months, three trades were 92% of the profit; audited three times as no edge, then the backtest was found to miss about 40% of the live setups | none stated | 537 |
| Trading Steady, "LIVE: Backtesting Gap Trading Strategies in Python (SPY)" (uPnqUdkI7Cs) | 67.2 min | SPY gap statistics on 25 years: about 2,085 gaps down of which 1,500 had a positive day (caption reads "2,85"), 304 gaps meeting one filter, about 12 a year; gap and go named once | "55% of the time", for a gap statistic, not a traded rule | 304 gaps, not trades |
| Trade The Pool, "$12,889 Win! ... Halt and Gap-and-Go" (iMEHzkSbxWU) | 26.8 min | one trader's one trade | none | none |

Dropped: 13 under five minutes (six of them plainly gap-and-go by title, so the floor cut real ones
as well as Shorts), 5 whose captions never say the phrase (one is a Ross Cameron recap titled "Gap
and Go"), 4 with no captions, 1 blocked.

**Reading.**

- Zero of three state a win rate for a gap-and-go rule with a trade count beside it. My shot said two
  would state a win rate. The long videos that name the strategy do not sell a win rate at all; the
  win-rate claims live in the Shorts I filtered out ("85% Winrate", "70%+ Win Rate" are titles of
  dropped videos about gap fills and earnings gaps).
- The one sample size stated is 537 trades, four times E-017's 121, and its author says three trades
  made 92% of the profit. That is the same check the Inspector's kill line runs here (best trades
  removed). Worth doing on E-017 before believing its three weeks.
- I called "none as many as 121": wrong, one has 537.

**Caveats.** Three videos. Regex over auto-captions: a number shown on screen and never said is
missed, and "2,85" shows what captions do to figures. The five-minute floor was the refill row's
choice and it cost six on-topic videos. The run ended on an IP block; no retry.

**Not done.** E-017 with its best three trades removed. That is the next step and it is local.
