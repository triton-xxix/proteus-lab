# P-0373: does the Met Office model carry ICON's Heathrow offset?

P-0323 found ICON runs 1.26 C cold against Heathrow's observed high at one day's lead. If that is an ICON habit, the Met Office's own model should not share it. If it is the site or the observation, it should.

## Method

`offset.py` pulls `ukmo_seamless` and `icon_seamless` from Open-Meteo's previous-runs API at 51.47,-0.4543 for Sep and Oct 2026, takes the daily max in London time, and compares with the Ogimet SYNOP highs P-0323 saved. Both models on the same 61 days.

## Numbers (observed minus forecast, C)

| Lead | UKMO mean | UKMO sd | UKMO MAE | ICON mean | ICON sd | ICON MAE | UKMO closer | ICON closer |
|---|---|---|---|---|---|---|---|---|
| 0 | +1.23 | 0.69 | 1.28 | +1.29 | 0.75 | 1.37 | 35 | 20 |
| 1 | +1.45 | 1.19 | 1.66 | +1.26 | 1.24 | 1.53 | 23 | 33 |

ICON's +1.26 and +1.29 reproduce P-0323's figures exactly on a fresh pull.

## Reading

The Met Office's own model is just as cold at its own airport, so the offset is not an ICON habit. Two models built separately agree within 0.2 C. That points at the site, the grid cell or how the station's maximum is taken, and this probe cannot say which. A 06 to 18 UTC maximum against a local-day maximum should push the other way, if anything, since the observation window is the shorter one.

At lead 1 UKMO is no better than ICON (MAE 1.66 against 1.53), so there is no reason here to prefer it.

## Called shot

Said about +0.6 and smaller than ICON. Measured +1.45 and larger than ICON at lead 1. Verdict right, number wrong by more than double.

## Not done

Two months, one site, one autumn. No test of the grid-cell explanation. Not used for any market.
