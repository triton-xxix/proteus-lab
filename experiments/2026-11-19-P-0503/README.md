# P-0503: the day half of Wikipedia's top 1,000 changed

Refill row 200, run 19 Nov 2026 in the nightly probe loop. P-0498 found that 67% to 74% of a day's
top 1,000 English articles is there the next day, except 3 Nov into 4 Nov 2026: 48%.

## Method

`nov4.py`, standard library, the keyless Wikimedia top-pageviews list for 1 to 6 Nov 2026, six calls.
Titles only: an entrant counts as electoral if its title carries one of eleven words (election,
senate, governor, congress, gubernatorial and so on).

## Numbers

- 508 articles entered on 4 Nov and 509 left. 500 of the 508 had not been listed on 2 Nov either.
- **154 of the 508 entrants carry an election word in the title** (called shot: at least 100), and the
  commonest words across entrant titles are "united" and "states" (111 each), "election" (67),
  "elections" (44), "senate" (38), "texas" (33), "gubernatorial" (26). The top entrants are people:
  Dan Osborn at rank 14 with 273,151 views, Chris Pappas at 30, Scott Colom at 35. Candidates' names
  carry no election word, so 154 is a floor. The US midterms were on 3 Nov; 4 Nov UTC is results day.
- The top list's total views doubled: 18.6 million on 3 Nov, **38.1 million on 4 Nov**, 24.1 on 5 Nov,
  21.1 on 6 Nov. The election did not push the usual articles out so much as bury them under new ones.
- It did not snap back. 237 of the 508 entrants were still listed on 5 Nov and 133 on 6 Nov; only 142
  of the 509 that left were back by 6 Nov. The 5 Nov list shares 47% with 2 Nov and so does 6 Nov,
  where P-0498's ordinary three and four day figures are 56% and 53%.

## Not done

No classification beyond title words, so the non-electoral entrants (a footballer, a cold case) are
not sorted from the noise. One event. Whether other fixed-date events (a World Cup final, an awards
night) leave the same shape is the comparison that would make this a pattern.
