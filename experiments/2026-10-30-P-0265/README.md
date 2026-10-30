# P-0265: 20/50 moving-average crossover against buy and hold, daily BTC

From H-0460 (a vault thread on simple crossover bots). `ma.py` pulls Binance BTCUSDT daily closes
keyless (17 Aug 2017 to 29 Oct 2026, 3,361 days), runs long-or-cash on SMA20 > SMA50 with next-close
fills and 0.10% a side, and compares with holding (one fee). 10/30 and 50/200 run beside it so the
pair is not special-cased. Numbers in `RESULT.md`.

## Reading

- **Over the whole history the rule loses to holding on return:** 16.2x against 18.2x, CAGR 36.0%
  against 37.7%, after 74 round trips. It wins on pain: max drawdown 75% against 83%.
- **Last three years, the same shape and worse:** 2.0x against 2.3x (-4.9 points of CAGR), drawdown
  39% against 53%.
- **Last year it wins big** because BTC fell 29% and the rule sat in cash: +5.6% against -29.2%.
  This is the window a seller would screenshot.
- **Neighbours disagree with each other:** 10/30 beats holding over all history (+3.4 points) and
  loses by 16.6 points over three years; 50/200 loses in both. The 20/50 answer is not robust to the
  pair, so the pair is the fit, not the finding.

## Verdict

Not worth it as a return rule: after fees it trails holding in two of three windows and only beats it
in a down year, where any rule that goes to cash looks good. What it does reliably is cut the maximum
drawdown by about a fifth, which is a volatility choice, not an edge. Fees were not the deciding
factor: 74 trades at 0.2% round trip cost about 14% of the multiple over nine years.
