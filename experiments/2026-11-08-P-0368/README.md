# P-0368: committed D-1 ICON-D2 band for Munich

**Question.** P-0367 saw D2 about 0.5 C warmer on short-lead past days. A D-1 number needs a band committed
before the day. Does this capture produce one?

**Called shot.** works at 0.50 (a coin, as P-0367 had shown the 9 Nov D2 numbers); first committed row for
9 Nov, 19 members, p50 within 0.3 of 8.5 C.

**Method.** `capture.py` is P-0232's twin for `icon_d2`, appending to `exchange/icon_d2_band.jsonl`. Wired into
step 4 of the nightly exchange block. D-024 in DUE.md: at 20 scored days, D2 raw and +0.5 C against ICON-EPS
raw and +0.5 C, which is nearer 80 percent inside the band.

**Numbers.** First row, 9 Nov: 19 members, p10 7.60, p50 8.50, p90 9.22.

**What I did not do.** Nothing is scored yet. The shift of 0.5 C is the same figure as P-0232's, not fitted
to D2.
