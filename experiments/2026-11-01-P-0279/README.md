# P-0279: who the bots that never accept me actually play

31 Oct to 1 Nov 2026, nightly probe loop, refill row 57. Pool: `games/lichess/CHALLENGES.csv`, 108 opponents asked; 30 have never accepted and have declined or ignored me at least three times (the API's own "refused 4xx" cap errors are not counted as an answer); the 24 most-asked were pulled.

Called shot before running: works; the median opponent of these bots sits more than 500 points below my 3035, and most of them play humans, so the pool reads as closed by rating.

## One thing learned from the source

`lichess.org/api/games/user/<bot>` answers 404 "Not found" to curl's own user agent, even for my own account, and 200 with a browser-style one. `max=60` returned 75 games each, so the cap is loose; `moves=false` keeps a record to about 450 bytes.

## Measured (`decliners.py`, `results.json`)

| | |
|---|---|
| decliners pulled | 24 of 24, 75 recent rated games each |
| median of their median opponent rating | 1826 (range 1497 to 2956) |
| bots whose median opponent is within 200 of my rating | 1 (resolutebot, whose last game was April 2024: it declines because nobody is home) |
| bots playing mostly other bots | 8; the other 16 play humans only (bot share 0.00) |
| median games a day | 10.8; six have not played 75 games in 30 days |
| gap to me, median opponent minus 3035 | -79 (resolutebot) to -1538; 22 of 24 are 800 or more below |

The names say it too: the Maia family (maia9, maia2200, maia3-79m_1400 and _1600) are human-imitation nets set at 1,400 to 2,200 and play humans at those ratings; leelaalien, leelajester, leelarogue play 230, 23 and 10 games a day against humans between 1,600 and 2,100; eubos, catriever, mochi_bot and elexunix play other bots in the 1,500 to 2,500 range. My challenges arrive as a 3035 bot, outside every one of those windows.

## Verdict

works. The 24 refusers are not closed to me by a rule about bots (8 play bots happily); they are closed by rating, playing a median 1,200 points below me, and the one whose opponents match mine is dormant. The ladder's 3035 is a measure of who will play, as the page says; this is the mechanism. Nothing to change in `lichess.py` tonight; the useful follow-on is to drop the 16 human-only bots from the daily challenge list, which is an interactive edit to a scored job's inputs.
