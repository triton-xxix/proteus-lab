# P-0343: rolling shots on target against rolling goals

Question: does a team's last-10 shots on target predict its next-match goals better than its last-10 goals?

Method: nine leagues from `pitch/cache/`, seasons 2022-23 to 2025-26, one row per team per match, last 10 matches
in the same season with no leakage. OLS with a home flag, fitted on 13,950 rows before 1 Jul 2025, tested on
4,608 rows of 2025-26. `xg_proxy.py`, `results.json`.

| Model | Test MSE | Skill over home-only |
|---|---|---|
| Home only | 1.3965 | 0 |
| Rolling goals | 1.3139 | 5.91% |
| Rolling shots | 1.3066 | 6.43% |
| Rolling shots on target | 1.3001 | 6.90% |
| Goals + shots on target | 1.2954 | 7.24% |

Goals minus shots on target: 0.0138 MSE, 1.05% of the goals model's error, se 0.0067, bootstrap 90% range 0.0035
to 0.0249. Shots on target wins in 7 of 9 leagues; Bundesliga and Eredivisie go the other way.

Mostly a repeat, found only after running it: P-0168 (16 Oct) had shots on target beating goal difference on
next-10 points, and P-0169 found `pitch/backtest.py` already runs a shots-on-target model that beats goals-only
every season and never the market. This adds a next-match figure and nothing the desk can use. The repeat guard
let the title through because the harvest worded it "xG proxy".

Caveats: one test season. The two rows of a match are treated as independent, so the se is slightly too small.
No opponent strength. This compares two rolling numbers; it is not a test against the Pitch model or the market.
