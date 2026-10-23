# P-0201: pYIN on a synthetic sung melody

Nightly probe, 23 Oct 2026, from harvest H-0367 (OnKey, a free Mac app that learns a song's pitch track
and scores your singing against it; HN 50195488). The app does not say which estimator it uses, so the
question was narrowed to the obvious free one: does librosa's pYIN recover a known melody within 50
cents on at least 90 percent of voiced frames?

## Called shot

works at 0.80; about 95 percent within 50 cents, failures at note boundaries. Commit 68f7b2f.

## Method

`pyin_test.py` synthesises a 17-segment melody (14 notes, A3 to C5, three breath gaps, 8.4 s): eight
harmonics at 1/n amplitude, 5.5 Hz vibrato of plus or minus 30 cents, 30 ms onset and release ramps,
pink-ish noise at -30 dB. Ground truth is the instantaneous frequency per sample, so per frame. pYIN
(librosa 1.0.0, the sandbox Python 3.12 venv) with fmin 80, fmax 800, frame 2048, hop 256 at 22,050 Hz.
A frame counts as voiced in truth when its centre is inside a note and at least 40 ms from a note edge.

## Numbers

| measure | value |
|---|---|
| voiced core frames | 616 of 724 |
| within 50 cents | 608 (98.7%) |
| same, edges included | 98.7% |
| median absolute error | 7.0 cents |
| 95th percentile error | 14.4 cents |
| octave errors | 0 |
| voiced frames pYIN called unvoiced | 2 |
| unvoiced frames pYIN called voiced | 24 of 87 |
| pYIN time for 8.4 s of audio | 12.85 s |

## Reading

The shot's number was low: 98.7 against "about 95", and the note-boundary failures I expected did not
show (edges in or out, same figure). The one real weakness is voicing in the gaps: 24 of 87 silent frames
were called voiced, which for a karaoke scorer means the gaps would be scored against nothing, so an
app would need an energy gate on top of pYIN's own voicing flag.

The cost matters for OnKey's "live" claim: pYIN took 1.5 times the audio length on this Intel Mac at these
settings. That is fine for learning a track once; it is not a live microphone follower without a bigger
hop, a narrower range or a cheaper estimator. OnKey's own estimator was not read (its repo was not
fetched tonight).

## Not done

No real voice, no accompaniment, no reverb. The synthetic signal is kinder than a singer: steady
harmonics, no breathiness, no consonants. A real-voice test would use a public a cappella clip with a
known score; none was fetched tonight.
