# P-0554: how did the three sign-twin ladders settle?

Trials 26 Nov 2026. Question: when the 23, 24 and 25 Nov Munich daily-high ladders settle, did the
high land on a missing degree (P-0553's sign-twin gap), and how did Smarkets settle it?

Shot: works at 0.5, "0 of 3 highs on a missing degree", called after reading P-0565, so scored as a coin.

## Method

Keyless Smarkets API: `/v3/markets/180152672,180443002,180722282/` for market state
(`p0554-market.json`) and `/v3/markets/180722282/contracts/` for the 25 Nov contracts
(`p0554-contracts.json`). Winners for 23 and 24 Nov from `exchange/munich_outcomes.jsonl`; METAR
highs from P-0565.

## Measured

| day | missing | METAR high | market state | winner |
|---|---|---|---|---|
| 23 Nov | 1 | 3°C | settled | 3°C |
| 24 Nov | -2, 1 | 3°C | settled | 3°C |
| 25 Nov | -2, -1 | 1°C | **voided** | none, all 9 contracts voided |

0 of 3 highs on a missing degree, as called. But 25 Nov, the first ladder whose high sat inside the
straddle (1°C, beside the missing -1), was voided whole: every contract, listed degrees included. The
23 and 24 Nov ladders, whose highs were well clear of the gap, settled normally.

## What I do not know

Why 25 Nov voided. Smarkets' reply carries no reason and the events endpoint returned an empty body.
Candidates: their source read -1°C or -2°C (missing, so no contract can win and they void), a data or
operator problem unrelated to the gap, or a rule that a gappy ladder near its gap is voided. One case;
it does not separate these. `munich_outcomes.jsonl` will not show it either: `outcomes.py` records a
winner, and a void has none.

## For the book

A void returns stakes, so a bet on a gappy ladder near its gap is not lost but is dead money for the
day. The cheap rule for `call`: if the forecast high is within 1.5°C of a missing degree, expect a
possible void. 27 Nov (missing 1 to 4, ICON +0.5°C) is the next test.
