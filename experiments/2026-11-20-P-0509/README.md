# P-0509: HippoMaps query parser on 15 plain-English place queries

Question (from harvest H-0706): of 15 queries, how many does HippoMaps turn into Overpass QL that
returns at least one result from a public Overpass endpoint?

Called shot (141f93c5): works at 0.55, 10 of 15 return results.

## Method

- Fetched the repo as a tarball (github cdutsov/hippomaps). It is Go, and there is no Go on this Mac.
  More to the point, the parser is not in it: `server/search.go` relays `/api/search/{query,search}` to
  a separate service, overpass-search (gitlab.com/cdutsov/overpass-search). So I called the public
  page's own parse endpoint, `https://hippomaps.ch/api/search/query?q=...&lang=en`, which returns
  `understood`, `exact` and the Overpass QL, and ran that QL myself on `overpass-api.de`, not on their
  engine. `run.py`, then `retry.py` once for the four that hit 502/504 on overpass-api.de.
- 15 queries, mostly UK, a few stacked (near X, within 200 m of, far from, along, between, over).

## Numbers

- Parsed to QL: 13 of 15. `exact` true on 10, false on 3 (the near-a-school, near-a-lake and
  far-from-motorway ones). Refused with HTTP 422: "petrol stations along the M4" and "restaurants
  between the river and the cathedral in Durham".
- Ran on overpass-api.de: 12 of 13 after one retry (first pass 9; four failed on server load, 502 or
  504, three came back on retry). Museums in Edinburgh got 502 twice and is unrun, not wrong.
- Returned at least one element: 11 of 15. Zero: "drinking water in Hyde Park" (parsed as the
  boundary of Hyde Park; not checked which Hyde Park or whether fountains are tagged there).
- Counts: Zurich cafés near a bus stop 319, Leeds pharmacies 152, York pubs within 200 m of a station 2,
  Tesco in Cardiff 31 (a brand query, 543 characters of QL), Cumbria campsites near a lake 356, Brighton
  chargers 68, Welsh castles 148, Oxford bike shops far from a motorway 9, Bristol pubs 293, Danube
  bridges 28, Manchester playgrounds near a school 178.
- Each Overpass run took 25 to 49 s on the public instance.

## Not done

Did not check any result count against the ground truth, only that the QL ran and returned something.
Did not build the Go server. Their own search engine (overpass-search on overpass.ch) was not used.
