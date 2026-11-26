# P-0570: how wide is the no-model ASVspoof EER across split seeds?

Trials 26 Nov 2026, refill row 244. P-0559 found P-0547's 16.0% EER sat below five other clip splits
(17.3 to 19.1). Question: over 50 clip-split and 50 speaker-split seeds, what is the spread, and do
P-0547's 16.0% and SEAR's published 17.65% sit inside it?

Shot: works at 0.75, "clip-split median about 17.8%, 5 to 95 band about 16 to 19.5". Hit.

## Method

`seeds.py`, py312 venv. P-0559's picking and cache (600 clips, 0 fetched), P-0546's 44 features computed
once; each seed refits the bonafide median/MAD and rescores. Seed 23 clip split reproduces 0.1600, so the
set is P-0547's. Seeds 1000 to 1049. 62 seconds.

## Numbers (`results.json`)

| split | median | 5th to 95th | min to max | sd |
|---|---|---|---|---|
| clip (half the bonafide) | **18.0%** | 16.2% to 19.3% | 15.3% to 19.5% | 0.95 |
| speaker (half the speakers) | 18.1% | 16.1% to 20.1% | 15.1% to 20.4% | 1.24 |

- P-0547's 16.0% is at the 6th percentile of clip splits: a lucky draw, not an error.
- SEAR's 17.65% sits at the 36th percentile of clip splits and the 38th of speaker splits: inside the
  band, so this sample does not contradict it.
- Speaker split moves the median by 0.1 point and widens the band by about a third. P-0559's 0.8 point
  gap was mostly seed noise too.

## So

On 600 clips, any single-split EER for this baseline carries about plus or minus 1.5 points from the
split alone, before the test-set bootstrap. Quote it as 18% (16 to 19), not 16.0%.

## Not done

No per-attack breakdown, no larger clip count (the band would narrow with more bonafide in the fit),
no second dataset. No browser.
