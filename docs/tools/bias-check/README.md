# Bias check

Does a weather model's bias on the daily high hold after you measured it?

`bias_check.py` fetches day-ahead forecasts from the Open-Meteo previous-runs API (hourly temperature as
issued one day before, max per local day, ICON, ECMWF IFS 0.25 and GFS by default), pairs them with
observed highs, and splits the days at `--split`. Before the split it learns each model's bias; after it,
it reports the bias again and the mean absolute error raw, after subtracting the learned bias, and after
any fixed `--correct` value. Standard library only, no keys.

```
python3 bias_check.py --lat 48.137 --lon 11.575 --tz Europe/Berlin --dwd 03379 --start 2026-08-15 --split 2026-10-13
python3 bias_check.py --lat 51.48 --lon -0.45 --meteostat 03772 --split 2026-10-01 --correct 1.0
python3 bias_check.py --lat 40.78 --lon -73.97 --csv my_station.csv --split 2026-10-01 --json out.json
```

Observations: `--dwd <DWD station id>` (German stations, recent daily file, TXK), `--meteostat <WMO id>`
(worldwide, bulk daily CSV, may lag a few days), or `--csv` with `date` and `tmax` columns.

Limits: the previous-runs API reaches back about three months, so the learning window is short. A
"helps" verdict on a dozen days is a reading, not a measurement; look at the standard error.

Checked on 26 Oct 2026: both Munich runs (`check-stadt-2026-10-26.json`, `check-flughafen-2026-10-26.json`)
reproduce every number in probe P-0225's `results.json`; `build.py` exits if they ever disagree.
Page: https://triton-xxix.github.io/proteus-lab/tools/bias-check/
