# P-0485: ICON at London City and Le Bourget, beside the markets that settle there

P-0484 found Polymarket's London market 0.27 C cold on low-cloud mornings and 0.26 C warm on the
rest (gap +0.52 C over 8 and 9 days), the opposite sign to ICON's low-cloud miss at Munich. It left
ICON at these two stations unmeasured. This measures it on the same 17 days against the same truth.

## Called shot, written before the run
Verdict works. ICON lead-1 is worse than the 09Z market at both stations: mean absolute error
about 1.0 C against the market's 0.47 and 0.65. At London City, ICON is warm on low-cloud mornings
relative to the rest (gap between -0.3 and -1.0 C), so the market's +0.52 is the market correcting
past the model, as at Munich. ICON's rounded degree hits on 5 or fewer of 17 in each city.
Stated p 0.5. Blind to every forecast value here.

## Run
`python3 -I /Users/triton/PROTEUS/experiments/2026-11-18-P-0485/icon.py` (keyless: Open-Meteo
previous-runs, Iowa State METAR archive; four requests).

## Result
17 days at each station. Truth is the market's resolved bucket; the METAR day high from the Iowa
archive matched that bucket on all 34 station-days (largest difference 0.0), so the truth is sound.

| | London City (EGLC) | Le Bourget (LFPB) |
|---|---|---|
| ICON lead-1, mean absolute error | 0.69 C | 0.87 C |
| Market at 09Z, mean absolute error | 0.47 C | 0.65 C |
| ICON bias (truth minus forecast) | +0.05 C | -0.39 C |
| ICON on low-cloud mornings | +0.66 C (8 days) | -0.55 C (2 days) |
| ICON on other mornings | -0.50 C (9 days) | -0.37 C (15 days) |
| ICON gap | +1.16 C | -0.18 C |
| Market gap (P-0484) | +0.52 C | +0.34 C |
| ICON's rounded degree right | 6 of 17 | 7 of 17 |
| Market favourite right | 11 of 17 | 7 of 17 |

- **At London City the low-cloud miss runs the other way.** ICON was 0.66 C too cold on the 8
  low-cloud mornings and 0.50 C too warm on the other 9, a gap of +1.16 C. At Munich over a year
  the same flag marked ICON 1.07 C too warm (P-0446). So the flag is not one effect that travels:
  at a riverside airport in a mild, cloudy fortnight, low cloud went with days that ended warmer
  than forecast. I do not know why, and 8 against 9 days in one month could be one weather pattern.
- **The market closes about half of it.** Its gap is +0.52 C where the model's is +1.16 C, the
  same shape as Munich (market -0.24 against model -1.07): by 09Z the price has taken most but not
  all of the model's conditional error out.
- **The market beats the raw model at both stations**, by about 0.2 C of mean absolute error. In
  London its favourite is right nearly twice as often as ICON's rounded degree (11 against 6). In
  Paris they tie at 7, so the Paris price is adding less.

Shot: verdict hit; market better than ICON at both hit, though ICON's error was 0.69 and 0.87, not
the 1.0 I called. The London gap missed on sign (+1.16 against a called -0.3 to -1.0). Degree hits
"5 or fewer" missed in both (6 and 7).

Caveats: 17 days, one month. The market price is at 09Z with the morning's observations in it and
the ICON figure is from the day before, so this is not a fair race; it measures how much is left
for a night-before forecaster to find. Airport point coordinates, UTC day against the market's
local day (same in London, one hour off in Paris). No permutation test: with 8 and 9 days it would
say little.

Next: close for now. Worth re-running at the end of November on 30 days, and only then deciding
whether London City's sign is real.
