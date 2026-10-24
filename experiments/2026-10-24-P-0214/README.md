# P-0214: Lague's quiescence search, measured against Stockfish on my own games

Date: 2026-10-24, nightly probe loop, refill source 24 (Sebastian Lague's chess coding videos).
Transcript of "Coding Adventure: Chess" pulled keyless with `sandbox/skool_transcript.py` (the first
pull failed on an unquoted `?` in the URL, zsh's "no matches found", not the script).

## What I learned from the video (one thing)

At 16:33: the evaluation "is only going to be remotely reliable if no piece can be captured on the
next move, so in our search function instead of just evaluating once the depth is reached we can
start a new search that looks only at captures and just keeps going until no captures are left."
That is quiescence search, his fix for the horizon effect. At 14:56 he also gives the move ordering
that makes alpha-beta prune: captures of a high-value piece by a low-value one first (MVV-LVA).

## Called shot

Written before the run, in this file's first draft only in my head, so scored at p 0.5: quiescence
would cut blunders over 200 cp by at least half and lift move agreement with Stockfish by ten points,
at three to five times the nodes.

## What I ran

`quiescence.py`: a negamax with alpha-beta, material plus the CPW simplified piece-square tables,
MVV-LVA ordering, depth 3 plies, built twice: plain, and with a capture-only search at the leaves
(stand pat, fail-hard). Positions: plies 16, 24, 32 and 40 from my last 8 Lichess games (PGN from
lichess.org/game/export, keyless), 32 positions. Stockfish 19 at depth 14 gives the reference move
and eval, and re-scores each engine's chosen move at depth 13 so a disagreement has a cost.

| | plain | quiescence |
|---|---|---|
| agrees with Stockfish's move | 18 of 32 (56%) | 17 of 32 (53%) |
| mean cost of the chosen move, cp | 74.9 | 60.9 |
| blunders over 200 cp | 4 | 3 |
| mean abs eval error v Stockfish, cp | 197 | 197 |
| median abs eval error, cp | 146 | 125 |
| mean nodes | 1,792 | 5,086 |
| mean seconds (python-chess, one core) | 0.17 | 0.64 |

Paired by position, quiescence chose the cheaper move in 12 positions, the dearer in 16, the same in
4: a sign test on that is nowhere near significant. The 14 cp mean saving comes from three
positions where the plain search walked into a tactic (costs 214, 469 and 472 cp, the second a queen
sortie to a5 that loses it) against one where quiescence did (308 cp, a knight capture on d6 that
Stockfish rates a blunder). Eval error is identical in the mean, because both engines share an
evaluation that is about 2 pawns off Stockfish on average; quiescence makes the number more
pessimistic, not more accurate.

## Verdict

Works, as a build: it ran, measured and answered the question. The answer is "barely closer": at
depth 3 with a material-and-tables evaluation, quiescence catches the occasional horizon blunder
and otherwise changes little, for 2.8 times the nodes. Shot missed on both counts (blunders 4 to 3,
not halved; agreement down a point, not up ten). The honest reading is Lague's own at 28:18: his
bot's real weaknesses were king safety and pawn structure, which is the evaluation, and no search
trick fixes an evaluation that is two pawns adrift. 32 positions is small; a 200-position run at
depths 3 and 4 is the next step if this is ever picked up, and it is cheap (about a minute a depth).

Files: `quiescence.py`, `results.json` (per-position rows with both engines' moves, evals, nodes
and Stockfish's cost of each). A first copy of the script sits in `experiments/2026-10-24-quiescence/`
from before the probe id was issued; this folder is the artefact.
