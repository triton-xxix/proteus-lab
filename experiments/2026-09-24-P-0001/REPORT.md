# P-0001: rugcheck insider flags on the Grinder's gate-passers

Snapshot 2026-09-24T07:32:26Z, 105 rows, 8 pass the v0.1 gate. Rugcheck report refetched 2026-09-24 09:21.

- gate-passers: 8 fetched; graphInsidersDetected > 0 on 6; insider-flagged top holders on 0; insider-named risks on 0.
- non-passers sample: 30 fetched; graphInsidersDetected > 0 on 16; insider-flagged top holders on 0; insider-named risks on 0.

| group | symbol | position | graphInsidersDetected | insider holders | insider pct | insider risks | score |
|---|---|---|---|---|---|---|---|
| gate-passers | SI | G-0004 | 0 | 0 | 0 |  | 1 |
| gate-passers | FUNKOS | G-0001 | 5 | 0 | 0 |  | 1 |
| gate-passers | familiars |  | 37 | 0 | 0 |  | 1 |
| gate-passers | NPC | G-0003 | 15 | 0 | 0 |  | 29 |
| gate-passers | goon |  | 4 | 0 | 0 |  | 1 |
| gate-passers | KCAT |  | 9 | 0 | 0 |  | 1 |
| gate-passers | JEANCOIN | G-0002 | 0 | 0 | 0 |  | 1 |
| gate-passers | UPTOBER |  | 5 | 0 | 0 |  | 1 |
| non-passers sample | UNTXD |  | 6 | 0 | 0 |  | 1 |
| non-passers sample | GATO |  | 6 | 0 | 0 |  | 1 |
| non-passers sample | BOME |  | 2483 | 0 | 0 |  | 37 |
| non-passers sample | SOON |  | 0 | 0 | 0 |  | 40 |
| non-passers sample | PEPENOM |  | 5 | 0 | 0 |  | 1 |
| non-passers sample | CYSIC |  | 0 | 0 | 0 |  | 34 |
| non-passers sample | Hermès |  | 33 | 0 | 0 |  | 33 |
| non-passers sample | SI |  | 0 | 0 | 0 |  | 32 |
| non-passers sample | RHEA |  | 14 | 0 | 0 |  | 74 |
| non-passers sample | CAME CMC |  | 0 | 0 | 0 |  | 1 |
| non-passers sample | ARCHIBROWN |  | 0 | 0 | 0 |  | 1 |
| non-passers sample | TROLL |  | 241 | 0 | 0 |  | 1 |
| non-passers sample | HOOD |  | 0 | 0 | 0 |  | 54 |
| non-passers sample | PUMP |  | 61 | 0 | 0 |  | 1 |
| non-passers sample | Egg |  | 25 | 0 | 0 |  | 1 |
| non-passers sample | MOONSHOT |  | 0 | 0 | 0 |  | 34 |
| non-passers sample | coomer |  | 0 | 0 | 0 |  | 1 |
| non-passers sample | USELESS |  | 2119 | 0 | 0 |  | 1 |
| non-passers sample | CATO |  | 10 | 0 | 0 |  | 33 |
| non-passers sample | Madison |  | 4 | 0 | 0 |  | 1 |
| non-passers sample | GIGACAT |  | 0 | 0 | 0 |  | 1 |
| non-passers sample | SUI |  | 0 | 0 | 0 |  | 1 |
| non-passers sample | AXIS |  | 0 | 0 | 0 |  | 52 |
| non-passers sample | .fomo |  | 0 | 0 | 0 |  | 1 |
| non-passers sample | OTC |  | 13 | 0 | 0 |  | 29 |
| non-passers sample | Bonk |  | 48 | 0 | 0 |  | 7 |
| non-passers sample | MGOAT |  | 0 | 0 | 0 |  | 1 |
| non-passers sample | IT |  | 6 | 0 | 0 |  | 1 |
| non-passers sample | RAY |  | 2099 | 0 | 0 |  | 56 |
| non-passers sample | AGENTX |  | 0 | 0 | 0 |  | 77 |

## What this says

- `graphInsidersDetected` is populated and cheap: one report call per token, already made by the scanner. Six of eight gate-passers and 16 of 30 non-passers carry a non-zero count. Median 5 in both groups.
- The per-holder `insider` flag is false on every top holder of all 38 tokens, and no `risks` entry names insiders. Those two are dead fields for this feed; the graph count is the only signal.
- The count is not normalised. BOME 2483, USELESS 2119, RAY 2099: big old tokens with many wallets score highest, so a raw threshold would punish age and size, not bundling. A useful gate needs it scaled by holder count or pair age.
- On the open positions: NPC (G-0003) 15, FUNKOS (G-0001) 5, SI (G-0004) 0, JEANCOIN (G-0002) 0. A "zero only" rule would have blocked two of the four and six of the eight passers; a "five or fewer" rule would have blocked NPC alone. Whether either rule earns its place is a question for scored outcomes, not for this probe. Rule unchanged.
- Next: once 20 positions are scored at 24h, split them by this count and look. Queued as a probe with a date.
