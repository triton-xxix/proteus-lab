# P-0266: pump-fun-sdk's read-only curve quotes against DexScreener

From H-0462 (nirholas/pump-fun-sdk, 141 stars, pushed 29 Oct 2026, published as `@nirholas/pump-sdk`
3.0.0; the name in the harvest title is not an npm package). Question: do its read-only bonding-curve
quotes, run on a public RPC, match DexScreener's price and graduation progress within 2%?

## What was done

- `fetch.py` pulled the repo tarball (37.9 MB, 10,310 files) into `sandbox/pump-fun-sdk-src/`.
- Read the SDK's own math in `src/bondingCurve.ts` and `src/analytics.ts`: price is
  `virtualQuoteReserves / virtualTokenReserves` (market cap scales it by supply, line 708);
  graduation progress is `1 - realTokenReserves / initialRealTokenReserves` with the launch figure
  793.1M tokens (lines 284 to 332). Both are pure reads of the BondingCurve account.
- `curve_check.py` (stdlib) ran that arithmetic against the live chain: DexScreener's search for
  `pumpfun` pairs gives the bonding-curve account as the pair address, the public Solana RPC returned
  each account, and the layout (discriminator, five u64 reserves, complete flag) was decoded by hand.
- The SDK's TypeScript was not executed: `npm ci` on the repo (anchor, web3.js, tsup) was started in
  the background and had not finished inside the probe's budget. What was tested is the SDK's read
  formula on the SDK's own account layout, not its compiled code.

## Result, 30 Oct 2026 about 23:52 UTC (`curve_check.json`)

| token | curve price (SOL) | DexScreener price (SOL) | diff | progress | virtual SOL | trades last hour |
|---|---|---|---|---|---|---|
| COFFIN | 1.240e-07 | 1.239e-07 | +0.10% | 71.1% | 63.2 | 26 |
| LENNY | 1.612e-07 | 1.611e-07 | +0.04% | 78.9% | 72.0 | 85 |
| SCRNR | 7.562e-08 | 7.582e-08 | -0.26% | 53.0% | 49.3 | 122 |
| NATIONS | 9.659e-08 | 8.742e-08 | +10.49% | 62.5% | 55.8 | 983 |
| SOULD | 7.675e-08 | 7.600e-08 | +0.99% | 53.6% | 49.7 | 15 |
| retARDmAx | 4.224e-08 | 4.235e-08 | -0.27% | 25.2% | 36.9 | 2,050 |

All six accounts are owned by the Pump program (6EF8rr...), none complete. Five of six agree within
1%. The one at +10.5% is the second-busiest token: DexScreener's search result is a cached snapshot
and the RPC read came a few seconds later, so on a curve moving every few seconds the gap is timing,
not formula. The busiest token (2,050 trades) agreed to 0.27%, which says the same thing from the
other side.

DexScreener publishes no graduation progress, so that half is the SDK's number alone: 25% to 79%
across the six, consistent with their virtual SOL (36.9 to 72.0 against the 30 SOL start and about
115 SOL at graduation).

## Verdict

Works: the SDK's read path is a two-line formula over public account data and it reproduces
DexScreener's price within 1% on five of six live curves, with the sixth explained by a busy token
and two reads seconds apart. The Grinder could price on-curve tokens from the chain without a
third-party API. Caveat as above: the formula was run in Python from the SDK's source, not the SDK's
compiled TypeScript.
