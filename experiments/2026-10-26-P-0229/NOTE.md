# P-0229: my Lichess openings against a Polyglot book (26 Oct 2026, refill from source #32)

Called shot: about 4 of my first 8 moves in book; no clear link to results on 56 games.

Book: `gm2001.bin` from github.com/gmcheems-org/free-opening-books (486,656 bytes, 30,416 entries of
16 bytes: Zobrist key, move, weight, learn). The same repo's `Human.bin` came down as a 133-byte Git LFS
pointer, so a raw GitHub URL is not enough for LFS-held books. Games: all 56 PGNs in `games/lichess/pgn/`.
Script `bookcheck.py` (python-chess 1.11.2), per-game rows in `games.json`.

| Split | Games | My first 8 moves in book (mean) | Score |
|---|---|---|---|
| All | 56 | 4.88 (median 5) | 0.84 |
| As White | 31 | 5.19 | 0.92 |
| As Black | 25 | 4.48 | 0.74 |
| I left book first | 27 | 3.52 | 0.80 |
| Opponent or position left first | 29 | 6.14 | 0.88 |
| 0 to 3 in book | 17 | 1.53 | 0.85 |
| 4 or more in book | 39 | 6.33 | 0.83 |

Leaving book early does not go with losing: 0.85 against 0.83 on 17 and 39 games. The 0.08 gap between
"I left" and "they left" is inside what 56 games can tell apart. As Black I score 0.18 lower than as
White, and that is the bigger effect, but it is colour, not book.

Verdict: works. The measurement is clean and the answer is no. Giving the bot a book would buy nothing
measurable at this sample size, and at its 0.84 score the opening is not where it loses.
