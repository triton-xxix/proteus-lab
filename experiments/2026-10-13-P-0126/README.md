# P-0126: Grinder fill check re-run, 13 Oct 2026 (DUE.md D-002)

`experiments/2026-10-06-grinder-fill-check/fillcheck.py` re-walked every closed v0.2 position with
saved candles under the four fill rules (touch as booked, close, late, depth). 68 trades, none
missing candles. The three rows Luke voided on 13 Oct (G-0075 to G-0077) are gone from the ledger and
so from this count; the 11 Oct run had 64.

Called shot: works at 0.85, about 69 trades, touch about -230 GBP, close about 120 GBP worse than touch.
Measured: 68 trades, touch -177.78, close -288.62 (111 worse). Trade count and the close penalty hit;
the touch total was 52 GBP better than I said, because G-0072 to G-0074 (11 Oct entries) all took
profit.

| Rule | n | Wins | Net GBP | Per trade |
|---|---|---|---|---|
| touch (as booked) | 68 | 24 | -177.78 | -2.61 |
| close | 68 | 22 | -288.62 | -4.24 |
| late | 68 | 24 | -211.82 | -3.11 |
| depth | 68 | 23 | -369.97 | -5.44 |

10 of the 24 booked wins had their touch minute close below 2x (7 of 19 on 6 Oct). The close rule
flips the same two to losses as before (G-0012 manifest, G-0031 TRUMP) and the depth rule turns
G-0023 ECTF into a rug (the touch minute traded 193 USD). The ordering of the four rules is the same
as on 6 Oct and 11 Oct: touch best, depth worst, about 190 GBP between them over the book.

The script's date-split labels are hard-coded (25 to 28 Sep and "29 Sep to 4 Oct") and the second
bucket now holds everything since 29 Sep, 52 trades at +84.98 under touch.

Files: `summary.json`, `per_trade.json` copied from the 6 Oct folder after tonight's run.
Next re-run: Sunday 18 Oct, as DUE.md D-002 says.
