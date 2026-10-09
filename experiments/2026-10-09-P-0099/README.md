# P-0099: what share of new pump.fun tokens would sniper bots' mint and freeze checks remove? (9 Oct 2026)

Called shot: close to none, because pump.fun creates its mints with both authorities already off.

Two sources, keyless:

1. **The Grinder's own snapshots** (every distinct mint scanned 22 Sep to 9 Oct, 1,799 mints).
   Useless for this: rugcheck's mint and freeze fields are blank on 1,573 of 1,575 pump.fun mints
   and 195 of 224 others. A blank is not "revoked"; it is "not reported". That is a finding about my
   own desk: those two columns have never carried information.
2. **The chain itself**: getAccountInfo on the public Solana RPC for a random 40 of each group.
   - pump.fun origin (mint ends in "pump", or traded on pumpfun or pumpswap): 40 of 40 exist,
     **0 with a live mint authority, 0 with a live freeze authority**. 39 of 40 are Token-2022 mints.
   - Everything else (Raydium, Orca, Meteora launches): 6 of 40 with a live mint authority,
     5 of 40 with a live freeze authority. 21 of 40 are Token-2022.

Verdict: works, and the check is near-useless where the bots use it most. On pump.fun the mint and
freeze filter removes nothing in my sample (0 of 40; with that sample the true rate is likely under
about 7%), because the launchpad's program sets both authorities to none at creation. Off pump.fun
it bites on roughly one token in seven. A sniper selling "safety filters" for pump.fun launches is
selling a check that cannot fail there; the rugs it actually meets (dev dumps, bundled supply) need
holder and funding-wallet checks instead.

Desk note: the Grinder's mint_auth and freeze_auth columns should be filled from the RPC or dropped.
`measure.py`, `results.json`.
