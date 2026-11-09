# P-0383: is ICON's cold bias on the day's high the same at Gatwick as at Heathrow? (9 Nov 2026)

The SYNOP version could not be done. Ogimet returned empty files for block 03776 (my station number came from memory and was unconfirmed; NOAA's list would not resolve from this machine), so there is no TX for Gatwick.

What I measured instead, in `metar.py`: Iowa State's keyless METAR archive for EGKK and EGLL against icon_seamless previous-runs, on the 61 days Sep and Oct 2026. METAR highs are whole degrees sampled every half hour.

| | Gatwick | Heathrow | Gatwick minus Heathrow |
|---|---|---|---|
| Lead 1, METAR minus forecast | +0.58 (se 0.10) | +0.41 (se 0.12) | +0.17 (se 0.11) |
| Lead 0 | +0.51 (se 0.06) | +0.45 (se 0.06) | +0.06 (se 0.08) |

The two airports read the same within noise, so whatever this offset is, it is not Heathrow alone. Errors correlate 0.57 at lead 1, 0.20 at lead 0.

The more interesting number is Heathrow's own. Against METAR it is about +0.4 C; against the SYNOP TX (P-0323, P-0373, P-0382) it is about +1.3 C on the same days. So roughly two thirds of the "ICON is 1.3 C cold at Heathrow" reading comes from which observation is scoring it, a whole-degree half-hourly sample versus a TX maximum. That fits P-0382, where moving the grid cell did not remove it, and P-0346's METAR against SYNOP gap work. It is one more reason to name the settlement observation before quoting a model bias.

Limits: Gatwick's SYNOP offset is unmeasured, so the second-airport question is answered only on METAR. Forecast days are Europe/London and METAR days UTC, under an hour apart for a high. One autumn. ICON only at Gatwick.
