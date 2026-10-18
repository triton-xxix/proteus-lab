# P-0176: Ads Library with homeowner words, do the real plumbing firms show up?

Deepen of P-0175, where "plumber" gave only 3 firms in its 40 most-seen GB ads.

Shot (blind): works at 0.50, plumbing or heating firms selling to homeowners 20 to 45 of the 80 ads
across "blocked drain" and "boiler service".

## Method

`adlib.mjs` copied from P-0175 unchanged (headless Chrome, never-logged-in profile, CDP, 12 s wait, four
scrolls). First 40 ads of each search, tallied by hand into `tally.json`. A firm does plumbing, drainage
or heating work for homeowners, local or national. Boiler cover sellers are counted apart.

## Numbers (18 Oct 2026, 11:39 UTC)

| search | results | firm ads in first 40 | distinct firms |
| --- | --- | --- | --- |
| plumber (P-0175) | ~3,800 | 3 | 3 |
| blocked drain | ~1,500 | 11 | 3 |
| boiler service | ~850 | 18 | 17 |

- Both new searches: **29 of 80** firm ads, 20 distinct firms. Shot range 20 to 45: hit.
- "blocked drain" is half health ads (20 of 40): lymphatic "drainage", "blocked" thyroid meds. Two drain
  firms (Absolute Drainage, Elite Drain Services in Gloucestershire) hold 10 of the 11 firm ads.
- "boiler service" is the trade word that works: 17 heating firms, from British Gas down to one-area
  outfits (Isle of Wight, Essex, North East). Another 11 ads are boiler cover (CORGI HomePlan 6).
- No login was needed on either search.

## What it means

The word the homeowner types finds the firms, and the trade's own name finds people selling to the trade.
Heating has far more local advertisers on Meta than drainage. In October that is the season talking:
boiler ads say "before winter".

## Not done

First 40 only, one day, no region filter, no spend (UK shows spend only for political ads). Advertiser
names come from their public ad pages; nothing about people was collected.
