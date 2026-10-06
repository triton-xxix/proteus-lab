# The exchange book

Started 3 Oct 2026 on Luke's word, after he asked what could stand in for Polymarket, which is
barred in the UK. Smarkets is a UK-regulated betting exchange whose politics and current-affairs
markets are the nearest legal thing: prices set by people trading against each other, readable
keyless (`api.smarkets.com/v3`). This book asks whether my forecasts beat those prices.

Paper only. No account, no stake. Charter: a stake stays on the execution ladder.

## What gets called

- Any open contract on a Smarkets politics or current-affairs market whose event starts within 120
  days of the call. Listed, without prices, by `exchange.py markets --days 120`.
- At most **two calls a night**, in the nightly or interactively, so the book is a steady habit and
  not a burst.
- Every call is a probability for one contract, with a one-line reason built from public sources
  (news, polls, official data). "No idea" is not a call; skip the market.

## Blind, then the price

1. Choose from `exchange.py markets` (names only). Do not open `SNAPSHOTS.csv`, the Smarkets site or
   any price for that market before the call.
2. `exchange.py call MARKET CONTRACT P "reason"`, then commit and push.
3. Only then `exchange.py anchor`, which records the market's mid price at that moment. It refuses a
   call that is not committed. The commit timestamp before the anchor time is the proof of order.

Blindness to the price is on my honour, as in the judgement book; the commit order is the part a
reader can check.

## Scoring

`exchange.py score` reads each contract's `state_or_outcome` (winner or loser) and scores my
probability and the anchored mid by Brier. The measure is me minus market, averaged over settled
calls. Negative means I am better. Voided markets are dropped, not scored.

A contract goes `open`, then `halted` from the event start, and stays halted until Smarkets
resolves it to `winner` or `loser`. Halted is not settled: the call waits, however long that takes.

**No anchor.** `anchor` is tried once per call, the first run after its commit. If the contract has
no two-sided price at that moment (only a bid, or only an offer), the call is recorded with
`mid_at` set and `market_mid` empty, and that is final. It is never re-anchored later, because a
later price is better informed than the one I called against, and after the event it is a
post-result price. A call with no anchor is still settled and its own Brier published in the book,
but it has nothing to be compared with, so it is outside me minus market and does not count toward
the 60 and 100 floors (the Counted line below already requires a two-sided price at anchor).
Written 7 Oct 2026 after X-0001 and X-0002 (Quebec, PQ) hit a one-sided book: bid 94.3, no offer.

## Pass marks (also in PASS-MARKS.md)

| Criterion | Line |
|---|---|
| Counted | settled calls committed before their anchor, with a two-sided price at anchor |
| Sample floor | 60 settled calls |
| KILL | At 60 or more, me minus market of +0.020 or worse; at 100, anything above 0.000 |
| KEEP | At 60 or more, me minus market at or below 0.000 |
| Horizon | 100 settled calls or 30 Jun 2027; at the horizon anything not KEEP is KILL |

On KEEP the book continues and it is the forecasting record Luke asked for. It does not earn an
executor on its own. On KILL calls stop and the book is published as it stands.

## Files

`exchange.py` (all commands), `SNAPSHOTS.csv` (nightly prices for every open market, the history
nobody else keeps in public), `BOOK.csv` (the calls).
