# P-0519: does alphagov/e-petitions' code history explain the Feb 2022 step?

**Question.** P-0517 found the share of UK petition signatures in no constituency drops as a step
between Jan 2022 (1.51%) and Feb 2022 (0.62%) by opening month. Does a commit around then explain it?

**Method.** `commits.py`: keyless GitHub REST API, every commit on alphagov/e-petitions between
1 Nov 2021 and 1 Apr 2022 (68), first lines listed, messages flagged on constituency, postcode, ONS,
geography, boundary, count, location, region. Then the one flagged commit that touches signature
data validation (`0fb8db0fa0`, 2 Mar 2022, "Ensure location_code is valid") read in full, saved
as `commit-0fb8db0fa0.json`. 21 Nov 2026 about 12:48Z.

**Called shot:** not-worth-it at 0.45; no commit in the window names constituencies, postcodes or
ONS data plainly.

## Numbers

- 68 commits; **0 name constituencies, postcodes, ONS or boundaries**. 16 matched the wider pattern,
  all false leads: "count" (signature-count state fixes, 11 Jan 2022), "location" (the 2 Mar commit),
  anonymisation and privacy work.
- `0fb8db0fa0` adds a format check to `location_code` (the country code, two or three capitals). It
  stops scripts inserting bad country values. It does not touch constituency lookup.
- The window's big theme is a new data-retention policy (24 Feb to 6 Mar 2022): privacy notice,
  automatic anonymisation of closed petitions' signatures. Nothing in the messages says anonymising
  clears the constituency, and I did not read those diffs.

## Shot v measured

Called no plain constituency or postcode commit: hit, 0 of 68.

## What it says

The code did not change how seats are assigned around Feb 2022, as far as commit messages and the
one candidate diff show. The step is more likely data-side (the postcode-to-seat lookup table the
site loads, refreshed outside git) or a side effect of the anonymisation run, which would need the
diffs of #808 and #828 read. Not worth more probes on its own: the open question is narrow and the
desk has nothing riding on it.

## What I did not do

- Did not read the anonymisation diffs (#808, #828, #831, #832).
- No look at the site's postcode lookup source (it is not in the repo's history as data).
