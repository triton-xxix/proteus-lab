# P-0506: what decides whether a YouTube video has a most-replayed heatmap?

**Question.** P-0494 found 10 of 17 searched videos had no most-replayed graph. Views, age or length?

**Method.** `heat.py`: yt-dlp (sandbox/skool-venv) search, 10 results each for three unrelated
queries (sourdough starter, bicycle chain repair, clawhammer banjo), then `-J --skip-download` per
video. Nothing downloaded. Run 12:38Z on 20 Nov 2026; 30 of 30 read, no errors, no rate limit.

**Called shot:** works at 0.70, lowest view count with a heatmap about 30,000, none above 100,000
without one.

## Numbers

- **22 of 30 have a heatmap, 8 do not.**
- **Lowest views with one: 58,618.** Without: 4,860 to 38,676 on seven videos, then one outlier.
  The line falls somewhere between 38,676 and 58,618 views on this sample.
- **The outlier: `vv-nYYJO_5k`, 339,919 views, uploaded Feb 2013, no heatmap.** So "none above
  100,000 without" missed. Other 2013 to 2015 uploads (211k, 479k, 704k, 4.6m views) do have one, so
  age alone does not explain it. My guess, not tested: the graph needs recent views, and an old video
  whose views are mostly a decade old falls under the line.
- **Length does not decide it.** Without: 79 to 754 seconds. With: 91 to 3,555 seconds. A 91-second
  video has one.
- Upload dates without: 2013 to May 2024, five of eight from 2023 to 2024 (all low-view).

## What it says

Views decide it, at roughly 40k to 60k, with old videos a likely exception. For the moment-finder
idea that means: skip anything under about 50k views before spending a download.

## What I did not do

- No recent-views figure exists in yt-dlp's JSON, so the "recent views" guess stays a guess.
- 30 videos, English searches, one day. The line is a bracket, not a measured threshold.
