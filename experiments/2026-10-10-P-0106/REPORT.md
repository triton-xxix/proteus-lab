# P-0106: Grinder bundles from the public Solana RPC, sized before running

Date: 2026-10-10, nightly probe loop.

## Called shot
The median gate-passer needs over 20 pages of 1,000 signatures to reach its first transaction, so all
163 is a multi-hour pull on the public RPC.

## What I ran
`size.py`: `getSignaturesForAddress` paged back from now for five Grinder entries (G-0059 to G-0063),
capped at 30 pages a mint, 0.4 s between pages. Numbers in `size.json`.

| Token | Pages | Signatures | Reached the first transaction? |
|---|---|---|---|
| Gary | 30 (cap) | 30,000+ | no |
| OWLNIGHT | 30 (cap) | 30,000+ | no |
| ZKDARK | 30 (cap) | 30,000+ | no |
| Gunner | 30 (cap) | 30,000+ | no |
| QPAWS | 29 | 28,032 | yes |

164 calls in 174 s, 13 of them 429s. About one page a second.

## Verdict
Blocked, on access, not on the idea. Four in five gate-passers have more than 30,000 transactions
by the time I look, so reaching the creator block costs 30 pages or more a token. For 163 tokens that is
over 5,000 calls and over 90 minutes even if none is deeper than the cap, which most are. Doing it at
snapshot time instead (a token a few hours old has far fewer transactions) or through an indexer that
returns a mint's first transactions directly would make it cheap. The forward version, recording the
creator block at each night's snapshot, is the one worth queuing.
