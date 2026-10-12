# P-0129: how far do Pitch prices move after the commit-time line? (first leg)

**Question.** Snapshot API-Football odds about two hours before kickoff beside the commit-time line, measure the
move, and see whether the desk's "beat the close" bets are just moves it never saw.

**Called shot.** blocked at 0.75: "0 Pitch-league kickoffs before 17 Oct". Wrong. I assumed an international
break without looking; `pitch/cache/apisports.json` holds five Monday fixtures (I1, E0, SP1, P1).

**Method.** `run.py <label>` re-pulls `/odds` for each fixture still to kick off and appends a snapshot to
`snapshots.json`, with the per-outcome move against last night's line (fetched 2026-10-11 22:30Z). Five
requests; 91 left today.

**Numbers, leg 1 (12:5x BST, 4.7 to 7.5 h before kickoff).** 15 prices (5 matches x 1X2). Mean absolute move
since the commit-time line 1.5%, largest 4.4% (Venezia out from 5.55 to 5.30). Levante v Sevilla moved most as a
match: Sevilla 2.60 to 2.70.

**Not done.** The two-hours-before leg (14:30Z to 17:15Z) falls after this slot. Not yet set beside which of these
matches the judgement book actually bet, so nothing yet on the "beat the close" question.
