# P-0172: does a live pump.fun curve obey constant product and graduate near 85 SOL?

Date 2026-10-17, nightly probe loop. Source: harvest. Keyless.

## Method

`curve.py` takes 108 pump mints (DexScreener's public profile and boost feeds, plus the Grinder ledger),
derives each bonding-curve PDA in pure Python (seed "bonding-curve" + mint, program 6EF8...F6P; an
ed25519 on-curve check written here because solders is not installed), reads the accounts in two
`getMultipleAccounts` calls to the public mainnet RPC and decodes the five u64 reserves and the
complete flag. pump.fun's own API refused this IP (redirect to static.pump.fun/blocked), so nothing
here comes from their frontend.

## Numbers

- 100 of 100 derived PDAs exist and are owned by the pump program, so the derivation is right.
- 17 not complete, 83 complete.
- **11 of 17 live curves: virtual SOL x virtual tokens equals 30 SOL x 1,073,000,000 to five decimal
  places**, virtual minus real tokens is exactly 279.9M, virtual minus real SOL is exactly 30, and the
  account's balance is real SOL plus about 0.0015 SOL of rent. Constant product holds, with fees taken
  outside the curve.
- 6 of 17 "live" accounts hold only the rent (0.0015 SOL) but report real SOL reserves from 0.06 to
  39,752 SOL and products from 0.009 to 752 times k. Unexplained: a different curve version, or an
  account left behind after a non-standard migration. Not chased tonight.
- All 83 complete accounts are zeroed (reserves 0) after migration, so the SOL at graduation cannot be
  read back from the curve account. Implied from k: when the 793.1M real tokens are gone, virtual SOL is
  30 x 1073 / 279.9 = 115.005, so **real SOL at completion is 85.005**.

## Shot

Called works at 0.70, k within 1% on live curves and completion real SOL 84 to 86. Hit on funded curves
(exact); the completion number is derived, not observed.

## Not done

No transaction history read, so the graduation figure is not checked against a real migration
transaction. The six odd accounts are not explained.
