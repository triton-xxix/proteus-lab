# luck_test.py

Does a daily trading rule beat a shuffled market? One file, numpy only.

```
python3 luck_test.py prices.csv --rule rsi5 --perms 1000
python3 luck_test.py prices.csv --rule sma --n 200 --from 2009-01-01
python3 luck_test.py prices.csv --rule rsi2 --threshold 9
```

The CSV needs `date, open, high, low, close`. If it has `adjclose`, prices are scaled to total
return unless you pass `--price-only`. Yahoo's daily download has this shape.

## What it does

It shuffles the overnight gaps and the moves inside each bar separately, rebuilds the series, runs
the same rule on it and scores it the same way: the profit factor of the rule's daily log returns.
p is (1 + shuffles at least as good as the real series) / (1 + shuffles). The shuffle keeps the
drift and the size of the moves and destroys their order, so a rule that only rides the drift gets
a p near 0.5. Method after neurotrader888's mcpt (github.com/neurotrader888/mcpt, MIT).

`--from` scores from a date and starts the shuffles there, leaving earlier bars real, so you can
test whether an edge survived after it was published.

## Rules built in

- `sma`: close above SMA(n), long from the next open; close below, flat from the next open.
- `rsi5`: above SMA(200) and RSI(5) below 30, buy at the close; RSI(5) above 50, sell at the close.
- `rsi2`: above SMA(200) and RSI(2) below the threshold, buy the next open; sell at the close above
  yesterday's high.

To test your own, write a function `(o, h, l, c, args) -> daily log returns` and add it to `RULES`.
If you chose a parameter by sweeping, sweep inside the function and return the best, so every
shuffle gets the same search and the p-value pays for it.

## Checked against the original

The numba version in `experiments/2026-10-07-P-0082/p0082.py` produced the published results.
This one, run 13 Oct 2026 on the same SPY file (`sandbox/p0082/data/SPY.csv`), gives the same
real profit factor on every rule tried:

| Rule | Original PF, p | This script PF, p (shuffles) |
|---|---|---|
| rsi5, 1993 on | 1.513, 0.001 | 1.513, 0.0033 (300) |
| rsi5, 2009 on | 1.393, 0.037 | 1.393, 0.0365 (300) |
| rsi2 below 30 | 1.221, 0.017 | 1.221, 0.0166 (300) |
| sma 200 | 1.143, 0.057 | 1.143, 0.0679 (1,000) |

p differs a little because the random generator differs; with 300 shuffles the floor is 0.0033.

One honest note: the first draft of the `sma` rule used each day's signal one bar early. It scored
1.294 and passed at p 0.03. The check against the original caught it. A lookahead turned a fail
into a pass, which is the whole reason to test a rule against something.

No costs or slippage. Not advice.
