# P-0039: Metaculus API with the vault token

## Verdict, written after the run (30 Sep 2026, scheduled nightly)

Works for access, not for the number that matters.

- The 1Password SDK read the token unattended in 2.0s. Last night `op` hung twice at the same
  step (P-0034). So the fix in `bin/secrets.py` holds in a scheduled run.
- Authenticated listing works: 100 open binary posts per call, HTTP 200 in about 2s.
- Community forecast was null on all 100, with and without `with_cp=true` (second pull saved in
  `with_cp.json`). Question 45810 in detail: 68 forecasters, 867 forecasts, `cp_reveal_time`
  29 Sep 17:00 UTC (already past), and still `recency_weighted.latest` null, history empty.
  Why the API withholds it from this token I do not know. Possibly an account-tier or
  forecast-first rule; unverified.
- Throttle: 429 on call 8 of a burst, 4.9s in, `Retry-After: 10`. The same limit P-0007 saw
  unauthenticated, so the token does not buy a higher rate.
- Football: `search=football` is a loose text match, not a filter. No match-level football
  questions; the nearest are England winning a major title before 2033 and Brazil by 2050.
  Nothing The Pitch could score against.

Without the community forecast, Metaculus gives the question list and nothing to benchmark against.
Next step, if any: check Metaculus's API docs interactively for how the aggregate is exposed.

## Script output

Vault listing: 9 items in 2.0s.
Items matching 'metaculus': ['MetaculusAPI Credentials']
Token read from field 'credential', length 40.

`/api/posts/` open binary, 100 by hotness: HTTP 200 in 2.00s. Rate headers: none
Returned 100 posts; total count reported None.
Community forecast present on 0 of 100.

Top 15 by hotness:

| id | title | closes | community p | forecasters |
|---|---|---|---|---|
| 45810 | Will Trump demolish the Kennedy Center before January 1, 2027? | 2026-12-15 | None | None |
| 45393 | Will a Space-domain AMC acting outside its mandate cause 100 deaths or $5bn in d | 2026-10-21 | None | None |
| 45812 | Will ChatGPT-type chatbots disappear before 2100? | 2099-12-21 | None | None |
| 45394 | Will a Space-domain AMC be employed in an irregular seizure or retention of powe | 2026-10-21 | None | None |
| 45407 | Will a Protection-domain AMO acting outside its mandate cause 100 deaths or $5bn | 2026-10-21 | None | None |
| 45399 | Will a Cognitive-domain AMC acting outside its mandate cause 100 deaths or $5bn  | 2026-10-21 | None | None |
| 45408 | Will a Protection-domain AMO be employed in an irregular seizure or retention of | 2026-10-21 | None | None |
| 45389 | Will a Land-domain AMC acting outside its mandate cause 100 deaths or $5bn in da | 2026-10-21 | None | None |
| 45395 | Will a Cyber-domain AMC acting outside its mandate cause 100 deaths or $5bn in d | 2026-10-21 | None | None |
| 45212 | Will an Air-domain AMC acting outside its mandate cause 100 deaths or $5bn in da | 2026-10-21 | None | None |
| 45213 | Will an Air-domain AMC be employed in an irregular seizure or retention of power | 2026-10-21 | None | None |
| 45391 | Will a Maritime-domain AMC acting outside its mandate cause 100 deaths or $5bn i | 2026-10-21 | None | None |
| 45397 | Will an Electromagnetic spectrum-domain AMC acting outside its mandate cause 100 | 2026-10-21 | None | None |
| 45401 | Will an Intelligence-domain AMO acting outside its mandate cause 100 deaths or $ | 2026-10-21 | None | None |
| 45403 | Will a Manoeuvre, fire, and effects domain AMO acting outside its mandate cause  | 2026-10-21 | None | None |

Search 'football' (open binary): HTTP 200 in 3.41s, 100 results. Keyword hits in the hotness 100: 1.

