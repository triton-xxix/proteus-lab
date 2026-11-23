# P-0553, Munich ladder gaps (23 Nov 2026, nightly, refill row 234)

Question: how many Munich daily-high ladders skip a whole degree inside their range, and did a skipped degree ever win?

## Sources

- `exchange/SNAPSHOTS.csv` carries only 4 Munich ladders (`gaps.py`, `results.json`), so I read the ladders from the Smarkets API instead (keyless `/v3/markets/<ids>/contracts/`): the last 8 settled markets the API still has (15 to 22 Nov) and the three still open (23, 24, 25 Nov). Raw replies `contracts.json`, `open_contracts.json`, `nov23_contracts.json`; counts `api_gaps.py`; names against slugs `slugs.py`.

## Measured

- 15 to 22 Nov: 8 of 8 ladders whole, 11 contracts each, no gap. Winners all inside, none at an open end.
- 23 Nov: 10 contracts, 1°C missing. 24 Nov: 9 contracts, -2°C and 1°C missing. 25 Nov: 9 contracts, -2°C and -1°C missing. All three span zero.
- Why: a contract's slug drops the minus sign. `-1°C` has slug `1degc`, the same slug `1°C` would have; `-3°C or below` is `3degc-or-below`. Every missing degree on the three ladders is the sign-twin of a degree that is listed (23 Nov keeps -1, loses 1; 24 Nov keeps -1 and 2, loses 1 and -2; 25 Nov keeps 1 and 2, loses -1 and -2). The 22 Nov ladder crossed zero only at its open end (`-1°C or below` against `1°C`, different slugs) and is whole. So it is consistent with one contract per slug, and a ladder whose exact bins straddle zero loses one of each pair. Inferred from 3 ladders, not from Smarkets saying so.

## Did a skipped degree win

Not yet: none of the three gappy ladders has settled. 24 Nov is the live test: my X-0067 is on 2°C with ICON at 2.2°C, and 1°C has no contract. If the high is 1°C, how Smarkets settles it (void, nearest bin, nobody wins) is the next thing to record; `outcomes.py` will catch the winner tomorrow night.

## What it means for the book

- On a winter ladder that straddles zero, one or two whole degrees can have no contract at all. A probability I put on 2°C is fine; a forecast that says "1°C" has nowhere to go. The `call` step should check the contract list for the sign-twin gap before choosing a degree.
- The market's own probabilities on a gappy ladder must sum over fewer bins, so the listed neighbours of a missing degree should carry its mass.

Verdict: works (the gap is real and has a plain cause; the settlement question waits for 24 Nov).
