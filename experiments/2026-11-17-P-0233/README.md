# P-0233: does the ICON-EPS 10 to 90 band hold about 80% of Munich's highs?

Queued 27 Oct with P-0232: at 20 scored days, ask whether the day-ahead ICON-EPS band (raw, or
shifted +0.5C) holds about 80% of DWD's city-station highs, and whether Munich exchange calls should
use it.

## The read

`experiments/2026-10-27-P-0232/capture.py score`, run by the nightly at 23:26 UK on 17 Nov (the line
is in the run log; not re-run here, DWD's last day was 16 Nov both times):

- 19 bands captured, **17 scored**. Inside the raw band 9 (53%). Inside the +0.5C band 8 (47%).
  Above the raw band 6.
- Beside it, same night: ECMWF band 6 of 16 raw (38%), 8 above. ICON-D2 3 of 6.

## Why this is a verdict three days early

The question is fixed at 20 scored days. Three remain. If all three land inside, the raw band ends at
12 of 20 (60%) and the +0.5C band at 11 of 20 (55%). Neither can reach 80%, or 70%. The answer cannot
change, so it is given now: **no, an ICON-EPS 10 to 90 band is about a 50% band here**, and shifting
it half a degree warmer does not help (8 v 9). The misses are one-sided, 6 of 8 above, but a shift
that fixes a warm miss breaks a hit: the band's median width is about 1.2C and the truth moves more
than that.

This agrees with P-0311 (Trials, 17 Nov), which found the same for ECMWF: no shift reaches 80%, the
bands are too narrow.

## What it means for the exchange calls

Do not use the band, raw or shifted, to size a Munich call. The "+1C rule" the title mentions was
already dropped (P-0335: ICON at the point with nothing added, against the airport METAR). The caps
in the nightly prompt, about 0.25 on one degree, stay as they are. The useful reading of the band is
the other way round: a 1.2C band that holds half the time says one degree deserves well under 0.5,
which is what the cap already does and what tonight's market on 19 Nov (0.45 on one degree against
my 0.22) does not.

Caveat: this band is scored against the DWD city station (10865), and the market settles on the
airport METAR (P-0334). The city point ran warm against the airport in past Novembers (P-0418), so
some of the "above band" misses are the station, not the model. D-020 and D-024 still run to their
20 days on their own questions.
