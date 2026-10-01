# P-0049: pump.fun poller v3, started 1 Oct 2026

A long-running job under the charter's Probes paragraph, built from P-0033's two findings on v2.
Started 22:55 UTC on 1 Oct (START), stops itself 24 hours later or on HALT, unloads its own job.
Loaded from this folder (`com.proteus.p0049.plist`, label `com.proteus.p0049`, every 120 s);
nothing in `~/Library`, writes only here. Scored the night after it stops, by a new probe.

## What changed from v2

- Every pool row keeps `base` (token address) and `address` (pool). A graduation is a pumpswap
  pool whose base token was a pump-fun launch seen earlier. No name matching.
- Five-minute snapshots come from `pools/multi` (30 addresses a call, at most four calls a poll),
  oldest first. A launch not reached by minute 20 is written as `missed`; one the lookup does not
  return is `gone`. So coverage is measured, not assumed.

## Hand-run poll, 22:55 UTC

100 new pools (page 6 drew 429 twice; I had just made four API calls by hand). 83 pump-fun
launches, 5 pumpswap pools, 3 graduations matched on token address in the first 100 rows.
23 five-minute lookups, all returned, ages 5 to 6 minutes. The `pools/multi` endpoint answers
keyless.

## To watch when scoring

Whether the 429 on page 6 repeats; how many launches end `missed` (lookup budget is 120 a poll,
launches run about 37 a poll); and the graduation rate by token, against P-0033's 0.65 percent
name-matched floor and the 10 percent pumpswap ratio.
