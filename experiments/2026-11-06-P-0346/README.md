# P-0346: METAR high against SYNOP TX at three airports

Question: is the gap between the whole-degree METAR high and the SYNOP maximum the same at Heathrow, Orly and Munich,
so that ICON offsets measured against one can carry over to the other?

Method: `three_airports.py`. Sep to Oct 2026. SYNOP 18 UTC report's 06 to 18 UTC maximum, METARs from the same window,
Iowa Mesonet raw reports. The window matters: SYNOP's 06 to 18 UTC is not the local day, so these numbers do not stand
in for P-0345's.

| Airport | Days | Mean METAR minus TX (se) | Same as rounded TX |
|---|---|---|---|
| Heathrow EGLL / 03772 | 61 | -0.93 C (0.08) | 28% |
| Orly LFPO / 07149 | 51 | -0.29 C (0.05) | 65% |
| Munich EDDM / 10870 | 30 | +0.19 C (0.07) | 80% |

No, the gap does not travel. Heathrow's METAR sits nearly a degree under its SYNOP maximum, and on 14 of 61 days two
whole degrees under the rounded figure. My shot, within 0.3 C of zero and 70 to 80% agreement at all three, missed at
Heathrow and half-missed at Orly.

So P-0323's +1.26 at Heathrow, measured against SYNOP, would be about +0.33 against a METAR target if the gap holds
(1.26 minus 0.93). That is arithmetic, not a measured ICON-against-METAR figure. Paris does not carry at all: P-0319 was
Paris-Montsouris and this is Orly, a different site.

Not established: why Heathrow runs so low. Truncation in the report, or a different sensor to the one behind the
SYNOP, would each fit; I have not separated them. Munich has only 30 days, half the window, and I did not check why.
No book or nightly rule changed; no London or Paris market is on the exchange list tonight.