| id | title | closes | community p | forecasters |
|---|---|---|---|---|
| 45462 | Will the 2026 World Cup deliver the predicted economic boost to US host cities? | 2027-01-01 | None | None |
| 397 | Will RoboCup announce that robots have beaten professional human soccer players  | 2050-01-01 | None | None |
| 23749 | Will an anthropomorphic robot with artificial intelligence win in a football (so | 2034-12-30 | None | None |
| 7072 | Will there be an breakaway European Soccer League match before 2030? | 2030-01-01 | None | None |
| 21485 | Will there be a Super Bowl 100 before 2076? | 2076-01-01 | None | None |
| 6885 | Will the Tennis be part of the 2044 Summer Olympics? | 2044-01-02 | None | None |
| 41176 | Will the England national men's team win a major international football title be | 2033-01-01 | None | None |
| 19408 | Will Cooper Flagg make the Naismith Basketball Hall of Fame before 2060? | 2060-01-01 | None | None |
| 17325 | Will Major League Baseball (MLB) expand by 2030? | 2030-04-01 | None | None |
| 6903 | Will the WTA and ATP merge before 2031? | 2030-01-01 | None | None |
| 29284 | Will Cristiano Ronaldo play again for Manchester United? | 2030-01-01 | None | None |
| 7010 | Will mixed doubles be a fixture at all four slams in 2040? | 2038-01-01 | None | None |
| 21829 | Will an MLB pitcher who averages 91.0 mph or slower on his fastball win the Cy Y | 2036-03-01 | None | None |
| 8805 | Will the New York Yankees win the World Series in 2032 in exactly 6 games? | 2032-09-01 | None | None |
| 31191 | Will at least 80% of the population take part in cultural activities? | 2034-12-31 | None | None |
| 9751 | Will any jurisdiction adopt futarchy by 2070? | 2049-01-01 | None | None |
| 6462 | Will the use of whips be banned on or before the 2026 Melbourne Cup thoroughbred | 2026-11-08 | None | None |
| 3812 | Will Valve release a game before 2030 with 3 in the Title? | 2029-12-31 | None | None |
| 6197 | Will Brazil win the FIFA World Cup by the end of 2050? | 2050-12-29 | None | None |
| 43265 | Will any national military or state-affiliated armed forces deploy at least 5,00 | 2031-01-01 | None | None |
| 45408 | Will a Protection-domain AMO be employed in an irregular seizure or retention of | 2026-10-21 | None | None |
| 43730 | Will US federal agencies cease international arrival processing at any of the fo | 2026-12-31 | None | None |
| 24803 | Will Dwayne Johnson, The Rock, make a serious run for President of the United St | 2052-11-01 | None | None |
| 25349 | Will the Arizona Coyotes rejoin the NHL by 2029? | 2028-12-30 | None | None |
| 20118 | Will 20 million people follow a new, AI-created religion by the end of 2035? | 2035-12-31 | None | None |
| 4527 | Will the S&P 500 hit 10,000 points by the end of the decade? | 2030-01-01 | None | None |
| 45398 | Will an Electromagnetic spectrum-domain AMC be employed in an irregular seizure  | 2026-10-21 | None | None |
| 45404 | Will a Manoeuvre, fire, and effects-domain AMO be employed in an irregular seizu | 2026-10-21 | None | None |
| 45406 | Will an Information effects-domain AMO be employed in an irregular seizure or re | 2026-10-21 | None | None |
| 21928 | Will Bryan Caplan win his bet that he will not be mistreated by George Mason Uni | 2031-01-01 | None | None |
| 42827 | Will all of these New England comic con events be held during 2026? | 2026-11-06 | None | None |
| 45407 | Will a Protection-domain AMO acting outside its mandate cause 100 deaths or $5bn | 2026-10-21 | None | None |
| 6502 | Will JavaScript be the most used programming language in the 2030 Stack Overflow | 2030-01-31 | None | None |
| 17824 | Will a major automobile manufacturer offer a V8 platform in a personal vehicle i | 2042-01-01 | None | None |
| 45410 | Will a Sustainment-domain AMO be employed in an irregular seizure or retention o | 2026-10-21 | None | None |
| 45397 | Will an Electromagnetic spectrum-domain AMC acting outside its mandate cause 100 | 2026-10-21 | None | None |
| 20767 | Will the Detroit Pistons change their name by 2055? | 2055-01-01 | None | None |
| 21927 | Will Aidan Caplan win his bet that the Supreme Court will not be packed as of Ju | 2028-07-04 | None | None |
| 45390 | Will a Land-domain AMC be employed in an irregular seizure or retention of power | 2026-10-21 | None | None |
| 45405 | Will an Information effects-domain AMO acting outside its mandate cause 100 deat | 2026-10-21 | None | None |
| 21965 | Will Bryan Caplan win his bet that the global temperature will not rise more tha | 2030-01-01 | None | None |
| 4349 | Will the Harvard endowment be larger in 2119 than in 2019? | 2100-01-01 | None | None |
| 45666 | Will Manifold exist in 2050? | 2049-12-31 | None | None |
| 8725 | Will the peak 7-day average of COVID-19 cases OR CLI in Virginia during a summer | 2026-10-31 | None | None |
| 3397 | Will any OECD country achieve a 10% or greater reduction in the national rate of | 2030-01-01 | None | None |
| 3360 | Will ≥8% of U.S. adults self-report to follow a vegetarian diet before 2036? | 2034-01-01 | None | None |
| 44419 | Will any social-media account reach 1 billion followers before 2031? | 2030-01-01 | None | None |
| 41563 | Will the Insurrection Act or a state of martial law be declared in relation to t | 2027-01-21 | None | None |
| 19776 | Will Russell Rickford cease to be a faculty member of Cornell before 2030? | 2029-12-31 | None | None |
| 5875 | Will online poker be dead on January 1, 2031? | 2031-01-01 | None | None |
| 45396 | Will a Cyber-domain AMC be employed in an irregular seizure or retention of powe | 2026-10-21 | None | None |
| 21930 | Will Bryan Caplan win his bet that there will be no civil war in a European coun | 2045-12-31 | None | None |
| 45213 | Will an Air-domain AMC be employed in an irregular seizure or retention of power | 2026-10-21 | None | None |
| 44176 | Will the S&P 500 close at or above 8,000 on December 31, 2026? | 2026-12-31 | None | None |
| 45394 | Will a Space-domain AMC be employed in an irregular seizure or retention of powe | 2026-10-21 | None | None |
| 39258 | Will two new or substantially upgraded youth/teen-oriented facilities (such as c | 2027-12-15 | None | None |
| 5716 | Longbets series: will the amount of geologically-derived crude oil consumed by t | 2032-01-01 | None | None |
| 19918 | Will Andy Carlile's 7:10 BTG Nürburgring Nordschleife motorcycle laptime be beat | 2029-12-31 | None | None |
| 40925 | Does $100k to fund cultured meat development have a greater animal welfare benef | 2027-01-01 | None | None |
| 7054 | Will any top 10 global meat processor/producer go bankrupt before 2028? | 2027-12-31 | None | None |
| 45403 | Will a Manoeuvre, fire, and effects domain AMO acting outside its mandate cause  | 2026-10-21 | None | None |
| 45400 | Will a Cognitive-domain AMC be employed in an irregular seizure or retention of  | 2026-10-21 | None | None |
| 4319 | Longbets series: By 2040 will the percentage of college-aged U.S. citizens who a | 2040-01-01 | None | None |
| 17825 | Will a female driver win a NASCAR Cup Series race before 2050? | 2050-01-01 | None | None |
| 45402 | Will an Intelligence-domain AMO be employed in an irregular seizure or retention | 2026-10-21 | None | None |
| 15853 | Will carbon dioxide emissions from fossil fuels and industry exceed 20 gigatons  | 2050-12-31 | None | None |
| 17746 | Will carbon dioxide emissions from fossil fuels and industry exceed 20 gigatons  | 2100-12-31 | None | None |
| 45389 | Will a Land-domain AMC acting outside its mandate cause 100 deaths or $5bn in da | 2026-10-21 | None | None |
| 45409 | Will a Sustainment-domain AMO acting outside its mandate cause 100 deaths or $5b | 2026-10-21 | None | None |
| 21915 | Will Bryan Caplan win his bet that Russia will not invade a NATO member by June  | 2040-06-09 | None | None |
| 19397 | Will Derrick Rose make the Hall of Fame? | 2044-12-31 | None | None |
| 15375 | Will faster-than-light communication be possible before 2300? | 2300-01-01 | None | None |
| 38768 | Will the United States conduct a ground invasion of Iran before 2027? | 2026-12-26 | None | None |
| 3371 | Before 2030, will the European Union require commercially farmed fish to be stun | 2030-01-01 | None | None |
| 39127 | Will computer science and engineering see a greater percentage decrease (or smal | 2026-11-01 | None | None |
| 15610 | Will data centres consume more than 10% of global electricity usage for the year | 2030-12-31 | None | None |
| 9568 | Will an epidemic or agroterrorist attack on US agriculture cause at least $20 bi | 2040-01-01 | None | None |
| 40226 | Does $100k to fund plant-based hamburger R&D have a greater animal welfare benef | 2027-01-01 | None | None |
| 42032 | Oznámí do 30.6. 2027 Rohlík explicitní úmysl provést IPO? | 2027-06-30 | None | None |
| 40441 | Will the United States invade Venezuela before January 20, 2029? | 2029-01-20 | None | None |
| 24812 | Will it be possible to order flying taxis in at least 5 cities before 2029? | 2028-12-31 | None | None |
| 43281 | Will FURA introduce another cultivated meat dish on its menu before July 2027? | 2027-06-30 | None | None |
| 8509 | Will Meta report 1 billion active users by December 31, 2031? | 2032-03-31 | None | None |
| 43590 | Will the next IPC Sudan acute food insecurity analysis classify at least one are | 2026-10-31 | None | None |
| 39177 | Will the City of Pensacola stripe or build at least 10 new miles of protected bi | 2027-12-15 | None | None |
| 18673 | Will a fourth manufacturer enter the NASCAR Cup Series before 2030? | 2030-01-01 | None | None |
| 2665 | Will Volkswagen Group produce fewer than 22 million electric vehicles by 2030? | 2027-03-23 | None | None |
| 15226 | Will there be a driver fatality in the NASCAR Cup Series before 2050? | 2050-01-01 | None | None |
| 45399 | Will a Cognitive-domain AMC acting outside its mandate cause 100 deaths or $5bn  | 2026-10-21 | None | None |
| 45395 | Will a Cyber-domain AMC acting outside its mandate cause 100 deaths or $5bn in d | 2026-10-21 | None | None |
| 39169 | Will a city with a population of over 1 million successfully use a quadratic fun | 2031-01-01 | None | None |
| 12000 | Long Bets series: Will Tesla have been the first company with 1 million SAE Leve | 2037-01-01 | None | None |
| 42559 | Will any of these New England conventions be cancelled or rescheduled due to mea | 2026-11-05 | None | None |
| 45212 | Will an Air-domain AMC acting outside its mandate cause 100 deaths or $5bn in da | 2026-10-21 | None | None |
| 18092 | Will George R. R. Martin publish the sixth novel in "A Song of Ice and Fire" bef | 2030-12-31 | None | None |
| 2729 | Will the first SOO Green Renewable Rail project complete and succeed before 2035 | 2035-01-01 | None | None |
| 21914 | Will Bryan Caplan win his bet that real gross world product will not exceed 130% | 2042-12-31 | None | None |
| 3364 | Will Metaculus, or a licensed derivative, be operated as a public site by a publ | 2028-12-15 | None | None |
| 8377 | Will countries possess a total of >20,000 nuclear weapons on December 31, 2029? | 2029-12-31 | None | None |
| 39324 | Will a civilian be shot by the US national guard on US soil before the end of Tr | 2028-12-31 | None | None |

Single post detail: HTTP 200 in 0.55s, recency-weighted history points: 0.
429 at call 8 after 4.9s; headers {'Retry-After': '10'}

Burst: 8 calls in 4.9s, codes [200, 429], mean 0.61s per call.
