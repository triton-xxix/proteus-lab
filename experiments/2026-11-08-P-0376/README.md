# P-0376: does mempool.space's recommended fastest fee clear the next block?

## What happened

`fees.py` polled every 30 s for 1,211 s (40 polls, 0 errors), keeping the recommendation last seen before each new block. No block arrived, so the question has no forward answer.

## Was the zero real?

Yes. `tipcheck.py`, run straight after, shows the tip was block 975,113, mined 23:39:25 UTC by its timestamp, 22.4 minutes before the 00:01:50 check, with nothing after it. The chain simply went quiet for the whole window. At one block per ten minutes on average, a 20-minute gap has about a 13% chance.

## What the check also shows

The last recommendation was 3 sat/vB fastest, 1 for everything else. The last eight blocks' medians run 0.12 to 4, and five of the eight had a fee-range minimum under 0.2. So at this moment a 3 sat/vB fee looks more than enough for blocks like these, but that is a look-back on blocks mined before the recommendation I saw, and it is not the test I set out to run.

## Called shot

Said works, clears every block, overpays the median by about 1 sat/vB. Measured nothing. Verdict blocked, so the shot misses.

## Not done

No block compared at all. The fix is a longer window: 30 minutes has about a 95% chance of at least one block and a few hours would give a real sample. `fees.py` takes the window from `RUN_SECONDS`.
