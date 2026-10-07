# A-quantified-strategies: digest

**Verdict:** 16 videos, about 12,000 spoken words, 44 entries. 23 have complete rules on free daily data, but most are short-term SPY or QQQ dip-buys sharing one exit, so they are one family, not many edges. The 14-minute survey is a catalogue with almost no rules.

**Test first:**
1. A-01 Darvas box breakout on SPY. The only complete breakout rule here; 279 trades, profit factor 3.08, era figures to reproduce, plus a same-exit random-entry control.
2. A-02 Williams %R(2) on 101 Nasdaq-100 stocks. Breadth is a better luck test than SPY; check the median profit factor of 1.57. Survivorship bias stated.
3. A-03 Williams %R(7) below -95 on SPY. 288 trades, profit factor 2.61, holdout 2.08. Shares the RSI(2) sweep's exit, which was not a survivor, so run the permutation test and measure overlap with the RSI(5) book.
4. A-05 Weak-Monday reversal (Monday closes below prior Friday's low, hold to Friday). Nothing like it in our set; claimed 0.6% a trade, but the figures do not reconcile.
5. A-04 Slow stochastic (7,3) below 25. 394 trades, profit factor 2.58 at the close, 2.47 at next open; run with A-03 as one family.

**Frameworks worth copying:**
- Frozen development and holdout, equal parameter budget, one common exit, grid median beside the winner (FXYI7n6XJlk). Their shortlist came from a full-sample ranking, which contaminates the holdout.
- Neighbourhood robustness: share of nearby settings passing, exit swaps, era splits, next-open delay, 10 and 20 basis point cost stress (5yq3TpRpzuM, 7RUVOGEtAe0).
- Event study against same-horizon unconditional drift (eTSkZScQVg0).

**Not testable on free daily data:**
- A-10 Euro Stoxx futures: per-contract P&L needs FESX data and costs; the cash index is a proxy, but the exit is withheld.
- A-37 QSRSI: formula unpublished.
- A-42 Sentiment: needs a named series and rules.
- A-43 VWAP and volume profile: needs intraday bars.
- A-44 Renko: needs tick or intraday data for realistic fills.

**Salesmanship noticed:**
- Every video ends with a Skool community pitch.
- The Euro Stoxx video withholds its exit for members; the survey says backtests are members-only and strategies are for sale.
- Titles lead with win rate, which the shared exit raises structurally. Costs are excluded almost everywhere.
- The channel's own QSRSI places second in its own ranking with no formula.
- The same 10.8% buy-and-hold figure is given for both SPY and QQQ.
