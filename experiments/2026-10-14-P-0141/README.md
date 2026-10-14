# P-0141: Kolscan v Grinder re-count, KOL-signed or balance-changed only

14 Oct 2026, Trials. Follows P-0128 (9 KOL wallets with activity spanning the window, 7 with a signature
inside it) and P-0134 (a no-op v1 transaction spamming 7 KOL DOGEUS accounts, so a signature on a KOL
account is not a KOL action).

**Question.** Of P-0128's 7 to 9 in-window wallets, how many have a transaction inside the window that the
KOL wallet signed or that changed the KOL token account's balance?

**Called shot.** works at 0.60; 2 of the 9 survive.

## Method

`recount.py`, keyless public RPC (api.mainnet-beta.solana.com), read-only. Window is P-0128's stored one
shifted +3600 s (its mktime bug), 11 Oct 21:23:37Z to 23:23:37Z. For each of the 9 "spans" rows:
`getSignaturesForAddress` (40 newest), keep those with blockTime in the window, `getTransaction`
(jsonParsed, maxSupportedTransactionVersion 1) on each, then: KOL signed = wallet pubkey among the
signers; balance changed = pre/post token balance differ at the token account's index. A wallet survives
if any in-window transaction meets either test. `daumen.py` re-fetched up to 1000 signatures for the two
accounts with none in the window, in case the 40 cap had hidden them.

63 RPC calls, 3 of them 429s retried, 63 s. Then 2 more calls for the full histories.

## Numbers

| wallet | pick | sigs in window | KOL signed | balance-only | survives |
|---|---|---|---|---|---|
| Naruza | trenchcat | 8 | 8 | 0 | yes |
| CoCo | trenchcat | 3 | 3 | 0 | yes |
| West | trenchcat | 16 | 16 | 0 | yes |
| bandit | trenchcat | 4 | 4 | 0 | yes |
| Yami | trenchcat | 2 | 2 | 0 | yes |
| Gasp | Normie | 7 | 7 | 0 | yes |
| Nyhrox | Normie | 11 | 11 | 0 | yes |
| Daumen | trenchcat | 0 of 391 | | | no |
| slingoor | Normie | 0 of 6 | | | no |

- **7 of 9 survive**, against the shot of 2. The 7 are exactly P-0128's floor (the wallets with a first or
  last signature inside the window); the 2 that fall are the span-only ones. Daumen's nearest signatures
  are 9.3 h before and 9.5 h after the window; slingoor's 3.6 h before and 26 min after.
- **All 51 in-window transactions were signed by the KOL wallet.** None was balance-change-only and none
  was spam of the P-0134 kind. The spam P-0134 found sits in the "ever" count (63 accounts), not in this
  window for these two picks.
- The deltas are real two-way trading: every surviving wallet has both negative and positive token
  deltas inside the two hours (buys and sells of trenchcat or Normie around the Grinder's pick time).
  Programs seen: FLASHX8Dr... (Naruza, West, bandit, Gasp), GMGNreQc... (CoCo), pAMMBay6... (Yami),
  term9YPb... (Nyhrox). Not decoded here.

## What it changes

P-0128's answer firms up from "7 to 9" to 7, and the 7 are not inflated by history spam. The weak part
of the P-0128 count was never the in-window figure; it was the window-free "ever had a transaction"
figure, which P-0134 showed includes spam.

## Not done

Did not decode the four programs or classify buys v sells against the pick direction. Did not check
whether the KOLs' trades were before or after the Grinder's 22:28Z pick inside the window (the times are
in results.json; a leg-three question). DOGEUS and Nuts had no spans rows in the right window, so they
were not re-counted.
