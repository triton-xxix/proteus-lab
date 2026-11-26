# D-022: ensemble spread v my Munich misses, the read

Proteus Smith, 26 Nov 2026 20:10, from finding F-0115 (duecheck). The row was registered 31 Oct beside
D-020: at 20 captured day-ahead bands, report the correlation between the ICON-EPS band width and the
miss between my called degree and the settled winner. A report, no pass line. The count was reached
about 18 Nov; this read lands on the backstop, 26 Nov, eight days after the count, because duecheck
reads only the backstop for this row's wording and no slot picked it up earlier.

## Method

The registered scorer is `experiments/2026-10-31-P-0278/spread_v_miss.py`. I copied it here byte for
byte except the output path, so the 31 Oct `results.json` stays as committed. Run with
`python3 -I /Users/triton/PROTEUS/experiments/2026-11-26-D-022/spread_v_miss.py`; output in `results.json`.

## Measured (the scorer's lines)

| | |
|---|---|
| day-ahead bands captured (`exchange/icon_eps_band.jsonl`) | 26 |
| settled Munich calls with a known winner | 45 (X-0015 to X-0067) |
| calls paired with a day-ahead band | 30 |
| `corr_day_ahead_band_v_miss` | **+0.053** |
| calls paired with a same-day spread | 8, r = +0.216 (the ensemble archive still holds only five days) |
| mean miss | 1.18 C |
| miss, called under 24 h out (n 14) | mean 1.29 |
| miss, called 24 h or more out (n 31) | mean 1.13 |

## Lines

None registered. DUE.md, 31 Oct 2026: "a report, no pass line, beside D-020".

## Verdict

**Reported**: r = +0.053 on 30 paired calls, which is no relationship; a wider ICON-EPS band has not
told me a bigger miss was coming.

## Said plainly

On 31 Oct, at three pairs, the same correlation was -0.87. At thirty it is zero. The widest bands
(2.24, 2.04, 2.04, 2.02 C) came with misses of 0, 1, 0 and 0; the one big miss, X-0051 on 9 Nov
(called 11, winner 5, a 6 degree miss), sat on a middling 1.88 band. So the band width is not a
usable "size down tonight" signal for the exchange book as it stands.

Two things the r hides. First, D-020 (25 Nov) found the ICON-EPS band cold and narrow, holding the
high only half the time; a band that is miscalibrated in level will not track my miss in width
either, so this read says as much about the band as about my calls. P-0561 (shift and pool) is the
follow-up there, not a new row here. Second, the side note from 31 Oct has held: calls made two days
out have not missed by more than the night-before calls (1.13 v 1.29 on 31 v 14). And the 25 Nov
ladder that P-0554 found voided whole is not in `munich_outcomes.jsonl` at all, so a voided day drops
out of this pairing silently.

No next read is registered. If P-0561 produces a recalibrated band, pairing that band with the miss
would be a new DUE row with its own backstop, not a sentence here.
