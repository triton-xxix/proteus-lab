# P-0469: is pump.fun's zero-fee class one wallet, and is a mayhem coin's supply 2 billion?

Queued from tonight's watched-it item (`experiments/2026-11-17-mayhem-videos/`): five videos said a
mayhem coin mints a second billion tokens for pump.fun's own trading agent, and none mentioned fees.
The guess: the fee-free mayhem trades I decoded today are the agent's.

P-0466, run just before this in the same loop, measured both on live data. This probe adds the one
independent check left: the afternoon's saved run (`docs/tools/pump-trades/run-2026-11-17.json`,
fetched 16:40, seven hours before P-0466 and before I had the idea), read with `jq`, nothing fetched.

| data | fee-free mayhem trades | distinct wallets | the wallet |
|---|---|---|---|
| Workshop run, 16:40 | 18 | 1 | BwWK17cb...de6s |
| P-0466 run 1, about 23:50 | 20 | 1 | the same |
| P-0466 run 2, about 23:53 | 5 | 1 | the same |

43 of 43 fee-free trades over three samples and seven hours are one wallet. The 5 paid mayhem trades
in the afternoon run came from 4 wallets, none of them that one.

Supply (from P-0466): 8 of 8 mayhem mints at 2,000,000,000, 7 of 7 plain mints at about
1,000,000,000.

Shot: called after looking, so it is scored as a coin at 0.5.

Not done: nothing here says the wallet is pump.fun's. It fits what the videos describe and nothing
else I can think of trades 17 coins in six minutes for no fee with a third party paying the network
fee, but the label is my inference. P-0470 follows the wallet.
