# P-0421: every registered edge rule with its best trades removed

12 Nov 2026, nightly probe loop, refill row 154. Follow-up to P-0410, which found ten trades are all of
E-017's admission profit.

**Question.** For E-011 to E-019, on each rule's own admission window, how many of the best trades must
go before the total is zero or less? Did the rules that passed a forward week need more removed than the
ones that failed?

**Called shot (commit 04c28fac, before the run).** works at 0.70; median to-zero 10 or fewer (band 4 to
12), and the passers do not need a larger share removed than the failers. Both parts hit: median 5.

**How.** `all_rules.py` imports `edges/scan/scan.py` untouched, pulls Yahoo 5-minute bars for the 12
stocks and Binance for the 6 coins, and rebuilds each rule's trades on its three admission blocks. The
trade count matched the register on all nine rules (179, 157, 124, 157, 126, 179, 121, 180, 145), so the
windows are the right ones.

| Edge | Rule | Trades | Total | To zero | Share of trades | Best 10 gone | Forward |
|---|---|---|---|---|---|---|---|
| E-011 | Morning direction into the afternoon | 179 | +10.03% | 5 | 2.8% | -6.91% | FAIL |
| E-012 | ORB 30m, target 1R | 157 | +16.96% | 9 | 5.7% | -1.56% | FAIL |
| E-013 | VWAP cross after 11:00 | 124 | +9.38% | 4 | 3.2% | -10.79% | PASS |
| E-014 | ORB 15m fade | 157 | +5.78% | 3 | 1.9% | -8.16% | PASS |
| E-015 | ORB NY open 30m, 1R (crypto) | 126 | +8.57% | 7 | 5.6% | -4.08% | FAIL |
| E-016 | Opening drive to 11:00 | 179 | +7.82% | 3 | 1.7% | -14.89% | PASS |
| E-017 | Gap and go 0.5% | 121 | +36.90% | 10 | 8.3% | -0.31% | pending |
| E-018 | Opening reversal | 180 | +17.11% | 6 | 3.3% | -10.51% | pending |
| E-019 | ORB 30m fade | 145 | +8.72% | 3 | 2.1% | -11.68% | pending |

**Reading.**

- Every one of the nine is under water with its best ten trades gone. The median rule needs only 5 of
  about 150 trades removed. None of these admissions is a broad edge; each is a handful of trades.
- The three forward passers needed fewer removed (4, 3, 3; mean 2.3% of trades) than the three failers
  (5, 9, 7; mean 4.7%). So "survives its best trades being removed" did not pick the passers here; it
  pointed the other way.
- E-017 is the sturdiest on this measure (10 trades, 8.3%) and its forward week is still open (D-026,
  17 Nov). E-019 is among the thinnest (3).

**Corrected the same night by P-0430.** The first bullet reads too much into it. Random-entry lists of
the same size die faster with their best trades gone, and no rule is more concentrated than its control.
See `experiments/2026-11-12-P-0430/`.

**Caveats.** Three against three; the difference could be nothing. A bigger admission total mechanically
needs more trades removed, and the failers had the bigger totals, so the measure partly restates the
total. The forward weeks are one week each. No rule, kill line or register row was changed.

**Next.** Close. If it is ever used as a filter it needs the forward results of E-017 to E-019 first.
