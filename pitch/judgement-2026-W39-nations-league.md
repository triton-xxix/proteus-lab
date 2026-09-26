# Judgement book: Nations League, 27 Sep to 1 Oct 2026

Committed 2026-09-26T20:10:15Z, before the first kickoff (27 Sep 13:00 UTC). Luke asked on 26 Sep why the Pitch
ignores internationals and whether calls can be made without years of history. This is the answer:
24 fixtures called on judgement, not on a model. Every number is mine and every one is checkable
against the closing line and the result. It is a separate book from the v0 Dixon-Coles ledger and
does not touch the pass marks or the review clock.

What went into each call: the market (UK books on The Odds API, overround removed, averaged),
world Elo ratings from eloratings.net as a sanity anchor (`sandbox/elo_world_2026-09-26.tsv`), and
what I know about squads, managers and style up to mid 2026. What I do not know: the 2026 World Cup
result, or which coaches changed after it. Where that matters I have said so in the note.

The four games on 26 Sep (England v Spain among them) kicked off before this was written and are
left out on purpose.

## Calls

Market and mine are P(home) / P(draw) / P(away). Over is P(over 2.5 goals), market then mine.

| Kickoff (UTC) | Fixture | Market | Mine | Over 2.5 | Call |
|---|---|---|---|---|---|
| 09-27 13:00 | Lithuania v Azerbaijan | 0.39 / 0.31 / 0.30 | 0.38 / 0.31 / 0.31 | 0.38 v 0.38 | no view |
| 09-27 16:00 | Gibraltar v Andorra | 0.26 / 0.34 / 0.40 | 0.25 / 0.35 / 0.40 | 0.30 v 0.25 | under 2.5 |
| 09-27 16:00 | Austria v Kosovo | 0.61 / 0.22 / 0.16 | 0.54 / 0.26 / 0.20 | 0.54 v 0.50 | draw or Kosovo (double chance) |
| 09-27 16:00 | Denmark v Wales | 0.65 / 0.21 / 0.14 | 0.55 / 0.26 / 0.19 | 0.54 v 0.50 | Wales or draw (double chance) |
| 09-27 16:00 | Serbia v Netherlands | 0.13 / 0.20 / 0.67 | 0.14 / 0.22 / 0.64 | 0.58 v 0.55 | Netherlands win |
| 09-27 18:45 | Germany v Greece | 0.68 / 0.19 / 0.14 | 0.60 / 0.23 / 0.17 | 0.63 v 0.52 | under 2.5 |
| 09-27 18:45 | Israel v Republic of Ireland | 0.37 / 0.29 / 0.34 | 0.33 / 0.29 / 0.38 | 0.44 v 0.40 | Ireland win, under 2.5 |
| 09-27 18:45 | Norway v Portugal | 0.38 / 0.25 / 0.36 | 0.44 / 0.24 / 0.32 | 0.63 v 0.66 | Norway win, over 2.5 |
| 09-28 16:00 | Armenia v Montenegro | 0.35 / 0.30 / 0.35 | 0.33 / 0.30 / 0.37 | 0.43 v 0.42 | no view |
| 09-28 16:00 | Latvia v Cyprus | 0.36 / 0.30 / 0.34 | 0.36 / 0.31 / 0.33 | 0.43 v 0.40 | no view |
| 09-28 16:00 | Georgia v Ukraine | 0.36 / 0.29 / 0.36 | 0.33 / 0.28 / 0.39 | 0.45 v 0.47 | Ukraine win |
| 09-28 18:45 | Belgium v France | 0.26 / 0.24 / 0.50 | 0.32 / 0.26 / 0.42 | 0.63 v 0.62 | Belgium or draw (double chance), both teams to score |
| 09-28 18:45 | Romania v Bosnia & Herzegovina | 0.44 / 0.28 / 0.28 | 0.40 / 0.29 / 0.31 | 0.47 v 0.45 | draw |
| 09-28 18:45 | Northern Ireland v Hungary | 0.35 / 0.31 / 0.34 | 0.38 / 0.30 / 0.32 | 0.37 v 0.36 | Northern Ireland win, under 2.5 |
| 09-28 18:45 | Turkey v Italy | 0.35 / 0.27 / 0.38 | 0.40 / 0.27 / 0.33 | 0.53 v 0.55 | Turkey win |
| 09-28 18:45 | Sweden v Poland | 0.49 / 0.26 / 0.26 | 0.50 / 0.25 / 0.25 | 0.55 v 0.58 | Sweden win, over 2.5 |
| 09-29 18:45 | Spain v Croatia | 0.76 / 0.15 / 0.08 | 0.75 / 0.16 / 0.09 | 0.60 v 0.62 | Spain win to nil |
| 09-29 18:45 | Czech Republic v England | 0.14 / 0.21 / 0.65 | 0.15 / 0.23 / 0.62 | 0.55 v 0.50 | England win, under 2.5 |
| 09-29 18:45 | Slovenia v North Macedonia | 0.55 / 0.26 / 0.18 | 0.52 / 0.28 / 0.20 | 0.44 v 0.36 | under 2.5 |
| 09-29 18:45 | Scotland v Switzerland | 0.27 / 0.28 / 0.45 | 0.32 / 0.28 / 0.40 | 0.48 v 0.45 | Scotland or draw (double chance) |
| 10-01 18:45 | Denmark v Portugal | 0.27 / 0.28 / 0.45 | 0.32 / 0.27 / 0.41 | 0.48 v 0.50 | Denmark or draw (double chance) |
| 10-01 18:45 | Germany v Serbia | 0.71 / 0.17 / 0.11 | 0.70 / 0.18 / 0.12 | 0.65 v 0.62 | Germany win |
| 10-01 18:45 | Greece v Netherlands | 0.26 / 0.27 / 0.47 | 0.30 / 0.27 / 0.43 | 0.52 v 0.50 | Greece or draw (double chance) |
| 10-01 18:45 | Wales v Norway | 0.26 / 0.24 / 0.50 | 0.27 / 0.25 / 0.48 | 0.55 v 0.58 | over 2.5 |

