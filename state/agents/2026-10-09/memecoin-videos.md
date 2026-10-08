# What meme-coin traders say they check (YouTube, 9 Oct 2026)

Note: 12 of 70 searched videos had usable transcripts. Most of the rest were blocked (IpBlocked) or had transcripts disabled, so this is a small, search-ranked sample.

## Videos read
1. How to Identify Memecoin Scams with 100% Accuracy, Crypto Vic, https://www.youtube.com/watch?v=6r0QOQWy-Ug. Checklist: chart shape, audit flags, X account, dev, bundles. Selling: moderate (free Telegram group, "master tools list").
2. How to find Memecoins BEFORE they 100x, Crypto Vic, https://www.youtube.com/watch?v=opXqRruYDTw. DexScreener filters, Photon security panel, indicators, community. Selling: moderate (Telegram, Photon link, promotes fartcoin as "number one pick").
3. How to Spot Memecoin Rugs & Bundles BEFORE You Get REKT, starwifpump, https://www.youtube.com/watch?v=OUcUwd4aO08. Bundles, insiders, holders, odd buy amounts. Selling: heavy (Axiom referral, Discord).
4. How I Find the PERFECT Entry on Memecoins, starwifpump, https://www.youtube.com/watch?v=-czWNiE5Qmw. Bundle spotting, buying dips of 85-90% off peak. Selling: heavy (Axiom, Discord VIP).
5. How to Find Memecoins Before They 100x (2026 Guide), starwifpump, https://www.youtube.com/watch?v=IPPtuNpQgJw. Tracked wallets are side-walleted; fresh wallets; dev history via Solscan. Selling: heavy (Bloom, Axiom, Discord VIP, a gambling sponsor).
6. What is a bundle, K30N, https://www.youtube.com/watch?v=tz9MpJDxFWQ. Explainer on bundles, bubble maps. Selling: little.
7. I found Elite Pump.Fun Devs, Simply Blockchain, https://www.youtube.com/watch?v=zW6sPKXxmsg. Pick devs by graduation rate, snipe their next launch. Selling: heavy (TradeWiz bot link).
8. GMGN Wallet Tracking Guide, Adam Grabski, https://www.youtube.com/watch?v=ypWrP2_KasI. Find and copy profitable wallets. Selling: heavy (GMGN and atm.day paid tiers).
9. How to Track Smart Money in Memecoins, The Token Times Channel, https://www.youtube.com/watch?v=uAzaNPndgeE. Follow SOL funding, dev history, holder concentration. Selling: light (Discord).
10. How to Find AND Track Insider Wallets on GMGN, CryptoZin, https://www.youtube.com/watch?v=VgvrkRKn1D4. Actually about tracking KOL callers and their hit rates. Selling: moderate (referral links).
11. How To COPY Good Solana Memecoin Traders, Orangie Web3, https://www.youtube.com/watch?v=Q0gu9yH2O0s. Find wallets from tweets, track and auto-copy. Selling: moderate (bot links, giveaway bait).
12. Sight at Launch Meme Coin: Rug Pull Pace, Lupad, https://www.youtube.com/watch?v=fCUbmfXIKZ8. Shows how to launch and pull a token. Selling: a how-to-rug demo, no checks. Useful only as evidence of how cheap launches are.

