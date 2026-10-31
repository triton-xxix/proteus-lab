---
name: restart-discord-session
description: Restart or health-check the Proteus Discord channel session (the proteus-discord screen) after a persona, model or start-script change, or when Luke says the bot is not answering. Interactive sessions only; screen is not on the unattended safe list.
---

# Restart the Proteus Discord session

Drafted 31 Oct 2026 by Smith after the restart was done by hand twice that day (11:17 for the
Neptune rooms in the persona, 18:21 for the model flag) and each time cost a dozen calls of
rediscovery. A scheduled run cannot write under `.claude/skills/`, so this sits here until an
interactive session copies it:
`cp -R /Users/triton/PROTEUS/state/loop/skill-drafts/restart-discord-session /Users/triton/PROTEUS/.claude/skills/restart-discord-session`
and deletes the draft.

## What runs where

- Screen session `proteus-discord`, started by `~/.claude/channels/discord-proteus/start.sh`
  (outside my write roots; edit it only on Luke's word in session). Working folder
  `/Users/triton/PROTEUS/sandbox/discord-session/` (git-ignored) holds the persona pieces
  (PERSONA.md plus DISCORD.md, concatenated into `.persona-combined.md` at start) and `access.json`.
- Healthy process tree, within about five seconds of start: `claude` (the `--model` flag on its
  command line since 31 Oct), then the discord plugin (`bun run ... discord/0.0.4 start`), then
  `bun server.ts` under it.
- Triton's own `claude-discord` screen (script in `~/.claude/channels/discord/`) sits beside it.
  Not mine: never quit it, never edit its script.

## When a restart is needed, and when it is not

- `access.json` edits (who may summon the bot, which rooms, requireMention) are live at once: the
  plugin re-reads the file on every message. No restart.
- `DISCORD.md` or `PERSONA.md` edits load only at start. Restart.
- A change to `start.sh` (model flag, allowed bots, env) needs a restart.
- Token or `.env` changes: restart, and check the token answers 200 on `/users/@me` first
  (print the length, never the value; the 31 Oct check printed two live tokens by matching the
  field type case-sensitively, and rotation became Luke's job).

## Procedure

1. `screen -ls` and note the pid of `proteus-discord`. If it is missing, skip to step 3.
2. `screen -S <pid>.proteus-discord -X quit`. The claude child and the gateway go with it.
3. `screen -U -dmS proteus-discord /Users/triton/.claude/channels/discord-proteus/start.sh`
   (`bash -n` the script first if it was edited; keep its mode 700).
4. Within ten seconds, `ps` for the three processes above. `screen -X hardcopy` comes back empty
   because the TUI draws on the alternate screen, so the process tree is the check, not the screen.
5. If the persona changed, confirm `.persona-combined.md` in the working folder has a fresh mtime
   and carries the new paragraph.
6. Run-log line: old screen pid, new screen pid, start time, the three process ids, what changed.
   Nothing is posted to Discord by a restart; a hello in any room is Luke's call.

## Traps hit

- 31 Oct 11:17: the two Neptune paragraphs added earlier that day had not loaded because DISCORD.md
  is read at start only; the restart was the fix, not another edit.
- 31 Oct 18:21: the model change is `--model claude-sonnet-5-5` on the exec line of `start.sh`,
  then quit and restart. Luke wants Triton C's session on the same model; that script is not mine.
- Posting unprompted in Neptune Work Station is outside the charter; the one-recipient rule stands.
