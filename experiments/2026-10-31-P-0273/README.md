# P-0273: Sketch Stadium's public watch stream

31 Oct 2026, nightly probe loop. Source: harvest H-0482, Show HN "Sketch Stadium, watch your agent play Pictionary" (sketch.wakeshift.ai, 35 points). Read-only: no MCP install, no agent connected, nothing from the page acted on.

Called shot before running: works; the watch page has a server-sent event stream readable without an account, and it emits somewhere between 20 and 100 events in two minutes.

## What I did

- `curl` the game page: 200, 5.2 KB of HTML, `<body data-live="/games/q5ucru/live">`. The page script (`/static/sketch.js`, 11 KB) opens `new EventSource(live)` and listens for `snap`, `gone` and `submit`; a 250 ms `setInterval` only redraws the clock.
- `curl -N` the live endpoint with `Accept: text/event-stream` for 125 seconds, saved to `sandbox/sketch-live.txt`: 200, `text/event-stream`, 183.5 KB, `retry: 2000` on the first line.
- `summarise.py` parses the blocks and writes `results.json`.

## Measured

| | |
|---|---|
| events in 125 s | 38 `snap`, 18.2 a minute; no `gone` or `submit` seen |
| shape | every event is the full game state (players, strokes, guesses, hint, word, phase, clock), not a delta; median 4.9 KB, 33 strokes and 11,369 polyline points at most in one snapshot |
| sequence | seq 228667 to 228723, so 19 of 57 sequence numbers never arrived: the server coalesces or skips snapshots a slow reader did not need |
| rounds | four (21957 to 21960), phases drawing 34, reveal 4; six named agents on the scoreboard |
| strokes | a polyline `p` of `[x, y]` pairs in a 0 to 100 box, with a stroke style; the "SVG subset" the author describes is this path form, not SVG text |
| guesses | the word is in the stream in the clear during the drawing phase (`word` and `hint` fields), so a watcher sees the answer before the guessers do |

## Verdict

works. The public page exposes an SSE stream with no account, about 18 full-state snapshots a minute at about 5 KB each (roughly 90 KB a minute to hold open). A listener needs only `curl -N` or `EventSource`. What I did not do: connect anything over `/mcp`, or run the agent-picker's install prompts, which the HN thread itself warns against pasting into an agent. The MCP push mechanism the author built it to show is therefore untested; what I measured is the spectator feed.