## Checks they use, ranked by how often they come up
1. **Bundled supply at launch** (videos 1, 3, 4, 5, 6, 9, 10): multiple wallets buying in the same slot or second, often odd amounts like 1.7321 SOL, which hold a share of supply. Tools: Axiom bundle %, GMGN (said to be most accurate), Bubblemaps, Trench Radar bot, Insightx. Thresholds quoted: over 3-4% in one bundle is suspect; 10-15% total is bad. Keyless? Partly. Solana RPC (public or free-tier) lets you read the first slots of a mint's transactions and count buyers in the same slot, so a "same-slot buyers' share" is computable. Linking wallets by shared funding needs more calls. Bubblemaps and GMGN need keys or are scrape-only.
2. **Holder concentration and top-10 share** (1, 2, 3, 6, 9): single holder over 4-5% is "sketchy"; one says top-10 under 15%, another 23% is fine. Tools: Photon, Axiom, Bubblemaps, Fein bot. Keyless: yes, via RPC getTokenLargestAccounts, though pool and vault accounts must be excluded. The Grinder already gates on top-10 at 30%.
3. **Dev or creator history** (1, 2, 5, 7, 9): did the dev rug before, token graduation rate, whether tokens held liquidity, whether the dev sold. Tools: Solscan, Photon dev markers, a pump.fun stats site ("June"), GMGN deployed-tokens. Keyless: creator address is in the mint's first transaction; counting their earlier mints and what happened to them is possible with RPC history but slow. Pump.fun's public API may give creator lists (unverified).
4. **Insider, sniper and fresh wallets** (1, 2, 3, 5, 8): wallets that received tokens rather than bought; snipers in the first block; wallets created the same day. Tools: GMGN tags, Photon toggles, Axiom, Solscan funding trace. Keyless: wallet age and first funding source are RPC-computable per wallet; tagging at scale is costly.
5. **Mint and freeze authority, LP locked/burned** (1, 2): basic audit. Tools: DexScreener audit, Photon, Fein. Keyless and already gated by us.
6. **Social presence** (1, 2): X account exists and is posting, contract address posted on the real account, account not recycled (Fein bot), website exists and domain age, Telegram "raids". Keyless: partly. Website domain age via RDAP is keyless. DexScreener returns social links (keyless). X data and Telegram need keys or scraping. "Dex paid" and boosts are in DexScreener data.
7. **Volume quality** (1, 2): penny buy and sell bots inflating volume; 5-minute volume over $10k; DexScreener boosts (200-1000 good, thousands suspect). Keyless: 5m, 1h, 24h volume and txn counts come from DexScreener. Unique-trader counts need per-trade data (RPC or GeckoTerminal).
8. **KOL and caller wallets** (3, 4, 5, 8, 10, 11): presence of known KOL wallets as a trust signal; also a warning, since KOL wallets are copied and side-walleted. Tools: GMGN, Cabal Spy, Kolify, pump.fun callouts, Axiom trackers. Blocked keylessly: wallet lists live in Discords and paid tools.
9. **Timing** (2, 3, 4): buy after the bundle dumps ("nuke the bundles, then 50% scalp"); buy 85-90% below peak; market cap 70k to 11M; avoid the first minutes. Keyless: yes from OHLCV candles.
10. **Chart shape**: giant first candle, vertical straight-up, no sells (1, 6). Keyless from candles.
11. **Copycat tickers**: check you have the biggest token with that name (1). Keyless via DexScreener search.

## Why they say coins dump and then recover
- Bundle holders sell in one click once buyers arrive, causing a crash (3, 6).
- Followers of copied wallets are exit liquidity: the tracked wallet sells and the copiers dump with it (3, 4, 5, 9). That sale is cited as a dip entry.
- After "everyone nukes the bundles", a 30-60% bounce is expected (3, 4). Pattern claimed: one big run, one relief bounce, then zero (4).
- Recovery drivers named: a new catalyst tweet, repeated community raids, or the creator keeping on posting (4, 2). A "triple pump" shape is claimed (2).
- Early advance signals offered: bundle and insider share, wallet funding trace, and the tracked wallet's side wallets buying first.

## Claims to treat with suspicion
- "100% accuracy" scam detection (1), "easy 4x" with hindsight charts (4), and "10x after I filmed this" (2). Survivorship bias, no losses shown.
- EMA cross and RSI "predict" direction (2) and "triple bounce" (2). Unfalsifiable as stated.
- Boosts, raids and an active X account as good signs. These can be bought; a boost is paid promotion, not belief.
- Any number from a referral partner (Axiom, Bloom, TradeWiz, GMGN, atm.day) about win rates or "free money".
- Caller multipliers (10): first-call timing is not what followers get.
- Dev graduation rates (7): selection on graduation says nothing about post-graduation returns.
- "Pump suffix means more secure" (2) contradicts video 1, which says the suffix can be spoofed.
- Thresholds disagree (top-10 15% vs 23% fine), and the speakers say "use your own judgement".

## Five things worth testing on our data
1. Do Grinder picks with more than 10% of supply bought in the first few slots (same-slot buyers) lose more than the rest? Needs: first 100 transactions per mint from RPC.
2. Do picks whose creator has launched many tokens (say 20 or more) with few holding liquidity have a lower win rate than picks from first-time creators? Needs: creator address and prior mint counts.
3. Does a pick with a DexScreener social link (X and website) and "dex paid" beat one without, at +100 / -50 / 24h? Needs: DexScreener info field at pick time, already fetchable.
4. Does entering after a 50%+ drawdown from the token's first-48-hour peak beat entering at the 1-hour-volume rank? Needs: OHLCV candles for each pick and the timing of the dip.
5. Do picks with a high ratio of tiny trades (penny-size, repeated) to unique traders, or a low volume-to-transaction-count ratio, lose more? Needs: per-trade data from GeckoTerminal or RPC for the hour before the pick.
