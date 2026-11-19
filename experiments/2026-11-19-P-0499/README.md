# P-0499: the successor's page moves first

Refill row 196, run 19 Nov 2026 in the nightly probe loop. P-0489 found no warning in a manager's
own Wikipedia pageviews before he was sacked. This looks at the man who replaced him.

## Question

For the seven in-season Premier League appointments of 2025-26 that had at least two days between
the vacancy and the appointment, how high did the incoming manager's article go before the day his
appointment was announced, against his own median?

## Method

`successors.py`, standard library, keyless. Titles settled by MediaWiki search; daily user pageviews
from Wikimedia. Dates are the vacancy and appointment dates in the season article's table (P-0489's
`changes-section.txt`). Base is the median of days 37 to 8 before the vacancy.

## Numbers (multiples of his own median)

| Successor | Club | Gap days | Week before vacancy, max | Vacancy day | Day before appointment | Appointment day |
|---|---|---|---|---|---|---|
| Dyche | Forest | 3 | 4.3 | 12.2 | 37.6 | 64.6 |
| Edwards | Wolves | 10 | 1.3 | 6.0 | 11.5 | 40.9 |
| Rosenior | Chelsea | 7 | 4.7 | 334 | 297 | 95.4 |
| Carrick | Man Utd | 8 | 2.0 | 19.9 | 98.5 | 132 |
| Tudor | Spurs | 3 | 1.2 | 1.6 | 1,211 | 416 |
| Pereira | Forest | 3 | 1.6 | 289 | 35.9 | 63.2 |
| De Zerbi | Spurs | 2 | 7.1 | 16.4 | 97.7 | 158 |

- **7 of 7** were at three times their median or more the day before the announcement (called shot:
  5 of 7). The median is 98 times.
- 6 of 7 were already over three times on the day the job fell vacant. Tudor is the exception: 1.6
  and 2.6, then 1,211 the day before.
- For Rosenior and Tudor the day before was bigger than the announcement day itself.
- Before the vacancy existed, 3 of 7 (Dyche, Rosenior, De Zerbi) had a day at four times or more in
  the week before. P-0489's outgoing managers showed nothing in that week.

## What it does not show

That pageviews pick the winner. Every name the papers link to a job will rise, and I have no control
group of candidates who were linked and not appointed; without one this is "the press named him
first", not a signal. The table's appointment date is the club's statement, and reporters often have
it a day earlier, which is probably the whole of the day-before column. Seven cases, one season.
The control group is the next probe if this is worth a second look.
