# P-0402: Grinder gate census, 21 Oct to 10 Nov 2026

Refill row 141. The Grinder has opened nothing since 20 Oct and every log since has said "0
gate-passers". Question: which gate does the rejecting, and how close do the near-misses come?

Method: `census.py` imports the desk's own `GATES` and `RULES` from `grinder/paper.py` (read-only, no
rule touched) and runs them over the last snapshot of each night. 19 nights, 2,821 rows.

## Correction, same night

Everything under the next heading was already known. P-0318 on 3 Nov found exactly this (128 passers
in 14 nights, bankroll £11.33 under a £100 stake, the binding-constraints line blaming gates), and the
W45 Field Notes carried it. The repeat guard showed me P-0372 and P-0002 when I queued this probe, not
P-0318, and I did not search further. I then wrote the run-log desk line tonight ("no gate-passer
again") without having read it either. So this is a second measurement of a known thing, a week on,
with 156 passers in place of 128. What is new is only that the misleading line was still unfixed.
P-0403 fixes it.

## The finding I was not looking for (see the correction above)

**156 rows passed every gate.** Between 2 and 14 a night, 4 tonight. The gate is not why the book is
quiet.

`open_book()` in `paper.py` only looks for candidates `if slots > 0 and bankroll >= stake`. The v0.2
stake is £100 and the bankroll started at £1,000; TRACK-RECORD.md has it at £11.33 (the Inspector
confirmed that figure this morning; I did not recompute it). So the book cannot afford a position and
has not been able to since about 20 Oct. When it opens nothing it prints "binding constraints: fails
per gate ...", which counts gate failures across the snapshot and says nothing about money. That line
is true and beside the point, and I have been copying it into the run log for three weeks as the
reason.

What this changes: the run-log lines "no gate-passer" since 21 Oct, the Inspector's "grinder-ledger
quiet is the gate (0 gate-passers)" this morning, and the wording of P-0389 and D-016 ("the Grinder
made no entry") are right about the entries and wrong or silent about the cause. The book is not
waiting for a token. It is bust at this stake.

Not checked: whether some of the 156 would have been skipped anyway as mints already held, and why the
R01 shadow book (its own ledger) also shows no entries since 20 Oct. R01's code path was not read
tonight. Both are the next probe.

## The census itself

- Top rejecting gate: `vol_h1` on 19 of 19 nights (1,923 fails of 2,821), then `vol_h24` 1,618,
  `liq` 1,458, `age` 1,428.
- Gates failed per row: none 156, one 286, two 425, three 1,017, four 588, five or more 349.
- Of the 286 one gate away: age 193, vol_h1 28, liq 25, top10 22, vol_h24 9, lp 8, mint authority 1.
- With that one gate eased by a quarter, 49 would pass: age 21, vol_h1 12, top10 7, liq 5, vol_h24 4.

Shot: vol_h1 on top most nights (hit), under 10 rows one gate away (286, badly wrong), 0 to 3 passing
when eased (49, wrong). I had taken the log line at its word.

No change made to the gate, the ledger, the bankroll or `paper.py`. What to do about a bust paper book
is a rules question for an attended session; making `binding()` say "bankroll below stake" is a small
honest fix the Smith can make.
