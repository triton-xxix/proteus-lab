# Skool survey 3, 7 Oct 2026: the best trading group

Luke asked for the best trading group on Skool and said he would join it. Goal line: trading is
one of his eleven areas, and nothing covers it except the Grinder's meme coins. What I make from it:
replicate published strategies on free daily data, then paper-track the ones that hold up,
committed before the open and scored in public like the other desks.

Method: 60 trading queries on the discovery page (`__NEXT_DATA__`, keyless) returned 1,003 unique
groups, 744 of them trading or investing. I cut the ones that sell signals, copy trading or
prop-firm challenge passes, the ones that teach discretionary chart reading I cannot test, and the
ones not in English. That left 29 about pages, which I read for reviews, activity and owner.

## Pick: Rule-Based Trading (`rulebasedtrading`), $99 a year, about £75

- **Owner:** Oddmund Grøtte, founder of QuantifiedStrategies.com, trading full time since 2001.
  He has the longest public record of any owner on this list.
- **Product:** one new backtested strategy every trading day. Each comes with explicit rules and
  20 to 30 years of results, mostly on end-of-day prices. Free daily data is enough to check it.
  789 lessons across 22 courses.
- **Why it fits:** every item is a claim I can falsify. A course only teaches me. This hands me a
  daily queue of things to test, which is how I already work.
- **Standard tier is enough.** Platform code (Python among six) is in the premium tier. I would
  rather write my own from the rules, because an independent replication is the point.
- **Reviews, 3.7 from 3.** Two paying members gave it 5 stars. One gave it 1 star and cancelled
  after four days. That member said the rules were loose ("exit on strength"), only about a fifth of
  the strategies were visible, and the rest unlocked through likes in a quiet group. The about page
  now says nothing paid for is locked behind levels. That conflict is the first thing to check.
- **Activity:** 364 members, 377 posts since April, 7 online when I looked. Quiet.

**Kill rule:** in week one, count the strategies visible at level 1 and try to code the first ten
from their rules alone. If fewer than half the library is visible, or three of the ten are too
vague to code, cancel and log the loss. Not grinding likes on Luke's profile.

**Test:** my backtest set against the published figures for each strategy. Count how many I
reproduce within a stated tolerance. The ones that replicate go on paper, forward, against buy and
hold. "Would I pay again" verdict at the year-end renewal.

## Runner-up: Quant Rick's trading academy (`quant-rick`), $41 a month

He teaches method, not strategies: factor investing, a Python backtest framework, and review of
members' code for lookahead bias and inflated Sharpe ratios. 5.0 from 10 reviews, all from paying
members, and the owner is active. Dropped on 7 Oct only because I had stretched it onto the
football model. For trading it is the better teacher. It is also four times the price, and the
owner is anonymous, so the "ex-macro quant" claim cannot be checked.

## Looked at and left

- **Algo Trading** (free, 3,705, 1,276 posts): the biggest English algo group. No reviews and no
  way to judge the owner's record. It was in the 29 Sep list. Fine as a free extra.
- **AI & Automated Trading** (DaviddTech, $49/mo, 5.0 from 6): 400+ no-code TradingView strategies
  sold around his own backtester. The reviews praise support, not results.
- **AI Pathways** ($149/mo): over budget, and its value list adds up to "$10,000".
- **Part-Time Quant Academy** ($29/mo): leads with a "180X in 3 years" claim and opened on 2 Sep.
- **Prediction Market Value** ($49/mo, 5.0 from 3): about Kalshi and Polymarket, not markets
  trading, and open since July. Worth a look for P-0079, not here.
- **Volpro, Tom Camp, Trading Bootcamp, The Vault, Trading Tribe:** large and active, well reviewed,
  but discretionary day trading. I cannot replicate it and would only be watching.

## Spend

Nothing yet. The join and the card are Luke's. The free strategies on QuantifiedStrategies.com
can start the replication before the group does.

## Revised the same night: YouTube, not Skool

Luke was not convinced by a group with three reviews, and said good people are on YouTube for
free. He was right, and I should have checked that first: the Quantified Strategies YouTube
channel (34.7k subscribers, 661 videos) is the same two people, Grøtte and Samuelsson, posting
several backtested strategies a day. The paid group mostly adds the library and the Q&A.

Method: 15 channel searches (keyless results page) found 246 channels. I added a seed list I already
knew, then read the latest uploads of 29.

Follow, all free:

| Channel | Subs | Why |
|---|---|---|
| Kevin Davey (`@AlgoTradingWithKevinDavey`) | 26.5k | Checkable record: World Cup Championship of Futures Trading, 2nd 2005 (148%), 1st 2006 (107%), 2nd 2007 (112%), real money. Teaches walk-forward and Monte Carlo testing, posts his live portfolio. Weekly |
| neurotrader (`@neurotrader888`) | 68.4k | The test I hold everything else to. His permutation-test video (580k views) shows how to tell an edge from data mining; the code is public (`neurotrader888/mcpt`, 425 stars). Quiet for a year, but that one video is the method |
| Quantified Strategies (`@QuantifiedStrategies`) | 34.7k | The Skool group's content, free. Every video is a stated rule set with a backtest, so a ready queue of claims |
| Algovibes (`@Algovibes`) | 133k | Python, and he tries to break strategies rather than sell them ("Then I tried to destroy it", "I traded the exact opposite of YouTube gurus"). Several a week |
| StatOasis, Ali Casey (`@StatOasis`) | 23.8k | Evidence-first: one recent video has 70,000 Monte Carlo runs saying yes and a walk-forward matrix saying no. Active |
| Top Traders Unplugged (`@TopTradersUnplugged`) | 39.4k | Interviews with people who run real trend-following funds. Background on how professionals do it, not strategies to copy |

Left: Trading Rush (352k, win rates from 100 hand-counted trades, no costs), Trading Strategy
Testing (914k, now prop-firm and price-action content), Algo-trading with Saleh (headline Sharpe
ratios from LLM-built strategies), CodeTradingCafe (good Python, but the titles lean on AI hype),
QuantPy (quiet for seven months), Quant Guild (quant maths and careers, not trading).

Queued **P-0082**: five strategy videos (three Quantified Strategies, two Kevin Davey). For each,
write the rules from the transcript, rebuild the backtest on free daily data and run the
permutation test. Report their figure against mine and the p-value. No account, no money, no click
from Luke. Rule-Based Trading stays parked. If the free channel's strategies replicate well and I
want the deeper library, that is the case for paying, made with numbers.
