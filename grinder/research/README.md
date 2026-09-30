# The research desk

Started 30 Sep 2026 on Luke's word ("yes start the research desk now"). The Grinder bought on
on-chain numbers alone, and the round-1 replay (`grinder/harness/REPLAY.md`) showed the tokens it
picks mostly die inside a day (median -71% at 24h) whatever the exit. This desk looks for what the
chain does not show: who is talking about a token, whether someone paid to be seen, and what the
market is talking about that night.

## What it produces

1. **`MENTIONS.csv`**, one row per token, night and source (`mentions.py`). Every row is as of the
   snapshot time; nothing after it is counted. Sources: X through the xAI API's `x_search` (Luke's
   key, named by him 30 Sep; about $0.04 a token measured over 58 (the first test was $0.16), at most 8 tokens a night), Reddit through the
   Arctic Shift archive (six subreddits, keyless), DexScreener paid orders and boosts (keyless).
2. **A nightly digest** (`digests/YYYY-MM-DD.md`), written by one Sonnet child from a pull of the
   night's narrative sources (`narrative.py`): what is being talked about, which tokens keep coming
   up, anything that contradicts the Grinder's picks.
3. **`SOURCES.md`**, the register. Every source carries how it is pulled and a track record I keep:
   for per-token sources, how the tokens it flagged did against the ones it did not; for narrative
   sources, whether what it said came true. A source earns trust by that record, not its name.

## How it feeds the Grinder

Only through the replay harness. A signal becomes an entry rule only after it is listed in
`harness/VARIANTS-2.md` (committed before the data existed) and clears the bar in PASS-MARKS. The
desk never buys anything and never changes a live rule.

## Costs

xAI spend lands on Luke's xAI account, not the Proteus card, and is recorded in `SPEND.md` under
its own line from the API's reported cost per call. Backfill of the 58 round-1 tokens: $2.51, measured. Nightly: 8 tokens and one narrative summary,
about $0.50 a night.
