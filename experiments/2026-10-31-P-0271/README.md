# P-0271: P-0250's zero terms against a small anchor

Refill row 51, Trials slot, 31 Oct 2026. P-0250 paired P-0150's 34 radar terms with "spreadsheet" and 17
of the 20 "rising" terms read zero over the last 14 days, because Trends rounds anything under about one
percent of the larger term to nothing. This probe lowers the floor by changing the anchor.

## Called shot

works at 0.70: 8 of the 17 zero rising terms show nonzero volume over the last 14 days against the
small anchor, 5 clear one percent of it. Commit c4c49da.

## Calibrating the anchor (`small_anchor.py calibrate`, `calibrate.json`)

The row asked for an anchor near one percent of "spreadsheet". That anchor does not work: a term at one
percent is itself at the rounding floor.

| candidate | share of spreadsheet, 3 months | days nonzero of 93 |
|---|---|---|
| sumproduct | 0.95% | 22 |
| countifs | 1.8% | 44 |
| index match | 6.3% | 86 |
| xlookup | 8.2% | 93 |
| pivot table | 21.7% | 93 |
| vlookup | 22.7% | 93 |

xlookup chosen: steady, nonzero every day, one twelfth of spreadsheet, so the floor drops from about
one percent of spreadsheet to about 0.08 percent.

## Numbers (`small_anchor.py run xlookup`, `results.json`)

P-0250 had 24 terms at zero over the last 14 days (17 rising, 7 not). All 24 answered 200.

| | all 24 zero terms | the 17 rising |
|---|---|---|
| nonzero over the last 14 days against xlookup | 12 | 11 |
| at or above 1% of xlookup, last 14 days | 7 | 6 |
| still zero | 12 | 6 |

The six rising terms that clear one percent of xlookup: replica skill 8.3%, DeepSeek Bot 7.5%, RustGIS
6.1%, DigUp 4.6%, doory 3.1%, mailcheap 1.8%. Universal modder (not rising) sits at 7.2%. The six rising
terms still at zero: huashu art motion, omdrop owl, fsearch, talorys, usd brep, and qwen21 nsfw pose skill
(0 of 93 days, so nobody searches the repo name).

Shot against measured: 11 of 17 nonzero against 8 called (miss, the small anchor resolved more than I
expected), 6 at one percent against 5 called (near). Called works, measured works.

## Reading

With the right anchor, P-0150's "20 of 34 rising" becomes: 3 terms visible against spreadsheet, a further
6 visible at one to eight percent of xlookup, 6 with no searches at all, the rest noise. Trends can rank
small terms keyless, but only through a chain of anchors, each about a tenth of the last, and the reading
is "x percent of xlookup", not a volume. One pull, one IP, 31 requests across both modes, no 429.

## Not done

No second anchor below xlookup to resolve the six still at zero; no check that a term's share is stable
across two anchors (xlookup against index match would show whether the ratios chain). The radar repo's
own Trends claim is still untested as it states it (pytrends, self-scaled).
