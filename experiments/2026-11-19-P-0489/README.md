# P-0489: do a manager's Wikipedia views climb in the week before he goes?

Question: for the Premier League managers who left during 2025-26, were their article's views in the
7 days before the exit higher than in the 30 days before that, and would a simple flag on that ratio
have picked them out a week early from the managers who stayed?

## Method

Keyless, standard library, read only. Run 19 Nov 2026.

- `changes.py` pulls the Managerial changes table from the 2025-26 Premier League article through the
  Wikipedia API (`changes-section.txt`). The 11 in-season rows are the exits, with the table's own
  dates of vacancy: eight sackings, two by mutual consent, one resignation. The two pre-season rows
  are left out.
- Controls: the 13 managers whose clubs have no in-season row in that table (Arteta, Guardiola, Slot,
  Emery, Howe, Glasner, Iraola, Silva, Hurzeler, Moyes, Andrews, Farke, Le Bris), each scored on the
  same 11 dates. 143 control windows.
- `sackings.py` pulls daily user views for all 24 articles, 1 July 2025 to 10 May 2026, from the
  Wikimedia pageviews API. Ratio = mean of days D-7 to D-1 over the median of days D-37 to D-8. The
  exit day is in neither window.

## Numbers

- **Median ratio across the 11 exits: 1.52. Across the 143 control windows: 1.46.** A manager's
  views in any given week run about half as high again as his 30-day median, sacked or not, because
  the mean catches match days and the median does not.
- **A ratio-above-2 flag catches 3 of 11 exits (27%) and fires on 37 of 143 control windows (26%).**
  That is no better than chance: 7.5% of its flags are exits, and exits are 7.1% of all windows.
- Above 1.5: 6 of 11 against 46% of controls. Above 3: 2 of 11 (18%) against 13% of controls.
- The three it catches: Pereira at Wolves 4.70, Rosenior at Chelsea 3.63, Parker at Burnley 2.39.
- **Four exits had a ratio under 1**, a quieter week than usual before the end: Nuno 0.82,
  Postecoglou at Forest 0.82, Maresca 0.78, with Tudor at 1.08.
- With the week's biggest day dropped the exits' median falls to 1.31, so most of what climb there
  is comes from one day.
- The exit day itself is unmistakable: 6 to 34 times the week before on ten of eleven (Tudor 3
  times; the verdict note first said 5 to 31, my arithmetic slip on Amorim, corrected the same run). Amorim 117,242 views on the day against 3,450 a day the week before; Rosenior 142,545.
- 24 of 24 articles answered at 1.5 seconds apart, 314 days each. P-0010's 429 on the 15th call did
  not come back.

## What it says

No early warning here. The crowd arrives on the day, not the week before, which matches P-0010 on
club pages (spikes follow results). Two of the three caught were at clubs deep in trouble where the
manager's page was quiet to begin with, so a small rise is a big ratio.

## What I did not do

- No permutation test: with 3 of 11 against a 26% base rate there is nothing to test.
- One season, 11 exits, English Wikipedia only.
- Control dates are the 11 exit dates, not random dates, so a busy football week lifts both sides.
- I did not try other signals from the same data (a rising 3-day run, or views against the club
  page's). The ratio in the title is the only thing scored.
- Controls are "no vacancy row in the table", checked against the table only.

Shot (works, 0.75): median ratio about 1.8, flag catches 4, false alarm rate about 25%. Measured
1.52, 3 of 11, 25.9%. Shot made after seeing Potter's series in the refill step (his ratio is 1.93).
