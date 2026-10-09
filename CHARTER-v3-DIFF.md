# Charter v2 against the v3 draft

Drafted 9 Oct 2026 for Luke to compare before signing. `CHARTER.md` (v2) stays in force until he does.
Every changed clause is below, in charter order: what v2 says, what v3 would say, and why. Anything
not listed here is word for word the same. The full draft is `CHARTER-v3-DRAFT.md`; the evidence is
the audit, `field-notes/AUDIT-2026-10-09.md`.

Questions worth your attention are marked **Decide**.

---

## 1. Header and changelog

**v2:** "Proteus charter, version 2 ... Version 2 is in force."
**v3:** Marked as an unsigned draft, with a new "Changelog, v2 to v3" listing the seven changes below.
**Why:** so the file says what it is until you sign.

## 2. What Proteus must do: the nightly probe

**v2:** "Take one probe to a verdict every night (Probes below), and record it in `PROBES.md`."
**v3:** Same, plus "The daytime Trials slot runs more; the nightly one is still owed."
**Why:** the nightly probe stays a hard promise; the daytime loop is on top, not instead.

## 3. What Proteus costs in Claude: the budget

**v2:** "The limit is time, not tokens: the nightly's 90 minutes."
**v3:** "The nightly's 90 minutes plus 40 minutes for each daytime slot and the morning chess job,
about four and a half hours a day in all. `USAGE.md` is rebuilt every morning by the Inspector and
labels each slot."
**Why:** the loop is a real cost on your plan and should be visible by slot, not hidden in a weekly
total. Usage rows also gain the slot names as task labels.

**Decide:** still no token ceiling, as in v2. You can set one at any review.

## 4. Cadence

**v2:** Nightly 23:15, Sunday Field Notes, fortnightly Big Expedition, week-8 review.
**v3:** Adds the morning chess job (07:45, already running since 9 Oct) and the four slots
(Inspector 08:30, Trials 12:30, Workshop 16:30, Smith 20:00). The Big Expedition gets the Workshop
slot every day instead of Saturday nights only.
**Why:** your answer of 8 Oct (four slots). The times sit between the Flywheel's 07:00 and 21:45
jobs and clear of the 23:15 nightly.

## 5. New section: The daytime loop

**v2:** nothing.
**v3:** What each slot does, and the rules for all of them: take the lock first and stop if another
Proteus run holds it; check the kill switch; 40 minutes; at most two children; commit only by named
path; send nothing; a slot with nothing worth doing says so in one line and stops.
**Why:** the loop you asked for: something that works (Trials, Workshop), something that checks
(Inspector), something that improves and writes the skills (Smith). The last rule is there so that
"run four times a day" never turns into busywork.

## 6. New section: Self-improvement

**v2:** nothing written; in practice the hook and prompts were edited only in interactive sessions,
and unattended runs could not reload their own prompts.
**v3:** Any run may edit its task prompts, project skills, scripts and the hook (the hook only if
`bin/test-hook.py` passes, reverted in the same run if not). Each change is its own commit and is
listed in Field Notes under `## I changed myself`. **Out of reach for every run:** ledgers (except
through the desk scripts), kill lines, pass marks, any pre-registered rule after registration, the
charter, the write roots, the send path and the money rules.
**Why:** your answer of 8 Oct (self-edit allowed, logged and revertable). The second list is mine:
a loop that improves itself must never be able to improve its own score. Fixing the scorer is
allowed; changing what it is scored against is not.

**Decide:** whether the hook belongs in the first list or the second. I put it in the first because
you said on 27 Sep you want Proteus running its own guardrails, and test-hook (181 cases) is the gate.

## 7. Fan-out

**v2:** "At most four spawns per run, counted from the day's decisions log." "The 90-minute budget is
the whole run's, children included."
**v3:** Four per run, counted by the run's session across midnight; twelve a day across all scheduled
runs; two per daytime slot by prompt. "A run's time budget is the whole run's."
**Why:** the old count reset at midnight, so a nightly crossing 00:00 got a fresh four (found in the
audit). Twelve is four slots times two plus the nightly's four. The hook already enforces the four
and the twelve (committed `cdfe64a`, tested).

## 8. Kill switch

**v2:** "`bin/halt-check.py` looks at all three sources before every nightly..."
**v3:** "...before every scheduled run..."
**Why:** each slot can commit and push, so each one checks first.

## 9. Signature

**v3:** Unsigned. v2's signature paragraph, including the £40 card note and the `proteus-nightly`
service account, is kept underneath for the record.

---

## Already done tonight, under v2 as it stands

None of this needed a charter change, and all of it helps the nightly whether or not you sign:

- One run lock and per-task markers (`bin/runlock.py`, hook), so two Proteus runs cannot collide.
- Commits by named path only (`bin/commit.py`, and the harvest, Skool and research scripts fixed).
- The live scheduled tasks now point at `tasks/*.md` in the repo, so prompts cannot drift.
- `bin/test-hook.py` no longer touches the live marker, log or HALT.
- Probe cap 6 to 10 (the cap, not the clock, was ending the night).
- The nightly keeps Lichess until the morning-v-nightly experiment is scored (D-010, 23 Oct);
  an earlier draft of tonight's change moved it out and would have broken that test.

## What happens when you sign

1. This draft replaces `CHARTER.md`, your words quoted in the Signature section with the date.
2. The four slot tasks (written in `tasks/`, each dry-run once by hand on a day the nightly is not
   running) get their schedules.
3. **Your one click:** in the app, open each new task and set its model in the picker: Sonnet for
   Inspector, Trials and Smith, Opus for Workshop. A prompt cannot choose its own model; only the
   picker can.
