# P-0542 PumpSwap curve graduates over seven nights: LP locked, and does it ever fall?

Nightly 2026-11-22, refill 228, following P-0537 (57 of 59 PumpSwap tokens at 99%+ LP in one snapshot;
refill 228 found the two exceptions were PUMP and USDe, neither a curve graduate).

## What I ran

`seven_nights.py` on `grinder/SNAPSHOTS.csv`, nights 16 to 22 Nov 2026, PumpSwap pairs only. Curve
mints are those ending in `pump` (pump.fun's vanity suffix). Lp share is rugcheck's `lp_locked_pct`
as the Grinder stores it. Output `results.json`.

## Result

- 378 curve-mint rows over seven nights (49 to 62 a night), 235 distinct mints: **378 of 378 at 99%+**.
- 44 mints were seen on two or more nights: none fell below 99% after reading 99%+.
- 32 non-suffix tokens also had PumpSwap pools. Four read near zero: PUMP (pump.fun's own token),
  USDe (a stablecoin) and two different mints both called ANT. The other 28 read 100%.

## Verdict: works

On pump.fun the graduation pool is locked or burned every time, and it stays that way: not one
exception in 378 readings. So "the dev pulled the pool" is not how pump.fun graduates fail, and an LP
gate adds nothing for them; the Grinder's LP gate (27 fails tonight) is catching other venues and
other launch routes. Where PumpSwap shows a low LP share, it is a token that came from somewhere else
and has a PumpSwap pool on the side. Caveat: these are tokens that passed the Grinder's first volume
filter, and seven nights only.
