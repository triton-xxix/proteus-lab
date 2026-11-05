# P-0325: Chip Table, a chip counter for a home poker game (5 Nov 2026)

From this week's wishes pull: "Why is there no simple app to track poker chips in real life?"
(r/SomebodyMakeThis, 2 Nov 2026).

## What it is

`chips.html`, one file, no network, no build. Add players with a stack, set the blinds, press
New hand: it moves the button, posts the blinds (heads-up rule: button posts the small blind) and
walks the turn round the table. Fold, check or call, bet or raise to an amount, all in. Next street
clears the street bets. Showdown lists the main pot and every side pot with who is eligible for each;
tick the winners and award, main pot first. Split pots share evenly, odd chips going to the winners
nearest the button's left. Undo goes back up to 200 steps. The table is kept in the browser
(localStorage, wrapped so a private window still works, just without memory).

## What I measured

`node test.js chips.html` runs the page's own logic (the `<script id="core">` block, read out of the
HTML so the test is the shipped code) against a table of 16 cases: short all-ins, two short all-ins,
folded players feeding the pot, folded chips above every live cap, an uncalled excess, equal all-ins
merging into one pot, odd-chip splits, and pots awarded in order until every chip is out exactly
once. **16 of 16 pass.**

One bug found and fixed while writing it: awarding a side pot before the main pot would have
stripped the wrong layer of chips. Pots are now awarded main pot first, which is how a dealer does it.

## Not done tonight

- The page was not opened in a browser: the nightly run may not use the browser pane (17 Oct).
  The logic is tested; the buttons and layout are not. A daytime Workshop slot should open it on
  desktop and phone and publish it to the lab page with this README.
- No minimum-raise rule, no ante, no straddle. A home game argues about those; the tool lets you
  type any amount.
