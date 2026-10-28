# P-0248: keep the Munich winners before Smarkets forgets them

28 Oct 2026, nightly probe loop. Built `outcomes.py`: for every Munich "Highest Temperature" market in
`exchange/SNAPSHOTS.csv` not yet recorded, ask the keyless API for the winner and append one line to
`exchange/munich_outcomes.jsonl` (append-only, a desk data file, so step 4 commits it nightly).

Measured on the first run: 28 markets in the snapshots, 9 winners kept (19 to 27 Oct), 3 not settled
(28 to 30 Oct), 16 already dropped by the API (3 to 18 Oct return no contracts now). A second run
added 0, so it does not duplicate. The API keeps a market about ten days, so a nightly run loses none.

Wired into `tasks/nightly.md` step 3 item 5. At 30 kept, P-0245's favourite check re-runs against
this file instead of whatever the API still remembers.
