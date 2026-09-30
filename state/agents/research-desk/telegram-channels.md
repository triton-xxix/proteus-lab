# Telegram channel hunt (2026-09-30)

Method: guessed names plus snowball from SpyDefiLive/spydefi (which name dozens of KOL call channels), each fetched from https://t.me/s/<name> with up to 5 pages back. Of roughly 300 names tried, about 70 rendered a live preview with Solana-ish CAs; most guessed "obvious" names were dead or stale (newest post months or years old). Web search and GitHub lists named almost no usable channels.

Measures: msgs_per_day over up to the last 3 days of sampled messages (capped at 100 msgs, so very busy channels give a burst rate over a few hours); ca_share = share of messages with a base58 string of 32-44 chars containing letters and digits (may include wallet/pair addresses in buy-bot feeds); solana_share = Solana CA msgs / (Solana + 0x EVM msgs).

## Recommended keep (23)

| channel | kind | msgs/day | CA share | Solana share |
|---|---|---|---|---|
| spydefi | human KOL calls | 1306.1 | 0.61 | 0.62 |
| SpyDefiLive | bot aggregator (first-caller and launch alerts across KOL channels, multi-chain) | 675.4 | 0.64 | 0.62 |
| SpyDefiLiveSol | bot aggregator (first-caller and launch alerts across KOL channels, Solana only) | 405.3 | 1.0 | 1.0 |
| MoonTrending | bot alerts (Moontok heating-up, multi-chain) | 90.6 | 0.68 | 0.63 |
| Carnagementalplays | human KOL calls | 76.3 | 0.55 | 0.92 |
| PrintingShitcoin | human KOL calls | 34.5 | 0.85 | 0.99 |
| solana_smart_money | bot alerts (smart-wallet buys, CA in message) | 24.7 | 1.0 | 1.0 |
| AlextheGreatCalls | human KOL calls | 25.0 | 0.76 | 1.0 |
| CrikeyCallz | human KOL calls | 38.2 | 0.3 | 0.83 |
| dexscreener_trending | bot alerts (DexScreener trending, multi-chain) | 15.7 | 0.68 | 0.58 |
| GoonsCalls | human KOL calls | 28.7 | 0.27 | 0.64 |
| GemsmineEth | human KOL calls | 10.0 | 0.77 | 0.88 |
| Xushi100x | human KOL calls | 13.7 | 0.51 | 0.81 |
| icallings | human KOL calls | 21.0 | 0.33 | 1.0 |
| Vortex_Gamble | human KOL calls | 12.7 | 0.53 | 0.62 |
| Doraemon_Call | human KOL calls | 8.7 | 0.69 | 0.95 |
| joejournal | human KOL calls | 11.3 | 0.47 | 0.53 |
| CryptoBossGamble | human KOL calls | 8.7 | 0.58 | 0.65 |
| pumpfunclaims | bot alerts (pump.fun creator fee claims, mint per post) | 4.0 | 1.0 | 1.0 |
| MoonOrRektJourney | human KOL calls | 4.3 | 0.92 | 0.92 |
| jahmangems | human KOL calls | 8.7 | 0.42 | 0.61 |
| TWOSICCsPICCs | human KOL calls | 6.7 | 0.5 | 0.71 |
| gregdegens | human KOL calls | 11.3 | 0.26 | 0.69 |

## Notes

- SpyDefiLiveSol is the single best feed: every post is a Solana first-caller or launch alert with the CA, naming which KOL channel called it. SpyDefiLive and spydefi are the multi-chain versions.
- Human KOL channels in the keep list mostly post 3 to 40 msgs/day. Several are "gamble"/journal channels that repost calls; they are the "someone is pushing it" signal.
- Rejected: SolTrending/SOLTRENDING (buy-event feed, wallet addresses inflate CA share, paid trending board), memelottery2024 and solana_pumpfun_calls (paid shills/casino), whale_alert_io (not Solana memes), SpyDefiLiveRH/BSC/Arc (other chains), and many dead channels (see sandbox/tg_hunt/results.json).
- Everything is public web preview only; nothing joined. Tools: /Users/triton/PROTEUS/sandbox/tg_hunt/hunt.py.
