# P-0437: is a flat tape before entry a rug tell?

Trials, 13 Nov 2026. Deepen of P-0436, where FPES traded $19k to $22k every hour for six hours and
then fell 99.999% in one.

**Question.** Do the six hourly volumes before a Grinder entry look flatter for trades that lost
(stop-loss, rug) than for trades that took profit?

**Shot.** works at 0.60: no separation, the losers' median coefficient of variation within 0.2 of
the winners'; FPES (about 0.05) flatter than every ledger trade measured; at least 30 trades fetched.

**Method.** `metronome.py`. From `grinder/LEDGER.csv` (89 rows: 61 losers, 27 take-profits), the
most recent 18 of each, interleaved. For each, the pool the scan saw and one keyless GeckoTerminal
call for hourly candles; the six whole hours before the entry hour, an hour with no candle counted
as zero. CV is the standard deviation over the mean of the six. Four seconds between calls and a
five-minute cap, which stopped it at 25 trades (13 losers, 12 winners), all served.

**What came back.**

| | n | median CV | flattest | CV under 0.5 | with six full hours | median CV, six full | median max over min, six full |
|---|---|---|---|---|---|---|---|
| losers | 13 | 1.009 | 0.149 | 4 | 7 | 0.377 | 3.4 |
| winners | 12 | 0.950 | 0.368 | 1 | 7 | 0.732 | 14.9 |
| FPES (P-0436) | 1 | 0.044 | | | | 0.044 | 1.15 |

- Over all 25, nothing: 1.009 against 0.950.
- Eleven of the 25 had trades in fewer than six of the hours, most of them two. For those the CV
  measures how young the token was, not how flat the tape was.
- Among the 14 with six full hours the losers are flatter, 0.377 against 0.732, and four of the five
  flattest trades of all are losers. The flattest, G-0090 (CV 0.149, $86k to $132k every hour), is a
  rug. Of the five rows flagged rugged, two had six full hours: 0.149 and 0.744.
- FPES at 0.044 is flatter than anything in the ledger sample by a factor of three.

**Reading.** As asked, the answer is no: flat volume does not split losers from winners across the
sample. Once the young tokens are set aside there is a lean the right way, on 7 against 7, with the
one metronome-like tape in the sample ending in a rug. That is a hint with a mechanism behind it
(wash volume is tidy, crowds are not) and no weight yet. FPES was an extreme case, not a typical one.

**Against the shot.** Medians within 0.2: yes (0.06 apart). FPES flatter than every trade: yes.
At least 30 fetched: no, 25; the time cap, not the API.

**Caveats.** 25 trades, the most recent ones, so mostly v0.2 entries in October. Hourly volume in
dollars from one source. The six-full-hours cut was made after seeing that two-hour tokens swamp the
measure; it is a post-hoc split and should be treated as one. Losers outnumber winners two to one in
the ledger, so "most flat tapes lost" is partly the base rate.

**Not done.** The other 64 ledger rows. A rule. Nothing in `grinder/` was written.
