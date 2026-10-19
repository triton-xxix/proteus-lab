# E-001: the Binance delisting fade, tested the short-window way

19 Oct 2026, interactive session on Luke's go. Scripts: `admission.py` (the recent-window test,
every number in `admission.json`), `watcher.py` (the forward detector, launchd `com.proteus.e001`),
`../edges.py` (fills, kill line, register). Keyless throughout. Paper only.

**First line, honestly: the sample is thin and the recent window does not admit the edge.** The
last 21 days hold one delisting notice (EPIC and QUICK, 14 Oct). The last four notices give 11
tickers, 8 with a perp to short, reaching back to 3 Aug 2026. On those 8, the short at notice
+5 min held 24 h lost a mean 17.3% after costs against a random-entry control of +0.2%. Two of
eight won. E-001 stays a candidate; the watcher runs; nothing is traded forward.

## What P-0109 said and what it did not say

P-0109 (10 Oct) measured 51 delisted tickers over 12 months on **spot**: median -13.2% inside
5 minutes, -19.7% by 24 h, -36.4% by 7 days, 45 of 51 down at 24 h. True, and useless for a
trade, for two reasons the recent window shows:

1. Most of the 24 h fall in the recent events happened inside the first five minutes, and the
   next 24 h on the perp went the other way. On 3 Aug (ACX, HFT, PIVX, PYR, VANRY, VIC) the
   dump was reversed within the day: HFT +41% from the +5 min price, VIC +122% (a 1x short is
   liquidated; counted as -100%). The 20 Aug batch split: SCRT -13% (the short won), ICX and
   STORJ bounced.
2. A 12-month median mixes the June regime (every one of COS, D, HIGH, MBOX kept falling, the
   short made +8% to +25%) with the August regime (squeezes). Luke's point exactly: the market
   changed between June and August, and a median over both tells you about neither.

## The recent-window test (admission.py, rules in its docstring)

Short the Binance USDT-M perp at the open of the 1-minute bar at release + 5 min (and +15 min),
exit at the close of the bar 24 h (and 72 h) later. Costs: taker 0.05% a side, slippage 0.10% a
side, funding over the hold (a short receives positive funding, pays negative). Control: 300
random-entry shorts a ticker on the same perp in the 21 days before the notice, same hold, same
costs and funding, hold ending before the notice. Loss capped at the stake (liquidation).

| Window | Tickers | Tradable | Reaches back | Short +5 min / 24 h, net mean | median | winners | control mean | perm p |
|---|---|---|---|---|---|---|---|---|
| Last 21 days | 2 | 1 (EPIC) | 14 Oct | +22.8% | +22.8% | 1 of 1 | +0.4% | n/a (one event) |
| Last 11 tickers (4 notices) | 11 | 8 | 3 Aug | **-17.3%** | -6.5% | 2 of 8 | +0.2% | 1.00 |
| Since 1 June (6 notices) | 19 | 13 | 5 Jun | -5.6% | -0.1% | 6 of 13 | +0.5% | 1.00 |
| Monitoring tags since June | 4 | 2 | 18 Jun | -0.9% | -0.9% | 1 of 2 | +0.6% | 0.67 |

The other cells (`+15 min`, `72 h`) are in `admission.json`; none changes the picture. Last 11,
+5 min / 72 h: mean -12.3%, 2 of 8. +15 min / 24 h: -16.0%. Per ticker, +5 min / 24 h, net:

| Ticker | Notice | Net | Rank in own control | Note |
|---|---|---|---|---|
| EPIC | 14 Oct | +22.8% | 1.00 | the one recent win; perp settles 20 Oct 09:00 |
| ICX | 20 Aug | -3.4% | 0.12 | |
| SCRT | 20 Aug | +13.2% | 0.96 | +30% at 72 h |
| STORJ | 20 Aug | -7.4% | 0.07 | |
| ACX | 3 Aug | -16.0% | 0.00 | |
| HFT | 3 Aug | -41.6% | 0.00 | -100% by 72 h (liquidated) |
| VANRY | 3 Aug | -5.6% | 0.14 | funding -1.4% in 24 h, the crowded-short tax |
| VIC | 3 Aug | -100% | 0.00 | +122% from the +5 min price; liquidated |

Skipped (no perp anywhere keyless at the notice): QUICK, PIVX, PYR, ALCX, ARDR, POND, QKC.
PYR has a Bybit perp but no Binance one; recorded, not filled (one venue order per rule, below).

Admission line (RULES.md): mean above the control, permutation p below 0.10, five winners of
eight. **Not admitted** on any window that holds more than one event. `edges.py admit E-001`
reads the same file and says the same.

## Can it be shorted, and where

Checked keyless on 19 Oct for every ticker since June:

