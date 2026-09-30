# P-0042: what happens to a fresh pump.fun token

30 launches heard on the public RPC websocket on 30 Sep 2026, each read from the chain at least 30 minutes after creation (first 40 transactions per mint). Nobody bought anything. 30 analysed.

| Measure | Median | Share of launches |
|---|---|---|
| Creator bought in the creation transaction | | 83% |
| Other wallets buying in the creation slot (first block) | 1.0 | 70% had any |
| Wallets buying in the first 3 slots (about 1.2 s) | 1.0 | |
| Buyers in the first 60 s | 3.0 | |
| Buyers seen (first 40 transactions) | 4.0 | |
| Seconds to the first sell | 2.0 | |
| Creator sold within 30 min | | 73% |
| Seconds to the creator's first sell, where they sold | 12.5 | |
| Share of first-block buyers' tokens sold within 5 min | 0.035 | |
| Share of first-60s buyers' tokens sold within 30 min | 0.204 | |
| Still trading after 10 minutes | | 27% |
| Seconds from creation to last trade seen | 39.5 | |

## Reading it

- 20 of the 30 launches had fewer than 40 transactions in their whole life, so for them this is the
  complete history. The other 10 hit the 40-transaction cap, so "still trading after 10 minutes" (27%)
  is a floor, and their "last trade seen" is only the 40th transaction.
- The typical launch: the creator buys in the creation transaction (83%), one other wallet buys in the
  same block (70% had one: a sniper or the creator's second wallet), the first sell comes 2 seconds in,
  the creator sells at a median of 12.5 seconds (73% sold within 30 minutes), and the token's last trade
  is 40 seconds after creation. Median buyers seen: 4.
- Most launches are not a market; they are a creator, a sniper and a couple of bots trading for under a
  minute. The long tail (5 of 30 still trading past 45 minutes) is where anything real happens.
- Not measured: creator fee take (needs the creator vault's balance history) and bundle funding links
  (needs each wallet's funding transactions). Both need more RPC reads than the public endpoint allows
  in an evening.
