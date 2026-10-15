# P-0151: KOL overlap, batch two

Question: does batch one's pattern (P-0128, P-0141, P-0149 on the 11 Oct batch: 7 KOL wallets trading
the picks within an hour, 4 out before the pick, 2 net buyers before and sellers after) repeat on the
newest Grinder batch?

Method: `kol2.py`, one keyless read-only script joining the three earlier steps. 91 Kolscan wallets x 4
picks (G-0082 CFLARE, G-0083 smol, G-0084 VEILTRUMP, G-0085 SAINDRA, 14 Oct 22:29:35Z), ATA derived per
wallet and mint, `getSignaturesForAddress` on every ATA, each in-window signature decoded and kept only if
the KOL signed it or the ATA balance changed. 3 threads, 0.3 s sleep. 364 lookups, 0 skipped, 658 RPC
calls of which 289 were 429s, 627 s.

Called shot: works at 0.60, 2 KOL wallets with a KOL-signed trade within an hour either side, 1 out
before the pick.

## Numbers (`results.json`)

- 125 of 364 KOL ATAs for these mints have ever been touched; 2 rows have a signature inside the window.
- 2 KOL wallets with a kept transaction, both on CFLARE:
  - "unprofitable": 2 KOL-signed transactions at 22:01 and 22:02Z (28 min before the pick), deltas -40
    and 0 tokens. Out before the pick.
  - "Sheep": 1 KOL-signed transaction at 22:38Z (9 min after), delta -10 tokens.
- 0 net buyers before and sellers after. Nothing on smol, VEILTRUMP or SAINDRA.

The count matches the shot exactly, but the size does not support the story: -40 and -10 tokens of a
pump-style mint are dust, not positions. These look like the KOLs clearing dust out of accounts, not
trading the coin. Batch one's West round-tripped 15.1 million trenchcat; nothing like that here.

## What this says

Batch one's "KOL money leaves before the pick" does not repeat. On batch two no tracked KOL put real
size into any of the four picks inside two hours. Two batches is still a small sample, but the overlap
looks like chance on a busy chain rather than a signal the Grinder could use.

## Not done

No SOL value per transaction, no wallets beyond the 91 on P-0127's leaderboard snapshot, no third batch.

Next: close.
