# Do UK Parliament petitions add up? (Fri 20 Nov 2026, persona pick, interest 8)

Script: `check.py` (run from `sandbox/petitions/check.py`). Output: `results.json`, pulled 2026-11-20T23:27:38Z.
Keyless JSON from petition.parliament.uk: the first 40 open petitions the list endpoint returns (it
sorts by signature count), each petition's own JSON fetched once.

## Result

- 40 petitions, 2,039,246 signatures, 0 fetch errors.
- Headline count equals the sum of `signatures_by_country`: 40 of 40, to the signature.
- The UK row (2,022,815 in all) is larger than the sum of `signatures_by_constituency` on 40 of 40.
  9,580 UK signatures (0.47%) sit in no constituency. Per petition 0.24% to 2.13%; the top is "Social
  media ban for under-13s" (502 of 23,567).
- `signatures_by_region` sums to exactly the constituency total on 40 of 40, so the region map is
  built from the constituencies and shares the same hole.
- Constituency lists are 516 to 650 long: petitions with no signer in a seat leave it out rather than
  print a zero.

## Not checked

Why the 9,580 are unplaced. My guess, untested: postcodes the site accepts but cannot map to a seat
(new builds, BFPO, typos). The site's own map would show the UK total as covered when about one UK
signer in 200 is on no part of it.
