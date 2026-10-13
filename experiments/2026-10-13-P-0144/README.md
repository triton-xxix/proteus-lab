# P-0144: does distance and angle alone reach held-out AUC above 0.75 on StatsBomb open data?

No. **0.735** on World Cup 2022 (1,099 non-penalty shots, 116 goals, 50 matches) and **0.701** on
Euro 2024 (1,304 shots, 98 goals, 51 matches), five-fold cross-validation split by match. Called shot
was works at 0.70 with AUC about 0.78: the probe ran, the number missed.

## Method

`xg.py`, numpy only (no scikit-learn in the venv). Events pulled keyless from the public StatsBomb
open-data repository on raw.githubusercontent.com, one file per match, 0.3 s apart. Shots of type
Shot, penalties excluded. Distance to the goal centre and the angle the 8-yard goal mouth subtends at
the shot, from StatsBomb's 120 by 80 pitch. Logistic regression by Newton steps with a tiny ridge,
folds assigned by match id, AUC from the rank statistic on out-of-fold probabilities. A third run
adds a header flag. StatsBomb's own `statsbomb_xg` is scored on the same shots as the reference.

## Numbers

| Sample | Shots | Goals | Distance + angle | + header | StatsBomb xG |
|---|---|---|---|---|---|
| World Cup 2022, 50 matches | 1,099 | 116 | 0.735 | 0.758 | 0.822 |
| Euro 2024, 51 matches | 1,304 | 98 | 0.701 | 0.735 | 0.787 |

Full-fit coefficients (World Cup): intercept -1.48, distance -0.083 per yard, angle +1.15 per radian.

## What it says

- The two-feature baseline the video builds is real but sits below 0.75 on tournament data at this
  sample size; a header flag adds about 0.03 and StatsBomb's full model another 0.05 to 0.06.
- Around 100 goals per sample, the AUC standard error is roughly 0.025, so the two tournaments
  agree within noise and neither is a fluke above the line.
- Tournament football is a hard case: few goals, many low-quality shots from distance. A club
  season with thousands of shots would narrow the error bar but is not in the open data at this scale.
- For the Pitch desk: xG from open data could only cover the competitions StatsBomb releases, none
  of which are the nine leagues the desk predicts, so it does not feed the Dixon-Coles model.

## Not done

- No log loss or calibration curve, no team xG v real goals comparison.
- No club-league sample (open data has Arsenal 2003-04 and some Bundesliga, La Liga Messi seasons;
  not pulled tonight).
