# Lead finder, step one: the pass mark (committed before any pull)

Written 23 Nov 2026, Workshop 16:30, before the first OpenStreetMap request. The Big Expedition for
23 Nov to 6 Dec (BACKLOG.md): a keyless lead finder for plumbing and heating firms in Greater
Manchester. The area was never answered, so I picked it. Never sends; nothing here contacts a firm.

## What the tool outputs

Every OpenStreetMap node, way or relation inside the Greater Manchester boundary (admin_level 6)
tagged `craft=plumber`, `craft=hvac`, `craft=heating_engineer` or `craft=gas_fitter`. A row is a
lead only if it carries a website (`website` or `contact:website`). Phone from `phone` or
`contact:phone`.

## The test (Saturday 28 Nov, by hand)

1. Sample: 30 leads drawn with Python `random.Random(20261123).sample(leads, 30)` over the leads
   sorted by OSM type and id. If there are fewer than 30 leads, all of them, and the verdict says so.
2. Each sampled row is checked by opening the firm's own site:
   - **working site**: the URL answers with a page that belongs to this firm (not parked, not
     another business, not a directory listing);
   - **phone matches**: a phone number shown on the firm's own site (contact page or footer)
     equals the OSM phone after stripping spaces and the +44 / 0 prefix. No OSM phone counts as no
     match.
3. A row passes when both hold.

## Pass mark

- **Pass**: 18 or more of 30 (60%).
- **Needs work**: 12 to 17.
- **Kill** (OSM alone is not a lead source; step two must find firms another way): 11 or fewer.

Also reported, not scored: how many leads in total, and the share of all tagged firms that have a
website at all.

## My call before the pull

About 120 tagged firms, about 45% with a website, so about 55 leads; on the sample I expect
about 15 of 30 to pass (needs work), mostly lost to OSM phones that are missing or out of date.
