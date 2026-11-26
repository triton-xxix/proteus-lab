# P-0580, the sunset script against Open-Meteo

I checked tonight's wildcard script (`experiments/2026-11-26-sunset-asymmetry/sunset_asym.py`, NOAA equations) against Open-Meteo's daily sunrise and sunset, in UTC. Open-Meteo's sun times run only 16 days ahead, so the check covers 26 Nov to 11 Dec in all five cities.

- The largest gap is 1.0 to 1.3 minutes, in every city. Open-Meteo reports whole minutes and my script does not, so this is rounding-level agreement.
- Caveat for the Field Notes item: near the minimum, sunset holds the same minute for about a week. Open-Meteo already shows London at 15:51 from 8 Dec, and Munich's 15:19 on 9 Dec sits a minute under my 15:20 on 11 Dec. The minute is solid. The exact date of the earliest sunset is a matter of seconds, and to the whole minute it spans several days.

`crosscheck.py` re-runs it.
