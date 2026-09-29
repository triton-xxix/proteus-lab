# P-0036: SportsGameOdds API, amateur tier, soccer coverage

Run 2026-09-29 00:20 UTC, interactively, key read through `bin/secrets.py` from the PROTEUS vault.

- `/v2/account/usage`: tier `amateur`, 10 requests a minute, 50,000 an hour, 500,000 a day; entities 250k an hour.
- `/v2/leagues/`: 8 leagues on the tier, 2 soccer: `UEFA_CHAMPIONS_LEAGUE` and `MLS`. `UEFA_NATIONS_LEAGUE` returns 400.
- `/v2/events/?leagueID=UEFA_CHAMPIONS_LEAGUE&oddsAvailable=true`: RC Lens v Sporting CP (13 Oct) carries 476 odd ids across stat types assists, bothTeamsScored, cornerKicks, firstToScore, goals+assists, lastToScore, points. No cards.
- Verdict: works, but not for the Pitch as it stands (internationals and the nine club leagues are not on the tier). Corners and scorer markets exist for the Champions League, which is the first keyed source of those I have found.
