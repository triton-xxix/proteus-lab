# Graduates

The written line a find has to clear before it leaves Proteus, pre-registered on 2026-09-27 before
any candidate exists, the way `PASS-MARKS.md` was. The charter's Graduation section is the
authority; this file is the test. If this file and the charter disagree, the charter wins and this
file is fixed in a dated commit.

## The standard

A find graduates only when all five are true, each with a link or a commit hash, not a sentence:

1. **It was run.** At least one probe verdict of "works" in `PROBES.md`, with an artefact in the
   repository that reruns it.
2. **It has a public record.** Its numbers or behaviour are in a file that is committed and shown
   on the lab page, and the commits that put them there are named.
3. **It survived two Sunday culls.** Two Sunday Field Notes, in different ISO weeks, after the
   first verdict, and neither culled it.
4. **It still works.** Rerun within the seven days before the handover note, from a clean
   checkout, with the result recorded. A find that only worked once does not graduate.
5. **The next step needs something only Luke has.** An account, money above the monthly ceiling,
   a place in a venture, or his name. If Proteus could take the next step itself, it is not a
   graduate; it is next week's work.

A desk (the Grinder, the Pitch, the judgement book) does not graduate through this file. Desks go
through `PASS-MARKS.md` at the week-8 review and the execution ladder in the charter.

## What happens when one clears it

- `graduates/<name>.md` is written: what it is, the evidence with commit hashes, how to run it, what
  it needs from Luke, and what Proteus keeps doing with it if nothing happens.
- It is mirrored to `TRITON-CORE/Proteus/graduates/` by `bin/mirror-vault.sh`.
- It appears once in Field Notes under `## Graduated`, and permanently on the lab page under
  Graduates. It is mentioned in email again only if the evidence changes materially, and then once.
- Nothing is opened in the Flywheel. Whether the chief-of-staff agent reads the graduates folder is
  Luke's call, asked once, in the first Field Notes after the charter is signed.

## Register

| Date | Name | Handover note | Needs from Luke | Status |
|---|---|---|---|---|

None yet.
