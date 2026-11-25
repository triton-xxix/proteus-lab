# P-0562: does DVSA MOT open data reproduce the Golf at 17.9%?

**Question.** A YouTube video (harvest H-0761, yt:uxUVGL8t2us) says 10-year-old VW Golfs (first used 2015)
failed their MOT at the first attempt 17.9% of the time across nearly 38,000 tests, against about
three in 10 for all cars of that age. Does the public bulk file reproduce it?

**What I found.**
- The data.gov.uk dataset `anonymised_mot_test` stops at 2023. `dft_test_result_2024.zip` is a 404. So
  the claim's cohort (2015 cars at age 10, tested 2025) cannot be checked from public bulk data today.
- The 2023 zip is Deflate64 (method 9), which Python's zipfile cannot read. bsdtar is not on the
  unattended safe list, and `zipfile-deflate64` will not build on this Intel Mac. `inflate64` (a binary
  wheel, installed into sandbox/py312-venv) plus a 25-line stream reader in `golf.py` works.
- The analogue: cars first used in 2013, tested in 2023 (age 10), class 4, normal tests only. A fail is
  F or PRS (the DVSA definition the video uses).

| | tests | first-attempt fail | still fail after the hour |
|---|---|---|---|
| All cars, age 10 (2023) | 2,143,564 | 31.71% | |
| VW Golf, age 10 (2023) | 55,784 | 22.80% | 18.53% |

The Golf ranks 24th lowest of 155 models with at least 2,500 tests. The all-car baseline of 31.7%
matches the video's "about three in 10". The Golf at 22.8% sits 4.9 points above the video's 17.9% for
the 2015 cohort. That gap could be real (the Mk7 Golf launched in 2013, so the 2015 cohort is
nearly all Mk7 and the 2013 cohort is a Mk6/Mk7 mix), or it could be the method. I cannot tell which from
this file.

**Run.** 42,216,721 rows in 1,684 s (28 min, single-threaded csv over a streamed Deflate64 member).
That is too slow for the Trials slot. A deepen should filter make first, or use the 2023 file once,
caching every model by first-use year.

**Did not do.** No 2024 or 2025 data (not published on data.gov.uk), no check of the "Car Control" or
second-analysis sources, no failure-item file, no dedupe to one test per vehicle.

Files: `golf.py` (the counter), `results.json` (numbers, best 10, worst 5). The zip stays in
sandbox/p0562 (gitignored, 1.19 GB).
