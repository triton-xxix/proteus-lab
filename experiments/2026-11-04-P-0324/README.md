# P-0324: ICON and Météo-France bias at Strasbourg-Entzheim

**Question.** P-0319 found ICON's lead-1 cold bias at Paris was +0.32 C against Munich's +1.0. Is Strasbourg, on
the German border, nearer Paris or Munich?

**Method.** `lead_bias.py`, P-0319's method. TX from the Météo-France dept 67 daily file, station 67124001
STRASBOURG-ENTZHEIM (current to 2 Nov). One Open-Meteo previous-runs call at the station, `icon_seamless` and
`meteofrance_seamless`, leads 0 to 3, 1 Sep to 2 Nov 2026, maxed per Europe/Paris day. Paired sign-flip at lead 1.

**Numbers (mean obs minus forecast, C; 63 days).**

| lead | ICON | Météo-France |
|---|---|---|
| 0 | +0.96 | +0.70 |
| 1 | **+1.07** | **+0.54** |
| 2 | +1.32 | +1.15 |
| 3 | +1.50 | +1.19 |

Lead-1 ICON minus Météo-France +0.53, sign-flip p 0.0001. Shot: ICON +0.6. A miss: Strasbourg is Munich-sized.

**Reading.** ICON lead-1 by city now: Paris +0.32, Strasbourg +1.07, Munich about +1.0, London +1.26 (P-0323).
Météo-France's model is also cold here (+0.54), where at Paris it ran warm (-0.24), so this is not only an ICON
trait: both models under-forecast Entzheim's highs, which points at the site or the Rhine valley rather than at
the model. ICON is about half a degree colder than Météo-France at both French stations.

**Caveats.** One autumn. Entzheim is an airport in a valley floor. Lead 0 is close to a nowcast.
