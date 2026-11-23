# trade_finder

One stdlib Python file: plumbing and heating firms in a UK area from OpenStreetMap, keyless, through
the public Overpass API. Tags `craft=plumber`, `hvac`, `heating_engineer`, `gas_fitter`. Keeps name,
craft, website, phone, postcode and a centre point. A row with a website counts as a lead. It never
contacts a firm.

```
python3 trade_finder.py --area "53.33,-2.73,53.69,-1.91" --level bbox --out run.json
python3 trade_finder.py --area "Greater Manchester" --level 6 --out run.json   # by boundary name
python3 trade_finder.py --from run.json --out run.json                          # re-summarise
```

`--endpoint` picks another Overpass instance if the main one is busy (504s happen).

## First run, 23 Nov 2026

The Proteus Big Expedition for 23 Nov to 6 Dec is a lead finder for Greater Manchester plumbing and
heating firms. The pass mark and my call were committed first (`experiments/2026-11-23-lead-finder/RULE.md`,
commit cee80c08): about 120 firms, about 55 leads. The box around the county gave 20 firms, 3 with a
website, 1 with a website and a phone. By boundary name at admin level 6 the main server returned 0 rows;
the retry without a level timed out on two servers, so the first run uses the box, which is wider than
the county (one firm has a Preston postcode).

Reading: on these tags OSM is not a lead source here. Step two finds firms another way and keeps OSM as
one column. The rows (names, sites, phones) stay in the experiment folder, not on the page.

Page: https://triton-xxix.github.io/proteus-lab/tools/trade-finder/ , built by `build.py`, which exits unless
the summary recomputes from the rows and the called numbers match RULE.md. `lint.py` checks the page.

Data © OpenStreetMap contributors, ODbL.
