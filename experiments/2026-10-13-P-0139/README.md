# P-0139: R01 backfill, 8 to 11 Oct

13 Oct 2026, Trials. Follows P-0121, which wired R01 (`paper.py --apply-r01`) forward only.

Question: VARIANTS-3 line 40 says the nights before the wiring can be scored after the fact from the
snapshots, the Telegram rows and minute candles, "so no night is lost". Can they?

Called shot: works at 0.60, "15 backfilled R01 rows (4+4+4+3), all closed by candles".

## Method

`backfill.py`: for each snapshot from 2026-10-08T12:00Z in order, close R01's open rows at that night's
paper time with `exit_v02` (minute candles through `paths`), then enter `select_r01` picks at the time
v0.2 entered that night (its first G- row within 3 h of the snapshot) at the snapshot price, with v0.2's
slots, stake and bankroll check. Then close what is still open as of now. It writes
`grinder/LEDGER-R01.csv` and lists the backfilled ids in `backfill.json`; it refuses to run on a
non-empty R01 ledger.

## Numbers

- 15 rows, R-0001 to R-0015: 4, 4, 4 and 3 a night (11 Oct had only three marker-free passers, as
  P-0121's replay found). All 15 closed on candles; no `_nightly` fallback, so no row used today's
  price for a past exit. Every night started with all slots free.
- R01: -£362.60 on 15 positions (12 stop-losses, 3 take-profits, 0 rugs), -£24.17 a position.
- v0.2 on the same nights (G-0059 to G-0074): -£389.04 on 16 positions (13 stop-losses, 3
  take-profits, 0 rugs), -£24.32 a position.
- 7 of R01's 15 are the same tokens v0.2 held, with identical exits. R01's own picks: BORDR (+£92.20),
  SENTS, PAWS, PQC, a different "Altai " mint, brigitte, Glorp (all stop-losses).

So far a draw: expectancy within 15p a position, and no rugs on either side, so the rug-rate test that
R01 exists for has nothing to bite on yet. 15 of the 40 R01 closes the verdict needs (D-008); the KILL
check at 20 is about two nights away.

## Not done, and caveats

- Entry time is v0.2's real entry time each night, entry price the snapshot's; same as paper.py.
- Glorp on 11 Oct is a legitimate R01 pick from the 11 Oct snapshot; it is unrelated to the voided
  G-0077 Glorp, which was v0.2 entered on 12 Oct from that same stale snapshot.
- PATHS.csv carries no R- rows. The ledger has no column for "backfilled"; `backfill.json` lists the
  ids, and every R- row up to R-0015 is backfilled.
