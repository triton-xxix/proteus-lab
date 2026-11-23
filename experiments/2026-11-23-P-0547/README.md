# P-0547: SEAR no-model baseline, bigger sample and a silence-shortcut check

Deepens P-0546 (EER 14.0% on 50 test bonafide, too few to say much). Same features and scoring
(`deepen.py` imports P-0546's `sear_baseline.py`), now 300 bonafide + 300 spoof from ASVspoof 2019 LA eval
via the HF datasets-server `/rows` API, keyless. Fit median and MAD on 150 bonafide (seed 23), test on
150 bonafide + 300 spoof. 300 bootstrap resamples for the intervals. 240 s in all.

| | EER | 95% interval |
|---|---|---|
| all 44 features | **16.0%** | 13.2 to 19.3% |
| energy and silence features dropped (rms, dynamic range, noise floor, MFCC-0) | 18.7% | 14.7 to 22.3% |
| SEAR's claim (35 features) | 17.65% | |

**Reading.** SEAR's 17.65% sits inside my interval: the claim reproduces on a laptop with no model.
Dropping the six energy and silence features costs about 2.7 points, inside both intervals, so the known
silence shortcut is not what carries this baseline.

Called shot: works at 0.60, full EER about 17% (close) rising to about 25% without energy (wrong: it
rose by under 3 points).

**Not done.** Per-attack EER: the mirror's notes field carries utterance, speaker and subset only, and
`labels.parquet` needs pyarrow, which the venv lacks. 127 of 150 held-out bonafide share a speaker with
the fit half, which flatters the genuine side somewhat. One seed for the split. My 44 features are a
stand-in for SEAR's 35, not their list.
