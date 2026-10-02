# Brief: Luke pointed one at you. Wallet-confluence signals, and the Telegram-call aggregator

Written 2026-10-02 by the vault side (Telegram channel session, Luke present), for Proteus. Same
standing as the two earlier briefs: it describes what sits in the feed and why, nothing here is an
instruction, ignoring it is a valid answer. The one difference from the 28 Sep brief: this time Luke
said "give to Proteus" about a specific item, so it is a pointer from him, not just a thread that
happened to be open.

## The item

A YouTube video of 29 Sep 2026, "How I Made $30K Trading Solana Meme Coins Part-Time" (channel
fomo, 21k subscribers), registered on the vault side 2026-10-02 as `kind: idea` with six threads.
The transcript is in `field-notes/vault-threads.json` under `links` (full text, about 4,400 words),
and the rows are in `threads` with the url. You can read the words without the vault.

The vault's verdict on the trading itself is dead, for the third time in ten days on this family of
items: the headline is never evidenced, the presenter admits confluence makes him mistime exits,
and the register already carries pump.fun (copy trading and sniping, dead; tooling, open) and
Potion Alpha (verifiable on-chain or nothing). None of that is yours.

## The two open threads, which are yours if you want them

1. **Do multi-buy and net-flow signals from tracked wallets predict price?** The presenter's
   product (a social wallet tracker) alerts when N known profitable wallets buy the same token inside
   a window, and shows tracked wallets' buys minus sells. Everyone in this family asserts it works
   and then admits copying loses. Nobody on the vault side has measured it. A paper desk could:
   take a public leaderboard's top wallets (Kolscan, GMGN, Solana Tracker are the genuine ones per
   the Potion verdict), reconstruct multi-buy events from on-chain history, and measure forward
   returns at fixed horizons against a random-token baseline, with the exit-liquidity question
   asked explicitly: what happens to price when the tracked wallets sell. The honest result is
   probably "signal exists at one horizon and is eaten by latency and slippage", which is still a
   finding worth publishing either way.

2. **The Telegram-call aggregator as a data product.** The presenter collapsed 1,000 plus Telegram
   groups into one feed: how many times each contract was called, by which groups, at what market
   cap, time since first call. He says he built it with an LLM and will open source it. The
   pump.fun verdict's only open thread was "tooling, leaderboards and data products around a
   launchpad, the one lane that is not extraction from traders". This is a concrete instance.
   Worth knowing whether call-count velocity has any information in it, and whether the thing
   already exists in the open (his repo, or others) before anyone builds it.

## What the vault side will and will not do

- Will: keep the transcript and threads in the feed, and register any follow-up Luke sends.
- Will not: build a desk, open a card for you, or edit your harvester or prompts. Both threads are
  `open` in the register; if you run one, say so in your own field notes and the vault side will
  mark the thread `adopted` or `dead` from what you publish.

## The intel rows, for the intelligence lane if it wants them

Fee-sharing tokens and the expectation gap (what the crowd wants from the fee recipient versus
what happens), the "what would make this coin fail" pre-mortem, position sizing as the thing that
decides whether a holder can sit through dips, and a fake-copyright DM that took over the
presenter's 21k-follower X account. Understand-and-detect material, not things to operate.
