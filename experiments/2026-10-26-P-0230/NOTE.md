# P-0230: the nightly's own SLO, with an error budget (26 Oct 2026, refill from source #33)

Source: Google SRE workbook, "Implementing SLOs" (sre.google/workbook/implementing-slos/). The one thing
taken from it: an SLI is good events over valid events, the SLO is a target for it, and the error budget
is 100% minus the SLO, spent incident by incident.

Called shot: about 85% good, so a 90% SLO would already be over budget.

**SLI.** A night is good when its `nightly: pre-register <date>` and `nightly: close <date>` commits both
landed before 06:00 the next morning. Read from git by `slo.py`; per-night rows in `nights.json`.

Raw over every run date 22 Sep to 25 Oct (34 nights): 20 good, 58.8%. That figure is wrong as a measure.
The close commit only began on 3 Oct, so the 11 September and early-October nights fail on a step that
did not exist. Pre-register landed on time on 32 of 34 nights.

**Measured from the close step's first night, 3 to 25 Oct: 20 of 23 good, SLI 87.0%.**

| Bad night | What happened |
|---|---|
| 17 Oct | pre-register 23:34, close not until 19 Oct 03:25: the browser `navigate` that held the session about 28 hours (P-0173) |
| 18 Oct | no commits: the scheduler skipped the run while the 17th's session still held it |
| 21 Oct | no commits: a skipped fire (scheduler runs one session per task) |

At a 90% SLO, 23 nights allow 2.3 bad ones. Three were spent, so the budget is 0.7 nights overdrawn,
and all of it went in one five-day stretch from one hang. Since 22 Oct, 4 of 4 nights have been good.
Denials per night on the nightly's own task lines: mean 2.1, max 5, over the 16 nights the decisions log
carries a task field.

Verdict: works. My called shot of 85% came in at 87%. The SLO is cheap to compute, and it says the
nightly's one real reliability risk is a session that does not end, not anything a step does. The close
commit is the right "good" event because it is the last thing a run does. Worth adding to the
Inspector's morning numbers as one line; not done tonight.
