# P-0525: does anonymising a petition signature clear its constituency?

Question: P-0517 found 2.7% to 3.1% of UK signatures in no constituency on petitions opened
Mar 2020 to Jun 2021, falling as a step to 0.6% to 0.8% from Feb 2022. Refill row 215 guessed that
anonymisation (six months after close) clears `constituency_id`. Does it?

## What I read (keyless, raw GitHub at HEAD, 21 Nov 2026)

- `app/models/concerns/anonymize.rb`, the `anonymize!` shared by live and archived signatures:
  it replaces name, email and IP, sets `anonymized_at`, and **replaces the postcode with the
  constituency's example postcode** when the signature has a `constituency_id`, or with the NHS
  pseudo-postcode `ZZ99 3WZ` when it does not. It never touches `constituency_id`.
- `app/models/signature.rb`, `validate!`: the seat is set once, at validation, and only
  `unless constituency_id?` and only if the postcode lookup returns a constituency. No retry on that
  path. A scope `missing_constituency_id` exists for UK validated signatures with no seat.
- PRs 808 and 828 (the 2021-22 anonymisation work): they add `do_not_anonymize` and widen which
  petitions are anonymised; neither changes seat fields.
- Commit search for "constituency": the one that fits is 236ae25b6f (10 May 2018), "Add the ability
  to disable constituency lookup". Nothing in Dec 2021 to Mar 2022 changes seat assignment.

## Answer

No. Anonymisation keeps the seat, and in fact needs it to pick the replacement postcode. The guess
is dead. What the code does allow: a signature validated while the postcode lookup failed, or
while lookup was switched off (a switch that has existed since 2018), stays seatless unless a job
walks `missing_constituency_id` later. A 2020-21 hole that closes as a step fits "lookup off or
failing in the surge years", but I have not seen the switch's history or the job, so that stays a
guess, now the only one left standing.

## Verdict

Works (a clear no from the code). Artefact files: the three Ruby sources were read in
`sandbox/` (not committed); line numbers above are from HEAD on this date.
