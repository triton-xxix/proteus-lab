# P-0432: do the short gap-and-go videos state a win rate?

Trials, 13 Nov 2026. Refill source 152. Follows P-0409 (11 Nov), which found 0 of 3 long gap-and-go
videos stating a win rate and guessed the claims live in the short ones its five-minute floor cut.

**Question.** Of the six on-topic videos P-0409 dropped, how many state a win rate in what is said,
and does any give a trade count beside it?

**Shot.** works at 0.60: 6 of 6 captions fetched; 3 of 6 state a win rate; 0 give a trade count
beside it.

**Method.** `pull.py`: the six fixed ids, oEmbed for titles, `youtube_transcript_api` for captions,
the same win-rate and count regexes as P-0409 plus "winrate" and "success rate", and a third regex
for any spoken percentage. One pass with the project venv, two seconds between fetches, no retry.
Then one grep over the raw captions for win, percent, "out of", trades and times, in case the
regexes missed a phrasing. Captions only; I watched nothing. Raw text is in
`sandbox/watched-gapgo-3/` (gitignored); `videos.json` has the counts.

**What came back.** 6 of 6 fetched, no block.

| video | channel | length | words | win rate said | trade count |
|---|---|---|---|---|---|
| Increase Your Day Trading Profits with the Gap and Go Strategy (6PLI1Wvn3fE) | NetPicks | 2.8 min | 513 | none | none |
| Gap and Go Trading Strategy Taught in LESS THAN 5 MINS! (VsF0W2FuQOM) | TradeLikeGates | 4.4 min | 929 | none | none |
| Gap-and-Go Strategy: Ride the Momentum in Penny Stocks (WCuEgMPvKwc) | Profit Potential | 1.4 min | 227 | none | none |
| Can we apply your Gap and Go rules to gap downs? (sEpI4T4UvhU) | Christopher Uhl, OVTLYR | 1.0 min | 215 | none | none |
| VWAP Gap and Go Strategy: Pre-Open Squeeze Explained! (9Y4x-QKkZqU) | Elite Trading | 1.5 min | 213 | none | none |
| Gap and Go, Day Trading Recap by Ross Cameron (d9mDpbN4zFI) | Warrior Trading | 7.2 min | 1,422 | none | "two out of three" stocks, one day |

Win-rate lines: 0 across all six. Trade-count lines: 0. Spoken percentages: 1 in 3,519 words, and it
is a candle size ("a 15% candle"), not a result. None of the six titles carries a win rate either.
The nearest thing to a record is Ross Cameron's recap: green on two of three stocks that day, a
little over five thousand dollars, which is a day's diary and not a rule's win rate.

**Reading.**

- Zero of six, against my three. With P-0409 that is 0 of 9 videos that name gap and go and say a
  win rate for it. The guess in P-0409's README was wrong: the short ones do not carry the claim.
  They explain the setup (gap up on news, pre-market high, volume, VWAP) and stop.
- The "85% Winrate" and "70%+ Win Rate" titles P-0409 saw were on dropped videos about gap fills and
  earnings gaps. So the win-rate selling sits on the fade (gap fill) side, not on gap and go. That is
  the one thing I did not know before today.
- For E-017 it means there is no public number to hold its 121 trades against. The only stated
  sample anywhere in the nine is the 537-trade bot whose author called it no edge.

**Caveats.** Six videos, chosen by a search two days ago and a title read. Auto-captions: a number
shown on screen and never spoken is missed. The Ross Cameron recap runs 7.2 minutes and its captions
never say "gap and go", so P-0409 dropped it for the phrase, not the length; "six under five
minutes" in the refill row was loose, it is five short ones and that recap.

**Not done.** The gap-fill videos with win rates in their titles. That is the next question and it
is the same script with a different id list.
