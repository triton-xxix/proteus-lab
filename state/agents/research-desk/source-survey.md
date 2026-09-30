# Research desk source survey, 30 Sep 2026

Every line below comes from a live curl call made today. Full detail is in source-survey.json. Nothing was signed up for, no CAPTCHA touched, no block worked around.

## The short version

Off-chain data you can script without a key is thin, and most of it is noisy. The two useful finds for the Grinder are Reddit through Arctic Shift (real history, 24-29 Sep backfill possible) and DexScreener's orders endpoint (paid promotion history per mint, with timestamps). Telegram gives a little, News RSS gives the daily narrative for free. X, GMGN, Birdeye, Solscan, pump.fun, PullPush, CryptoPanic and Messari are closed to keyless scripts.

## (a) Per-token mention counts, ranked

1. **DexScreener orders** (`api.dexscreener.com/orders/v1/solana/<mint>`). Searches by mint, no key, history by payment timestamp. Not mentions but paid attention: profile buys and boosts with amounts. Best backfill for 24-29 Sep. It tells you when someone paid to be seen, which is arguably the more useful thing.
2. **Arctic Shift posts and comments.** Free, no key, full date range, fresh to within about an hour. Reliable way to use it: page each subreddit by date window (100 rows a call) and grep locally for the mint or $SYMBOL. Server-side text search (`selftext=`, `body=`) works only some of the time and often times out. Sample: r/pumpfun post about $OMTAB found by `selftext=OMTAB`. Meme tokens 1 to 48 hours old will mostly have zero Reddit mentions, so expect sparse counts.
3. **Telegram t.me/s/solana_pumpfun_calls.** Live to today, carries `Ca:` contract addresses. Pages back with `?before=<id>`, about 12 days in one page. Paid shills, mixed chains, casino adverts, so treat it as a promotion signal.
4. **Telegram t.me/s/alphacalls.** Live to 29 Sep, $TICKER calls and DexScreener links. Same caveats, less Solana-specific.
5. **Jupiter lite-api token search** (`lite-api.jup.ag/tokens/v2/search?query=<mint>`). Not a mention count. It returns holder count, organic score, dev address and the token's twitter, telegram and website, which you need before you can count anything on those platforms.

Everything else (news RSS, CoinGecko) will not mention a day-old meme coin, so it scores nothing here.

## (b) Daily narrative, ranked

1. **Cointelegraph Solana tag RSS** (`cointelegraph.com/rss/tag/solana`). Actual Solana filter, keyless, back to 28 Jul.
2. **CoinDesk RSS** (`coindesk.com/arc/outboundfeeds/rss`). Fresh to the hour, 25 items.
3. **CoinGecko trending** (`api.coingecko.com/api/v3/search/trending`). Trending coins plus trending categories (today: Privacy Infrastructure, Binance Alpha Spotlight). Snapshot only, so store it nightly. Listed coins only.
4. **Decrypt, The Block, Blockworks, The Defiant, CryptoSlate RSS.** All keyless and fresh today. Blockworks and Defiant carry the most items. Bankless (`bankless.com/rss/feed`) reaches back to 19 Aug.
5. **Telegram t.me/s/WatcherGuru** and **Reddit r/memecoins, r/pumpfun, r/SolanaMemeCoins** via Arctic Shift for the mood on the ground. WatcherGuru is macro headlines; the subreddits are mostly promotion posts and beginners asking if memecoins are scams, which is itself a decent sentiment read.

## Closed doors (recorded, not bypassed)

- PullPush: 429 with a message refusing agents. Reddit .json: block page.
- pump.fun frontend API: geo-blocked, redirects to a blocked page.
- X: nitter hosts do not connect, syndication 429, API 401, search redirects to login.
- GMGN and Solscan api-v2: Cloudflare 403. Birdeye and Solscan pro: need a key.
- CryptoPanic and Messari: key or payment. Kaito: 403. Cryptonary: no RSS; the site is a JavaScript shell and the paid research is not scriptable, only the free Telegram channel.
- GeckoTerminal returned 429 on both trending and new pools during the survey. That is our existing dependency, so avoid running research pulls at the same moment as a Grinder scan.

## Things to know before building

- Arctic Shift throttles hard and answers "Timeout. Maybe slow down a bit". Run calls one at a time, with a few seconds between.
- Telegram channel names are mostly dead or preview-disabled. About 8 in 60 guessed names worked. Keep a vetted list and check freshness on each run.
- Nothing here offers Twitter/X volume, which is where most meme-coin attention lives. Any mention count from these sources is a partial view and should be logged that way.
