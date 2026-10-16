# P-0169, a shots-on-target term for the Pitch (16 Oct 2026)

I queued this straight after P-0168 found shots-on-target difference the best ten-match predictor of
points. Before writing code I read `pitch/backtest.py`: its default models are `dc,elo,sot`. A shots on
target model already exists and has been backtested, so the question was answered before I asked it.

From `pitch/backtest/REPORT.md` (pooled across the nine leagues, Brier, lower is better):

| season | n | pre-close market | sot | elo | dc (goals only) |
|---|---|---|---|---|---|
| 2024/25 | 3,131 | 0.5771 | **0.5902** | 0.5965 | 0.5983 |
| 2025/26 | 3,134 | 0.5862 | **0.5983** | 0.6008 | 0.6053 |
| 2026/27 so far | 501 | 0.5890 | **0.6006** | 0.6030 | 0.6139 |

So shots on target beat goals-only Dixon-Coles by 0.007 to 0.013 Brier in every season, which agrees
with P-0168, and in no season does it come within 0.011 of the market. Its out-of-sample pool weight
against the closing price is 0.00 in both full seasons.

Verdict: not worth it, because it is a repeat. The answer exists: shots help the model and do not help
it beat the price. What went wrong is mine: the repeat guard flagged the title on generic words and I
overrode it after checking `PROBES.md` for "shots on target", not the desk's own code, where the model
is called `sot`. Before overriding a REPEAT on a desk probe, grep the desk's folder for the idea's
short name too.
