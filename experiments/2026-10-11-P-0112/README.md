# P-0112: a cheaper X cashtag count, 11 Oct 2026

Target: under $0.05 a coin, so the pre-listing X case-control can run on 30 pairs and nightly.

**Keyless mirrors, tried tonight.** xcancel.com returns HTTP 451 "service is suspended". nitter.net
returns 200 but serves a funding and legal notice with no results. nitter.poast.org doesn't resolve,
and nitter.privacydev.net timed out after 20 s. No keyless X search was found working.

**xAI, from the ten xmentions calls already paid for** (`costfit.py`, `costfit.json`). Cost is
$0.034 a call plus $0.00804 per post the search cites, R² 0.977 over ten calls, mean $0.62 a coin.
The model counts by reading posts, so cost scales with the count. $0.05 buys about two cited posts,
and a count capped at two measures nothing. No prompt change gets under the target, because the
reading is the cost.

**Verdict: blocked.** A per-day cashtag count under $0.05 needs a source that returns counts without
returning posts. That means X's own counts endpoint (paid API) or a working Nitter-style mirror. Neither
is available keyless tonight. At about $0.62 a coin, 30 pairs (60 coins) would cost roughly $37 of xAI,
which is over the $10 cap set for this work. That number goes in Field Notes as a costed figure, not a
spend.
