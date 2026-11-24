# P-0559: does P-0547's 16.0% EER survive a speaker split?

## Question

P-0547 scored SEAR's no-model baseline (robust z-scores from a bonafide median and MAD over P-0546's
44 librosa features) at 16.0% EER on ASVspoof 2019 LA eval, fitting on a random half of 300 bonafide
clips. 127 of its 150 held-out bonafide shared a speaker with the fit half. Was that flattering it?

## Method

`speaker_split.py`, the py312 venv. The same 600 clips as P-0547 (same offsets and picking, all audio from
the cache, 0 fetched). Check first: the clip split with P-0547's seed 23 gives 0.1600 again, so the set is
the same. Then five seeds: fit on bonafide from 33 of the 66 bonafide speakers, test on bonafide from
the other 33 plus all 300 spoof. Beside each, a clip split of the same sizes with the same seed.

## Numbers

| | mean EER | range over 5 seeds |
| --- | --- | --- |
| speaker split | **18.5%** | 17.2% to 19.8% |
| clip split, same sizes | 17.7% | 17.3% to 19.1% |
| P-0547 (clip split, seed 23) | 16.0% | one draw |

- Speaker overlap is worth about 0.8 points of EER. Small.
- The bigger gap is the seed: P-0547's 16.0% sits below all five other clip splits (17.3 to 19.1).
  P-0547's own bootstrap (13.2 upward) resampled the test set, not the fit/test split, so it missed this.
- 47 of the 48 spoof speakers are also bonafide speakers (LA spoofs real speakers' voices), so a
  speaker-disjoint test on the spoof side is not possible in this sample; only the genuine side was split.

## Called shot

works at p 0.6, "mean about 18 percent, within 4 points of 16.0". Measured 18.5%. Hit.

## What I did not do

No per-attack breakdown (labels.parquet needs pyarrow, still absent). No speaker split of spoofs. No
second dataset. No browser.
