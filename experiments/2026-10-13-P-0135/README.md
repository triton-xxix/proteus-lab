# P-0135 leg 2: the late move before kick-off, 13 Oct 2026

Run interactively at 18:02 BST on Luke's yes. The one-off schedule I planned for 17:45 BST could not be
created because that time had already passed, so this is 1.7 to 1.95 h before kick-off, not 2 h. The
probe's verdict stays blocked (recorded at Trials); this README is the artefact for the leg.

## Numbers

`run.py ko-1h45` (P-0129's script) re-pulled API-Football's 10-bookmaker average for tonight's 8
Championship fixtures, beside the commit-time line fetched 12 Oct 22:56Z:

- 24 prices, mean absolute move 3.4%, largest +21.5% (Preston out from 5.23 to 6.35, Birmingham in from
  1.59 to 1.47). On Monday's leg 1, 4.7 to 7.5 h out, it was 1.5% mean and 4.4% largest, so the late
  hours move prices about twice as much.
- `compare.py`: the books placed no judgement rows and no model bets on these matches. Against the model's
  probabilities in `pitch/PREDICTIONS.csv`, outcomes where the model leaned at least 2 points off the
  commit line and the price moved at least 0.2 points: 7 moved toward the model, 5 away, and 12 had no lean
  or no move. Birmingham v Preston, the biggest move, had no model lean.

So the "beat the close" question is still unanswered, because there was no bet to test. On this one
night, the late market does not move toward the model's leans any more often than a coin would (7 v 5).

## Not done

No judgement-book rows existed for these matches. One night of 12 leaning outcomes is far too few to
tell anything apart from noise. The 2 h leg needs a slot near kick-off: none of the four daytime slots
covers an evening kick-off two hours out.
