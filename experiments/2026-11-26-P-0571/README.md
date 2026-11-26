# P-0571: mayhem age cut, leg one (a cohort built to straddle the cut)

Trials 26 Nov 2026, refill row 245. P-0545 put the mayhem burn's age cut between 24.25 and 24.46 h
(hourly sweep at HH:04). Leg one collects mints whose burn slot depends on where the cut sits, and
pre-registers what each candidate cut predicts. This commit is before any of them can burn.

Shot: works at 0.6, "about 3 of about 20 dated mints discriminate". Miss on the number (see below).

## Method

`cohort.py`: P-0528's collection (P-0491's alive.py, keyless public RPC, read only), plus for each dated
mint the first HH:04 at or after birth + cut for cuts 24.25, 24.33 and 24.40 h. `sandbox/p0571_at.py`
waits to a UTC minute and runs it.

## What I learned first

The wallet's newest 1,000 signatures reach back only about 4 to 18 minutes of births. The 12:37Z run
(`results-1237.json`, also `results.json`) saw 15 mints born 12:32 to 12:37: 0 discriminate, every
cut sends them to 13:04Z on 27 Nov. A straddling cohort cannot be gathered at any time; it has to be
gathered at about HH:46, so the births sit in HH:40 to HH:49. The window in the probe's title (30
minutes) is not reachable with this method.

## The cohort (`results-1246.json`, run 12:46Z)

22 mints, all dated, births 12:28:23 to 12:45:53Z on 26 Nov. 20 discriminate:

| births (26 Nov) | n | 24.25 h | 24.33 h | 24.40 h |
|---|---|---|---|---|
| 12:44:17 to 12:45:53 | 12 | 13:04Z | 14:04Z | 14:04Z |
| 12:40:38 to 12:44:04 | 8 | 13:04Z | 13:04Z | 14:04Z |
| 12:28 and 12:35 | 2 | 13:04Z | 13:04Z | 13:04Z |

Pre-registered (27 Nov): a mint that burns within 3 min after 13:04Z had a cut at or below its age at
13:04; one that survives 13:04 and burns at 14:04Z had a cut above it. The cut sits between the age of
the youngest mint burned at 13:04 and the oldest that waited. With births spread over 5 minutes, that
pins it to within about a minute if every mint is swept on time. Leg two reads after 14:14Z 27 Nov
with P-0545's `sweep.py` method (newest burn per mint).

## Not done

No burn read (cannot be known yet). No trading. No browser. `mv` of the first results file was denied
by the hook; copied instead, so `results.json` and `results-1237.json` are the same run.
