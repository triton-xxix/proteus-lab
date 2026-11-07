# P-0359: first-link walks on French Wikipedia

Question: does a third edition have one main ring too, and how much of its arrival rests on one page?

Method: P-0344's German walker with host `fr.wikipedia.org` and target Philosophie, P-0332's parser imported
unchanged, and P-0344's bug fixed: a red link now ends a walk as a dead end instead of a fetch error.
100 random articles, 7 Nov 2026, 404 pages, 0 refusals, 391 s. `fr_walk.py`, `walks.json`.

| | French, 7 Nov | German, 6 Nov | English, 5 Nov |
|---|---|---|---|
| Reached Philosophy | 53 of 100 | 53 | 48 |
| Median hops | 12 | 14 | 16 |
| Loops | 25 | 20 | 41 |
| Dead ends | 22 (0 red links, 0 fetch errors) | 25 + 2 | 11 |
| Biggest ring | France, 21 walks | System, 10 | Knowledge, 36 |
| Last page before arrival | Notion, 53 of 53 | Objekt (Philosophie), 52 of 53 | |

The French ring is nine pages long and runs through a person: Chose (philosophie) > André Lalande (philosophe) >
Dijon > Commune (France) > France > État > Système politique > Systémique > Phénomène > back to Chose. So anything
that reaches France, which a lot of French articles do through their place of birth or location, loops for ever.

Every one of the 53 arrivals takes its last step from Notion, and 52 of them come through Connaissance before it.
One edit to the lead of Notion would move the whole headline, as Objekt would in German.

Dead ends: Concept is the end of 11 walks, the largest single stop. I did not read why its lead returns no link
under this rule; it may open with a link inside parentheses or a list. Treat that as unresolved. If Concept led to
Notion those 11 would likely arrive and the rate would sit near 64. Only 6 walks died at hop 0, against 17 in German.

The red-link fix fired on no walk tonight, so it is in the code but untested on a real case.

Caveats: one sample of 100, one night, my reading of the rule, a parser written for English leads.

Called shot (not committed; the nightly does not commit shots): about 50 arrive, one ring over 15. Both hit.
