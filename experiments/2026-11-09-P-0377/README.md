# P-0377: does mempool.space's fastest fee clear the next block, over a longer watch?

## Question

P-0376 watched for 20 minutes and no block arrived. Same test, 30 minutes: does the recommended next-block fee, seen before the block, clear it, and by how much does it overpay the block's median?

## Method

`fees.py` polled the recommended fees and the chain tip every 30 s from about 12:32 to 13:02 UTC on 9 Nov 2026. For each new block it kept the recommendation last seen before the block appeared and compared it with the block's fee range and median from the API. Forward only. It is P-0376's script with a longer window, a results file written at each block, and added columns (block time, full range, at or above median).

## Numbers

1,815 s, 60 polls, 0 errors, 2 blocks. `results.json` has the rows.

| block | rec seen before | block min | block median | over median |
|---|---|---|---|---|
| 975,177 | 1 sat/vB | 0.124 | 1.098 | -0.098 |
| 975,178 | 1 sat/vB | 0.110 | 0.136 | +0.864 |

The fastest fee cleared the minimum of both blocks, and sat at or above the median of one of the two. Mean over the median +0.383 sat/vB. The recommendation was 1 sat/vB for both, and every tier read 1, so the tiers said nothing different from each other. By the last poll fastest had moved to 2.

## Called shot

Said works at 0.85, clears the minimum of every block, overpays the median by about +1 sat/vB. Measured: cleared both, mean +0.383. The verdict and the clearing hit; the size was out by more than half.

## What this does not say

Two blocks, one quiet half-hour, so the mean is close to no information. "Clears the block minimum" is a weak test: the minimum was 0.11 to 0.12 and the recommendation about eight to nine times that, so almost any fee passes. It says nothing about a busy mempool, which is when a fee estimate earns its keep. I did not send a transaction, so whether a real 1 sat/vB payment confirmed in the next block is not measured here. A block's median and whether a given fee gets in are different things.
