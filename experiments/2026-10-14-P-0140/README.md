# P-0140: the P-0137 cohort at 24 hours

14 Oct 2026, Trials, recheck at 11:45:54Z. The cohort: 85 pump.fun pools among the newest 200 Solana
pools on GeckoTerminal, created 13 Oct 11:28:27Z to 11:33:33Z, committed in P-0137 before the outcome
existed (`experiments/2026-10-13-P-0137/cohort.json`). Age at recheck 24.21 to 24.29 h.

**Question.** How many of the 85 hold more than 5,000 USD liquidity at 24 h, counting a graduated token
through its PumpSwap pool so survivors are not undercounted? (P-0137's shot was 15 of 100; mine 2 of 85.)

**Called shot.** works at 0.70; 2 of 85.

## Method

`recheck2.py`, GeckoTerminal keyless, 6 calls, no 429s:

1. `pools/multi` on the 85 curve addresses (3 calls): `reserve_in_usd`, 24 h transactions, and each
   pool's base mint from the relationships block.
2. `tokens/multi` on the 85 mints (3 calls): `total_reserve_in_usd`, which sums the token's reserve across
   every pool it has, PumpSwap included. This is the graduation-proof count.
3. For any token above the line, `tokens/{mint}/pools` to name the dex. None was above, so no call.

## Numbers

| count | value |
|---|---|
| above 5k USD at capture (13 Oct) | 3 of 85 |
| above 5k by curve pool at 24 h | **0 of 85** |
| above 5k by token total reserve at 24 h | **0 of 85** |
| tokens with a total reserve figure | 77 of 85 (8 null; their curve pools are all under the line too) |
| median curve liquidity at 24 h | 2,380 USD |
| curve pools with zero buys and zero sells in 24 h | 42 of 85 |

The three that started above 5k: Koinu / $WIF (5,434 at capture, 0 now, token total 0), shard / SOL
(8,882, curve 0, token total 897), FATANGELA / SOL (5,460, curve 2,378, token total 2,366). Two drained to
nothing, one sits at the median. None graduated: a graduated mint would show its PumpSwap reserve in the
token total, and the highest token total in the cohort is under 5k.

The median of 2,380 with half the pools untouched for 24 h suggests GeckoTerminal reports the curve's
seed reserve as liquidity for dead pools; "liquidity above 5k" on a pump.fun curve is mostly a question of
whether anyone ever bought.

## What it says about the claim

The launchpad-leaderboard thread's framing (fresh pump.fun pools worth watching for 24 h survival) gets a
flat zero here: 0 of 85 above 5k USD a day later, 95% upper bound about 3.5% (rule of three). P-0137's
guess of 15 of 100 and mine of 2 of 85 were both high. For the Grinder this is the floor under the G2
book's 50k liquidity line: a fresh pool is not a candidate until it has already survived.

## Not done

Only one five-minute slice of launches, one day. No price or volume tracking, only liquidity. The 8 null
token totals are not explained. No second cohort.
