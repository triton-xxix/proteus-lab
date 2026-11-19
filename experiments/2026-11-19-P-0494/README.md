# P-0494: do loudness peaks find the moments people replay?

From the harvest (H-0694, a clipping "moment-finder" idea). Run 19 Nov 2026 in the nightly probe loop.

## Question

On a public video, do the five loudest moments land within 15 seconds of the five highest points on
YouTube's most-replayed graph?

## Method

`moments.py`, standard library plus the yt-dlp and ffmpeg already in the folder, keyless. yt-dlp searches,
reads each video's heatmap (100 segments) and downloads the audio. Loudness is RMS per second in dB,
smoothed over five seconds. On each side: the top five peaks at least 30 seconds apart, leaving out the
first 5% of the video (the graph always starts high) and the last 10 seconds. A hit is a loudness peak
within 15 seconds of a replay peak. Chance is five times the share of the video that lies within 15
seconds of a replay peak.

## Numbers

| Video | Length | Hits | Chance |
|---|---|---|---|
| oWEQ3nQHNYM (fails compilation) | 946 s | 1 of 5 | 0.84 |
| 84UcOcuuMUc (goals) | 300 s | 3 of 5 | 2.58 |
| pH3vPDJwuSM (goals) | 908 s | 1 of 5 | 0.89 |
| R9upxtnvy9c (goals) | 827 s | 1 of 5 | 0.97 |
| Total | | 6 of 20 | 5.28 |

Called shot, committed first (242bfc8d): works at 0.55, 2 of 5. The first video gave 1 of 5; the four
together give 1.5 of 5 against 1.3 by chance. Loudness alone does not find the replayed moments.

Also measured: 10 of 17 videos checked had no heatmap at all, so the most-replayed graph is missing for
most of what a search returns.

## Not done

Four videos, two genres, one loudness measure. No onset or crowd-noise feature, no speech, no picture.
The three-of-five on the short video is what chance gives when five 30-second windows cover half of it.
Files: `results-fails-of-the.json`, `results-greatest-goals-premier.json`.
