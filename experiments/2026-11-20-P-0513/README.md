# P-0513: a control for P-0499's appointee pageviews

Question: P-0499 found 7 of 7 incoming Premier League managers at 3x their own median pageviews or more
the day before they were announced (median 98x). Do managers who did not get that job do the same?

Called shot (5afa74dd): works at 0.6, at most 6 of 42 control pairs at 3x.

## What the control is, and is not

The probe asked for names linked in each club's season article but not appointed. Pulling those
keyless means reading prose for "linked with" names, which I could not do reliably in the time. The
control here is weaker: each of P-0499's seven appointees, read on the other six vacancies' day before
the appointment, against his own median of days -37 to -8 before that vacancy. These are managers in
the news that season who did not get that job. `control.py`, Wikimedia pageviews, keyless, 7 calls.

## Numbers

- Appointees: 7 of 7 at 3x or more, median 97.7x (P-0499's figure, recomputed).
- Controls: 7 of 42 at 3x or more, median 1.26x.
- Four of the seven are a manager in his own appointment week: Carrick on Chelsea's day (21.8x, he was
  named six days later), Rosenior on United's (66.3x), Pereira on Spurs' (89.3x) and Tudor on Forest's
  (419.9x, the same week as his Spurs job). Take those out and 3 of 38 pass 3x: De Zerbi 4.7x before
  Chelsea's appointment, Tudor 4.6x before United's, Dyche 4.8x before Spurs'.
- No control outside its own appointment week went above 5x. The lowest appointee was Rob Edwards at
  11.5x; the others 35.9x to 1,210.7x (P-0499's `day_before_x`).

So the 3x line catches the appointee every time and a not-appointed manager about one time in thirteen
(3 of 38); the size of the jump, tens of times against under five, separates them better than the line.

Shot: 7 against at most 6, a narrow miss as called (counting the own-week pairs).

## Not done

No genuinely linked-but-not-appointed names, so this cannot say whether the press's other candidates
spike as hard. Seven vacancies, one season.
