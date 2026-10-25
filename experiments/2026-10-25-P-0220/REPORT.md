# P-0220: xG from scratch on StatsBomb open data

Question: does a two-feature logistic model (distance to goal centre, angle of the goal mouth) beat the base-rate log loss on held-out shots?

Data: StatsBomb open data, World Cup 2022, all 64 matches, 1,430 non-penalty shots, fetched keyless from raw.githubusercontent.com. Train on the first 44 matches by date (953 shots), test on the last 20 (477 shots, 54 goals). `xg.py`, numbers in `results.json`.

| On the 477 test shots | Log loss |
|---|---|
| Base rate (10.3% for every shot) | 0.354 |
| My distance and angle model | 0.309 |
| StatsBomb's own xG | 0.277 |

So yes: two geometric features recover about 59% of the gap between knowing nothing and StatsBomb's model ((0.354 minus 0.309) over (0.354 minus 0.277)). Summed xG on the test set: mine 48.2, StatsBomb 46.8, goals 54, so both under-read a knockout stage that finished well.

What StatsBomb has that I do not: body part, assist type, defender and keeper positions from the freeze frame. Those would be the next features; the freeze frame is in the same open files.

For the Pitch: the desk models goals from results, not shots, so this does not plug in tonight. It is a working, keyless xG baseline if the desk ever wants shot-level data.

Verdict: works.
