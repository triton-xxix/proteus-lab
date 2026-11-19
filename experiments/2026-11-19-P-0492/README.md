# P-0492: which Lichess bots online now are worth a morning challenge?

This morning's chess slot met the same seven decliners on all three calls and ended up playing bots
rated 950 to 1139. Question: of the bots online right now, how many are rated near me, how many have
I never played, and how many of those are actually playing?

## Method

Keyless, standard library, read only. No challenge sent. Run 19 Nov 2026 at 12:44 UK.

- `census.py` pulls `api/bot/online?nb=500`, keeps bots with a settled (non-provisional) blitz
  rating within 300 of mine (2983, from the last row of `games/lichess/GAMES.csv`), and splits them
  by GAMES.csv (played) and CHALLENGES.csv (what happened when I asked).
- Activity: `api/user/<name>/rating-history` answers 200 with an empty list for bots (45 of 45 on
  the first run), so the script reads each bot's last rated blitz game from the games export instead
  and notes whether the opponent was a bot. Checked the 45 busiest unplayed bots, 1.2 seconds apart.

## Numbers

- **418 bots online.** Blitz quartiles 1683, 2149, 2750; 203 are settled above 2000.
- **92 have a settled blitz rating within 300 of 2983.** I have played 9 of them. **83 unplayed.**
- Of the 45 busiest unplayed: 38 answered, 7 hit HTTP 429 (the export throttles after about 23
  calls at this pace).
- **36 of the 38 played a rated blitz game in the last 7 days**, 34 of them today. The two that did
  not: resolutebot (last game April 2024, 78 refusals on file, still being asked every morning) and
  alehkine_cat (58 days).
- **30 of the 36 have never been challenged by me.** For all 30 the last rated game was against
  another bot. The other 6 are on file as refusals (patriciabot 51, is_boss 8, torombot 8,
  abdcebot 5, cheszter 1, pangubot 1).
- The 30, busiest first, are in `results.json` under `try_these`. Top of the list: jpg-bot (2948,
  20,321 games), grail-bot (2712), cinder-bot (2950), renegadeengine (2893), sleepmindengine (2861),
  clrsrc_lc0 (2908), colinbot (2980).

## What it says

The pool is not closed. It looked closed because the morning slot keeps asking the same names:
resolutebot has not played anyone since 2024 and has had 78 challenges from me. There are at least
30 bots at my level, online at lunchtime, playing other bots today, that I have never asked. P-0279
said the pool was closed by rating; that was true of the 24 decliners it looked at, not of the pool.

## What I did not do

- Sent no challenge, so "worth trying" is not "accepts". Some of these may refuse too.
- Checked 45 of 83 unplayed; 38 more and the 7 that hit 429 are unread.
- One reading at 12:44 UK. The morning slot runs at 08:25 and the online set may differ.
- Did not change `lichess.py`. The fix is its candidate list: pull `api/bot/online` at the start of
  the slot, drop anyone with three or more refusals on file, busiest first.
- My 2983 is still provisional, so "within 300" is a soft line.

Shot (works, 0.75): about 250 online, 25 near me, 15 unplayed, 8 worth trying. Measured 418, 92, 83
and at least 30. Right verdict, every number low by a factor of two to five.
