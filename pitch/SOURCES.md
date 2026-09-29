# Where the Pitch gets its information

Written 2026-09-29 because Luke asked. Every source the desk and the judgement book actually use,
what each gives, how fresh it is, and what it is bad at. Then what is missing. Anything not on this
list did not go into a call. Keys now come from the PROTEUS vault in 1Password through `bin/secrets.py`
(service account), so a scheduled run does not wait on the desktop app.

## Used now

| Source | What it gives | Key | Freshness | Weak spots |
|---|---|---|---|---|
| The Odds API, events endpoint | Upcoming fixtures and kickoff times, no prices. Free of quota. | 1Password "The Odds API" | Live | Nations League only so far (one sport key per competition; club competitions exist on it too) |
| The Odds API, odds endpoint | 1X2 and over/under 2.5 from about eleven UK books. I strip each book's margin and average. This is "the market" in every table. | same | Live, one request per pull, 500 a month free | It is the pre-match price at the moment I pull, not the true closing line. No corners, cards or scorers on the free tier. |
| eloratings.net | World Elo ratings for every national side (`World.tsv`), results within hours of full time (`latest.tsv`), team names (`en.teams.tsv`). This is also the results feed the scorer uses. | none | Ratings and results updated same day | Elo is results only: no lineups, no injuries, no xG. The trend columns in the file are unlabelled and I have read them as one-year change without verifying the header. Codes are not ISO (NI is Nicaragua), so match by name. |
| football-data.co.uk | Club results, xG, opening and closing odds for nine leagues back to 2022. The model desk runs on it. | none | Weekly | Club only, no internationals. Fixture file only carries the next round. |
| fixturedownload.com | Club fixtures for the whole season, no odds. Fallback for the model desk. | none | Season | Club only |
| `pitch/brief.py`, before any blind call | One block per team: current head coach from the Wikipedia infobox, Elo and world rank, last six results with scores from eloratings.net. Keyless. Written 2026-09-29 after the Germany mistake; the same run showed Belgium are under Mark van Bommel, not Rudi Garcia as I had assumed. | none | Live; Wikipedia allows about twenty quick calls then 429s, so the script paces itself | Coach only, no squad or injuries. Wikipedia infoboxes lag a day or two after an appointment. |
| Web search, per team, before any blind call | Current manager, notable absences, last result. Three searches and a page read took under a minute on 29 Sep and corrected a fact I had wrong with confidence (Germany: Klopp since 15 Aug 2026, not Nagelsmann). | none | Live | Done by hand at call time, not scripted yet; must happen before the blind numbers are written, never after the price. |
| SportsGameOdds API (PROTEUS vault) | Odds with corners, both teams to score, first and last scorer, assists, per bookmaker with open and close. Amateur tier: 10 requests a minute, 50k an hour. | 1Password PROTEUS vault | Live | Soccer coverage on this tier is Champions League and MLS only, so nothing for internationals or the nine leagues the model desk runs. No cards. Worth it for a Champions League corners book, not for the Pitch as it stands. |
| My own knowledge to mid 2026 | Squads, managers, style, recent form, venues (Israel and Belarus play on neutral ground). | n/a | Stale: nothing after roughly June 2026, so I do not know the World Cup result or the coaching changes after it | This is where most of the losing calls came from. Stories about momentum and managers that the price had already discounted. |

## Not used yet, in the order I would add them

1. **Named squads and probable lineups.** UEFA publishes squad lists; FotMob and Sofascore carry
   probable and confirmed lineups an hour before kickoff. Post-tournament windows are rotation
   windows and a rating means little if the first eleven is not playing.
2. **Whether the game matters.** Group tables and qualification state, from UEFA. A dead rubber
   is a different fixture.
3. **International xG.** FBref covers the Nations League and qualifiers. Turns "Slovenia are low
   scoring" from memory into a number.
4. **Line movement.** Opening price to closing price. The Odds API historical endpoint costs
   quota; Oddsportal shows it on the page. If the market moves toward my lean before kickoff, that
   is evidence I was early rather than wrong.
5. **Head-to-head and venue records** from eloratings.net's own match archive, which is keyless.
6. **Corners, cards and scorers.** No keyless source found for internationals. Those markets stay
   off the table until one appears.

## What I do not use, on purpose

Tipster sites, social media form guides, and anything that will not show its inputs. If a source
cannot be checked, its opinion is not information.
