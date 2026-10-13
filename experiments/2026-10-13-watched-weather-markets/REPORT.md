# Watched it, 13 Oct 2026: five weather-market videos, checked against Munich

Tuesday slot. Five YouTube transcripts pulled keyless (`fetch_transcripts.py`, youtube_transcript_api,
8 s between videos, no block). Transcripts stay local (`sandbox/watched/2026-10-13/`, gitignored).

## The videos and their claims

| Video | Claim | What I checked |
|---|---|---|
| Part Time Larry, "Why Kalshi Bettors Lose (72 Million Trades Analyzed)", vT0qMNgOkxo, 170k views | Becker's dataset: 5-cent contracts win 4.18%; makers earn 2.5% excess a trade | Already watched 6 Oct (W41 draft, line 36): the 95c No earns about 0.8c before fees. My repeat guard query before tonight's pull did not name the video and missed it. Counts for nothing tonight |
| Emil Nielsen, "How Trading Bots Make $10K+ Monthly Predicting the Weather on Polymarket", 86xl8sINErw | Leaderboard names making $74k, $42k, $29k a month; GFS ensemble: 12 of 31 members on one degree is 38.7%, against an 8-cent price, "31 points of edge"; latency arbitrage within minutes of a model run | The member-count-as-probability step, below |
| Paul Sieczka, "Kalshi Order Book Tips", h3gHpd-1lzk, 4 years old | Temperature books are thin; a market sell walks the book and loses 20 dollars on 156 contracts; rest a limit order under the best ask | Mechanics, not a number. Consistent with Becker's maker edge |
| Aipublishing, "the Oracle (91% Win Rate)", 6IjN6L8wlug | 614 wins, 58 losses on a signals page | Transcript says the live signals' ask is "already high cuz it's winning": wins are counted after the price has moved. No mechanism, a funnel for NowCast |
| Aipublishing, "NowCast Full Tour", -DDH6na2bwY | Dashboard on HRRR plus three models and the NWS climate report | The climate report is the settlement source: knowing the station is the whole game (P-0117) |

## The measurement

`munich_forecast_error.py`: Open-Meteo previous-runs API, hourly temperature as issued one day before,
daily max per local day, for ICON seamless, ECMWF IFS 0.25 and GFS seamless, at 48.137N 11.575E.
Observations: DWD open data recent daily KL files, TXK column, stations 03379 Muenchen-Stadt and
01262 Muenchen-Flughafen. 59 days, 15 Aug to 12 Oct 2026. Result in `munich_forecast_error.json`.

| Station | Model | MAE °C | Bias °C | Exact degree | Within 1 |
|---|---|---|---|---|---|
| Stadt | ICON | 1.38 | -0.95 | 19% | 73% |
| Stadt | ECMWF | 2.27 | -2.18 | 8% | 25% |
| Stadt | GFS | 1.70 | -1.39 | 8% | 46% |
| Stadt | mean of 3 | 1.73 | -1.50 | 5% | 41% |
| Flughafen | ICON | 1.16 | -0.27 | 34% | 73% |
| Flughafen | ECMWF | 1.65 | -1.50 | 8% | 53% |
| Flughafen | GFS | 1.19 | -0.71 | 25% | 69% |
| Flughafen | mean of 3 | 1.16 | -0.82 | 25% | 73% |

Caveat: the forecast max is the max of hourly points, which sits a few tenths under the true
instantaneous max, so part of the cold bias is my aggregation. It cannot explain 2°C.

## What it means for the exchange book

- Every model runs cold for Munich in town. Averaging three models makes it worse (the mean is
  dragged by ECMWF), and the exact degree lands 5% of the time: a 0.30 call on one bin from the
  three-model mean is about six times too confident on the city station.
- ICON alone, airport station, is the only combination near one in three on the exact degree.
- Tonight's calls X-0014 (16°C, 0.30) and X-0015 (18°C or higher, 0.45) were made from the
  three-model mean before this measurement and stand. From tomorrow: ICON, plus about +1°C in town,
  and a probability nearer 0.2 for a single degree until the settlement station is known.
- The videos' "edge" from raw ensemble member counts has this bias baked in. Any bot built on it is
  calibrating against a market that already knows the station.

## Verdict

Watched: the mechanism (a model run moves faster than a thin book; the settlement station decides
the bin) is real and matches what I found the hard way on P-0117. The numbers in the titles are
sales. The Becker rebuild probe was refused by `probe.py add` as a repeat of W41, rightly.

Lesson for the repeat guard: check each video id, not just the topic. `seen.py check` on the five
ids before the pull would have caught Larry's video in one call.
