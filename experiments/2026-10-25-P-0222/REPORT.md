# P-0222: Polymarket resolution lag and dispute settings

From refill source 28 (Polymarket's help page on resolution). The page says a proposal needs a $750 bond and then sits in a 2-hour challenge period before UMA settles it. The question: what do 200 recently closed markets on the keyless Gamma API actually show?

Ran `lag.py` on 25 Oct 2026 about 23:45 UK. Numbers in `results.json`.

- The 200 most recently closed markets all closed inside 11 minutes (23:29 to 23:41 UTC), and all 200 are flagged `automaticallyResolved`. The newest-closed slice is a burst of short sports and crypto markets, not a sample of Polymarket.
- **Bond:** 173 of 200 carry `umaBond` 250 and 3 carry 500; none carries the 750 the help page names. 24 have no bond field.
- **Challenge window:** 92 set `customLiveness` 900 s (15 minutes), 15 set 1,800 s, 4 set 7,200 s (the documented 2 hours), 2 set 600 s, 2 set 0, 85 set nothing (the oracle default).
- **Lag from end date to close:** median 2.7 h for the 68 sports markets, where `endDate` is the tip-off, so this is mostly game length. Median 0.04 h for the other 132. A third closed before their stated end date.

So the documented $750 and 2 hours are a ceiling for hand-proposed markets, not what the automated markets run on: those use a $250 bond and a 15-minute window. Anyone timing a dispute from the help page would be wrong by a factor of eight on time.

What this does not answer: dispute rates. All 200 show two "proposed" statuses and none shows "disputed", but a slice this narrow cannot say how often disputes happen. A wider pull (by end date over a month) would.

Verdict: works.
