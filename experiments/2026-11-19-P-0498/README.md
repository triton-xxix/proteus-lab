# P-0498: the half-life of a day's attention on Wikipedia

Refill row 194, run 19 Nov 2026 in the nightly probe loop.

## Question

Of each day's 1,000 most-viewed English Wikipedia articles, what share is in the list the next day,
and how long does an article that enters stay?

## Method

`halflife.py`, standard library, Wikimedia's keyless pageviews API, one call per day paced at two
seconds, 21 of 21 answered. Days 28 Oct to 17 Nov 2026. The main page and special pages are dropped,
leaving 984 to 988 articles a day. Next-day share is over the last 14 day-pairs. A new entrant is an
article in the list today and on none of the seven days before; its stay is the run of consecutive
days it remains.

## Numbers

- **70.6%** of a day's list is in the next day's (called shot: about 70). Thirteen of the fourteen
  pairs sit between 0.67 and 0.74.
- The odd one is 3 Nov into 4 Nov: 48.4%. Half the list turned over in one day. I did not check why.
- Still listed after k days, averaged: 72% at 1, 61% at 2, 56% at 3, 53% at 4, 50% at 5, 48% at 6,
  47% at 7. So the half-life of a day's list is about five days, but the curve is two populations:
  a fast-leaving third and a core that hardly moves.
- 184 articles were in the list on all 21 days.
- 2,846 new entrants over 13 days, about 219 a day. Median stay **1 day** (called shot: 1); 58% are
  gone the next day. 298 runs were cut by the end of the window, so longer stays are undercounted.

## Not done

One three-week window. Bots and scripted traffic are in the "all-access, all-agents" list and some of
the one-day entrants will be those, not attention. No look at which articles the 184 are.
