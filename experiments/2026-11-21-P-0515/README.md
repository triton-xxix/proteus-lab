# P-0515: where does YouTube's most-replayed line fall, and do old videos need more views?

**Question.** P-0506 bracketed the line for a most-replayed heatmap between 38,676 and 58,618 views on
30 videos, with one 2013 video at 339,919 views and no graph. Narrow the bracket and test age.

**Method.** `heat2.py`: yt-dlp (sandbox/skool-venv) flat searches on ten craft and lesson queries,
30 results each, keeping ids whose flat view count was 30,000 to 80,000 and not in P-0506 (46
candidates), then `-J --skip-download` per video until 25 were read. Run 12:33Z to 12:35Z on
21 Nov 2026; 25 of 25 read, no errors, no rate limit. Nothing downloaded.

**Called shot:** works at 0.65; lowest view count with a heatmap 40k to 50k, and videos over five
years old without one at higher views than new ones.

## Numbers

- **7 of 25 have a heatmap.** Lowest with: **51,534**. Highest without: **52,222**.
- Every video at 51,496 views or fewer lacked one (17 of 17). Every video at 52,257 or more had one
  (6 of 6).
- **Pooled with P-0506 (55 videos), the line sits between 51,496 and 52,257 views**, with one
  crossover: 52,222 views and no graph (`96ZNp2fDLh4`, a 55-minute knitting video). Above 52,257 the
  only video without one is still P-0506's 2013 outlier at 339,919.
- **Age, over five years (before 21 Nov 2021) v newer:** old without at 45,136 to 51,496, old with
  from 58,271. New without up to 52,222, new with from 51,534. Same line on both sides; this sample
  shows no sign old videos need more views. 7 old v 18 new, so it is weak either way.

## Shot v measured

- Verdict called works: hit.
- Number: I said the lowest with would be 40k to 50k. It was 51,534. Miss, by a little.
- Age: I said old videos would need more. They did not, on 7 old videos. Miss.

## What it says

The graph appears at roughly 52,000 lifetime views, and the line is sharp: a 700-view window held
the whole crossover in 55 videos. For a moment-finder, skip anything under 52k views before spending
a download. The 2013 outlier stays unexplained; one video is not an age effect.

## What I did not do

- No recent-views figure exists in yt-dlp's JSON, so "it needs recent views" is still untested.
- English craft searches, one day, YouTube can move the line any time.
- Did not read the remaining 21 candidates; the 25 cap was the probe's.
