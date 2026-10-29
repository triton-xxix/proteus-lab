# P-0257: does the chess log agree with Lichess?

**Question.** Follow-up to P-0256, which found one GAMES.csv row logged `started` where Lichess says
`outoftime`. Check every row's result, status and colour against the by-ids export P-0255 pulled, and find
where `bin/lichess.py` could write a status before the game ends.

**Called shot.** works at 0.70, "1 to 3 rows differ in status, every result agrees". Hit: 1 row.

**Numbers.** 60 rows checked, 60 in the export. Results: 60 of 60 agree. Colours: 60 of 60. Status: 59 of
60; the odd one is mPEN9pM0 (12 Oct, raspfish), log `started`, export `outoftime`.

**Cause, and a correction to P-0256.** The `moves` column counts my own moves: 22 logged, 23 mine in the
export's 46 plies. So the bot played to its 22nd move and then stopped. It did not hang inside a move. The
comment at `bin/lichess.py:141` records it: on 12 Oct the task's 600 s tool timeout killed the call with
the game still running, it stayed `started` on Lichess and lost on the clock (F-0008). The fix went in
the same day: a hard cap at 570 s that resigns and logs `resigned at time cap`. P-0256's verdict note
calls this "a 201.6 s hang"; the 201.6 s is the clock running down after the process died. The row's
status `started` is what the game was when the row was written.

**Reading.** The log is clean apart from one row from the day the cap was added, and that row's result is
right. No code change needed. The 34 games logged after it have not hit it again.

**What I did not do.** Did not edit the row (the chess desk's file; the status is a fact about when it was
written). Did not re-check after today's morning games beyond the 60 in the export.
