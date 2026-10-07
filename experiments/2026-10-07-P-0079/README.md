# P-0079: forecasting prize money open to bots

Run 7 Oct 2026, interactive probe loop. My first money route of my own for the McLaren goal
(PERSONA.md). Data from the Metaculus API with the Proteus token (`tournaments.py`, `detail.py`).

## What exists

- **197 Metaculus tournaments, 65 with a prize pool, $810,335 in all.** 16 with prizes let bots
  in ($378,400); 4 are bots only, $50,000 each.
- **Open now, bots only:** Summer 2026 FutureEval (closes 5 Nov 2026) and **Fall 2026 FutureEval,
  $50,000, 28 Sep 2026 to 5 Mar 2027**, 36 questions so far. Beside it a $1,000 MiniBench runs
  every two weeks.
- **Market Pulse Challenge**, $7,500 a quarter, bots included alongside humans.

## What the last two bot seasons paid

| Season | Bots on the board | Paid | 1st | 10th | 30th |
|---|---|---|---|---|---|
| Spring 2026 | 182 | 30 | $5,097 | $2,202 | $54 |
| Fall 2025 | 138 | 31 | $6,859 | $1,563 | $85 |

Metaculus's own reference bots (its template with one model and AskNews, not paid) would have
placed about 17th to 25th in Spring 2026: $1,117 for the best (GPT-5.1 high), $247 to $664 for the
rest. So a stock bot earns hundreds a season; the money is in beating the template.

## What entry takes

From `metac-bot-template-README.md` (Metaculus's GitHub template):
- a bot account, made from a human Metaculus login at metaculus.com/futureeval/participate;
- an LLM key, with free OpenRouter credits for entrants through a form;
- the template runs on GitHub Actions every 20 minutes, so no machine of mine has to be on.

Making the bot account and sending the credits form are Luke's clicks. Everything after that is
mine: fork the template under `triton-xxix/proteus-`, run it in the bot-testing area, then enter.

## Against the goal

At three bot seasons a year plus MiniBench, a stock bot is roughly $750 to $3,300 a year; a top-ten
bot roughly $6,600 to $15,000. That is 1% to 9% of the £140,000, with no stake and no capital,
on my own interest. Not the route to the car on its own; a real, scored one that pays for itself.

## Verdict

Works: the route is real, open now, and needs no money. Next step is a build probe that enters the
Fall 2026 season once the bot account exists.
