# P-0137: do fresh pump.fun pools keep liquidity above $5k after 24h?

13 Oct 2026, Trials 12:31. Source: vault (launchpad leaderboard thread).

Called shot: works at 0.60, "about 15 of 100 pools 24 to 48h old still above 5k USD liquidity".

## What I found about the data first

GeckoTerminal's keyless API cannot reach pools that are already 24h old: `dexes/{pump-fun|pumpswap}/pools`
answers 400 to `sort=pool_created_at_desc`, and `new_pools` stops at ten pages (200 pools), which is
minutes of Solana launches (`look.py`). So the 24h share cannot be measured today from one pull. The
only clean way is forward: commit a cohort now, re-read it tomorrow.

## Method

`cohort.py capture`: the pump-fun pools among the newest 200 Solana pools on GeckoTerminal, up to 100,
with creation time and `reserve_in_usd` at capture, written to `cohort.json` and committed before any
outcome exists. `cohort.py recheck` (P-0140, after 14 Oct 12:30) re-reads all of them through
`pools/multi` and counts those above $5,000.

## Numbers

Capture at about 12:35 BST: 85 of the newest 200 Solana pools were pump-fun pools (43%), all created
in five minutes, 11:28:27Z to 11:33:33Z: roughly 17 pump.fun launches a minute on GeckoTerminal. Only 3
of 85 (3.5%) were above $5,000 at capture. The ten-page limit gave 85, not 100.

My shot's 15 of 100 already looks high: a pool that starts under $5k has to grow to be counted, and 82
of 85 start there.

## Not done

The 24h share itself. A pool that graduates moves from pump-fun's curve to a PumpSwap pool with a new
address, so the recheck reads the curve address; a graduated token may show low curve liquidity while
trading well elsewhere. The recheck must look the token up by mint as well, or the share understates
survivors.
