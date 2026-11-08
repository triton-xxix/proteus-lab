# P-0366: nightly log of what trades on Munich daily-high markets

**Question.** P-0365 could only see 4 of 12 recent Munich markets, because the API drops volumes about
three days after close. Can a nightly log keep the number before it goes, so the weather book can say
how many of its anchors were ever traded?

**Called shot.** works at 0.50 (a coin, since I had read P-0365's raw pull first); at least 4 markets
logged on the first run, total volume about 2.

**Method.** `exchange/volumes_log.py` (standard library, keyless) takes every Munich market in
`exchange/SNAPSHOTS.csv` and `exchange/BOOK.csv` starting within the last three days or later, calls
`/volumes/` and `/last_executed_prices/`, and appends one row per market to `exchange/munich_volumes.jsonl`.
Wired as step 6 of the exchange block in `tasks/nightly.md`.

**Numbers, first run 8 Nov.** 4 markets logged, total volume 2, book contracts with a visible trade 0 of 4,
errors 0.

**A thing P-0365 got wrong.** Last executed prices are overwritten at settlement: every loser prints 0 at
about 23:46 UTC. So the absence of a trade on a settled loser means nothing. Only a row logged before
settlement can tell. The nightly at about 22:30 UTC is before it, for the market of that day.

**What I did not do.** The 0 of 4 is uninformative for the two settled markets, for that reason. No row has
yet been logged before a settlement. The first useful row is tonight's. A market with a settlement later
than the 22:30 UTC run would still be read, but its losers' prints would be from the earlier close, so check
the timestamps at 14 nights. Nothing in the book or scoring changed.
