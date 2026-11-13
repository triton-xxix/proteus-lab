# P-0436: where FPES went (voided G-0075)

Trials, 13 Nov 2026. Refill source 165. P-0425 got no minute candles for G-0075 from the pool the
11 Oct snapshot named, so one of the three voided trades could not be walked.

**Question.** Which pools does the token have, what happened to the $1.8m of liquidity, and can the
12 to 13 Oct trade be walked from any of them?

**Shot.** works at 0.60: daily candles show FPES fell more than 99% from 0.42 before the 12 Oct
22:54Z entry; 0 minute candles in the 24 h after entry from either pool, so the trade still cannot
be walked. Called after seeing the pool list (price $0.0000017, reserve $1,900) and no candles.

**Method.** `pools.py`, keyless GeckoTerminal: the token's pool list, then daily, hourly and minute
candles per pool. Six requests two seconds apart, no retry. Read only.

**What came back.**

| pool | dex | daily candles | now |
|---|---|---|---|
| 6ZWXXub4... (the one the snapshot named) | pumpswap | 13, 10 Oct to 6 Nov | $0.0000017, reserve $1,901, 0 trades in 24 h |
| DF5dbQwJ... | pump-fun curve | 1, 10 Oct only | reserve $0 |

The pumpswap pool, hour by hour around the snapshot (22:23Z on 11 Oct):

| hour (UTC) | open | close | volume |
|---|---|---|---|
| 11 Oct 17:00 to 22:00, six hours | 0.3865 | 0.4237 | $18,908 to $21,657 every hour |
| 11 Oct 23:00 | 0.4237 | 0.0000028 | $966,807 |
| 12 Oct 00:00 | 0.0000028 | 0.0000029 | $380 |
| 12 Oct 22:00 (last before entry) | 0.0000036 | 0.0000035 | $2 |
| 13 Oct 23:00 (next trade at all) | 0.0000035 | 0.0000033 | $134 |

- The token went from 0.42 to 0.0000028 inside the 23:00Z hour of 11 Oct, at most 97 minutes after
  the snapshot was taken and 23 hours before the paper entry. A fall of 99.999%.
- At the entry minute the last traded price was 0.0000035. The stale 0.4202 was about 119,000 times
  the market.
- Minute candles in the 24 h after entry: 0. The pool's next trade of any kind was at 23:00Z on
  13 Oct, 24 hours and 6 minutes later. P-0425's empty answer was right: there was nothing to serve.
- The curve pool has one day of life (10 Oct, the launch) and nothing after. Its hourly and minute
  requests came back 429; with one daily candle on 10 Oct they could not hold the entry window.

**Reading.**

- G-0075 cannot be walked, and now I know why: it was a paper buy of a token that had been dead for
  a day. From the stale price, v0.2 would have booked a rug at the first candle, about a full stake.
  From the live price there was no candle to enter on. The void was the right call.
- The six hours before the collapse are the interesting part. Price up about 1% an hour, every hour,
  on $19k to $22k of volume, never more, never less. That is not a crowd. The snapshot saw $1.8m of
  liquidity and a steady climb and the v0.2 gate passed it.
- So the one thing I did not know: the rug was in the hour after the scan, and the pre-rug tape was
  a metronome. Whether that flatness is visible at scan time for other rugs in the ledger is the
  next question.

**Against the shot.** More than 99% down before entry: yes, 99.999%. Zero minute candles in the
window from either pool: yes for the pumpswap pool; the curve pool's minute call was refused (429),
and its only daily candle is 10 Oct. Still cannot be walked: yes.

**Caveats.** One token. The 23:00Z hour is one candle; the minute the liquidity left is in the
minute file range (the call returned 1,000 candles ending 12 Oct 22:11Z) but I did not read it.
"Not a crowd" is my reading of six hourly volumes, not a measurement against other tokens.

**Not done.** The ledger and VOIDED.csv were not touched. The metronome check across the ledger's
rug exits is queued.
