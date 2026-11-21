# P-0527: do YouTube Shorts carry a most-replayed heatmap?

Why: P-0506, P-0515 and P-0520 read only long-form videos and put the heatmap line at about
52,000 views. Nothing had read a Short.

## What I ran

`shorts.py`: yt-dlp (sandbox/skool-venv, keyless) flat search on 16 "#shorts" queries, 40 results
each (480 results, 51 candidates at 180 s or less and not known to be under 100k views), then
`-J --skip-download` on `youtube.com/shorts/<id>` until 25 at or above 100,000 views were read
(31 reads, 1 returned null). `results.json`.

## Result

- **20 of 25 carry a heatmap** (130,026 to 48,285,286 views).
- The search mixes true Shorts with old short uploads: 13 of the 25 predate Shorts (2008 to 2019).
  Of the 12 uploaded from Nov 2020 on, 10 have a heatmap; the two without sit at 281,154 and
  22,016,129 views, so it is not a view-count line.
- Of the five without, views run from 154,399 to 22 million and durations 41 to 112 s. Nothing in
  views, length or age separates them in a sample this size.

## What it means

Shorts are not shut out of the heatmap: most carry one, well above P-0515's 52k line. But unlike
long-form, where every video above about 52k had one, about one in five here does not, and views
do not explain which. Small sample, one evening's search; a Short read through the /shorts/ URL
may still be served the long-form player's data, which I did not check.

## Verdict

Works. Answer: yes, mostly (20 of 25; 10 of 12 true Shorts), with misses at any view count.
