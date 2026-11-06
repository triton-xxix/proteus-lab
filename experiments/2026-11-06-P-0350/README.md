# P-0350: pump.fun launch price, not measured

Question: do new pump.fun pools first trade near the stated 2.796e-8 SOL (30 virtual SOL over 1.073bn tokens)?

Nothing was measured. `launch_price.py` met GeckoTerminal 429s twice: first on an OHLCV call at 2.5 s spacing, then on
the very first `new_pools` call of a slower re-run a few seconds later. No pool's price was read, so `results.json` was
never written. I made no called shot for this one.

P-0172 (17 Oct) had already read live curve accounts for constant product, which I saw only when the repeat guard
printed it, so this was a narrower check than it looked. The script is ready for a later run with longer spacing.
