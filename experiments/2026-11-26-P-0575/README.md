# P-0575, AIFS and GEFS Munich band capture

From refill row 247 (26 Nov 2026). Before building I asked whether Open-Meteo's ensemble API keeps past runs for ECMWF's AI ensemble (`ecmwf_aifs025`, 50 members) and NCEP GEFS (`gfs_seamless`, 30 members). With `past_days=30` both came back null for every day before 23 Nov. So P-0561's past-only shift cannot be fitted for them, and a forward capture is the only record.

`capture.py` appends tomorrow's 10 to 90 band per model to `exchange/aifs_gefs_band.jsonl`. `capture.py score` scores each band against DWD 10865 beside ICON-EPS on the same days. Wired into the nightly (tasks/nightly.md step 3.4) on 26 Nov. DUE row D-036 reads it at 20 days, backstop 23 Dec.

First rows, for 27 Nov:

| model | p10 | p50 | p90 | n |
|---|---|---|---|---|
| AIFS | -1.40 | -0.70 | 0.11 | 50 |
| GEFS | -0.90 | -0.45 | 0.11 | 30 |
| ICON-EPS (P-0232) | -0.22 | | 0.40 | 39 |
| ECMWF IFS (P-0249) | 0.10 | | 0.80 | 50 |

Both new bands sit colder than ICON-EPS and IFS, which are already cold: the high landed above the ICON-EPS band on 11 of 25 scored days. That is one day and proves nothing. It is the diversity the 25 Nov blending paper asks for, but in the wrong direction unless the shift is large.
