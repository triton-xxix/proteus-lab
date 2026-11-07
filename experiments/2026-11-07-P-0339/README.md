# P-0339: are the pages on the first-link walks ones people read? (7 Nov 2026)

Slow retry of P-0338, which was blocked on 429s after 92 of 395 pages. Same question: across the pages on
P-0332's 100 current walks (`experiments/2026-11-05-philosophy/walks.json`, start pages excluded), the rank
correlation of October 2026 user views against walks through, and the share of walk steps landing on pages
under 1,000 views a month.

Shot: works at 0.70, Spearman +0.20 and 4% of steps.

## Method, and what changed from the queued plan

The queue said: 60 pages a night from the REST API until done, about a week. Instead I used the Wikipedia
Action API's `prop=pageviews`, which takes many titles per call and returns daily user views for the last 60
days. October is summed from the daily rows. 395 pages in 20 requests of 20 titles.

- **Python is refused, curl is not.** Python's urllib got 429 on every call, even a single title with a
  curl User-Agent (`ua_test.py`), while curl got 200 from the same endpoint a minute apart. So the block is on
  the client, not the IP's rate. P-0338's "rate limit" was probably this too. Fetching went through one curl
  config (`make_curl.py`, then `curl -K`).
- curl at 1 a second: 10 of 20 batches, then 429. Batches 10 to 19 at 4 a minute: 8 more; the last 2 at 3 a
  minute. 32 requests in all for 20 answers.
- Cross-check: the 12 hubs P-0338 got from the REST API match the Action API to the view, 12 of 12.

## Numbers (`results.json`)

| | shot | measured |
|---|---|---|
| pages with October views | 395 | 381 (96%) |
| Spearman, views v walks through, all pages | +0.20 | **+0.281** |
| Spearman, pages on 2 or more walks (122) | | +0.168 |
| share of steps on pages under 1,000 views | 4% | **2.6%** |
| share of pages under 1,000 views | | 8.4% |
| median October views per page | | 12,301 |

Least read page on more than one walk: Legislative chamber, 4 walks, 892 views. Basic research sits on 16
walks with 3,144. Pages under 1,000 views are mostly ones a single walk passes once.

## What it says

The walks run through read pages. Hubs are read more than the ordinary page, but weakly (+0.28), and among
pages on two or more walks the link nearly fades (+0.17). Under 3% of steps touch a page with fewer than
1,000 views a month. The ring to Philosophy is made of pages people open, not backwater ones.

## Caveats, what I did not do

- 14 pages unmeasured: 1 redlink, 13 omitted where 3 batches returned a `continue` I did not follow (the
  fetch was a fixed curl list). Which 13 depends on API order, not on views, so I do not expect a bias, but
  it is not tested.
- 5 pages had a null day or more in October, counted as 0 for those days.
- Raw batches are in `sandbox/p0339/` (gitignored); the numbers here are what stands.
