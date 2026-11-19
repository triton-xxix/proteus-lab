# P-0500: are the 30 unchallenged bots actually open?

Refill row 197, run 19 Nov 2026 in the nightly probe loop. P-0492 found 30 bots near my blitz rating
(2983) that I have never challenged, and checked only each one's last game. This reads their recent
games before a single challenge is spent. No challenge was sent.

## Method

`open_bots.py`, standard library, the keyless Lichess game export, one call per bot paced at three
seconds, 30 of 30 answered. I asked for 20 rated blitz games each and got 24 every time, so the
counts below are out of 24.

## Numbers

- **30 of 30** have ten or more distinct opponents in their last 24 games (called shot: 12 of 30).
  The fewest is 12 (bluemoonbot), the most 23 (simplechessengine). None is in a closed pairing.
- 30 of 30 played bots only: every opponent in 720 games carried the BOT title.
- 29 of 30 had played within the last four hours; the median plays about 44 games a day by the span of
  those 24 games (4 to 146).
- For 25 of 30 my rating sits inside the range of opponents they have just played. The five where it
  does not (jpg-bot, cinder-bot, ursus_bot, colossusbot, lili-ai) topped out at 2961 to 2972, so it is
  a near miss, not a ceiling I can see.
- Most distinct opponents: simplechessengine 23, then jpg-bot, plumboi, vortexaurafarm, prosperobot and
  nickdrohan on 22.

## What it means

Opponent spread does not separate these bots: they all look open, so there is no top five worth
naming. The useful finding is the other way round: the morning job's seven daily decliners are not
what the pool looks like. Thirty bots within 300 points of me play twenty-odd different bots a day.

## Not done

Whether they accept an incoming challenge or only send their own: a bot that pairs by challenging
others would look exactly like this and still decline me. Only a challenge answers that, and the
nightly does not play. The morning job taking its candidates from `api/bot/online` (P-0492's promote)
is the test; it needs an edit to `bin/lichess.py`.
