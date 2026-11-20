# P-0507: when are mayhem coins burned?

**Question.** Is the 24-hour burn a sweep that runs on a clock, and what age are coins when it reaches
them? Two cohorts born a day and a half apart: P-0473's 19 (born 17 Nov 23:42 to 23:47 UK) and
P-0491's 20 (born 19 Nov 12:33 to 12:39Z, plus `HXgTg5...` born 11:48Z).

**Method.** `burns.py`: keyless public RPC. Newest signature per mint, `getTransaction` jsonParsed, a
burn if any parsed instruction is burn/burnChecked on that mint or a log says Burn. Run 12:40Z, 20 Nov.

**Called shot** (p 0.5, called after seeing P-0504's newest-signature ages for the second cohort):
P-0473 cohort all burned at 24.3 to 24.9 hours, in two or more clusters about 50 minutes apart.

## Numbers, first read 12:40Z

- **P-0473 cohort: 17 of 19 burned, all inside 94 seconds**, 00:03:52 to 00:05:26Z on 19 Nov, at
  ages 24.28 to 24.38 hours (median 24.30). One cluster, not two. The first burn time, 1795046632,
  is the same block time as P-0502's batch `qBwrJwYG`: this is the same sweep, which also took coins
  born from about 23:10 (P-0502's 24.86 hours).
- The two not burned last: `71MuQEj1...` newest at 39.8 hours and `9YWWW3dt...` (the one the wallet
  sold out of, P-0473) at 46.0 hours. Newest is not a burn; whether they were burned earlier and
  traded after is not read here.
- **P-0491 cohort: 1 of 20 burned so far.** `HXgTg5...` (born 11:48Z) burned 12:05:10Z today at
  24.28 hours. The other 19 are 24.02 to 24.12 hours old at the read and unburned.

## Forecast, committed before it can be known (12:42Z)

If the burn is a sweep that takes coins at about 24.28 hours or more, the other 19 P-0491 coins
(born 12:33:31 to 12:39:12Z) burn **between 12:50 and 13:00Z today, in one cluster under three
minutes.** Re-read at about 12:58Z with `recheck.py`. A miss is any of the 19 burned before 12:50 or
still unburned at the re-read.
