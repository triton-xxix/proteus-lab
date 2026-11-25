# P-0565: Munich straddle ladders, settled and open

Nightly 25 Nov 2026, refill from REFILL-SOURCES row 240. P-0553 (23 Nov) found that Munich ladders which
straddle zero drop the sign-twin of a listed degree (Smarkets slugs lose the minus), and none of those
ladders had settled. No called shot was written before this one ran; that is a slip, noted here.

The learning step: tonight's markets listing shows only Munich weather markets open, so row 240's "other
cities" question has no other city to look at tonight.

## What I ran

`settle.py`: P-0553's gap lists for the 23, 24 and 25 Nov ladders, the winners kept in
`exchange/munich_outcomes.jsonl`, and the highest EDDM METAR temperature per Berlin-local day
(aviationweather.gov, keyless, 96 hours, 48 reports a day). Then tonight's two ladders (names from
`exchange.py markets`, no prices) against icon_seamless's day high at 48.137,11.575.

## Result (`results.json`)

| day | missing | METAR high | listed? | winner |
|---|---|---|---|---|
| 23 Nov | 1 | 3°C | yes | 3°C, matches |
| 24 Nov | -2, 1 | 3°C | yes | 3°C, matches |
| 25 Nov | -2, -1 | 1°C | yes | not settled yet |

| open | listed inner degrees | missing | ICON point | plausible (within 1.5°C) | plausible and missing |
|---|---|---|---|---|---|
| 26 Nov | -3, -1, 0, 2, 4 | -4, -2, 1, 3 | -0.3°C | -1, 0, 1 | **1** |
| 27 Nov | -4 to 0 | 1, 2, 3, 4 | +0.5°C | -1, 0, 1, 2 | **1, 2** |

## Verdict: works

The gaps have not bitten yet: on both settled ladders the METAR high landed on a listed degree, the winner
matched it, and 25 Nov's 1°C is listed too. So nothing yet says how Smarkets settles a missing degree. But
tonight both ladders miss 1°C, which is within 1.5°C of ICON's point both days, and the 27 Nov ladder,
which has lost all of 1 to 4, sits under a forecast that has warmed from -0.1°C (when X-0070 was called)
to +0.5°C. If 27 Nov's high is 1 or 2°C, a missing degree wins for the first time. `munich_outcomes.jsonl`
will show what settled; a recheck probe after 28 Nov reads it.
