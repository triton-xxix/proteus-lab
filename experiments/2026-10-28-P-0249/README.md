# P-0249: ECMWF IFS ensemble band for Munich, beside ICON-EPS

28 Oct 2026, nightly probe loop, refill row 41. `capture.py` reuses P-0232's capture and scorer with the
model swapped to `ecmwf_ifs025` and rows to `exchange/ecmwf_ens_band.jsonl`. Keyless.

First capture, for 29 Oct, at about 23:45 UK time on 28 Oct:

| model | members | p10 | p90 | width |
|---|---|---|---|---|
| ICON-EPS (P-0232) | 39 | 10.06 | 11.32 | 1.26 |
| ECMWF IFS ensemble | 50 returned (51 advertised) | 8.29 | 10.62 | 2.33 |

ECMWF's band is nearly twice as wide and sits about 1.2C colder at the bottom; the two bands overlap
only from 10.06 to 10.62. That fits the 13 Oct finding (ECMWF ran 2.2C cold against the city station,
ICON 1.0C). A second run in the night added nothing (one row a night).

Pre-registered (DUE D-020, backstop 25 Nov): at 20 scored days each, which raw band holds the DWD Stadt
high nearer 80%, and each one's share above its band. My guess, written now: ICON's narrow band holds
under 60%, with most misses above; ECMWF's wider one holds more, but also misses mostly above.
Wired into `tasks/nightly.md` step 3 item 4. Neither band is used for calls until D-020 reads.
