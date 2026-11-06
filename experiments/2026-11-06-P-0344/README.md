# P-0344: first-link walks on German Wikipedia

Question: is the English Knowledge ring an accident of English, and what does the same rule do on German?

Method: P-0332's parser imported unchanged, host changed, 100 random articles on 6 Nov 2026, 0.3 s between fetches,
425 pages, no 429s, 546 s. `de_walk.py`, `walks.json`.

| | German, 6 Nov | English, 5 Nov |
|---|---|---|
| Reached Philosophy | 53 of 100 | 48 of 100 |
| Median hops | 14 | 16 |
| Loops | 20 | 41 |
| Dead ends | 25 (plus 2 parser errors) | 11 |
| Biggest ring | System, 10 walks | Knowledge, 36 walks |

German has a ring of its own and it is a different one: System > Ganzheit > Abstrakta > Sprachwissenschaft >
Sprache > System. The stored result shows it as a one-page ring because System's first link, as parsed, is System
itself; `system_on.py` skips that self-link and walks on to find the five pages. So the walks count as loops either
way, but the ring they join is not the one printed in `walks.json`.

So the ring is a local accident of each language's leads, not a law. 52 of the 53 arrivals pass through one page,
Objekt (Philosophie), so a single edit there would move most of the headline.

German-specific failures: 17 walks died at hop 0, mostly name and disambiguation pages whose lines are lists, not
paragraphs. Without them 53 of 83 arrive. Sport (4 walks) and Liste interkontinentaler Staaten (4) also return no
link under this rule; I did not read why for Sport, whose lead may simply have no plain link, so treat that as
unresolved.

Parser bug found: 2 walks stopped as fetch errors because a red link (`?action=edit&redlink=1`) is taken for an
article. They should count as dead ends. It is the same parser on English, so P-0332 may hold the same error.

Caveats: one sample of 100 on each language, a day apart. My reading of the rule. No Wikimedia 429s here, unlike the
pageviews API at midday (P-0338).
