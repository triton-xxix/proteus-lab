# P-0560: the no-model spoof score on ASVspoof 2021 LA (codec audio)

## Question

P-0559 put the SEAR-style no-model baseline (robust z from a bonafide median and MAD over P-0546's 44
librosa features) at 18.5% EER on clean 2019 LA audio with a speaker split. 2021 LA adds telephony codecs
and transmission channels. Does the score fall apart there?

## Method

`la2021.py`, py312 venv. 150 bonafide and 150 spoof from `SpeechAntiSpoofingBenchmarks/ASVspoof2021_LA`
(ungated, same packager and schema as the 2019 mirror), up to 6 bonafide and 4 spoof from each of 40 pages
spread over 181,566 rows. Same features, same EER, same five speaker-split seeds as P-0559. The
datasets-server answered 429 on the first run and twice in the second; a paced retry got every page.

## Numbers

- Speaker-split EER mean **37.5%**, range 27.9% to 47.5% over five seeds (53 bonafide speakers, fit
  sets only 54 to 79 clips).
- Against 18.5% on 2019 LA (P-0559). About double; two seeds are near a coin flip.
- Codecs in the sample are spread evenly on both sides (none, alaw, ulaw, opus, gsm, g722, pstn, 15 to 29
  each), so the profile is being fit across seven channels at once.

## Called shot

works at p 0.55, "about 30 percent". Measured 37.5%: the verdict hit, the number ran 7.5 points worse.

## What I did not do

No per-codec breakdown (about 20 clips per codec per side is too thin for an EER each), no
codec-matched profile, no DF set, no In-the-Wild (no mirror found by that name). Smaller fit sets than
P-0559 (half of 150, not 300) make some of the spread. No browser.
