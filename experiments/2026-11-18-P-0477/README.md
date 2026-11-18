# P-0477: the exchange book's gap to the market, split by how the call was made

Why: tonight's read-it papers (ForecastGym, One Fabrication Is Enough) put an AI forecaster's loss
to the market on its search evidence. My book has two kinds of call: Munich daily highs from a
weather model with no search, and politics and current-affairs calls from public sources. If the
papers' story held here, the search half would carry the loss.

## Called shot, written before the first run
Verdict works. About 30 of the 45 counted rows are Munich. Both halves are worse than the market:
Munich about +0.07, search about +0.05, so the split does not explain the gap. Stated p 0.55.
Not blind: tonight I read four Munich rows in the tail of BOOK.csv (three of four worse than the
market) and the kill check's pooled +0.0651.

## Run
`python3 /Users/triton/PROTEUS/experiments/2026-11-18-P-0477/split.py` (reads BOOK.csv, writes
`results.json`, changes nothing in the book).

## Result
| Half | Counted | My Brier | Market Brier | Me minus market | se | Rows worse than market |
|---|---|---|---|---|---|---|
| Munich, weather model, no search | 39 | 0.2135 | 0.1396 | +0.0739 | 0.0219 | 26 |
| Politics and current affairs, search | 6 | 0.1327 | 0.1249 | +0.0078 | 0.0777 | 5 |
| All | 45 | | | +0.0651 | 0.0215 | 31 |

The Munich half again, by whether the degree I called came in:

| Munich rows | n | My mean p | Me minus market | se |
|---|---|---|---|---|
| My degree won | 12 | 0.268 | +0.2377 | 0.0322 |
| My degree lost | 27 | 0.254 | +0.0011 | 0.0125 |

- **The loss is in the half with no search in it.** 39 of the 45 counted rows are Munich and they
  carry +0.074. The six search calls sit at +0.008 with an error bar ten times that, so they say
  nothing either way. The papers' story (search evidence is where an AI forecaster loses) is not
  what is happening on this book; this book barely tests it.
- **All of the Munich gap is on the 12 days I was right.** I picked the right degree 12 times in
  39 (31%), a little better than the 0.26 I put on it. On those 12 I lose to the market by 0.24 a
  row, every one of the 12. On the 27 I got wrong I am level. Working back from the Brier numbers,
  the market had about 0.46 on my degree on the days it won and about 0.25 on the days it lost. I
  had about 0.26 on both. The market can tell a good day from a bad one and I say the same number
  every night.
- So the 0.25 single-degree cap is part of it but not all of it: lifting every call to 0.31 would
  help on winners and hurt on losers. What is missing is a reason to say 0.45 on some nights and
  0.15 on others, which is what the ensemble bands (D-020, D-024) are being scored for.

Shot: verdict hit. Munich count missed (39, I said about 30). Munich gap hit (+0.074 against
about +0.07, not blind). Search gap missed (+0.008 against about +0.05), and the sentence the
shot rested on, that the split would not explain the gap, was wrong: it explains nearly all of it.

Caveats: six search rows; two of the six are the same by-election called twice. The market
probabilities above are backed out of mean Brier scores, not read from the anchors, so treat 0.46
and 0.25 as rough. Ten settled rows have no anchor and are not counted. Nothing in the book or its
rules was changed: the cap is in the nightly prompt and the kill line (+0.020) is out of reach.

Next: deepen. Read the anchors directly: for each Munich call, my p and the market mid, and whether
the nights the market was above 0.40 could have been told apart beforehand from the ensemble band
width captured the same night.
