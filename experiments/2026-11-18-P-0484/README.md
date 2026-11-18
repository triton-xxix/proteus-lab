# P-0484: Polymarket's London and Paris daily-high markets, 1 to 17 Nov, read the way P-0459 read Munich

Refill source 181. P-0459 (17 Nov) found the Munich market's implied high was only 0.24 C warm on
low-cloud mornings, where ICON alone was 1.07 C warm (P-0446): the market had mostly priced the
thing the model misses. P-0447 found ICON has the same low-cloud miss at Heathrow and Paris CDG.
Do the London and Paris markets price it too?

Learned in the refill step: the London market exists and settles on London City Airport (EGLC),
not Heathrow, on the tenths-of-a-degree remark rounded half up. So P-0447's Heathrow figure is not
this market's station.

## Called shot, written before the run
Verdict works. Both cities have events for at least 15 of the 17 days. The 09Z favourite hits on
45 to 60% of days in each city (Smarkets' Munich night-before favourite: 53.6%, P-0478). Mean
absolute error of the implied high under 1.0 C in both. Low-cloud mornings are rare at both this
month (3 or fewer of 17), so the gap is not readable: the honest answer on the question asked is
"too few days". Stated p 0.5. Blind to every price and outcome in both cities.

## Run
`python3 -I /Users/triton/PROTEUS/experiments/2026-11-18-P-0484/cities.py` (keyless: gamma-api,
clob prices-history, Iowa State METAR archive; about 400 requests, paced).

## Result
All 17 days scored in both cities, nothing skipped, every bucket in Celsius.

| | London | Paris | Munich (P-0459, 1 to 16 Nov) |
|---|---|---|---|
| Station in the market's own rules | EGLC, London City | LFPB, Le Bourget | EDDM |
| 09Z favourite hit | 11 of 17 (65%) | 7 of 17 (41%) | see P-0459 |
| Mean price of the favourite | 0.545 | 0.536 | |
| Mean error of the implied high (truth minus market) | -0.01 C | -0.17 C | |
| Mean absolute error | 0.47 C | 0.65 C | |
| Low-cloud mornings | 8 | 2 | |
| Error on low-cloud mornings | +0.27 C | +0.13 C | |
| Error on other mornings | -0.26 C | -0.21 C | |
| Gap (low-cloud minus other) | +0.52 C | +0.34 C | -0.24 C |

- **Neither market settles where I assumed.** London is London City, not Heathrow; Paris is Le
  Bourget, not Charles de Gaulle. P-0447's ICON figures were for EGLL and LFPG, so they are not
  these markets' stations and cannot be laid beside these numbers.
- **The low-cloud warm miss is not in these prices.** At London City, with 8 low-cloud mornings
  out of 17, the market was if anything 0.27 C cold on them and 0.26 C warm on the rest. That is
  the opposite sign to ICON's miss at Munich. Eight against nine days is thin, but it is not the
  "too few days" I called: London City sits by the river and had low cloud on nearly half the
  mornings.
- **By 09Z the market is close.** The implied high is within half a degree on average in London
  and two thirds in Paris, with no bias in London. The favourite at about 0.54 won 65% of the
  time in London and 41% in Paris; pooled, 18 of 34 (53%), which is what a 0.54 price should do.
  So no sign here of a favourite that is under- or over-priced.
- Paris's two low-cloud days are too few to read; its favourite missed on both.

Shot: verdict hit. Days hit (17 and 17). Favourite band (45 to 60%) missed both ways: London 65%,
Paris 41%. Mean absolute error under 1.0 C hit in both. Low-cloud mornings "3 or fewer" hit for
Paris (2) and missed for London (8).

Caveats: 09Z is hours into the day, so the price already holds the morning's observations; this
is not the night-before price that the Smarkets Munich check uses. Prices are the last trade at or
before 09Z within three days, hourly fidelity. One month, 17 days a city. Tails are counted at
their edge degree. No ICON forecast was pulled for EGLC or LFPB, so the model's own gap at these
two stations is unmeasured.

Next: deepen. Pull ICON's lead-1 error at EGLC and LFPB on the same 17 days, so the market's
+0.52 C at London City has the model's number beside it.
