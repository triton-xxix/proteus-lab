# P-0546: does a laptop reproduce SEAR's no-model baseline on ASVspoof 2019 LA?

**Question.** SEAR (arXiv 2609.39847, intel write-up 21 Nov) says a tools-only baseline, 35 librosa
features with median and MAD from genuine clips only, scores EER 17.65% on ASVspoof 2019 LA with no
model. On 200 labelled clips, do I get near that, and which features move most on spoofed audio?

**Source.** SEAR ships questions only (refill 218 hold, 22 Nov). Audio came from the ungated HF mirror
`SpeechAntiSpoofingBenchmarks/ASVspoof2019_LA` (LA eval, 71,237 rows) through the datasets-server
`/rows` API, keyless. Its `/filter` API answered HTTP 500, so I paged `/rows` at 31 offsets spread across
the split and kept the first 100 of each label. 200 flacs in 102 s, then 29 s to score on the Intel Mac.

**Method** (`sear_baseline.py`). 44 features per clip (13 MFCC means and stds, spectral centroid,
bandwidth, rolloff, flatness, ZCR, RMS means and stds, contrast, a noise floor, dynamic range, YIN f0
median and spread, high-band energy share). Not SEAR's exact 35: their list is in the paper, mine is a
close stand-in written from memory of the write-up. Median and MAD fitted on 50 bonafide clips (seed
23); scored on the other 50 bonafide plus all 100 spoof. Score = mean robust |z| (primary, as coded
before the run); median |z| also reported.

**Numbers** (`results.json`):

| | EER |
|---|---|
| mean robust \|z\|, 44 features | **14.0%** |
| median robust \|z\| | 26.0% |
| SEAR's claim | 17.65% |

Features that move most on spoof (median |z| spoof minus held-out bonafide): f0 spread +1.31, spectral
bandwidth +1.30, MFCC-0 spread (loudness variation) +1.29, dynamic range +1.21, RMS mean +1.10. Best
single feature: bandwidth, EER 20%.

Called shot: works at 0.50, EER about 25%. Verdict right, number wrong: the crude version did better
than the paper, not worse.

**What I did not do / caveats.** 50 test bonafide means each bonafide clip moves EER by about 2 points,
so 14% against 17.65% is inside the noise; "reproduces, not beats". Speakers can repeat across fit and
test halves. ASVspoof 2019 LA has a known silence-length shortcut, and the RMS and dynamic-range
features may be reading it rather than synthesis artefacts. No 2021 LA, no per-attack breakdown, one
seed. Detection side only.
