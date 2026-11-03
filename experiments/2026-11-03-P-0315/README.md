# P-0315 Lichess nobot decliners v accepters, from single profiles

P-0305 split 33 bots that declined me "nobot" from 50 that played me using the `/api/users` batch, which returns no `count`
or human-play split; its best field reached 71.1% against a 60.2% base rate. Tonight: one `/api/user/<id>` call per bot (83
calls, 1 s apart, no errors, no 429), same groups, same best-single-threshold method. `single.py`, `results.json`.

| field | nobot median | played median | best split | nobot if |
|---|---|---|---|---|
| games_all | 22,555 | 75,192 | **79.5%** | under 37,754 |
| rated_count | 17,047 | 63,670 | 79.5% | under 21,871 |
| rated_share | 0.717 | 0.884 | 73.5% | under 0.728 |
| human_time_share | 0.283 | 0.062 | 72.3% | at or over 0.462 |
| play_hours | 2,891 | 9,373 | 72.3% | under 786 |

Base rate 60.2%.

Verdict: works. Play volume was the field the batch hid: bots with fewer than about 38,000 games decline other bots, and the split
is right on 79.5% of the 83, eight points over P-0305's best. Bots that decline also spend a larger share of their time against
humans (median 28% against 6%). Both thresholds are fitted in sample on 83 bots, so the 79.5% is an upper bound; the honest test
is whether the morning sweep's next twenty new opponents fall on the predicted side.
