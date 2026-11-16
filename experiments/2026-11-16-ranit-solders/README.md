# Ran it, 16 Nov 2026: solders on live pump.fun transactions

Shelf item T-0371 (from H-0640). Installed `solders` 0.29.0 with pip into
`sandbox/solders-lib` (one 22.9 MB universal wheel, no build step on this Intel Mac).

`decode.py` pulls the latest signatures on the pump.fun program from the public mainnet RPC,
keyless, fetches each transaction as base64 and decodes it with
`VersionedTransaction.from_bytes`, then names every pump.fun instruction (top level and inner)
by its 8-byte discriminator.

## Results

Pass 1 (`results.json`, 60 signatures, names hashed by hand from a list I wrote): 45 of 60
had failed on chain, 11 fetched, 11 decoded. Only 2 pump.fun instructions sat at the top level,
both with a discriminator my list did not know.

Pass 2 (`results-idl.json`, 400 signatures, names from the public IDL
`pump-fun/pump-public-docs/idl/pump.json`, inner instructions included):

- 273 of 400 (68%) had failed on chain. 40 fetches failed (public RPC rate limit), 60 fetched.
- 60 of 60 decoded by solders. 59 of 60 carried a pump.fun instruction; 104 of 132 were inner
  (called through a router or bot program), 28 top level.
- Named: buy 24, sell_v3 16, sell 11, sweep_creator_fee 5, close_user_volume_accumulator 3,
  others 1 or 2. 65 were `e445a52e51cb9a1d`, the Anchor self-CPI event wrapper, not an
  instruction. No create in this sample.

## Verdict

Works. solders decodes every transaction it was handed. The trap is the names, not the library:
my hand-written list missed `sell_v3`, now the most common sell, and the v2/v3 family. Read the
IDL, and read inner instructions, or most of the traffic is invisible.
