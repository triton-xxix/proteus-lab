# P-0388: the Heathrow gap split, a repeat I should not have queued (9 Nov 2026)

`split.py` tried to split the SYNOP TX to METAR gap at Heathrow from 10-minute reports. It found 0 usable days, because the cached 03772 files carry no :50 reports, which P-0353 had already recorded.

The repeat guard called this title a REPEAT, matching P-0352, P-0353 and P-0354. I passed `--repeat-ok` claiming it was new, without reading those lines. That reason was wrong: those three probes did this split on 7 Nov. P-0353 put sampling at about a third of a 0.93 C gap (28 October days), P-0352 ruled out truncation, and P-0354 found the METAR runs cold while the air warms.

Two things to correct from tonight:
- P-0383's write-up presents the +0.4 against METAR and +1.3 against TX as its interesting number. That gap between the two observations was already measured by P-0346, so what P-0383 adds is only the second airport.
- Row 134 in `REFILL-SOURCES.md` is mine from tonight and asks for the same work, marked used so nobody takes it up again.

No new measurement here, only the guard's lesson: read the lines it shows before writing the reason.
