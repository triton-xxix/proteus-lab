# P-0374: how much has actually traded on the exchange book's non-weather markets?

`volumes.py` asks Smarkets' keyless volumes endpoint about every non-Munich market in `exchange/BOOK.csv`. Volumes only, no prices. Results in `results.json`.

## Numbers

10 non-weather markets, 12 calls on them.

4 report a volume and 6 do not, with 0 errors. The 4 that report are exactly the 4 markets still open. The 6 silent ones are all settled, so this is the same retention P-0365 found on Munich: the API forgets a market after it closes.

| Open call | Event | Volume |
|---|---|---|
| X-0005 | UK Annual GDP Growth 2026 | 3,919 |
| X-0006 | Global Temperature | 3,854 |
| X-0049 | General Election 2026 (New Zealand) | 948 |
| X-0052 | Victorian State Election 2026 | 100 |

## Reading

These markets trade far more than Munich (2 units across four markets in P-0365), so the politics markets have real trading behind them and Munich barely any. I measured volume per market only, not whether the contract the book priced was the one that traded. Still, the gap is a reason to read the two halves of the book separately.

Tonight's Victoria call sits on the thinnest one, exactly 100 units. Its anchor of 0.93 was taken on that, so the 0.72 against 0.93 disagreement should not be read as a strong market view.

## Called shot

Said about a third report, and about 1 in 4 of those under 100. 40% report; none is under 100, though one is exactly on the line. Verdict right, share close, second number wrong on a technicality and thin at n = 4.

## Not done

Settled markets cannot be measured after the fact, which is most of the book's scored rows. Smarkets does not document the volume unit; football at 119 to 230 suggested pounds in P-0365.
