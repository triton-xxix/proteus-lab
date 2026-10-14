# P-0157: a sales-call funnel and opener-consistency check (from Skool S-21)

Question: does a stdlib script on 200 calls report pickup by hour, the 60-second conversation rate,
booking and show rates, and how many distinct openers a team uses, and does it recover truth planted
in the data?

`funnel.py --synth` writes 200 calls with planted truth: four opener scripts (reps paraphrase 40% of
the time), 10:00 as the best pickup hour (0.35 against 0.12 to 0.20), and the website opener converting
best (longer talk, 0.5 booking against 0.25). `funnel.py calls.csv` reports. difflib ratio 0.75 clusters
openers; the name in each opener differs every call.

Result on `calls-synthetic.csv`:
- Funnel: 200 dials, pickup 20.5%, pickup to 60 s 29%, conversation to booking 33%, show 75%.
- Best hour: 10:00 at 44% on 27 dials (planted 35%). Recovered.
- Distinct openers: 4, uses 58/54/46/42. Recovered exactly, paraphrases included.
- The planted best opener (website) shows 1 conversation and 1 booking; the cold-call opener 3 and 0.
  At 200 dials there are 12 conversations in all, so a per-opener conversion difference of 2x is not
  visible. That is the useful number for a pitch: a team needs roughly thousands of dials logged per
  opener before "which opener works" is answerable, while "how many openers are in use" is answerable
  on day one.

Shot: works at 0.60, four openers within one and the planted hour: hit.
Limits: synthetic data proves the code and the sample-size point, not that a firm needs this. No real
call data, no transcription; Matt Ryder's "80% pickup to conversation" target not checked (no data).
Next: close, unless Triton's M1 lane gets a firm's call log; then this is the first thing to run on it.
