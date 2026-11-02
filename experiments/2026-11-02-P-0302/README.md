# P-0302, ICON lead curve at Munich airport (2 Nov 2026, nightly refill from source 71)

P-0293 for the airport station. ICON seamless hourly temperature at the airport grid point as issued 0 to
6 days before (Open-Meteo previous-runs API, one keyless call), maxed per Berlin day, against DWD 01262
Muenchen-Flughafen daily highs, 61 days, 1 Sep to 31 Oct 2026. Script `lead_curve_airport.py`, numbers
`results.json`; the city columns are P-0293's.

| lead (days) | bias obs minus ICON | sd | hit at +0.3 | hit at +1.0 | city sd | city hit at +1.0 |
|---|---|---|---|---|---|---|
| 0 | +0.13 | 0.56 | 62% | 26% | 0.68 | 59% |
| 1 | +0.35 | 1.47 | 38% | 28% | 1.32 | 39% |
| 2 | +0.54 | 1.22 | 34% | 33% | 1.35 | 39% |
| 3 | +0.66 | 1.75 | 25% (24.6) | 30% | 1.78 | 30% |
| 4 | +0.64 | 2.14 | 18% | 20% | 2.21 | 28% |
| 5 | +0.44 | 2.64 | 16% | 10% | 2.64 | 16% |
| 6 | +0.53 | 2.78 | 12% | 11% | 2.74 | 13% |

What it says:
- The sd grows at the same rate at both stations: within about 0.15°C at every lead. The spread is the
  forecast's, not the station's.
- The airport bias is small at lead 0 (+0.13, matching P-0291) and drifts to about +0.5 to +0.65 from
  lead 2. So the nightly's flat +0.3 airport correction is right for a same-day or next-day call and a
  little low beyond that.
- The last lead with an exact-degree hit of 25% or more at +0.3 is 2 (lead 3 sits on the line at 24.6%).
  The city managed lead 4 at +1.0. Two days out is the comfortable limit for an airport call.

Caveats: two months, one grid point, about 6 points of standard error on each hit rate; the best
in-sample corrections (-0.8 to +0.8) jump around and mean nothing at n=61.
