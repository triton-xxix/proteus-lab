# P-0117: which city settles Smarkets' Highest Temperature markets? 11 Oct 2026

**Answer: Munich, not London.** The public, keyless Smarkets API (`/v3/events/<id>/`) gives every one of
the five temperature events I have called (9 to 13 Oct) a `full_slug` of
`/current-affairs/weather/munich/october-Nth-2026`. Its `special_rules` say the market settles on the
temperature "officially recorded for Munich on that calendar date by the designated weather station
reporting source", rounded to whole degrees. The station isn't named in the rules.
The market name ("Highest Temperature") and event name ("October 13th, 2026") carry no city, which
is why `exchange.py markets` never showed one.

**What it means for the book.** X-0009 to X-0013 were all forecast for central London. Open-Meteo for
Munich (ICON, ECMWF) has maxima of 15.4/14.9 on the 9th, 13.0/12.5 on the 10th, 13.4/13.0 on the 11th,
13.7/13.3 on the 12th and 16.3/14.9 on the 13th. The market's 13°C on 10 Oct was right, and my London
read was the wrong city. X-0011 (15°C at 0.30), X-0012 (18°C or higher at 0.52) and tonight's X-0013
(20°C or higher at 0.60) are near-certain losses. They stand: calls are append-only and are scored as
committed. The two settled calls already counted as losers.

**Fix.** The blind list must show the city. Every temperature call from now on is forecast for the
slug's city, and none is made where the slug doesn't name one.

Files: `market.json`, `event.json`, `events4.json` (copied from sandbox).
