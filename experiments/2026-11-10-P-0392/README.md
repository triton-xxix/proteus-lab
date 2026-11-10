# P-0392: Munich METAR minus city-point ICON, by day set and by week

**Question.** P-0335 read METAR minus city-point ICON lead 1 at +0.03 on 24 days; P-0387 read -0.49 on
12. Same span, one script: is the gap the day set, the method, or a drift colder into November that the
exchange book's zero correction misses?

**Shot.** works at 0.75: week from 3 Nov below -0.3 C, week from 13 Oct above 0.

**Method.** `weeks.py`: Open-Meteo previous-runs `icon_seamless` `temperature_2m_previous_day1` at
48.137, 11.575 for 13 Oct to 9 Nov, maxed per day on UTC and on Europe/Berlin days; EDDM METAR high from
Iowa State (keyless, 12 or more reports a day). Scored on P-0335's day list, P-0387's band days, all 28,
and four weeks. 3 calls.

**Numbers** (results.json, METAR minus point):

- P-0335's 24 days: +0.03 (se 0.18). P-0387's 12 days: -0.49 (se 0.35). Both reproduced to the hundredth,
  so the gap is the day set, not either method. UTC and Berlin days gave identical figures.
- All 28 days: -0.21 (se 0.21).
- Weeks: 13 to 19 Oct +0.04, 20 to 26 Oct -0.13, 27 Oct to 2 Nov +0.13, 3 to 9 Nov -0.87 (se 0.57).
- One day carries it: 9 Nov at -3.6. Without it P-0387's days read -0.21 and the last week -0.42.
  7 and 8 Nov (-1.2, -1.7) are the rest.

**Answer.** The shot's two numbers hit, but the story is not a drift. Three flat weeks then one cold
week driven by 9 Nov, under 2 se. Zero correction on the city point is still inside the noise
(all 28 days -0.21, se 0.21).

**Caveats.** 28 days; identical UTC and Berlin figures may mean the API ignores the timezone for this
endpoint, or only that highs fall mid-day; not checked.

**Not done.** No change to the exchange book. D-023 is where its correction gets scored.
