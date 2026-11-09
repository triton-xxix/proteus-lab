# P-0382: is ICON's Heathrow offset one bad grid cell? (9 Nov 2026)

P-0323 and P-0373 found ICON about 1.3 C below Heathrow's SYNOP high at one point. `cells.py` repeats that against the same
observations at Heathrow's cell and four points about 11 km north, south, east and west, 61 days, Sep and Oct 2026.

| Point | Elevation, m | Lead 1, obs minus forecast | Lead 0 |
|---|---|---|---|
| Heathrow | 26 | +1.26 (se 0.16) | +1.29 (se 0.10) |
| North | 41 | +1.41 | +1.47 |
| South | 25 | +1.22 | +1.19 |
| West | 24 | +1.28 | +1.28 |
| East | 13 | +1.01 | +1.01 |

The offset stays above +1.0 C in every cell at both leads. Its spread, 1.01 to 1.41, is about one of the 0.16 standard errors each side of the middle
on any one point, though the days are shared so the cell differences are tighter than that suggests. East is the warmest cell by a mean 0.25 to 0.29 C and is also the lowest.
A single bad cell is out: moving a cell changes the offset by at most 0.3 C of about 1.3 C. Most of it survives, so the cause is more likely the observation, the region, or the model's near-surface physics. This does not say which.

Limits: one airport, 61 autumn days, 11 km steps, and "cell" here means whichever nearest grid point Open-Meteo returns, shown by the `got` coordinates in `results.json`.
