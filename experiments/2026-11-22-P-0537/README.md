# P-0537 Bonding-curve graduation: what share of graduated tokens have 99%+ LP locked or burned?

Nightly 2026-11-22. Harvest item yt:YBVozFI3lnw, a 30-second short saying the pool is locked "the
second it graduates" on one launchpad, with pulled pools as the catch elsewhere.

## Data

Tonight's Grinder snapshot (`grinder/SNAPSHOTS.csv`, 23:xx UTC 22 Nov, 142 tokens), whose
`lp_locked_pct` comes from rugcheck's report per token. No new pull. Script `lp_share.py`, output
`results.json`.

## Result

| dex | tokens | LP 99%+ | LP under 50% |
|---|---|---|---|
| pumpswap (pump.fun graduates) | 59 | 57 | 2 |
| pumpfun (still on the curve) | 20 | 20 | 0 |
| meteora | 43 | 28 | 12 |
| raydium | 13 | 7 | 6 |
| orca | 6 | 0 | 6 |

The 30 youngest pump.fun / PumpSwap tokens: 30 of 30 at 100%.

## Verdict: works

Locked-at-graduation is already the default on pump.fun: 77 of 79 of its tokens tonight read 99%+
locked or burned, against 28 of 43 on Meteora and 7 of 13 on Raydium. So the short's selling point
is not unique to its own launchpad, and on pump.fun the "dev pulls the pool" risk it warns about
mostly lives elsewhere (supply held by insiders, mint authority, the other gates the Grinder already
checks). The two PumpSwap tokens under 50% are worth a look as exceptions. Caveat: one snapshot, and
the Grinder's candidate list is filtered by volume first, so this is the share among tokens anyone
is trading, not among every graduate.
