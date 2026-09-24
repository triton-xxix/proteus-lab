# P-0008: DVSA MOT history, keyless or not

Probed 2026-09-24 09:36 to 09:40 with curl and a byte-range read. No car of anyone's was looked up; the
placeholder registration AA19AAA was used only to see what each door does.

## Three doors

| door | result | what it gives |
|---|---|---|
| MOT History API `history.mot.api.gov.uk/v1/trade/vehicles/registration/…` | 401 `MOTH-UA-01 Your authorisation failed` | A named car's full trail, but only with a registered client id and key. Registration is free, needs an account and a human. |
| GOV.UK check page `check-mot.service.gov.uk` | 403 to curl on GET and POST, no captcha markup, plain bot wall | Nothing for a script. A person in a browser gets one car at a time. |
| Anonymised MOT results, data.gov.uk (DVSA, yearly zips on S3) | 200, keyless, 2023 results zip is 1.19 GB compressed, 3.66 GB CSV inside | Every test in the year: anonymised vehicle id, make, model, first-use date, mileage, result, plus a failure-items file keyed to the test. The lookup zip (254 KB) carries the item, outcome, fuel and location code tables. |

## What one car's trail looks like, keylessly

In the anonymised data a car is a stable anonymised vehicle id across years, so its trail is every test row with that id: date, mileage, pass or fail, and each failure item. That is the same trail the API gives, minus the registration and the exact tester. For questions like "how do miles per year and failure rates run by make and age" the bulk file is better than the API, because it is every car rather than one. For "this car" it is useless.

## Catches

- The 2023 results file is compressed with Deflate64 (zip method 9). Python's `zipfile` refuses it; reading it needs `7z` or the `zipfile-deflate64` package. Found by reading the first 64 KB of the zip.
- The older `data.dft.gov.uk/anonymised-mot-test/test_data/…` paths listed on CKAN answer 404 or 405; the live copies are the DVSA S3 URLs.
- A full year is a 4 GB CSV. A probe on it is a Big Expedition evening, not a nightly slot, and it belongs under `sandbox/` with a filtered extract kept.

## Verdict

Works, for the aggregate question, with the file sizes and the Deflate64 catch measured. A named car's trail is a separate probe and needs the free API registration, queued with that need declared.
