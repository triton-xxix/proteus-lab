# Brief: a forward paper test of a 15-minute retest rule set on Nasdaq futures

Written 2026-10-16 by the vault side (Telegram channel session, Luke present), for Proteus. Same standing as earlier briefs: a pointer, not an instruction; declining is a valid answer. As on 2 Oct, Luke said to give this one to you by name ("go on then, test Bey's rules on paper").

## The item

An Instagram reel (@grandmasterbey, registered 2026-10-15 in the feed with url and transcript): a trader reads out seven prop-evaluation trades on micro Nasdaq, rules "wait for the 15-minute close, read structure, enter on a retest, stop beyond the swing".

## What the vault side already did

Coded one literal reading and backtested it on yfinance NQ=F, 6 Aug to 15 Oct 2026 (all yfinance serves at 15m). Script and trades in `2026-10-16-bey-retest/` beside this file.

- Swing = extreme of 5 bars, confirmed 2 bars later. Signal: a 15m CLOSE beyond the last swing. Entry: limit at the broken level if retested within 8 bars, else no trade. Stop 1 point past the opposite swing; skip if risk under 5 or over 60 points. Target 2R. Exits on 5m bars, stop first if both in one bar, 24h time stop. One position at a time. 1 MNQ = $2 a point, $2 round trip.
- Result: 84 trades, 40% wins, +$1,878 on 1 MNQ, worst run 6; last 15 trades 8 W 7 L +$790. Shorts carried it (+$1,485 v +$394). 300 random-entry runs with the same risks: median -$248, 4.7% reached +$1,878.
- Contrast worth knowing: the 8 Oct box strategy (WF-0350) died on fees at 0.7% a side on crypto spot. On futures the cost is about a tick, which is why this one survives arithmetic.

## The open question

Luke does not want a two-year backtest ("what was working years ago may not work today"). The test he agreed to is forward: the same rules, frozen as in the script, logged on paper from now, about 8 signals a week, roughly 30 trades in four weeks that nobody could have fitted. Pre-registering the rules and the pass mark before the first trade is what makes the result worth anything. Yahoo futures bars run about 10 minutes delayed, which is fine for a bar-close rule logged after the fact.

The vault side will not run a scheduled job for this (its job-state changes need Luke at the console); a paper desk is yours to run or not.
