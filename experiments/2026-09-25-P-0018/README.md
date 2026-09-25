# P-0018: the statutory Fuel Finder scheme, keyless?

Run 25 Sep 2026, 23:30 to 23:50, from the nightly. Scripts: `sandbox/fuel_finder_probe.py`,
`fuel_finder_read.py`, `fuel_finder_csv.py`, `fuel_finder_js.py`, `fuel_finder_download.py`.

## What I found by running it

1. **It exists and is the replacement.** GOV.UK's keyless search API (`/api/search.json`) finds a
   Fuel Finder collection (Feb 2026), a CMA enforcement guidance (Dec 2025), a drivers' factsheet
   (Mar 2026) and a "Road fuel monitoring and enforcement" collection updated 18 Aug 2026. The access
   guidance promises every forecourt's price by fuel type, published within 30 minutes of a change.
   `probe.json` has the search hits.
2. **The API needs an account.** The guidance says access needs a GOV.UK One Login and OAuth 2.0
   client credentials. Tried bare: `https://www.fuel-finder.service.gov.uk/api/v1/pfs` returns 403,
   "Missing access token". That is an account I cannot create. `access-notes.md` has the guidance text.
3. **The CSV is public in a browser, not in a script.** The developer page's download button calls
   `/fuel-finder/internal-api/download-csv` (sets a cookie `x-downloadcsv-cookie`), then
   `/internal/v1.0.2/csv/generate-presigned-url`. I reproduced both calls exactly as the button makes
   them. The second answers 200, but the body is `{"nxhex": "..."}`, an obfuscated blob the page
   decodes client-side before redirecting. I stopped there. Decoding a deliberate client-side
   scramble is working around a control, not reading open data, and the charter's line on pointing
   things at systems Luke does not own covers it in spirit.

## What I did not do

- Did not create a One Login, did not download the CSV through a browser (a file download needs
  Luke's yes), did not decode `nxhex`.
- So the comparison the probe asked for (coverage and freshness against the five live retailer
  feeds) is not done.

## Verdict

Blocked, on a GOV.UK One Login with OAuth client credentials (or a human pressing the CSV download
once, which would give a one-off comparison but not a nightly feed). Meanwhile the five live CMA
interim feeds still work keyless (`sandbox/fuel_prices.py`, 2,266 stations tonight).
