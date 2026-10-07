# D-systematic-pros: neurotrader888 GitHub

Verdict: Rich folder. 18 ideas from 10 repos: five complete, daily-ready and new to us, plus three testing frameworks we lack. No README states results; the only number is an in-sample Donchian lookback of 19 with profit factor 1.08 (mcpt/donchian.py).

Test first:
1. D-01 RSI-PCA walk-forward model: extends our one survivor (RSI dip-buying) to a multi-period model. Fix the eigenvector bug, train on 8+ years.
2. D-02 ETH minus BTC relative strength (CMMA difference): new cross-asset idea. Also run on sector ETF vs SPY pairs.
3. D-03 Hawkes volatility breakout: wait for volatility to compress, then follow the first spike. Complete rules.
4. D-04 Visibility-graph path length: 12-bar window, almost free to test on 28 ETFs.
5. D-05 Market-profile support/resistance penetration: written on daily BTC already.

Frameworks worth copying:
- Walk-forward permutation (mcpt/walkforward_donchian_mcpt.py): permute only bars after the training window and rerun the whole re-optimisation inside every permutation.
- Joint multi-market permutation (mcpt/bar_permute.py, list input): one shuffle across all markets keeps correlations. Needed for P-0084 and D-02; dates must match exactly.
- Meta-labelling with purged walk-forward (TrendlineBreakoutMetaLabel/walkforward.py): random forest trained only on trades finished before the fit date, taken if probability above 0.5. Could filter the RSI(5) book.

Not testable on free daily data:
- Hourly replications (D-01, D-02, D-03, D-13): need hourly BTC/ETH history, for example Binance exports. Daily versions are a different, lower-powered test.
- D-15 swing-structure engine: built for 1-minute BTC bars; the logic still runs on daily.
- D-14 permutation entropy and D-18 visibility forecast: no trading rule in the code.

Code problems noticed:
- RSI-PCA.txt lines 39, 114, 189, 241: evecs[j] takes a row, but eigh returns eigenvectors as columns. Not true PCA.
- flags_pennants.py (TechnicalAnalysisAutomation.txt lines 591, 604): pennant loops reuse stale flag.conf_x; lines 391, 441 project the trendline one bar too far.
- mp_support_resist.py (line 1506): a scalar gaussian_kde bandwidth scales the price standard deviation, so it is not ATR times 3.
- Every repo fills at the signal bar's close and sweeps parameters in-sample. No strict look-ahead found.
