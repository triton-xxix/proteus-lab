# Grinder fill check, 6 Oct 2026

Luke asked whether the Grinder's better week was real. The worry: v0.2 books a take-profit the
moment any one-minute candle's high touches 2x, and a wick can be a single trade. `fillcheck.py`
re-walks every closed v0.2 position (44, all with saved candles) under three stricter fills, same
stops and the same cost model (`paths.pnl_v02`: pool fee, price impact, slippage).

| Rule | What it demands | All 44 | 25 to 28 Sep (16) | 29 Sep to 5 Oct (28) |
|---|---|---|---|---|
| touch (as booked) | high touches 2x | +£392, 19 wins | -£263, 4 | **+£655, 15** |
| close | minute closes at or above 2x, fill at that close | +£218, 17 | -£393, 3 | **+£611, 14** |
| late | sell lands at the next minute's open | +£388, 19 | -£275, 4 | **+£663, 15** |
| depth | touch minute traded at least 10x the stake ($1,300) | +£200, 18 | -£263, 4 | **+£462, 14** |

£100 paper stakes. "29 Sep to 5 Oct" includes the four positions the 6 Oct nightly closed.

## What it says

- The recent profit survives every stricter fill. The worst case (depth) keeps +£462 over 28
  trades, about +£16.50 a trade.
- The wick worry is half right: 7 of the 19 booked wins had their touch minute close below 2x. But
  most of them closed above 2x a minute or two later, so demanding a close only loses 2 wins.
  The two that flip to losses are G-0012 (manifest) and G-0031 (TRUMP).
- The split by date is the stronger finding. The same rules lost under every fill from 25 to 28 Sep
  and won under every fill afterwards. Nothing in the rules changed on 29 Sep (v0.2 since 25 Sep).
  So it is the market or luck, not a fix of mine. 44 trades cannot tell those apart.

## What it does not test

Whether a real order of about $130 would fill at all on a pool of $30k to $400k: the impact model
assumes a constant-product pool. And the 24h scores show most of the "winners" are down 90 to 99
percent a day later, so the whole edge is the first spike. A one-minute delay at entry is not tested
here (entries are booked at the snapshot price).

## Next

- Keep v0.2 running unchanged. A rule change now would be fitted to one good week.
- Re-run this check every Sunday so a better week cannot hide a fill problem.
- Add an entry-delay variant (buy one minute after the snapshot) to the harness.
