# P-0053: Lichess bot v0, one game against another bot

Run interactively 2 Oct 2026, 01:16 BST, on Luke's word ("bot against bot is fine").

## Setup

- Engine: Stockfish 19, official macOS universal build from GitHub releases (sf_19, sha256
  a1f0e3bc...daa77), unpacked in `sandbox/stockfish/`. This Mac is an Intel i7-9750H.
- python-chess 1.11.2 installed into the project venv.
- `bot.py`: lists online bots (`/api/bot/online`, 60 returned), challenges them casual 3+2 one at a
  time, listens on `/api/stream/event` for accept or decline, then plays from
  `/api/bot/game/stream/{id}` at 0.3 s of Stockfish a move.

## What happened

- Two bots declined: "I'm not accepting challenges from bots" (leelapieceodds, leelaqueenforknight).
- charibot accepted inside a second. I had Black.
- **Won by mate on move 17**, in 16 seconds of wall time. 17 moves sent, 0 errors.
  https://lichess.org/L8DoZpEZ
- charibot is not a 2000 player: it gave up its queen with 11. Qxf7+. The 2000 shown for all three
  bots looks like Lichess's default for an unplayed blitz rating, so the opponent picker sorted on a
  placeholder. The PGN also shows my side as 3000, presumably the same kind of default.

## Verdict

Works: the full loop (challenge, accept, stream, move, finish, export) runs with no errors. It says
nothing about strength. v1 should pick opponents by games played, not by the rating number, and
accept incoming challenges as well as sending them.

Files: `bot.py`, `log.txt`, `result.json`, `game.pgn`.
