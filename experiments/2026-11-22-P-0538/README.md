# P-0538 ASVspoof 2019 dummy zip on Hugging Face: real dev flacs, and do they match SEAR?

Nightly 2026-11-22, from refill 224 (which searched the Hugging Face datasets API for an ungated
ASVspoof 2019 LA mirror so refill 218, the SEAR tools-only baseline, could run).

## What I ran

`check_zip.py` fetched `LanceaKing/asvspoof2019` `dummy/LA/1.0.0/dummy_data.zip` (3.75 MB, ungated)
and SEAR's `t1/19LA_dev.jsonl` and `t1/19LA_train.jsonl` into `sandbox/p0538/`, listed the zip with
`zipfile` (nothing executed), and intersected ids. Output `results.json`.

## Result

- The zip is a real cut-down copy of LA.zip: 76 entries, 45 flacs (35 to 183 KB, real audio sizes),
  the cm and asv protocol files, the README and the licence.
- Countermeasure clips: 5 train, 10 dev, 10 eval (the other 20 flacs are ASV enrolment files).
- SEAR t1 dev names 24,844 clip ids; all 10 dev clips in the zip are among them. Train: 5 of 5.

## Verdict: works, and it closes the route

The only ungated 2019 mirror the search found holds 15 clips SEAR labels (25 with eval), against
the 200 refill 218 wanted, and its loader fetches the full set from the same DataShare URL that
answers with an HTML page. So row 218 stays held: no keyless route to 200 LA clips tonight. Ten
clips is enough to smoke-test a librosa feature script end to end, not to estimate an EER.
