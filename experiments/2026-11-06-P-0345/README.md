# P-0345: the airport's METAR high against the airport's own 10-minute record

Question: if Munich settles on the highest whole-degree METAR at EDDM (P-0334), how far is that from DWD's own record
at the same airport, station 01262?

Method: `metar_vs_tx.py`. 26,345 METAR reports from Iowa Mesonet, DWD TX_10 and TT_10 for 01262, Berlin local days,
540 days with near-complete DWD data, 6 May 2025 to 5 Nov 2026.

- METAR high equals rounded TX_10 on 424 of 540 days, 78.5%. My shot was about 65%.
- Of the 116 differences, 63 are the METAR 1 degree lower, 52 are the METAR 1 degree higher, and 1 is 8 lower, which
  I read as a gap in the reports rather than weather and did not chase.
- Mean METAR minus TX_10 is +0.03 C, so no bias worth correcting.
- The 10-minute spot at :20 and :50, rounded, explains 58 of the 116, half. My shot said most.
- Since 1 Sep: 49 of 64, 77%. By month the share runs from 66% (July) to 90% (January).

What it means: a perfect forecast of the airport station's high would hit the exact METAR degree only about four days
in five, and the misses fall on both sides. That is a ceiling on exact-degree calls under this rule, against the
25% to 38% ICON managed in P-0335.

The higher-than-record days are the surprise. A report cannot be warmer than the peak if both read one sensor, so the
METAR probably comes from a different sensor or rounding path. I did not establish which.

Caveats: the rule itself is still on trial under D-023; X-0046 settled for it tonight, X-0047 and X-0048 are open.
Nothing in the nightly's correction or the book changed.
