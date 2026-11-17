# P-0470: what the fee-free mayhem wallet does

The wallet `BwWK17cbHxwWBKZkUYvzxLcNQ1YVyaFezduWbtm2de6s` made every fee-free pump.fun trade I have
seen (P-0466, P-0469). I asked for trades per coin, holding time and profit and loss over its last
1,000 signatures.

## Method

`wallet.py`, keyless, public RPC, standard library, read only. `getSignaturesForAddress` for the
wallet (limit 1,000), block times read straight from that list; then the newest 150 transactions
fetched and decoded with the pump-trades decoder.

## Numbers (17 Nov 2026, about 23:47 UK)

- **1,000 signatures span 65 seconds.** About 15 transactions a second, 500 in the median minute
  bucket, 688 in the busiest. 7 of the 1,000 failed on chain.
- 150 fetched (3 refused): one fee payer for all 150, `Gygj9QQb...BUpA`, never the wallet itself.
- 142 trades in **11 seconds**, across 19 coins: 74 buys, 68 sells, all 142 fee-free, all 142 flagged
  mayhem. Median trade 0.037 SOL, largest 0.764 SOL. Median 6 trades a coin in those 11 seconds.
- SOL: 6.693 spent, 5.929 received, net -0.764 SOL in the window. 11 coins net positive, 8 negative;
  4 coins bought only, 3 sold only.

## What it answers and what it does not

Trades per coin: yes, about one trade every two seconds on each of about 19 coins at once.

Holding time and profit and loss: no. I sized the pull for a wallet that trades a few times a minute.
At 15 a second, 1,000 signatures is one minute and my sample is 11 seconds, so "net -0.76 SOL" is one
breath, not a result. My shot said net seller; in this window it was a net buyer, and neither means
anything at this length. A day of this wallet is about 1.3 million transactions; at the public RPC's
rate (about 3 a second before refusals) it cannot be followed transaction by transaction.

What would work instead: the wallet's SOL balance and its token balances per coin, sampled every few
minutes with `getBalance` and `getTokenAccountsByOwner` (two calls a sample, whatever the trade
rate), which gives profit and loss directly. That is a long-running job, not a night's probe.

Also not done: whether its trades lead or follow other traders on the same coin. The videos say
people launch coins to sell into its buys; with 19 coins live at once that is checkable from the
public trade stream, coin by coin.
