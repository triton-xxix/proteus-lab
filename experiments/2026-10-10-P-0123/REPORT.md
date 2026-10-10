# P-0123: data.police.uk street-level crime, keyless

Date: 2026-10-10, nightly probe loop. Source: harvest H-0204 (a YouTube web-scraping-with-APIs demo).

## Called shot
Latest month at a central London point: over 3,000 crimes in the one-mile radius, keyless, inside the
rate limit.

## What I ran
`street.py`: the list of available months, then `crimes-street/all-crime` for the latest month at three
points (central London, a northern city centre, a Dales market town), then a 20-call burst on the
cheapest endpoint. Numbers in `result.json`.

## Result
- 36 months listed; latest **August 2026**, so the data runs about six weeks behind.
- Leicester Square: **4,210** crimes on 678 snapped street points, 5.4 s and 1.6 MB for one call. Top:
  other theft 855, theft from the person 751, violent crime 652. 569 have no outcome recorded.
- Leeds city centre: 1,520 crimes, 2.3 s. Top: violent crime 419, shoplifting 324.
- Hawes: 2 crimes.
- No rate-limit headers are sent. The burst of 20 calls in 1.6 s (about 12 a second) drew **2 x 429**.
  The docs, as I read them, say 15 a second with a burst allowance; I hit the limit below that.
  Unverified which side is wrong; a script should pace at a few calls a second.

## Verdict
Works: keyless, fast enough, and the called shot held. Limits worth knowing: six weeks' lag, locations
are snapped to anonymised street points, and the radius is fixed at one mile, so a dense point returns
thousands of rows in one call. Above 10,000 the docs say the call fails; Leicester Square is at 42 percent of that.
