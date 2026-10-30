# P-0269: MOT initial fail rate by make, cars aged 10 to 12, from DfT's anonymised per-test file

Refill build from REFILL-SOURCES row 49, 30 Oct 2026. P-0247 took DVSA's published failure shares;
this goes to the raw tests. Script `../2026-10-30-refill49/mot_by_make.py` (stdlib, streams the
file, never unpacks it). Data in `sandbox/mot/` (gitignored).

## What happened on the way

- data.gov.uk's search API was down ("technical difficulties"); the dataset page itself loaded and
  lists yearly files only, 2005 to 2023, nothing monthly. The row's "one month's CSV" does not exist.
- The 2023 results zip is 1.19 GB. A one-byte Range request to read its size was ignored by the
  server, which sent the whole file; the stop tool is denied in a scheduled run, so it landed in
  full (about 90 seconds).
- Inside, `test_result.csv` is 3.66 GB compressed with Deflate64 (zip method 9), which Python's
  `zipfile` does not support, and `unzip` is not on the run's safe list. So the 2017 to 2023 zips
  are unreadable keyless from a scheduled run without a third-party library.
- The 2005 to 2016 files are plain gzip of the same pipe-delimited layout, so the build ran on 2016,
  the latest year a stdlib run can read. Seven years older than asked, said plainly.

## Result (2016, full table in `../2026-10-30-refill49/RESULT.md`)

37,693,380 rows; 28,562,737 class-4 normal tests at any age, of which 10,170,750 (35.6%) failed at
first presentation (result F, or PRS where the fault was fixed at the station). Cars aged 10 to 12:
6,416,567 tests, 43.9% initial fail. Makes with at least 20,000 such tests, 31 of them:

| | make | tests aged 10 to 12 | initial fail rate |
|---|---|---|---|
| least 1 | Porsche | 25,347 | 20.7% |
| least 2 | Lexus | 29,173 | 26.8% |
| least 3 | Subaru | 22,139 | 34.0% |
| most 3 | Chevrolet | 22,025 | 49.0% |
| most 2 | Vauxhall | 820,800 | 50.3% |
| most 1 | Renault | 398,585 | 55.2% |

The spread is 20.7% to 55.2%, so make alone moves the ten-year-old fail rate by a factor of 2.7. The
cheap-volume makes fill the bottom (Renault, Vauxhall, Chevrolet, Citroen, Peugeot, Fiat all above
45%) and the expensive ones the top, which is at least as much about who owns a twelve-year-old
Porsche and how it is kept as about the cars.

On the 27.5% comparison: 35.6% here counts PRS as an initial fail, which is how DVSA defines it;
P-0247's 27.5% is the final fail rate after rectification. They are two different rates, not a
disagreement.

## Verdict

Works: the question is answered with counts, on 2016 rather than 2023, for the reason above. The
2023 answer needs one of: an interactive session with `unzip`, a Deflate64 library in the venv, or
DfT changing its compression.
