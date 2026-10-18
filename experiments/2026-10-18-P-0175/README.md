# P-0175: Meta Ads Library without login, who advertises on "plumber" in the UK?

Refill source 7. Learned first: plain curl on the Ads Library search URL gets HTTP 403, 481 bytes.
Question: does a real browser get results with no login, and what does the "plumber" search hold?

Shot (blind): works at 0.55, a real browser gets results without login, about 200 to 5,000 active GB ads.

## Method

`adlib.mjs`: headless Chrome, a fresh profile that has never logged in, a normal desktop user agent, over
CDP. Open `ads/library/?active_status=active&ad_type=all&country=GB&q=plumber`, wait 12 s, scroll four
times, save the page text, a screenshot (`shot-plumber.png`) and `summary-plumber.json`. Advertisers were
read from the line above each "Sponsored" and tallied by hand into `tally.json`.

## Numbers (18 Oct 2026, 11:37 UTC)

- No login wall: the page served **~3,800 results** and 40 ads after four scrolls. (The summary's
  `login_wall: true` is a false positive: it matched the header's "Log in" link.)
- Meta's default sort is total impressions, so these 40 are the most-seen ads matching the word.
- Of 40: **17** sell *to* tradespeople (MyJobQuote lead-gen fronted by trade creators 6, Tradesman
  Nutrition 4, a merchant 2, insurance, training, flyers, a "free course", Dan Lok), **14** sell water and
  DIY products to consumers (Water2 8), **4** are health funnels that tell a story about a plumber, and
  only **3** are plumbers selling plumbing to homeowners (High Tide Plumbing, Ninja Plumbers London, and a
  US firm in San Mateo). 2 other.
- The single most-seen "plumber" ad in the UK today is a cholesterol scare story about a plumber on statins.

## What it means

A keyword search for a trade finds the people *marketing to* that trade far more than the trade itself.
MyJobQuote's pattern (a trade creator's page "with MyJobQuote", telling trades that homeowners no longer
search "local trades near me") is the one with the most variants. To see actual plumbing firms the search
needs homeowner words ("blocked drain", "boiler service") or advertiser search.

## Not done

Only the first 40 of ~3,800. No region filter. No spend or reach numbers (Meta shows those only for
political ads in the UK). Raw page text not committed (third-party ad copy); `adlib.mjs` regenerates it.
