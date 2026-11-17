# P-0466: does pump.fun's zero-fee class truly pay nothing? And who is it?

P-0465 found pump.fun trades whose event records no fee in any field, all flagged mayhem mode, while
other mayhem trades pay the usual 95 + 30 bps. An event can leave things out; a balance cannot. This
compares each trader's SOL balance change with the event's `sol_amount`.

## Method

`balance.py`, keyless, public RPC, standard library, read only, reusing the decoder in
`docs/tools/pump-trades/`. For each live transaction with exactly one SOL-quoted TradeEvent: the
trader's `postBalances - preBalances`, less the network fee when the trader pays it, against
`sol_amount`. The gap in bps is what the trade cost beyond the curve price. It also keeps who the
trader was and the supply of the mints seen (`getTokenSupply`).

Two runs, about 23:50 and 23:53 UK on 17 Nov. The first (`run1-first.json`, 32 transactions read,
29 fetches refused by the rate limit) could not find the zero-fee trader's balance because that
wallet sits in the transaction's loaded address table, which I had not added to the key list. Fixed,
then the second (`results.json`, 70 read, 11 refused).

## Numbers

| | run 1 | run 2 |
|---|---|---|
| single-event trades | 31 | 12 |
| mayhem, no fee | 20 | 5 |
| distinct traders in that class | 1 | 1 |
| mints they traded | 12 | 5 |
| trader was the fee payer | 0 of 20 | 0 of 5 |
| balance gap, bps of sol_amount | not measured | 0.0 on 5 of 5 |
| mayhem, paid | 6 trades, 5 traders | 3 trades, 3 traders |
| plain, paid | 5 trades, 4 traders | 4 trades, 4 traders |

- **All 25 zero-fee trades were made by one wallet**, `BwWK17cbHxwWBKZkUYvzxLcNQ1YVyaFezduWbtm2de6s`,
  buying and selling (11 buys, 14 sells) across up to 17 mints, with someone else paying the network
  fee every time. In run 2 its SOL balance moved by exactly `sol_amount` on all five: it pays nothing.
- Every paid mayhem trade (9, by 8 wallets) was an ordinary trader on a mayhem coin.
- **Supply: 8 of 8 mayhem mints show 2,000,000,000 tokens** (one 1,999,999,775); 7 of 7 plain mints
  show about 1,000,000,000 (one 901,633,004, so someone burned).

So the zero-fee class is pump.fun's mayhem agent trading the coins it was assigned, and the two
things tonight's videos said (a second billion minted, an agent that buys and sells) hold on chain.
The wallet is not labelled anywhere I read; "the agent" is my inference from one wallet, no fee, no
fee payment and 17 mints in six minutes.

## What did not work

The gap for paid trades is noise at this sample: run 2's plain paid trades read 125, 135 and 360 bps
(the floor is the 125 bps fee; the rest is token-account rent and tips), mayhem paid 998 to 3,900 bps
on three small buys, and run 1's paid gaps were wild (one sell at -764,324 bps) because those wallets
moved other SOL in the same transaction. The method answers "zero or not"; it does not measure a fee.

Not done: the agent's profit and loss, how long it trades a coin, whether its buys can be seen
coming. Those are the next questions and they are worth more than this one.
