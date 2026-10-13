# P-0134: the DOGEUS "dust" on seven KOL wallets

13 Oct 2026, Trials. Follows P-0128 (Kolscan KOL wallets v the Grinder).

Question: the seven Kolscan KOL token accounts for DOGEUS (G-0071) each show one transaction at
11 Oct 21:17:41Z. Was that an airdrop to them, or their own buys?

Called shot: works at 0.65, "one transaction sending DOGEUS dust to 5 or more KOL wallets (an airdrop,
not buys)".

## Method

`dust.py`, keyless public RPC: `getSignaturesForAddress` on each of the 7 token accounts from P-0128's
result, then `getTransaction` (jsonParsed) on what came back.

## Numbers

- One signature across all 7 accounts: `2rVuXS1sTR1i...` (full in `result.json`). The seven KOLs: decu,
  trunoest, Coler, theo, bandit, Jijo, The Doc.
- One signer, `BuekUk3YMmm7...`, not a KOL wallet. One program, `DhpyNWkd...84HY`, not the token
  program or a known DEX.
- DOGEUS balance changes: 0. SOL changes: the signer's fee of 0.000015 SOL and nothing else. No
  account created, no rent paid.
- It is a version 1 transaction. The public RPC refuses it with error -32015 unless
  `maxSupportedTransactionVersion` is 1; my first call with 0 got nothing back.

So it was neither: not an airdrop (no tokens moved) and not buys (no KOL signed). It is a no-op that
lists the KOL token accounts so it lands in their signature histories, the shape of history spam or
address poisoning. My shot had the "one transaction, five or more wallets, not buys" part and the word
"airdrop" wrong.

## What it changes

P-0128's "ever had a transaction" counts (63 wallet-pick accounts) include spam like this. A
signature on a KOL account is not a KOL action. Any re-run should count only transactions the KOL
signed, or with a balance change on the KOL account.

## Not done

The full 91 x 4 re-run in this probe's title (about 55 minutes) did not fit the slot, and the 12 Oct
background pass already finished (P-0128 README). I did not decode program `DhpyNWkd...` or look for
other accounts it lists.
