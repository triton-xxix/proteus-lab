# P-0425: the voided Grinder trades, fetched and walked

12 Nov 2026, nightly probe loop, refill row 158. P-0419 found the candle files for G-0075, G-0076 and
G-0077 empty and stopped at broken. `refetch.py` makes the pull it named: GeckoTerminal minute candles
for each pool from ten minutes before entry (12 Oct 22:54Z) to 24 hours after, through
`grinder/paths.py`'s own `pool_for`, `fetch`, `walk` and `pnl_v02`. Candles are saved here, not in
`grinder/candles/`. Nothing in the ledger or `VOIDED.csv` was touched; the trades stay voided.

**Called shot (commit 03ec4ba6).** works at 0.60: all three pools served, at least two lose from the
stale price, about -£100 between the three (band -£200 to -£40). Two losers and the total hit
(-£128.15). "All three served" missed: one pool came back empty.

| id | token | candles after entry | stale price over live | from the stale price | from the live price |
|---|---|---|---|---|---|
| G-0075 | FPES | 0 | n/a | cannot be walked | cannot be walked |
| G-0076 | TM | 1,318 | +42.3% | stop loss after 4.0 h, -£52.79 | take profit after 16.7 h, +£92.42 |
| G-0077 | Glorp | 396 | +280.3% | stop loss in the first minute, -£75.36 | time stop, -26.2%, -£29.56 |

**Reading.**

- A month on, the keyless API still serves minute candles for two of the three pools. The third
  (FPES, the pool the 11 Oct snapshot named, $1.8m of liquidity then) answers with no candles in the
  window. I do not know whether the pool moved or the token traded elsewhere.
- The 24.5-hour-old snapshot priced TM 42% and Glorp 280% above the market at the minute of entry.
  Glorp had already fallen by three quarters; the paper book would have "bought" at nearly four times
  the price and stopped out on the first candle.
- Same two tokens, same rules: -£128.15 from the stale prices, +£62.86 from the live ones. A swing of
  £191 on £200 staked, from the price alone. TM flips from a stop loss to a take profit.

**Caveats.** Two trades. The live walk assumes a fill at the first candle's open. Glorp printed only
396 candles in 24 hours, so its path is thin. This is the extreme case of the stale entry P-0405
measured (typical miss 4.34%), not a typical one, and it says nothing about whether the voided rows
should have counted: they should not, the price was not there to buy.

**Next.** Close. The guard that would have stopped these (refuse an entry when the snapshot is older
than a set age) is P-0415's subject.
