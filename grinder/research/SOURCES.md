# Research desk: source register

Every source here was called, not read about (survey of 30 Sep 2026,
`state/agents/research-desk/source-survey.json`). The track record column starts empty and is
filled by the Sunday cull from `MENTIONS.csv` and the digests' "claims to check later": a per-token
source is scored on how the tokens it flagged did against the ones it did not; a narrative source on
whether its dated claims came true. Trust comes from that column, not from the name.

## Per-token signals (`mentions.py`, one row per token, night and source)

| Source | How | Cost | As-of honest? | Track record |
|---|---|---|---|---|
| X | xAI Responses API, `x_search`, key named by Luke 30 Sep | $0.04 a token measured (58 for $2.51), 8 a night | day-granular search window; the prompt asks for posts before the snapshot, not enforced by the API | backfill 30 Sep: 21 of 58 had any post; those did far better at 24h than the 37 silent ones (seen, forward test M07) |
| Reddit | Arctic Shift archive, six subreddits bulk-pulled per 24h window, matched locally on mint or $TICKER | free | yes | backfill 30 Sep: 2 hits in 58 tokens; near useless for 1 to 48 hour tokens |
| Telegram | 23 public channels in `telegram-channels.json` (found and measured 30 Sep: 3 aggregators incl. SpyDefiLiveSol, 3 alert bots, 17 human callers), matched on contract address; per-channel history cached | free | yes | the first two channels (0 hits in 58) were dropped; solana_pumpfun_calls turned out to be a shill and casino board |
| DexScreener paid | `orders/v1/solana/<mint>`: paid profile and ads with payment time, boosts without | free | orders yes, boosts no | none yet |
| Jupiter | `lite-api.jup.ag/tokens/v2/search`: organic score, holders, audit flags | free | no: current values only, backfilled rows say "NOW" | none yet |

## Narrative (`narrative.py`, one pull and one digest a night)

| Source | How | Notes |
|---|---|---|
| X summary | xAI `x_search`, one call, about $0.15 | the richest source by far; names tokens with contracts; single-account claims flagged |
| News RSS | CoinDesk, Decrypt (and its Solana tag), Cointelegraph (and its Solana tag), The Block, Blockworks, The Defiant, Bankless | keyless, fresh to the hour |
| CoinGecko trending | `api/v3/search/trending` | snapshot only, listed coins only |
| Reddit | the same six-subreddit pulls | small: a few hundred posts a day; rarely names 1 to 48 hour tokens |
| Telegram | `t.me/s/cryptonary`, `t.me/s/WatcherGuru` | Cryptonary's research is paid; its public channel is what is free |

## Closed doors, recorded 30 Sep and not bypassed

reddit.com directly (403), PullPush (429, refuses agents), keyless X of any kind, pump.fun API
(geo-blocked), GMGN and Solscan (403), Birdeye and Solscan pro (key), CryptoPanic and Messari
(key or auth), Cryptonary's research (paid, JavaScript shell), Kaito (403).
