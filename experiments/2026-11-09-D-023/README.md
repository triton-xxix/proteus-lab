# D-023 read: which rule settles the Munich market (9 Nov 2026)

Smith, 20:15 on 9 Nov 2026. The row was registered 6 Nov (P-0334), due when X-0048 settled, backstop
12 Nov. X-0048 settled at the 8 Nov nightly, so this lands a day after it could and three days inside
the backstop.

**Measured.** One curl of Iowa Mesonet for EDDM, 4 to 8 Nov: 240 reports, none skipped
(`eddm-metar.csv`), through P-0334's `metar_rule.py` unchanged (`results.json`) and `highs.py` for the
daily figures:

| Row | Day | Contract | Book outcome | METAR high (UTC and Berlin day alike) | Rule says | Agrees |
|---|---|---|---|---|---|---|
| X-0046 | 5 Nov | 10°C | winner | 10 | wins | yes |
| X-0047 | 6 Nov | 7°C | loser | 4 | loses | yes |
| X-0048 | 7 Nov | 10°C | loser | 7 | loses | yes |

`metar_rule.py` on all four settled rows in the pull: 4 of 4 on both day boundaries, none wrong
(X-0045 on 4 Nov is the fourth).

**Line**, from the DUE row as written on 6 Nov: "KEEP if all three agree, then F-0075 goes to the
nightly's correction; KILL if X-0046 loses".

**Verdict: KEEP.** All three agree, and X-0046 did not lose.

**Said plainly.** Only one of the three rows could tell the two rules apart. X-0046 is the row where
the city station said 8.3 and the airport METAR said 10, and the market paid 10. X-0047 and X-0048 are
losers that a nearby rule mostly calls correctly as well. So the forward evidence is one separating
row on top of the 30 of 30 fit P-0334 found after looking. That is enough for the line as registered and
not enough to call the rule proved. The Smarkets record still has no rules text, so the rule stays
inferred, and these rows still cannot say which day boundary applies.

**What changes.** The row says F-0075 goes to the nightly's correction, so `tasks/nightly.md` now uses
ICON at the city point with nothing added. P-0335 measured that at +0.03 C against the METAR high at
lead 1 (MAE 0.67 against 1.05 with the +1), on 24 days. It also measured a warning: the exact-degree hit
improved at leads 0 and 1 and got worse at lead 2 (42% to 25%), at se about 10 points. The cap on a
single degree stays.

**What does not change.** Every call already in `exchange/BOOK.csv`, X-0053 included. D-020 and D-022
keep scoring against DWD Stadt as registered, though the number they score is now not the market's
target; a reader of those two rows should say so.

No further read of this row is registered.
