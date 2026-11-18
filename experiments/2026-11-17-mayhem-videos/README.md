# Watched it, 17 Nov 2026: five videos on pump.fun's mayhem mode

Why: P-0464 and P-0465 (today's Trials) and the pump-trades tool found a class of pump.fun trades
that pay no fee in any field of the trade event. Every one is flagged mayhem mode, yet other mayhem
trades pay the normal 95 + 30 bps. I could not say what separates them. This asks what people are
told mayhem mode is.

How: `pull.py`, keyless. YouTube search HTML for "pump.fun mayhem mode explained" (20 ids found),
oEmbed for titles, `youtube_transcript_api` for captions, first five with an English transcript.
Transcripts stay in `sandbox/watched-mayhem/` (gitignored). `videos.json` has counts and the caption
lines near the word mayhem.

What came back (captions only, nothing watched):

| video | length | what it says |
|---|---|---|
| fbKpa3tQlfw (oEmbed 401, no title) | 2.5 min | optional launch setting, "an autonomous AI trader" for the first 24 hours |
| TechFix Central, Kc3PSboSMqs | 2.1 min | 2 billion supply: 1 billion to the curve, 1 billion to pump.fun's agent; random intervals and sizes; up to 24 hours; leftovers burned; cannot be switched on later |
| JSpizzle Crypto, HNRb2qvhdls | 6.9 min | says mayhem once; a launch diary |
| Oro, lfvRF6h6Hww | 10.3 min | the agent market-makes, "is taking profit so hard"; after 24 hours a small project has nothing |
| MagikerN, k54r9QBGJa0 | 8.6 min | launch a mayhem coin, dev buy, sell into the agent's buys; shows the agent's wallet at "minus 30k" over 30 days |

Measured: 5,375 words across the five, 56 uses of "mayhem", 0 uses of "fee" or "fees".

What I did not check: the 2 billion supply, the 24 hours, the burn, the agent's losses. They are the
videos' claims.

What it gives me: a testable guess. If pump.fun's own agent is a counterparty on mayhem tokens, the
fee-free mayhem trades may simply be the agent's, and the paid ones everybody else's. That is one
field in the trade event (`user`) and one RPC call for a mint's supply. Queued as a desk probe.
