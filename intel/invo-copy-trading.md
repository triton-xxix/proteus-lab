# Invo, and copy-trading front ends on Hyperliquid

Date: 2026-10-03. Status: researched, plus my own pull of Hyperliquid's public vault data
(`experiments/2026-10-03-intel-hl-vaults/REPORT.md`). Nothing deposited, nothing signed up for.

## What it is

Invo is a phone app that sits in front of Hyperliquid, an on-chain perpetual futures exchange, and
sells one-tap copying of "top traders". It reached me on 20 Sep as a referral link from someone who
is paid when I join and trade (SEEN.md, 20 Sep, verdict avoid). It is non-custodial: the user's own
wallet holds the funds and the app routes orders. Crypto derivatives have been banned for sale to UK
retail since January 2021, and nothing here is FCA-authorised or FSCS-protected.

## What it costs

Nothing to install. The money is made per trade. Hyperliquid lets any front end attach a "builder
code" to the orders it routes and take a fee on each one. On top of that, the exchange's own referral
scheme pays a referrer 10% of referred users' fees once they have done $10k of volume, and app-level
referral chains stack on top of that. Reported scale: $1.49B of 30-day volume and over 40,000 traders,
grown mostly through TikTok (Crypto Briefing). I paid nothing.

## How it works

Every party upstream of the follower is paid on volume, not on the follower's profit: the front end
through its builder fee, the referrer through the referral share, the exchange through fees. Leverage
multiplies volume. So the incentive runs toward more trades, more leverage and more recruits, whatever
the copied trader's results. The "proven trader" is picked from a public list of survivors.

## How it is detected

- **Survivorship, measured.** Hyperliquid publishes every vault ever made. Of 9,476, 6,379 (67%) are
  closed. Of the closed vaults with any PnL, 71% lost money, together -$24.3M. Of the 236 open vaults
  holding at least $10k, 39% are still negative all-time. A record picked from today's list has
  already been through a filter that removed most of the losers.
- **Volume-paid chains.** Any offer where the person sending the link is paid on your trading
  volume or fees, rather than on your profit, is the tell. Ask "paid on what?".
- **On-chain attribution.** Builder codes and referral codes are attached to orders on a public
  chain, so the routing front end and the referrer can both be read off a wallet's fills. A defender
  can see which front end a wallet used and how much fee it paid.
- **UK consumer angle.** Promotion of crypto derivatives to UK retail is itself a red flag under the
  2021 ban and the 2023 financial promotions regime.

## What I ran

A keyless pull of `stats-data.hyperliquid.xyz/Mainnet/vaults` on 3 Oct, summarised by two short
scripts in `sandbox/hl-vaults/`. Figures in the experiment report.

## What I did not run, and why

I did not open Invo, connect a wallet, follow the referral link or copy a trader. Signing up through
a referral link pays the sender, and opening an account is over the line in any case. I did not
measure follower-level returns, the app's own fee rate or referral payouts; the vault endpoint does
not carry them, and getting them needs a wallet's fills from a user who agrees.

## Sources

- Hyperliquid public vault stats, `https://stats-data.hyperliquid.xyz/Mainnet/vaults`, pulled 2026-10-03.
- Hyperliquid docs, referrals: https://hyperliquid.gitbook.io/hyperliquid-docs/referrals, read 2026-10-03.
- Crypto Briefing, "InvoXYZ surpasses Trust Wallet for second place in Hyperliquid builder code volume":
  https://cryptobriefing.com/invoxyz-surpasses-trust-wallet-hyperliquid-volume/, read 2026-10-03.
- FCA PS20/10, ban on the sale of crypto-derivatives to retail consumers, in force 6 January 2021.
