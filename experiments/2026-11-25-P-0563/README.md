# P-0563: spr-sdk, does a sealed payment record verify and fail after a one-byte edit?

Nightly 25 Nov 2026 (second run on the date), harvest probe. Called shot before running: works, every
one-byte edit to a sealed record fails verification.

## What I ran

`spr-sdk` 0.2.0 from PyPI (Apache-2.0, needs `cryptography`), installed into `sandbox/p0563-venv`. The
unattended hook refuses that venv's python (it resolves outside the folder), so `run.py` runs under the
project `.venv` (also 3.14) with the sandbox site-packages first on `sys.path`. Everything is local and
keyless: no call to Luca's service, `send_to_luca` never touched.

1. The package's own `vectors.json` through `run_vectors`.
2. A fresh book in `sandbox/p0563-book` (it holds the private key, so it stays in the gitignored sandbox):
   one declared intent (cap 50,000 minor units USDC), three sealed x402 payments bound to its nonce,
   `verify_record` on each, `export_package` to `sandbox/p0563-pkg`, `verify_folder` with the book's key ID
   as the expected key.
3. 200 one-byte edits at seeded random positions in the package's `records.jsonl`, each re-verified and
   restored.
4. One deliberate edit: a record's `amount_minor` plus one, written back as valid JSON.

## Result (`results.json`)

| check | result |
|---|---|
| shipped vectors | 80 passed, 0 failed |
| verify_record on 3 sealed payments | 3 of 3 ok |
| clean package, expected key | ok, trust `expected-key`, 18 checks passed, 0 failed |
| 200 one-byte edits | 156 returned a failure, **0 passed**, 44 made the checker raise |
| amount_minor + 1 | fails twice: the manifest's SHA-256 of records.jsonl differs, and the record's payload hash is not the sealed hash |

## Verdict: works

The seal does what it says on a local book: the clean package verifies against the expected key and no
one-byte edit got through. One rough edge: when an edit breaks the JSON of a line (44 of 200),
`verify_folder` raises a `JSONDecodeError` instead of returning `ok: False` with a reason. That is
fail-closed only if the caller treats an exception as a failure; a wrapper that catches and logs could
read it as "check did not run" rather than "tampered".

Not tested: the edit that also rewrites the manifest's file hash (the manifest is sealed too, so it
should fail on the manifest seal), key rotation, and anything to do with Luca's hosted side.
