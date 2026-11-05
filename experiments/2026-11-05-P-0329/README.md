# P-0329: Munich-Stadt highs from Ogimet SYNOP v DWD's daily high (5 Nov 2026)

Refill from REFILL-SOURCES row 93. The Munich weather markets settle on the city station
(WMO 10865, DWD 03379). DWD's daily high, which the exchange scoring uses, arrives a day late. Can
Ogimet's keyless SYNOP archive give the same number, and how far apart are the definitions?

## What I ran

One curl of `ogimet.com/cgi-bin/getsynop?block=10865` for October 2026 (464 KB, 4,214 reports),
then `synop_v_dwd.py` against `munich_forecast_error.observed("10865")`. `result.json` has each day.

## What I found

1. **The 12-hour max group is gone.** The 18 UTC report's 333 1snTxTxTx (06 to 18 UTC max) is
   there on 1 and 2 October only, and matches DWD exactly both days (25.5, 19.0). From 3 October
   the station sends abbreviated reports with no max group.
2. **Two report streams share the number 10865.** Besides the real 10-minute reports there is a
   second stream (visibility `///`, a 555 section, mostly at the hour; the OOXX lines look the
   same). Its temperatures run up to 6 C above DWD's high (29.0 against 23.0 on 4 Oct). Taking the
   highest temperature of every report without the filter gave a mean gap of -1.9 C; with reports
   carrying a 555 section dropped it reconciles.
3. **With the filter, the 10-minute maximum works:** over 31 October days DWD's high minus the
   highest 10-minute reading is +0.19 C on average (sd 0.18, never negative, at most 0.8), and both
   round to the same whole degree on 26 of 31 days. The gap is the expected one: DWD's maximum is
   continuous, the reports are spot readings every ten minutes.

## For the desk

A same-day keyless Munich-Stadt high: max of the section-1 1sTTT over the UTC day from reports with
no 555 section, plus about 0.2 C. It agrees with the settlement-relevant DWD number to the degree
84% of the time. Not wired into the exchange scorer tonight; a daytime slot can add it as a check.

The repeat warning on this probe was fair in method (P-0323 did London) and wrong in substance: the
second stream and the missing max group are Munich-only findings.
