# P-0319: does ICON's Munich warm bias travel to Paris, and does Arome carry it?

**Question.** At Munich, ICON's day high runs cold by about 1.0 C (obs minus forecast, P-0281, P-0293). Is that
an ICON trait that shows up at a third city outside the DWD grid, and does Météo-France's own model show it?

**Method.** `lead_bias.py`. Observed TX at Paris-Montsouris (Météo-France station 75114001) from the open daily
file for dept 75. Forecasts from one Open-Meteo previous-runs call at Montsouris, `icon_seamless` and
`meteofrance_seamless`, hourly, leads 0 to 3, maxed per Europe/Paris day, 1 Sep to 2 Nov 2026 (63 days).
Lead-1 difference between models tested with a 10,000-draw paired sign-flip.

**Numbers (mean obs minus forecast, C; sd in brackets; 63 days).**

| lead | ICON | Météo-France |
|---|---|---|
| 0 | +0.10 (0.54) | -0.27 (0.74) |
| 1 | **+0.32** (1.10) | **-0.24** (1.05) |
| 2 | +0.83 (1.37) | +0.86 (1.61) |
| 3 | +0.87 (1.61) | +0.87 (1.79) |

Lead-1 ICON minus Météo-France: +0.57 C, sign-flip p < 0.0001. Shot was ICON +0.5, Arome near 0.

**Reading.** ICON runs cold at Paris too, but a third of Munich's size at lead 1. Météo-France runs slightly
warm at leads 0 and 1, where Arome is in the blend, then at leads 2 and 3 the two models land within 0.03 C
of each other: `meteofrance_seamless` past Arome's 2-day range is Arpege or a fallback, so leads 2 to 3 say
nothing about Arome. The +1.0 is not a constant that travels: it is mostly a Munich number.

**What I did not do.** No check of whether `meteofrance_seamless` leads 2 to 3 are literally ICON values hour
by hour. One autumn only. Lead 0 is the latest run, close to a nowcast on the day.

**A trap found.** The data.gouv.fr object mirror (`object.files.data.gouv.fr/meteofrance/...`) served a copy
ending 22 Jun 2026. The dataset API's own URL (`meteofrance.s3.sbg.io.cloud.ovh.net/...`) is current to
2 Nov. Meteostat bulk for 07156 ends 11 Mar 2026.
