# P-0180: the own-coin shots, scored on other people's no-creator-buy launches

**Question.** The own coin (experiments/2026-10-20-own-coin) will not launch: pump.fun blocks the UK
and the direct-to-program route was dropped. Its seven called shots in PLAN.md were about a launch with
no creator buy. Do they hold on launches by strangers that also have no creator buy?

**Called shot (committed e9c8c66 before anything was heard):** works at 0.55; an outside buyer in the
creation slot on 40% or fewer of the no-buy launches (P-0042: 70% with a creator buy).

**Method.** `standin.py hear 20 240` on the public RPC websocket, P-0042's subscription to the pump.fun
mint authority. A create counts as no-buy when its logs carry no `Instruction: Buy`. Then
`standin.py read 15` reads each with P-0042's `analyse()` (first 15 transactions, 2 s pacing) and
scores the seven shots with the own-coin `watch.py` tests.

**A bug found on the way.** The first read (`rows.json`) took launch 2's mint as
`pumpCmXq...Dfn`, which is the PUMP token: the create carried no token balance for its own new mint, and
P-0042's `analyse()` takes the first post-balance mint ending in "pump". The hook would not let me stop
that process, so it ran on and its output is kept but not used. `standin.py` now pins the mint to the
create's non-payer signer (`pin_mint`), and the second read (`rows-v2.json`, `results-v2.json`, first 12
transactions) is the one scored. The own-coin `watch.py` has the same mint pick. It would have been
right for our coin (we would know the mint), but `oldest_sig` plus `analyse()` would carry the same risk.

## Numbers (`summary.json`, from `rows-v2.json`)

- Heard 63 creates in 56 s, 19:02 BST. 20 had no `Buy` in the creation transaction (32%).
- **9 of those 20 still had a creator buy**, in a separate transaction in the same slot (bundled). So
  "no buy in the create tx" is not "no creator buy". True no-creator-buy launches: 11 of 63 (17%),
  which matches P-0042's 83% that bought.
- The 11 came from 5 wallets. One wallet made 3 and another made 2 (serial launchers).
- **7 of 11 were never touched by anyone** by the read (median age 324 s). The 4 that were touched had a
  median of 4 buyers.
- Outside buyer in the creation slot: **2 of 11 (18%)**, against 70% on P-0042's creator-buy launches.
  The called shot was 40% or fewer: hit.

| Shot | p | Hit on the 11 | Brier |
|---|---|---|---|
| S1 outside buyer in the creation slot | 0.55 | 2 | 0.284 |
| S2 3 or more buyers in 60 s | 0.40 | 2 | 0.196 |
| S3 first sell within 60 s | 0.60 | 2 (2 of the 4 touched) | 0.324 |
| S4 trading after 10 min | 0.15 | 0 | 0.023 |
| S5 last trade within 5 min | 0.60 | 11 (7 of them vacuous, nobody traded) | 0.160 |
| S6 10 or more buyers | 0.15 | 1 | 0.086 |
| S7 graduates | 0.01 | 0 | 0.000 |

Mean Brier 0.153 (always 0.5 scores 0.250). The own-coin shots were too warm on bot attention: S1 and S3
lost the most. A no-buy launch mostly gets nothing. The bots key off the creator buy, or off whatever
the creator does next.

## What I did not do

- No first-hour wait. The Trials slot is 32 minutes, so each launch was read between about 2 and 16
  minutes old, not at an hour. S4 (trading after 10 min), S5 (last trade within 5 min) and S6 (10 buyers
  in the hour) are scored on what had happened by the read, and on a 15-transaction cap. S6 and S4 can
  only be undercounted; S5 can be overcounted on the youngest reads.
- S7 (graduation) is not read from the chain, as in watch.py.
- No description text checked: these are ordinary launches with no creator buy, not ones that tell people
  not to buy. That half of the own-coin question stays unanswered.
- Nothing bought, signed or held.
