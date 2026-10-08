# What the Grinder's winners and losers have in common (9 Oct 2026, with Luke)

Luke's questions, in session: what do winners share, what do losers share, is it luck, why do some
coins crash and then come back, how is Telegram checked, where else could we look, who are the
creators. Everything here was measured tonight; nothing is a rule yet. Leads that survive go into a
pre-registered shadow book before they touch the live one.

Files: `winners_losers.py` (report.txt, features.csv), `bounce.py` (bounce.json),
`creator_insiders.py` (creator_insiders.csv), `yt_pull.py` and the reading digest
`state/agents/2026-10-09/memecoin-videos.md` (12 videos with transcripts out of 76 tried).

## The population

163 tokens passed the Grinder's gates since 22 Sep, each replayed under the live exits (+100%, -50%,
24 hours, real costs) on its minute candles: 41 winners, 78 stop-outs, 33 rugs, 11 time stops,
-£21 a position. The 48 the live book bought (top 4 by 1h volume a night): 20 wins, 27 stops, 1 rug,
+£6.7 a position. The 115 it did not buy: 21 wins, 32 rugs, -£32.5.

## What separates them

1. **The ranking already works.** Top tercile of 1h volume wins 42%, the bottom two 17%. Same for
   1h volume as a share of the day (42% v 15%) and volume against liquidity (38% v 6%). That is why
   the bought four win 42% and the rest of the field 18%. The busiest coin right now is the best
   single thing we measure.
2. **Rugs look different from the rest before entry.** A rugcheck risk named: 8% wins (3 of 37)
   against 30%. No paid DexScreener profile: 7% wins (2 of 28). Rugs had no Telegram mentions
   (median 0 against 7 to 14), 98% of the last hour's trades were buys (one-way bot flow), almost no
   turnover against their liquidity (0.02), and implausible liquidity and market caps ($1.6m and
   $320m medians). Several look like fake or wash-traded pools, not real launches.
3. **Rising in the last hour is slightly worse.** Winners' median 1h change was -4%, stop-outs +2.5%.
   Small, but it agrees with the 30 Sep marker.
4. **Inside the four we buy, I cannot see a difference.** Winners and stop-outs have near-identical
   medians on every field. On 48 trades a split like 19% v 50% is three wins against eight, inside
   noise. So among the coins that already pass the gates and top the volume list, which ones double
   and which ones halve is, on our data so far, mostly luck.
5. **rugcheck's insider fields (read today, not at entry).** Tokens where rugcheck found no insider
   network: 12% wins, 35% rugs (48). With one or more: 30% wins, 14% rugs (115). Probably "rugcheck
   analysed this as a real pump.fun launch" rather than "insiders are good". P-0001 (24 Sep) found
   the insider count grows with a token's age and activity, so a busy token collects more of them;
   read at entry, the number may say nothing. Creator launch history
   came back for only 7 tokens and no creator was behind two of the 163, so creator track record is
   not measurable from rugcheck alone.

## The four that crashed and then ran

| token | low | when | bounce | volume from low to peak | Telegram |
|---|---|---|---|---|---|
| AIRPAD | -96% | 6 min in | +194% | $1.3k | none |
| Human | -85% | 24 min in | +517% | $9.8m | 28 calls, all after it had doubled off the low |
| Agency | -62% | 7.4 h in | +665% | $13.1m | 40, first one 9 h after it doubled ("x60 call" brags) |
| EGO | -83% | 17 h in | +106% | $0.36m | none |

AIRPAD's bounce is $1,300 of trading in a near-empty pool: a print, not a price anyone could sell at.
Human and Agency were real second waves on millions of dollars, but the Telegram calls followed the
move rather than led it; SpyDefi posts "achievement" brags after a call has paid. The 27 stop-outs
that stayed down bounced a median 1.3x off their low on $1.6k of volume. So I cannot see the bounce
coming in anything we collect. The YouTube traders' explanation is that launch bundles dump, then a
relief bounce follows; that needs per-wallet data we do not have yet.

## How Telegram is checked

No account and no bot. 23 public channels (callers, the SpyDefi aggregators, trending bots) chosen in
a 30 Sep survey publish a web preview at t.me/s/<channel>. `grinder/research/mentions.py` reads those
pages back 24 hours each night, caches them, and counts messages containing each pick's contract
address. Also checked: X through xAI's search (about 16p a token, Luke's key), Reddit through the
Arctic Shift archive, DexScreener's paid-promotion orders, Jupiter.

## Where else to look (from the videos and the data)

- **Bundles and snipers at launch**: wallets buying in the same block as the creator. Readable from
  public Solana RPC (first transactions of the mint). The most-cited check in the videos.
- **Creator history**: the creator address is in rugcheck's report already; prior launches need
  Solana RPC history or a pump.fun stats source (pump.fun's API is geo-blocked here).
- **Fresh and linked wallets** among top holders: wallet age and funding source, RPC-readable, slow.
- **YouTube** as a mention source: possible keyless, but meme-coin chatter there is days behind; X and
  Telegram are where calls happen. Discord groups are closed.
- **GMGN, Bubblemaps, Axiom, Photon**: the tools the traders use. All need accounts or are
  scrape-only; the vault judged GMGN before.
