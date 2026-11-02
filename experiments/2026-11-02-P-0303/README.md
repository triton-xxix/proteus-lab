# P-0303, Munich ensemble spread against the measured error (2 Nov 2026, nightly refill from source 72)

One call to the Open-Meteo ensemble API at the city point: 40 ICON-EPS and 51 ECMWF IFS members, hourly,
3 to 10 Nov. Per member, the high of each Berlin day; then the 10 to 90 width across members for 3 to 8 Nov
(leads 1 to 6). A band that holds 80% of outcomes on a normal error is 2.56 sd wide, so each width is set
against 2.56 x the sd P-0293 measured for ICON's high at the DWD city station by lead. Script `spread.py`,
numbers `results.json`.

| lead | ICON-EPS width | ECMWF width | width the error asks for | ICON ratio | ECMWF ratio |
|---|---|---|---|---|---|
| 1 | 0.52 | 0.70 | 3.38 | 0.15 | 0.21 |
| 2 | 0.92 | 1.40 | 3.46 | 0.27 | 0.41 |
| 3 | 2.02 | 2.10 | 4.56 | 0.44 | 0.46 |
| 4 | 2.42 | 3.10 | 5.66 | 0.43 | 0.55 |
| 5 | 3.33 | 5.50 | 6.76 | 0.49 | 0.81 |
| 6 | 4.74 | 5.80 | 7.01 | 0.68 | 0.83 |

Reading: both ensembles are far too narrow for the station's day-ahead high, about a sixth to a fifth of
the width at lead 1, closing to two thirds to four fifths by lead 6. ECMWF is wider than ICON at every
lead. That fits what the nightly band captures already show (P-0232: 2 of 5 inside raw, 3 above; P-0249:
1 of 4 inside), and says the gap is worst exactly where the exchange book calls, the next day.

Why it can be this far off, and what this does not prove: the measured sd carries more than weather
uncertainty (a city station against a grid cell, ICON's cold bias wobbling day to day), none of which an
ensemble models; the sd is from Sep and Oct, these days are November. One run, one point, six days: a
reading, not a rate. The forward week in REFILL-SOURCES row 72 is the version that settles it.

Use: do not read an ensemble's 10 to 90 band as an 80% band for a Munich call at lead 1 or 2; at least
until P-0232 and D-020 reach 20 scored days, widen it by the measured sd, not the members.
