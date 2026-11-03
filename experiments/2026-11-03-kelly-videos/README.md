# Kelly criterion, five videos, every number checked (Field Notes, watched it, 3 Nov 2026)

Videos (transcripts pulled keyless with youtube_transcript_api; kept local in `sandbox/kelly-videos/`, not committed):

| id | channel | title | words | last caption |
|---|---|---|---|---|
| -9JM9suCIHs | Mutual Information | The Kelly Criterion | 1485 | 536 s |
| b-G7ukH8Dks | Mind Math Money | Kelly Criterion Explained In Under 7 Minutes | 1030 | 404 s |
| THYLv5_0Vm8 | Financial Wisdom | KELLY CRITERION, Ed Thorp, Optimal Position Sizing | 1207 | 484 s |
| beR_vw1Du5c | GG Easy | The Kelly Criterion Explained in 60 Seconds | 156 | 52 s |
| rFr6AUMRd_Y | ProfitPulse | Why 1% Risk Is Holding You Back | 282 | 94 s |

`check.py` recomputes each video's numbers and simulates 20,000 runs of 100 bets (seed 7).

## Output

```
Mutual Information: p 0.7, odds 4 to 6 (b=2/3)
  Kelly f 0.250, growth 2.16% a flip, $50 after 100 flips 434
  bet $5 of $50 fixed fraction 0.1: growth 1.36% a flip
Mind Math Money and GG Easy: p 0.6, b 1 -> 0.2
Financial Wisdom: boxer p 0.55 b 0.9 -> 0.05 | trader p 0.59 b 4.04 -> 0.4885 | p 0.5 b 2 -> 0.25
p 0.6, b 1, 100 bets, 20,000 runs: share that ever fall 50% from a peak, median final, share ending below start
  full Kelly 20%     99.0%  median x  7.49  below start 17.9%
  half Kelly 10%     43.3%  median x  4.50  below start  6.6%
  fifth Kelly 4%      0.4%  median x  2.06  below start  4.2%
  double Kelly 40%  100.0%  median x  0.78  below start 54.3%
Edge misjudged: true p 0.55 while you bet Kelly for 0.6 (20%)
  full Kelly at true 0.55: fall 50% 99.9%, median x0.99, below start 53.8%
  half Kelly at true 0.55: fall 50% 71.4%, median x1.65, below start 31.1%
```

## Verdicts

- Every formula result in the five videos is right (20%, 5%, 48.85%, 25%), and Mutual Information's "nearly 2 and 1/4% a flip, around $450" is 2.16% and $434.
- Mutual Information's "bet five always" strategy is quoted at "about 1.1% per flip"; a fixed $5 of a $50 stake read as a fixed 10% fraction gives 1.36%. The video's version bets a fixed $5 (not a fraction), which grows slower, so 1.1% is plausible and not checked further.
- Financial Wisdom takes the Kelly fraction as position size, then risks 10% of the position (1.63% of equity). Kelly's f with b as the win-to-loss ratio is the fraction at risk, so his "33% fractional Kelly" is about 1/30 of Kelly on risk. The labels are wrong; the sizing is conservative.
- Mind Math Money's "full Kelly will ruin you": a fixed fraction never reaches zero, so literal ruin does not happen; but a 50% fall from a peak inside 100 bets happened in 99% of runs.