## Why

- **Lithuania v Azerbaijan.** Bottom tier, market is as good as I am.
- **Gibraltar v Andorra.** Two sides that barely score; the market already has over at 0.30 and I would go lower still.
- **Austria v Kosovo.** Kosovo beat Sweden and Slovenia in qualifying and are still climbing; Rangnick's Austria are good but this is priced like a stroll.
- **Denmark v Wales.** Bellamy's Wales are hard to break down; Denmark at 0.65 is a legacy price for a side that has gone backwards. Under 2.5 too.
- **Serbia v Netherlands.** Agree with the market. Serbia are a mess since Stojkovic left; Belgrade noise is worth a little, not much.
- **Germany v Greece.** Greece under Jovanovic are organised and rising, Germany's rating has gone nowhere in a year. Germany still win most often, but 0.68 and over at 0.63 both look a touch rich.
- **Israel v Republic of Ireland.** Neutral venue, so no real home edge. Hallgrimsson's Ireland are the better organised side and Israel leak goals to decent teams.
- **Norway v Portugal.** Haaland, Sorloth and Nusa at home; Norway's rating has risen faster than anyone's. Portugal are better on paper and worse in September. Haaland anytime scorer is the obvious side market.
- **Armenia v Montenegro.** Coin flip on a small sample. Pass.
- **Latvia v Cyprus.** Pass.
- **Georgia v Ukraine.** Ukraine are on the way up and Georgia have drifted since Euro 2024; Kvaratskhelia alone does not carry a side at this level.
- **Belgium v France.** Belgium's rating is up almost 100 in a year and France's is down 40; France are also in their first window after a change of coach, and post-tournament Septembers are where favourites get caught.
- **Romania v Bosnia & Herzegovina.** Bosnia had the better of Romania in qualifying; two cagey sides. Under 2.5 as well.
- **Northern Ireland v Hungary.** Windsor Park, a young side that keeps improving, against a Hungary still bruised from losing their World Cup place in stoppage time. Low-scoring either way.
- **Turkey v Italy.** Montella's Turkey at home with Guler and Yildiz against an Italy in transition. The market makes Italy favourites on the badge.
- **Sweden v Poland.** Isak and Gyokeres against an ageing Poland. Agree with the market on the result; the goals angle is the one I like.
- **Spain v Croatia.** Spain are the best side in the world by a distance and Croatia's core is past 35. Spain took Croatia 3-0 at the Euros. No edge on the result, the angle is the clean sheet.
- **Czech Republic v England.** England win these, usually without much noise. The Czechs have been unsettled since sacking Hasek. Slightly below market on England because it is Prague and the window after a tournament.
- **Slovenia v North Macedonia.** Slovenia games are low-scoring by habit: Oblak behind a deep block, Sesko the one outlet. Market has over at 0.44, I would be well under that.
- **Scotland v Switzerland.** Hampden, a Scotland side that qualified for the World Cup and plays above its rating at home. Switzerland are the better team but 0.45 away here is generous.
- **Denmark v Portugal.** Denmark beat Portugal 1-0 in Copenhagen in March 2025 and Portugal do not travel well in these. Priced at 0.27, I have Denmark nearer a third.
- **Germany v Serbia.** Agree with the market. Nothing to add.
- **Greece v Netherlands.** Athens is a hard place to visit and Greece are the most improved side in the group. Netherlands still favourites, but 0.47 away is thin.
- **Wales v Norway.** Agree with Norway favourites. Cardiff will not stop Haaland but Wales will score; goals is the angle.

## How it gets scored

`pitch/JUDGEMENT.csv` holds the same rows. When results land, each row gets a Brier score for my
probabilities and for the market's, on the same matches, and the note gets a table: how many calls
landed, paired Brier (mine minus market), and a replay of the calls as £10 flat stakes at the
closing price. If the market beats me, that is the finding and it is published the same way.
