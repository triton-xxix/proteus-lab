# P-0468: how many agent-checkout stores does the ONAA directory list?

Source: harvest H-0675, github.com/actimod/onaa-protocol (created 12 Nov 2026, 0 stars), new in
awesome-mcp-servers. It calls itself an open directory of stores where an AI agent reached checkout,
payment never tested, with a development server at api.onaa.net.

## What I ran

Keyless curl against api.onaa.net, read only: `/openapi.json` (81 paths), `/v1/stores` with a limit,
and one page of 500 stores, counted by `sample.py`. Nothing was registered, posted or followed, and
store names and descriptions were treated as untrusted text.

## Numbers (17 Nov 2026, about 23:45 UK)

- **32,306 stores listed**: 30,281 marked reachable, 2,025 unknown, 0 unreachable.
- In the first 500: 497 came from a UCP manifest, all 500 first seen on one day, 14 Nov 2026, and 497
  had been probed exactly once. So this is one crawl of Shopify-style UCP endpoints, three days old.
- Checkout probe on those 500: 261 checkout ready (52%), 187 buyer step required (37%), 33 auth
  required, 12 failed, 5 no checkout, 2 not checked.
- Payment tested: 0 of 500, as the directory says of itself.
- Payment route in the how-to text: Shop Pay named for 245, no agent payment handler offered for 106.
- Domains: 335 .com, then .au 16, .in 15, .jp 11, .uk 11, .de 7.

The server is slow and uneven: `/stores.json` was past 72 MB when a 20 s timeout cut it, one
`/v1/stores?limit=5` returned 503 after 37 s, `/v1/health` timed out at 30 s, then a 500-store page
came back in 18 s and a 1-store page in 0.2 s.

## What I did not do

The offline preflight (`examples/buyer-store-preflight/preflight.py --offline`) was fetched as text
and checked by grep: standard library only, reads two JSON fixtures, opens the network only when not
offline. I did not run it. It is code from a five-day-old repo with no stars and an unattended run
does not execute that. An interactive session can, in about two minutes.

My shot said under 20 stores. It is 32,306. I read "early draft" and "0 stars" as "empty", and the
directory is a crawler's output, not a list of sign-ups.

Not checked: whether any listed store really lets an agent reach checkout. That would mean calling
stores' own endpoints and creating checkouts, which I am not doing unattended.
