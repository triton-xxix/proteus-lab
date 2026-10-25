# P-0218: ALPR cameras in OpenStreetMap, UK and US

Question: how many objects tagged `surveillance:type=ALPR` does Overpass return for the UK and the US?

Ran `count.py` on 25 Oct 2026 about 23:40 UK against overpass-api.de, `out count` only, country areas by ISO3166-1 code.

| Country | Nodes | Ways | Query time |
|---|---|---|---|
| UK (GB) | 1,409 | 0 | 68 s |
| US | 144,723 | 20 | 170 s |

The US figure is about 100 times the UK one. That says more about who maps than about cameras: the US count is driven by the volunteer push to map Flock and similar readers (the harvest item), while the UK has thousands of ANPR cameras on the national network that nobody has tagged. So OSM is a usable keyless count for the US mapping effort and a poor one for UK coverage.

Keyless, no account, one public endpoint; the US query is near Overpass's comfort limit (170 s of a 180 s timeout), so a repeat should split by state.

Verdict: works.
