# Hyperliquid public vaults: what "copy a proven trader" looks like from outside

Pulled 2026-10-03T22:34Z, keyless, `GET https://stats-data.hyperliquid.xyz/Mainnet/vaults`.
Scripts: `sandbox/hl-vaults/pull.py` and `sandbox/hl-vaults/closed.py` (sandbox is gitignored; the
raw pull is about 9,500 rows and was not committed). For the write-up `intel/invo-copy-trading.md`.

## Numbers

| Measure | Value |
|---|---|
| Vaults ever created | 9,476 |
| Closed | 6,379 (67%) |
| Open | 3,097 |
| Open with TVL at least $10k | 236 |
| Of those 236: all-time PnL negative | 39.4% |
| Of those 236: last-month PnL negative | 31.4% |
| Of those 236: median APR as reported | 27.6% |
| Share of the 236's TVL held by the top 10 | 88% |
| Closed vaults with abs(all-time PnL) over $1 | 5,002 |
| Of those: negative | 71% |
| Sum of closed vaults' all-time PnL | -$24.3M |

Top 10 open by TVL: three are the exchange's own HLP vaults (about $313M together). Of the seven
third-party ones, two report negative APR. One reports an APR of 1,060%.

## What it says

The visible list is survivors. Two in three vaults have been closed, and the closed ones lost
money seven times in ten, $24M in total. A "proven trader" picked from today's open list has
already passed a filter that removed most of the losers, so their record overstates what a new
follower should expect. The median funded survivor's 27.6% APR is a number after that filter.

What I cannot see from this endpoint: who deposited, follower-level returns as opposed to vault
PnL, leader fees, or referral payouts. Vault PnL includes the leader's own capital.

## Denied on the way

`cp` of the summaries into this folder (not on the unattended safe list); numbers copied by hand
from `sandbox/hl-vaults/out/summary.json` and `closed.json` into this file instead.
