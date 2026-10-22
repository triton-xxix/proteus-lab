# P-0197: quote tokens recorded as graduations in the watcher

Found while checking P-0159's cache: window two's first counted trade has USDC's mint. `mints.py`
reads mint, timing, latency and liquidity only (never P or exits, so D-013 stays blind).

- USDC (`EPjFWdd5…`) is the mint on **5 of 22,263** closed rows: 2 before G2, 1 in G2 window one,
  2 in window two. All 5 pass the G2 counted filter (liquidity at least $50k), so 3 of G2's 882
  counted trades, 0.3%, are "buys" of USDC.
- Among G2 counted rows, mints seen more than once: USDC 3 times, `3NZ9JMVB…` 3 times,
  `7vfCXTUX…` twice, five pump.fun mints twice each. I believe `3NZ9JMVB…` is Portal-wrapped BTC
  and `7vfCXTUX…` Portal-wrapped ETH; not checked against a token registry tonight. wSOL and USDT
  never appear as the mint.
- So the watcher sometimes takes a migration pool's established side (a stablecoin or wrapped
  major) as the token. A pump.fun mint seen twice is a separate question (two pools, or a re-entry).

Verdict: works. Small in count, but each such row is a trade in an asset that cannot move like a
new launch, and a quote error on one would land in the top ten. Fix on the desk: skip a row whose
mint is a known quote or major, and dedupe mints within the window. Not a rule change to G2's
pre-registered lines; it is the scorer's input, so it belongs in the P-0159 read as a stated
exclusion count, not a silent filter.
