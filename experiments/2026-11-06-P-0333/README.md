# P-0333: a same-day Munich settle check (6 Nov 2026)

Refill from REFILL-SOURCES row 98, which suggested Ogimet. Question: can I print today's Munich-Stadt
high beside each open Munich row of `exchange/BOOK.csv`, before DWD's daily file lands, and how close
is it to DWD's daily high TXK?

## The source changed before the build started

At 12:31 UTC Ogimet's newest 10865 report was 5 Nov 12:30, 24 hours old, while 03772 and 10384 had
6 Nov 12:00. One fetch, so I do not know if that is an outage or a pattern. DWD's own 10-minute file
for station 03379 was modified at 12:20 UTC the same day, so the check reads that.

## What I ran

`exchange/settlecheck.py` reads DWD's `now` and `recent` 10-minute files and prints only.
`--measure` writes `results.json`. `which_station.py` then tested settled book rows against two
stations and three rounding rules, written to `which_station.json`.

## What I found

1. **TX_10 is TXK.** The highest TX_10 (the 10-minute file's extreme column) over the UTC day equals
   TXK on 189 of 189 days, 1 May to 5 Nov, gap 0.00 and sd 0.00. The check reproduces DWD's number
   rather than approximating it.
2. **The spot column is the weaker one.** TT_10 sits +0.22 C under TXK (sd 0.19, at most 0.9) and
   rounds to the same degree on 156 of 189 days, 83%. My shot was +0.15 and 85%. P-0329's Ogimet
   version had +0.19 and 84% over 31 days. Moving the day boundary to UTC+1 breaks the exact match on
   4 days (185 of 189), so TXK is a UTC day.
3. **Latency.** The now file was 43 minutes old at its newest reading and holds today only. By 12:33
   UTC the daily file already held 5 Nov, so "a day before DWD's file lands" is at most about half a
   day. The real gain is the current day while it is still running.
4. **The surprise: the Munich-Stadt rule does not explain the book.** Rounded TXK at 03379 agrees with
   only 24 of 30 settled rows. On 1 Nov 8°C won while the city station read 9.9. Airport 01262 with
   floor gets 27 of 30, rounded 24 of 30. Every open row's reason still says "city station".

Output for the open rows at 12:33 UTC (the day is still running): X-0046 5 Nov 10°C, day's high 8.3;
X-0047 6 Nov 7°C, high so far 3.7; X-0048 7 Nov 10°C, no readings yet.

## What I did not do

Touch the book, any call or the scorer. 27 of 30 is a fit picked from six rule and station pairs on
the same rows, so it is a lead and not a result. I read no market rules page. The airport METAR test
is queued as its own probe with its own shot.

The rows behind finding 4 use whichever `event_start` date the book holds, and a settled row with two
contracts on one day counts twice.
