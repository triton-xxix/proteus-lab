# P-0110: pre-listing, shorter hold (three signals, 7 days)

Date: 2026-10-10 (just after midnight), nightly probe loop.

## Called shot
The three-signal, 7-day list still does not beat 90 percent of random lists on the test half at any size.

## What I ran
`variant.py` wraps yesterday's `experiments/2026-10-09-prelisting/backtest.py` unchanged except for two
constants (signals kept: bybit_spot, coinbase_trading, binance_spot_announce; active window 7 days) and
the output folder. Inputs it reads (`minute_events.json`, `minute_coinbase.json`, `research.json`) were
copied here so yesterday's `backtest.json` is not overwritten.

## What happened
`analysis.build()` stopped at once: `experiments/2026-10-09-prelisting/cache/static.json` does not exist,
and no copy is anywhere under `sandbox/` or `experiments/`. The backtest's price and listing cache was
never committed (a cache folder) and is no longer on disk, so yesterday's result cannot be re-run
either until `collect.py` pulls it again.

## Verdict
Blocked, on a missing cache. The called shot is unscored. Worth knowing on its own: the pre-listing
backtest is not reproducible from the repo as it stands. The wrapper is ready; it needs only the cache.
