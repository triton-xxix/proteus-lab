# synop-highs

Daily highs for any WMO station from Ogimet's SYNOP archive. Keyless, current to the day, standard library only.

```
python3 synop_highs.py --wmo 03772 --start 2026-09 --end 2026-11 --csv heathrow.csv
```

It reads the `1snTxTxTx` group in section 333 of the report at `--hour` (default 18 UTC, which in the UK and
France carries the 06 to 18 UTC maximum) and writes `date,tmax`. One request per month, two seconds apart. It
prints how many reports at that hour had no max group, so a wrong `--hour` for your country shows at once.

The CSV goes straight into [bias-check](../bias-check/) as `--csv`.

Checked on 4 Nov 2026 (`build.py` exits if either fails):
- Heathrow: the parser over probe P-0323's saved pulls gives its 61 days, and a fresh pull matches every one.
- Strasbourg-Entzheim (07190): 63 of 63 days identical to Météo-France's own daily TX for the station.

Built from probe P-0323. Page: https://triton-xxix.github.io/proteus-lab/tools/synop-highs/
