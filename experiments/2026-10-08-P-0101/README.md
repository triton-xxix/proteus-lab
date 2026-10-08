# P-0101: Form 4 cluster buys against SPY, 2025 (8 Oct 2026)

## Rerun, 9 Oct 2026 00:30: no edge

Luke named a contact for the SEC user agent in session, and EDGAR served all four 2025 quarters
(about 39 MB). Same script, rules unchanged from the text below:

- 20,945 open-market purchase rows on Form 4; 691 cluster events (3+ insiders, 14 days); 611 priced.
- 30-day excess return over SPY: mean -0.2%, median -1.6%, 5% trimmed mean -1.2%.
- 45% of clusters beat SPY. t = -0.24.

Verdict: **not worth it**. Cluster buys as defined here, bought the day after the filing, did not beat
the index over a month in 2025. `summary.json` and `events.json` hold the numbers. The register
line still reads blocked because `probe.py` takes one verdict per probe; this section supersedes it.

## Original run, 8 Oct

Verdict: **blocked**, before any data arrived.

`cluster.py` is written and ready: SEC's quarterly Insider Transactions Data Sets (2025 Q1 to Q4),
open-market purchases (code P) on Form 4, a cluster is three or more distinct owners buying the same
issuer within 14 trade days, the event is dated by the filing that completes it, entry at the
first close after that filing, exit 30 calendar days on, excess over SPY on the same dates, one
event per ticker per 30 days. Prices from Yahoo's keyless chart endpoint.

What happened: sec.gov answered 403 to the zip with two user agents (a project string, then a
GitHub noreply address), and the datasets page itself returned "Request Rate Threshold Exceeded",
which is EDGAR's fair-access block for automated clients without a declared contact. I did not try
further addresses: SEC asks for a real contact, and making one up to get past the gate is not mine
to do.

Needs: a contact name and email Luke is happy to put in an EDGAR user agent (SEC's own rule for
automated access). With that, the script runs unchanged; estimated 10 to 15 minutes.
