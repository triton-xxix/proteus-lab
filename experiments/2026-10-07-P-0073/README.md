# P-0073: supercar price map, first pass

Run 7 Oct 2026, interactive probe loop, from AutoTrader UK in the browser pane (sorted by price,
national). The listings load through AutoTrader's private API, so this pass reads the rendered
pages only. Data in `listings-2026-10-07.csv`.

## The target: McLaren 720S

23 for sale in the UK; 21 parsed. 13 are coupés, the rest Spiders and Performance trims.

| Year | Coupés | Cheapest | Median |
|---|---|---|---|
| 2017 | 4 | £134,949 | £142,495 |
| 2018 | 4 | £134,995 | £147,245 |
| 2019 | 3 | £143,290 | £144,990 |
| 2020 | 1 | £134,100 | £134,100 |
| 2022 | 1 | £169,950 | £169,950 |

- Cheapest 720S of any kind: £134,100 (2020, 37,000 miles). Four coupés are at or under £140,000.
  Luke's £140,000 target buys one today, at the bottom of the market.
- 2017 to 2020 coupés sit in one band, £134k to £150k, whatever the year. Age stopped mattering;
  mileage and spec (warranty, paint film, carbon packs in the ad titles) move the price instead.
  Median mileage 19,100.

## Against two rivals, same year

| 2017 car | Listings | Cheapest | Median |
|---|---|---|---|
| McLaren 720S coupé | 4 | £134,949 | £142,495 |
| Ferrari 488 GTB | 6 | £157,500 | £174,990 |
| Lamborghini Huracán coupé | 2 | £134,975 | £147,483 |

The 488 holds about £30k more than the 720S at the same age; the Huracán sits with the McLaren.
Caveat: for the 488 (45 listed) and the Huracán (100 listed) I read only the cheapest page, 19 and
22 cars, so their medians are biased low. The gap to the 488 is therefore if anything larger.

## Not done tonight

- Every Ferrari (658) and Lamborghini (479) by model: needs either 46 pages through the browser or
  AutoTrader's API, which I did not reverse-engineer.
- A year's running costs for a 720S (insurance, servicing, tyres, road tax): GOV.UK's tax tables did
  not come back cleanly, and I will not guess figures. Queued as its own probe.
- Five-year value history: one day's listings show today's floor, not the path to it. Repeating
  this pull monthly would build that.

## Verdict

Works as a first map: the target car is buyable at £134k to £140k today, the 2017 to 2020 cars have
found a floor, and a Ferrari 488 of the same age keeps more of its value.
