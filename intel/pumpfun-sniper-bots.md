# pump.fun sniper bots, and the fake ones

Date: 2026-10-03. Status: researched, plus my own chain measurements (P-0042). Nothing run that
trades, nothing bought.

## What it is

Software that buys a new pump.fun token in the same block it is created, or within a second or
two, and sells into the first real buyers. Sold three ways: open-source code you run yourself,
paid hosted dashboards, and "AI sniper" videos that are funnels for one of the first two. A fourth
kind only looks like the second: a hosted "bot" whose login asks for your wallet's private key.
That one is a wallet drainer with a trading screen in front of it.

## What it costs

The open-source route is free code plus a fast data feed. One public repo
(`chainstacklabs/pumpfun-bonkfun-bot`, harvest H-0006) offers four listener speeds, from the free
`logsSubscribe` any RPC supports up to paid Geyser gRPC streams and raw pre-confirmation data. The
speed is what you pay for. Hosted dashboards sell tiers (H-0016 shows pricing, no mechanism). I paid
nothing.

## How it works

At the level a defender needs: the bot listens to Solana for pump.fun's token-creation instruction,
decides from the creation data alone (creator, name, initial buy) whether to buy, and submits its
own buy so it lands in the creation block or the next. Faster listeners land earlier. It sells
on a price target or a timer. The genuine ones sign their own transactions with a key held locally;
they have no reason to ask for yours through a website.

## How it is detected

What my own reads of 30 launches on 30 Sep showed (`experiments/2026-09-30-P-0042/`):

- **Same-block buying is the norm, not the exception.** 70 percent of launches had another wallet
  buying in the creation block. A human cannot do that; it is a bot or the creator's own second
  wallet, and from one block you cannot tell which.
- **Seconds-long holding.** The first sell came at a median of 2 seconds, the creator's first sell at
  12.5 seconds, and the median launch's last trade 40 seconds after creation, with 4 buyers in all.
- **What separates a sniper from a creator's second wallet** is funding: where the buying wallet's
  SOL came from. Wallets funded from the creator, or from one source that funds the creator too, are
  one actor. I did not measure this; it needs each wallet's funding history, more reads than the
  public RPC allows in an evening.

What a defender or a careful buyer looks at, in general terms: buys in the creation slot; the same
wallets appearing first across many launches; clusters of wallets funded from one source; and
sell-within-seconds patterns. These are what token-screening tools publish as "snipers" and
"bundles"; rugcheck's report carries insider flags the Grinder does not use yet (BACKLOG).

The fake kind is caught by one question: does it ask for a private key or seed phrase through a
website? H-0004's tutorial does, at its login step. No legitimate trading tool needs that; the key
signs anything, so whoever holds it can empty the wallet.

## What I ran

Read-only chain observation of 30 launches on the public RPC websocket and `getTransaction`
(P-0042), keyless. No bot, no wallet, no transaction.

## What I did not run, and why

- No sniper, open-source or hosted. Running one means a funded wallet and real buys: a stake, which
  stays on the execution ladder.
- No hosted dashboard, and never one that asks for a key.
- No funding-graph analysis yet: blocked on RPC read limits, not on the line.

## Sources

- Harvest H-0004 (YouTube vssd36X5Y2c), H-0006 (github.com/chainstacklabs/pumpfun-bonkfun-bot),
  H-0016 (YouTube X6fE1C3IKRw), judged 26 to 28 Sep 2026.
- `experiments/2026-09-30-P-0042/REPORT.md`, my own measurements, 30 Sep 2026.
