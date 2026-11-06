# P-0335: ICON against the METAR high at Munich airport (6 Nov 2026)

P-0334 found that the highest EDDM METAR temperature fits all 30 settled Munich rows. If that is the
target, how does the nightly's rule do against it? The nightly takes ICON at the city point and adds
1 C, for a city station the market may not read.

Shot: METAR high minus airport ICON day-ahead about +0.1 C, exact-degree hit about 35% at lead 1.
Measured: +0.15 C and 33%.

## What I ran

Two Open-Meteo previous-runs calls (`icon_seamless`, UTC, 13 Oct to 5 Nov) at the airport and at the
city point the nightly uses, against P-0334's METAR file. 24 days. `icon_v_metar.py`, `results.json`.

## What I found

Lead 1 is what the desk mostly calls:

| Forecast | Mean METAR minus forecast | sd | MAE | Exact degree |
|---|---|---|---|---|
| City grid +1.0 (the nightly) | -0.97 | 0.87 | 1.05 | 6 of 24 (25%) |
| City grid +0 | +0.03 | 0.87 | 0.67 | 9 of 24 (38%) |
| Airport grid +0 | +0.15 | 1.56 | 1.13 | 8 of 24 (33%) |
| Airport grid +0.3 | -0.15 | 1.56 | 1.15 | 7 of 24 (29%) |

1. **Against this target, the +1 C is the error.** The nightly runs 0.97 C warm at lead 1, t about
   -5.5 on 24 days. Dropping it cuts MAE at every lead: 1.05 to 0.83, 1.05 to 0.67, 1.25 to 1.06.
2. **The exact-degree hit does not move cleanly.** Dropping the +1 helps at lead 0 (21% to 46%) and
   lead 1 (25% to 38%) and hurts at lead 2 (42% to 25%). At se about 10 points on 24 days, that lead 2
   swing is the warning. The degree hit is noisier than the error.
3. **The airport grid is not the obvious fix.** At lead 0 it is far better (71%, sd 0.44). At lead 1
   its sd is 1.56 against the city grid's 0.87, and it hits no more often. I expected the opposite.
   Do not read that as a preference for the city grid: 24 days and one model.
4. **A half-sample check says little.** A correction fitted on the first 12 days (+0.45) hits 3 of the
   last 12 at the airport, against 4 of 12 for the nightly's rule.

## What I did not do

Change the nightly or any call. All of this depends on P-0334's rule, which has not predicted anything
yet: X-0046 settling is the test, and a due row now holds that. I did not run a permutation test: the
bias t is large and the exact-degree differences are inside the noise, so neither needs one to say what
I say here. I did not replay Brier on the book's actual rows, because the desk's probabilities came from
more than this rule.
