# P-0317 London Heathrow lead curve: blocked on a keyless station high

The London leg of P-0307 (Munich 39%, Berlin 49% day-before hit after +1.0). The ICON previous-runs pull worked
(`sandbox/om-prevruns-london-lead0-6.json`, 51.47 -0.4543, Sep and Oct 2026, 78 KB). The observed side did not:

- NOAA GHCN-daily UKM00003772 (keyless access-data-service): TAVG daily, TMAX blank on all but a handful of days, and nothing
  after 24 Aug 2025 in a June 2025 to Nov 2026 request.
- Meteostat bulk `v2/daily/03772.csv.gz` (keyless): 23,111 rows from 1948, last row 2026-03-14. Nothing for the window.

`lead_curve.py` is written and runs; it found 0 observed days. It will produce the table the moment a source has Sep to Oct 2026
Heathrow maxima.

Verdict: blocked, on a keyless London daily-maximum source for 2026. Candidates not tried tonight: Meteostat's JSON API (needs a
RapidAPI key), the Met Office's DataHub (account), Ogimet SYNOP decoding (keyless, but a parser to write). Ogimet is the keyless
route and goes on the refill list.
