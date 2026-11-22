# P-0533: the Aurora detector, deepened

P-0532 caught 16 of 28 Kp 7+ days with en Aurora view spikes and had 11 spikes on calm days. Does a
second article help, and what were the calm spikes?

## Method

`deepen.py`, keyless Wikimedia REST, on P-0532's rows. Same spike rule (above twice the trailing 30-day
median, that day or next) for en `Geomagnetic_storm`. For each calm Aurora spike, the day's top-read
articles filtered for sky words.

## Numbers

- **Geomagnetic_storm catches 22 of 28 Kp 7+ days (79%)**, Aurora 16; either catches the same 22.
- The price: Geomagnetic_storm spikes on 38 calm days against Aurora's 11 (43 for either). It is a
  noisier article: smaller base, so small news bumps double it.
- The calm Aurora spikes are mostly tails: 15 and 19 May 2024 follow the 10 to 12 May storm (the
  `May_2024_solar_storms` article was still read 13,864 times on the 15th), 13 to 15 Oct 2024 follow
  10 to 11 Oct, 15 to 16 Nov 2025 follow 12 to 13 Nov. 7 of the 8 named are within five days of a
  Kp 8+ storm; 30 Jan 2026 is unexplained; three August 2026 dates were refused (HTTP 429).

## What I did not do

The three 429 dates were not retried. No news search. The calm rule counts a day calm if Kp stayed
under 5 that day and the day before, which marks storm tails as false alarms.
