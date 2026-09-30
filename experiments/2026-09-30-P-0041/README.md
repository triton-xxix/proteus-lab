# P-0041: the scanner looks past 48 hours

Done 30 Sep 2026 in an interactive session (commit 8e6ca7c). `grinder/scan.py` now adds up to 40
established pools a night (7 to 400 days old, found by 24h volume on PumpSwap, Meteora and Raydium,
majors excluded) to the same snapshot as the young candidates. A standing list,
`grinder/established.json`, keeps the set when GeckoTerminal throttles: seeded with the 20 tokens the
48h gate rejected on 24 to 28 Sep, 34 on the first run. v0.2's age gate keeps them out of the live
book, so nothing live changes; rule E06 in `grinder/harness/VARIANTS-2.md` can now be replayed on
nights after 30 Sep.

Why: of those 20, the eight past 50 days with large holder bases moved -32% to +60% (median about
-5%) over the next 2 to 6 days and all still traded thousands of times a day, while the 2 to 35 day
group split between +73% and -100% (median -70%). Discovery by volume was thin the first time
(7 to 9 pools per call while GeckoTerminal was throttling), hence the standing list.