- **Binance USDT-M**: the perp existed at the notice for 13 of 19 delist tickers and both tradable
  monitoring tickers. Binance settles the perp **after** the spot notice, never before, in this
  sample: 101.5 h after (3 Aug batch, settled 7 Aug 09:00), 147 h after (20 Aug batch, 26 Aug
  09:00; EPIC, 20 Oct 09:00; June batch, 11 Jun 09:00), 144 h for NFP. So a 24 h and a 72 h hold
  both fit before settlement every time, and the futures delisting is announced separately in the
  same catalogue (`Binance Futures Will Delist ...`), which the watcher records as its own kind.
  Binance still serves 1-minute klines and funding for settled perps, which is what made this test
  possible; after settlement it serves flat zero-volume bars, so fills are cut at the delivery time.
- **Bybit linear**: has the pair for 7 of the 8 recent tradable tickers (all but VIC) and for
  HIGH, MBOX, ACT and BLUR; fills within 0.3% of Binance's at every entry and exit checked, and
  its funding over the 24 h hold agrees with Binance's (VANRY -1.41% v -1.40%, MBOX -2.29% v
  -2.26%). For an hour tonight I had Bybit's funding endpoint down as inconsistent; the hand
  checks were aimed three days late (my arithmetic, 1787464800 is 23 Aug, not 20 Aug), the
  script was right, and the note is here so the mistake is on the record. Bybit's STORJ funding
  did reach -1.5% to -1.8% per 8 h on 23 to 25 Aug, after the hold and around Binance's
  settlement: a crowded short on the second venue once the first one closes its perp.
- **OKX, Hyperliquid**: none of the delisted tickers (BLUR only, a monitoring tag). **Gate**: EPIC,
  STORJ, SCRT, ACT, BLUR live today, but its keyless candles reach back only 10,000 bars, so no
  history for August. **Bitget**: EPIC only today, STORJ "removed".

Venue order for a forward fill, fixed now: Binance USDT-M if the perp is live at detection, else
Bybit, else skipped. Never spot.

**Funding.** Benign in the first 24 h on most (the 0.005% per 8 h floor), with the crowded-short
tax showing on the ones that kept falling: VANRY -1.4% in 24 h, MBOX -2.3% in 24 h and -4.0% over
72 h, COS -1.3%. On the squeezes funding went the other way (HFT +0.23% to +0.30% per 8 h on
days 2 and 3, paid to shorts while the price tripled). Funding is a cost of being right late,
not the reason the trade lost.

## Kill line, fixed 19 Oct 2026 before any forward trade is possible

Applies the day E-001 (or its mirror E-002) is admitted and set to `forward`; `edges.py kill`
reads it, `edges.py status` prints it nightly.

- **KILL when the mean net of the last 6 closed forward trades is below zero.** Six is about two
  notices' worth of tickers (batches run 2 to 6), so one bad batch cannot kill alone but two can.
- **KILL on 4 consecutive losses.** Under the 12-month spot hit rate (45 of 51 down at 24 h) four
  straight losses had odds near 1 in 1,700; if it happens, the regime is not that one.
- **KILL on any single trade at or below -50%.** A VIC or HFT is a squeeze regime, not noise; one
  is enough.
- **RETIRE after 60 days with fewer than 3 forward trades.** Notices arrive every 2 to 6 weeks;
  no flow is an end, not a loss.
- Tickers from one notice are correlated. The line counts them as separate trades on purpose: it
  makes the kill faster, not slower.

## The forward machinery

- `watcher.py` polls catalogue 161 every 2 minutes under launchd (`com.proteus.e001`, loaded
  19 Oct 00:55 UTC, first poll seeded 20 notices, second poll at load confirmed clean). A new
  notice goes to `detections.jsonl` with the detection time and Binance's release time; every
  ticker in a delist or monitoring notice gets a same-poll snapshot of bid and ask on Binance
  USDT-M, Bybit, OKX, Gate, Bitget and Hyperliquid in `snapshots.jsonl`. Futures delistings and
  Alpha removals are recorded, not traded. HALT: logs and does nothing. No git from launchd.
- `edges.py score` fills each detection from 1-minute klines at detection + 5 min, exits at
  +24 h, costs and Binance funding in, writes both the short's net (E-001) and the long's net
  (E-002) to `trades.jsonl`, append-only, latest row per id wins. Rows are **shadow** while both
  edges are candidates: they build the re-admission window and never touch a kill line.
- Re-admission: when 8 tradable delist tickers have been detected after 19 Oct, `admission.py`
  is re-run and `edges.py admit` reads it (DUE D-015, backstop 19 Dec 2026).

## E-002, the mirror, and why it is not admitted either

The same eight August-to-October trades flipped (long the +5 min dump, exit +24 h) would show
+17% mean. That is the sign of E-001's failure read backwards, found after looking, on eight
events. RULES.md says a flipped edge's window starts the day the flip is written, so E-002 is a
candidate scored from the same detections and admitted only on events after today. If the
August regime persists it will show by itself; if June's returns, E-001 will.

## What happens next

The watcher runs. The nightly scores and reads. At 8 tradable tickers after today both sides get
their admission read; whichever passes goes forward under the kill line above. If neither does,
both rows go to `killed` with the numbers and the watcher stays up as the cheapest delisting
event feed the lab has (two calls a minute, one file a notice). Nothing here asks for money.
