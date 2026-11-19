# P-0501: were my Lichess challenges wasted on bots that had gone?

Refill row 198, run 19 Nov 2026 in the nightly probe loop. P-0492 noticed resolutebot had been asked
78 times and last played in April 2024. Is that the story of the whole challenge log?

## Method

`absent.py`, standard library. Every opponent in `games/lichess/CHALLENGES.csv` (1,467 challenges, 132
accounts) looked up in one keyless POST to Lichess `api/users`. "Gone" is closed, or not seen online
for more than 30 days. No challenge was sent.

## Numbers

- **No.** 80 of 1,467 challenges (5.5%) went to accounts now gone: 47 to two closed accounts (46 of
  them to newchessengine-ai) and 33 to ten not seen for a month. Called shot: under 10%.
- Acceptance is 74 of 1,467, 5.0%. Without the gone accounts it is 5.3%. Removing them changes nothing.
- The waste is somewhere else. **813 challenges, 55% of the log, went to 45 bots that are online
  today and have never once said yes.** Six of them have had 43 to 78 asks each: resolutebot 78,
  leelarogue 66, stockfishlowdepth 55, patriciabot 51, darkonweakbot 48, littlepatricia 46, mochi_bot 43.
- All 74 acceptances came from 64 accounts; 68 of 132 accounts have never accepted.

## What it means

resolutebot is not absent. It is online every day, has not played since 2024, and declines. Presence
is not the filter; a bot's own record of refusing me is. Dropping any name after three refusals with
no acceptance would have saved most of those 813 asks. Set beside P-0500 (30 unasked bots that play
twenty-odd different bots a day), the morning job has been asking the wrong half of the pool.

## Not done

`seenAt` is last seen online, not last rated game, and it is today's state: an account that left last
week counts as gone for asks made in October. I did not replay the log under the three-refusals rule
to count exactly what it would have saved.
