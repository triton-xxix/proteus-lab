# P-0264: the martingale grid, simulated

From H-0455 (a reel selling a $159 MT5 grid bot for gold on the strength of one green day). Question:
what share of days are green, and how big is the worst day against the average win?

`grid.py`, stdlib only, 3000 simulated days per setting, driftless geometric random walk on 1-minute
steps, no spread or swap (both would make every number worse). Bot: long 1 lot at the day's first
print, add a position x2 every 0.3% lower, close the whole stack at average entry +0.2%, re-enter at
once; 12 levels sized so the full stack is the account's leverage; stop-out when the unrealised loss
equals the equity. Daily result is realised closes plus the open stack marked at the day's end.

## Result

| sigma | grid | mult | tp | lev | green (realised) | green (marked) | avg win | worst day | worst / avg win | mean day | 1st pct day |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1.0% | 0.30% | 2.0 | 0.20% | 20 | 98.0% | 82.3% | +0.030% | -5.22% | 175x | +0.001% | -0.56% |
| 1.0% | 0.30% | 2.0 | 0.20% | 100 | 98.5% | 83.6% | +0.159% | -13.10% | 82x | +0.033% | -2.27% |
| 1.0% | 0.30% | 1.5 | 0.20% | 20 | 96.4% | 75.0% | +0.221% | -10.00% | 45x | +0.006% | -2.66% |
| 1.0% | 0.50% | 2.0 | 0.30% | 20 | 89.9% | 72.2% | +0.010% | -0.67% | 66x | +0.000% | -0.11% |
| 3.0% | 1.00% | 2.0 | 0.50% | 10 | 98.5% | 80.4% | +0.034% | -8.89% | 262x | -0.001% | -0.52% |

- **The reel is right about the screen.** Counting only realised closes, the thing a dashboard or a
  reel shows, 98% of days are green. Mark the open stack to market and it is 82%.
- **The mean is zero.** On a driftless walk the bot has no edge, by construction: +0.001% a day in
  the base case. Green days are not profit, they are timing of recognition.
- **The worst day is 45 to 262 average wins.** Base case: the average green day makes +0.030% and
  the worst of 3000 days loses 5.22%, which is 175 days of winning gone in one. The 1st-percentile
  day alone (-0.56%) is 19 average wins, so a bad day arrives about every five months and costs a
  month.
- **No stop-outs in a single day**, because a 12-level 0.3% ladder needs a 3.6% fall and gold moves
  1% a day. The one-day failure the reel's commenters describe needs a multi-day trend with the
  stack carried overnight, which this daily-reset simulation does not model. That makes these tail
  numbers a floor, not an estimate.

## Verdict

Works, as a measurement: the "always green" claim is 98% true on a day-count and worthless as a
record, because the one day in several hundred costs roughly 175 of the others. Not a bot to run.

## Not done

Spread, swap, overnight carry of the stack, and a real gold price path. Each would push the tail out.
Real XAUUSD minute data would be the next step; Stooq's daily is keyless but minute bars are not.
