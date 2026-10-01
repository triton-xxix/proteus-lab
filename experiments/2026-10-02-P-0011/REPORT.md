# P-0011: Lichess bot API, what a bot account needs

Run interactively 2 Oct 2026, on Luke's go ("convert the chess account, all permissions stay").

## What a bot needs, as found

1. A fresh account with no games played (a played game blocks the upgrade). Luke made it on 1 Oct;
   the login is in the PROTEUS vault as "Login".
2. A personal API token with `bot:play`. Only the account owner can make one, because it needs a
   password sign-in. Luke's token is "LiChess Triton-proteus": never expires, 21 scopes including
   `bot:play` (also email, messaging and preferences, kept on his word).
3. One call: `POST /api/bot/account/upgrade` returned 200 `{"ok":true}`. The account title is now
   BOT. This cannot be undone: the account can never play as a human again.
4. To take challenges, a bot holds `GET /api/stream/event` open. It answered 200 and sent two
   keep-alive lines in 8 seconds, with nothing queued.

## Not yet done

No engine is wired and no game has been played. The first game is planned against Luke. Next
probe: a minimal bot (accept a challenge from one named account only, play legal moves from a
local engine, resign after N moves) run in the sandbox. Bots cannot play humans in rated pools,
only by challenge, which suits a one-opponent test.

Script `upgrade.py`, numbers `result.json`.
