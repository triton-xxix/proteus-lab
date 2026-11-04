# P-0323: Heathrow day highs from SYNOP, and ICON's bias at London

**Question.** P-0317 had the ICON lead curve for Heathrow ready but no keyless 2026 observations (GHCN stops
Aug 2025, Meteostat bulk Mar 2026). Can Ogimet's SYNOP archive supply them, and what is ICON's day-high bias?

**Method.** `lead_curve.py`. Ogimet `getsynop?block=03772`, one call for September and one for October 2026
(7191 report lines). Day high = the 18 UTC report's section 333 group `1snTxTxTx`, the UK's 06 to 18 UTC maximum.
Forecasts: P-0317's ICON seamless previous-runs pull, maxed per Europe/London day. Same columns as P-0317.

**Numbers.** 61 days, 1 Sep to 31 Oct, no gaps.

| lead | mean obs minus ICON | sd | hit at +0 | hit at +1 |
|---|---|---|---|---|
| 0 | +1.29 | 0.75 | 0.18 | 0.38 |
| 1 | **+1.26** | 1.24 | 0.20 | 0.21 |
| 2 | +1.50 | 1.35 | 0.13 | 0.20 |
| 3 | +1.49 | 1.46 | 0.12 | 0.28 |
| 6 | +1.22 | 2.29 | 0.15 | 0.13 |

Shot: +0.5. Missed by 0.76.

**Reading.** Across the cities so far, ICON's lead-1 cold bias runs Paris +0.32 (P-0319), Munich about +1.0,
London +1.26. Here it is flat across leads, and lead 0 (sd 0.75) has the same +1.29 as lead 1, so it is a fixed
offset between the grid cell and the Heathrow thermometer (an urban airport site), not error that grows with
lead time. Any London day-high market priced off ICON would need about +1.3, more than Munich's +1.0.

**Caveats.** The 18 UTC TX covers 06 to 18 UTC, not the climate day; a late warm evening is missed and the bias
would be larger if anything. One autumn. No other model checked here.

Ogimet works keyless and current to the day, which makes it the observation source wherever Meteostat bulk has
gone stale.
