# P-0221: top-10 holder share from public Solana RPC

Question: what share of supply do the top 10 holders of ten recent Solana tokens hold, read from public RPC alone, and does it agree with the rugcheck `top10_pct` the Grinder already stores?

What I ran (25 Oct 2026, 23:35 UK): `holders.py` on the ten newest mints in tonight's `grinder/SNAPSHOTS.csv`, calling `getTokenSupply` and `getTokenLargestAccounts`.

Result: 0 of 10 answered. Measured per endpoint:

- `api.mainnet-beta.solana.com`: `getTokenSupply` returns 200; `getTokenLargestAccounts` returns 429 "Too many requests for a specific RPC call" on the very first call, from Python and from curl, even for wrapped SOL. It is throttled per method, not per client.
- `solana-rpc.publicnode.com`: 403, "Indexed requests require a personal token".

So the keyless slice does not exist: the method that answers the question is the one both public endpoints gate. Rugcheck's figure (24% to 94% on these ten, in `results.json`) stays the only top-10 number the desk has, unverified.

Verdict: blocked, on a free RPC key (Helius or similar free tier needs an account). No retry: the 429 is a policy, not a burst.
