# P-0058: is the Pitch's results feed stuck at 20 Sep?

Raised on 2 Oct and again tonight: every model prints "as of 2026-09-20", `score.py` scored 0 of 0.

## Measured (`check_results.py`, `check_played.py`, `results.json`, `played.json`)

- `as_of` in `pitch/model.py` is simply the latest result date in the data, not a frozen setting.
- All nine 2026-27 files, cached and live from football-data.co.uk, end on 20 Sep and match row for
  row (E0 50, E1 95, SP1 69, D1 36, I1 50, F1 45, N1 63, P1 62, SC0 42). Live `Last-Modified` is
  21 Sep 17:50 GMT on all of them.
- fixturedownload (refreshed tonight) has no E0 or E1 match after 21 Sep with a score, and the first
  unplayed Premier League match is number 51, round 6, on 10 Oct. 50 matches is exactly five rounds.
- `PREDICTIONS.csv` has no row after 20 Sep waiting for a result.

## Verdict

Works: the feed is not stuck. There has been no league football in these competitions since 20 Sep
(an international window), so nothing is missing and nothing is unscored. The first real test of the
refresh is the weekend of 10 Oct: if `as_of` has not moved past 9 Oct by the 13 Oct nightly, that is a
real fault.
