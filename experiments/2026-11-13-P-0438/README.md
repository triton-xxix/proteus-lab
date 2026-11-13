# P-0438: the metronome measure on more of the ledger

Trials, 13 Nov 2026. Second leg of P-0437, with its post-hoc cut stated first this time: only trades
with volume in all six pre-entry hours count.

**Shot.** works at 0.55: the hint fades, pooled medians within 0.2 of each other (losers about 0.50,
winners about 0.65); at least 30 six-full trades pooled; fewer than 6 trades under CV 0.3. Called
after seeing P-0437's first 14.

**Method.** `rest.py` imports P-0437's fetch and statistics unchanged and tries the 64 exited ledger
rows it had not reached, newest first, 3.5 s apart with a 330 s cap. The cap stopped it at 28 of 64:
26 served, 1 refused (429), 1 with no trades in the window. 36 rows were not reached.

**What came back.** Pooled with P-0437: 51 trades measured, 28 with six full hours.

| six full hours | n | median CV |
|---|---|---|
| losers (stop-loss, rug) | 19 | 0.598 |
| take-profits | 8 | 0.861 |
| other exits | 1 | 0.618 |

| CV band | trades | lost money |
|---|---|---|
| under 0.3 | 2 | 2 |
| 0.3 to 0.6 | 11 | 8 (73%) |
| 0.6 and over | 15 | 9 (60%) |
| all 28 | 28 | 19 (68%) |

Seven of the eight flattest trades lost; the two flattest are a rug (G-0090, 0.149) and a stop-loss
(G-0061, 0.159). The new rows alone were 12 losers and 1 winner with six full hours, so they add
losers and almost nothing to compare them with.

**Reading.** The lean survives and stays small. Losers are flatter by 0.26 on the median; the loss
share climbs from 60% to 73% to 2 of 2 as the tape gets flatter. But 68% of these trades lost
anyway: seven or more losers among any eight has a chance of about 0.22 at that base rate. Nothing
here would have kept the Grinder out of a trade it should have skipped, except possibly the two
under 0.3, and two is two. FPES at 0.044 remains far outside anything the ledger holds.

**Against the shot.** Medians within 0.2: no, 0.26 apart, so the hint faded less than I called.
At least 30 six-full trades: no, 28. Fewer than 6 under 0.3: yes, 2.

**Caveats.** 36 ledger rows unreached, all older (v0.1 era mostly). Eight winners. The measure is
six numbers a trade from one source. Losers and winners were entered under two rule versions.

**Not done.** The last 36 rows; I do not expect eight more winners to move a base-rate result. A
forward version would log the CV at scan time beside each new entry, which costs one call a trade.
Nothing in `grinder/` was written.
