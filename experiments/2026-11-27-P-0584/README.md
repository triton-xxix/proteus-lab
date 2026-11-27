# P-0584: feed-hole block edge in the committed ladders (deepen of P-0583)

**Question.** P-0583 found that dropping the holed 5 Nov session swaps 4 Nov into W3 and keeps four ORB
rules at rung 2 instead of 3 on the 26 Nov pull. Which committed `edges/scan/` runs had a stock week that
held 4 Nov because 5 Nov was dropped, and where did those four ORB rules sit?

**Method.** `ladders.py` reads every `edges/scan/<date>/results.json` (31 runs), counts weekdays in each
stock week's range (26 Nov holiday excluded), and flags a week that holds both 4 and 5 Nov but spans six
weekdays, so 5 Nov was the one dropped. Reads the four ORB rules' rungs from each run.

**Numbers.**
- 15 of 31 runs had the dropped 5 Nov inside W1 to W3: W1 from 7 to 12 Nov, W2 from 16 to 19 Nov, W3
  from 21 to 26 Nov. (13 and 20 Nov show none: the block edge fell elsewhere that day.)
- In the last five runs (21, 22, 23, 25, 26 Nov) the dropped week was W3, and 3 or 4 of the four ORB
  rules sat at **rung 2**: 17 rule-runs, none at rung 3. These are the ladders where a full climb was one
  week short, and that week was the one the hole moved.
- Before 16 Nov the four sat at rung 0 in every flagged run, so the hole could not have mattered there.

**Reading.** For P-0583's 26 Nov window, keeping 5 Nov gives all four a full ladder. The 21 to 25 Nov runs
were not re-run, so whether they too would have climbed is not measured. If the edge desk ever reported "no
stock rule reached rung 3" across those days, that line rested on a feed hole and a hard 70-bar floor.

**Called shot.** works at 0.70, about 8 runs, at least one ORB at rung 2 or more. Measured 15 runs, 17
rule-runs at rung 2.

**Not done.** No re-run of the 21 to 25 Nov ladders with 5 Nov kept (those pulls were not saved raw).
No change to scan.py's floor: that is a desk choice, and a floor of 50 lets real half-days in.
