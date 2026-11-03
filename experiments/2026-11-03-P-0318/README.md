# P-0318 Why the Grinder has been quiet since 20 Oct: not the gates, the bankroll

P-0185 found 0 G entries after 16 Oct and 0 R01 entries after 20 Oct, and the nightly's "binding constraints" line has been read
as a gate story every night since. `gates.py` replays every snapshot since 20 Oct through paper.py's own `GATES` (imported,
unchanged). `results.json`.

| | 14 nights, 20 Oct to 3 Nov |
|---|---|
| candidates | 2,081 |
| passed every gate | **128** (4 to 14 a night; 9 tonight) |
| failed exactly one gate | 200: age 128, vol_h1 21, liq 20, top10 16, lp 7, vol_h24 7, mint_auth 1 |

So the gates were letting tokens through every night. The block is one step later, in `open_book`: it enters only while
`bankroll >= stake`. The v0.2 book has 83 closed trades, 0 open, and a bankroll of £1,000 plus realised P&L = **£11.33**,
under its £100 stake. The book is bust and cannot open anything. The "binding constraints" line prints whenever 0 entries open,
so it has been naming the biggest gate when the real cause was the money.

Verdict: works. The desk is quiet because the v0.2 bankroll is gone (£11.33 of £1,000), not because of a filter. Two things follow,
neither done tonight, since a scheduled run does not change a pre-registered rule: the zero-entry line should say "bankroll
below stake" when that is the reason (a scorer-side fix, allowed), and whether a bust book restarts is Luke's call or a new
registered version, not a patch. Age is the gate that turns away most near-misses (128 of 200).
