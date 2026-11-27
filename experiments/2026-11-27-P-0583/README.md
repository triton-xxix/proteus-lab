# P-0583: feed hole, keep v drop (refill 253)

**Question.** Yahoo's 5-minute feed has a hole on 5 Nov (P-0573). `edges/scan/scan.py` `prepare()` drops
any stock day under 70 bars. Does that drop change the stock ladder?

**Method.** `keepdrop.py`, offline over P-0573's leg-one pull (26 Nov 23:35Z, 12 stocks). It execs a copy
of scan.py with the bar floor changed and runs the 36 stock rules twice: as-is (floor 70) and with the floor
at 50 so 5 Nov stays. Totals and rungs only; the random-entry p-values are not compared (PERMS set to 2).

**Numbers.**
- 5 Nov is 78 bars with 19 null rows in every symbol, 59 usable (not 63: all 19 nulls sit on that day in
  SPY). A floor of 60 still dropped it; 50 kept it.
- With 5 Nov dropped, W3 is 4, 6, 9, 10, 11 Nov; with it kept, 5, 6, 9, 10, 11 Nov. W1 and W2 identical.
- Rung counts changed: **4 of 36**, all ORB, all from 2 to 3 (a full ladder): ORB 15m 2R (W3 -11.2 to
  +25.3), ORB 15m close (-15.1 to +21.4), ORB 30m 1R (-11.9 to +11.2), ORB 30m 2R (-14.8 to +11.3).
- W3 total moved by more than 1 point in 36 of 36 rules; median move 20.2 points.

**Reading.** The hole itself is not what moves the numbers: dropping the day swaps one whole session
(4 Nov for 5 Nov) into W3, and one session in five is enough to turn four ORB rules from losers to winners
over that week. So a feed hole can make or break a climber, by moving the block edge. A 1-point line was far
too tight; W3 totals are sums over 12 stocks.

**Called shot.** works at 0.70, 2 rules change rung count. Measured 4.

**Not done.** No check of which committed ladder runs used a W3 holding 4 Nov, or whether any of these
four ORB rules was reported as a climber from one. ORB reads the morning, which the 17:15 to 18:30Z hole
does not touch; rules that read the afternoon on 5 Nov are reading a gap.
