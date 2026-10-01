# P-0046: xG from scratch on StatsBomb open data

Ran 1 Oct 2026, keyless (raw GitHub). World Cup 2022 and Euro 2024, 115 matches, 2,734 non-penalty
shots. Split by match, a third held out (843 shots, 78 goals). Script `xg.py`, numbers `result.json`.

| Model (test set) | Log loss | Brier |
|---|---|---|
| Constant (train goal rate 9.1%) | 0.3084 | 0.0840 |
| Logistic, distance and angle | 0.2804 | 0.0778 |
| Logistic, distance, angle, header | 0.2678 | 0.0741 |
| StatsBomb's own xG | 0.2493 | 0.0688 |

Answer to the probe question: yes. Two geometric features take 47 percent of the log-loss gap
between a constant and StatsBomb's model; adding one header flag takes 69 percent. The rest is
what StatsBomb pays for: defender positions, goalkeeper position, shot technique.

Caveats: one seed, tournament football only, 843 test shots. Not a Pitch input yet; the Pitch
desk models goals, not shots, and the open data has no Premier League season after 2015/16.
