# P-0321: do Fed cuts land in uptrends before 2009 too?

**Question.** P-0314 found 8 of the 11 cuts since 2008 (DFEDTARU, all from 2019) landed with SPY above its
SMA200 and up over 20 days, so a "rate cut" signal is mostly invisible to the systems book's 200-day filter.
Is that a property of cuts, or of 2019 to 2025?

**Method.** `check.py`. FRED DFEDTAR (single target, one curl 4 Nov 2026), every decrease; decision day is the
last SPY trading day before FRED's effective date. SPY adjusted closes from Yahoo, 1993 to Feb 2009. Cuts
before SPY has 200 days of history are dropped (51 cuts, 1982 to 1993). Control: 10,000 draws of 28 random SPY
trading days between the first and last cut, share with both conditions; permutation p for a count as low
as the one measured. This is the random-entry control from the retired backtest-with-luck-test procedure.

**Numbers.** 28 cuts, 5 Jul 1995 to 28 Oct 2008.

| | cuts | share | random days |
|---|---|---|---|
| above SMA200 | 8 | 0.29 | |
| up over 20 days | 15 | 0.54 | |
| **both** | **7** | **0.25** | **0.51** |

Permutation p (as low or lower) 0.004, two-sided 0.008. Shot: 0.30 against about 0.50. Mean SPY return 20 days
after a cut 0.47 percent.

**Reading.** Before 2009 the pattern runs the other way. The 1995 to 1998 and 2003 insurance cuts sit in
uptrends (6 of 7 with both conditions); the 2001 and 2007 to 2008 easing cycles (19 cuts) sit below the 200-day
in all but three. 2019 to 2025 looked like 1995 to 1998. So "cuts land in uptrends" was an accident of which
cycles were in the sample, and a cut is no signal on its own: it depends on whether it is an insurance cut
or a recession cut, which the 200-day line already sorts.

**What I did not do.** No trade test, only the state on the day. Unscheduled cuts (Jan 2008, Sep and Oct 2001,
Oct 2008) are mixed in with scheduled ones. 11 Sep 2001 closure moves that decision day to 10 Sep. The
16 Dec 2008 move to a range is in DFEDTARU, not here.
