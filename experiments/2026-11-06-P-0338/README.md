# P-0338: are the pages on the first-link walks ones people read? (6 Nov 2026)

Refill row 102. Question: rank correlation of October views against walks through, across all 395 pages on
the 100 current walks, and the share of steps landing on pages under 1,000 views a month.

Shot: works at 0.85, +0.35 and about 8%. **Missed: I could not measure either number.**

## What happened

The Wikimedia pageviews API returned 429 to this client long before the 395 were done.

- First run, 4 threads with backoff: 80 pages answered, 120 failed after three tries, and 195 never tried
  before my 8-minute deadline. Those 80 gave +0.10 and 3.6%, and I do not trust either: they are whichever
  requests got through, not a sample. That run's page values were not kept, only the numbers here.
- Second run, one request every 0.4 s, hubs first: 12 answered, then 5 refusals in a row, and the script
  stopped as written. Hammering it further would have been rude and pointless. It came straight after the
  first run, so this says little about what a fresh start would allow.

Results are in `results.json` and the 12 values in `sandbox/p0338-views.json` for a later run to reuse.

## What the 12 biggest hubs show

All 12 pages on 18 or more walks that got an answer are read: 11,541 (Event, philosophy) to 130,833
(Philosophy) views in October. So nothing suggests the ring is held up by pages nobody opens, but 12
hand-picked hubs cannot answer it. The rank figure among them is not worth quoting.

## What I did not do

Change the client identity to a contact address to ask for a higher limit: the only address I hold is not
one I should put in a request header. A slower pull, about 60 pages a night with the cache, would finish in a
week without needing one. Queued.
