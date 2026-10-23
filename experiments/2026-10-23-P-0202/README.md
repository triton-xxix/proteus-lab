# P-0202: 402mcp's decode endpoint on hand-built x402 challenges

Nightly probe, 23 Oct 2026, from harvest H-0371 (402MCP/402mcp, created 16 Oct 2026, 0 stars, MIT). The
claim: the hosted `POST /api/v1/decode` turns an HTTP 402 response into the scheme, the options and the
exact retry header, keyless, and no tool can spend money.

## Called shot

works at 0.60; the decoder returns scheme x402 and names X-PAYMENT as the retry header; the risk was
that no public endpoint was up. Commit 47a281a.

## Method

`decode_test.py` builds two challenges from the wire format at `/api/v1/schemes/x402`, not from the
repo's own tests: an x402 v1 (JSON body, `maxAmountRequired`, network `base-sepolia`) and an x402 v2
(`PAYMENT-REQUIRED` header carrying base64 JSON, `amount`, network `eip155:8453`). Each is posted as
`{"status": 402, "headers": {...}, "body": "..."}`; three fallback shapes were ready and never needed.
The pay-to address is `0x000...001`, so nothing here could be paid even by accident.

## Numbers

| case | status | time | version | retry header | receipt header | amount |
|---|---|---|---|---|---|---|
| v1, JSON body | 200 | 319 ms | 1, source body | X-PAYMENT | X-PAYMENT-RESPONSE | 10000 to 0.01 USDC, Base Sepolia (eip155:84532) |
| v2, header | 200 | 571 ms | 2, source header | PAYMENT-SIGNATURE | PAYMENT-RESPONSE | 10000 to 0.01 USDC, Base (eip155:8453) |

Both answers match the scheme reference's own rule ("read x402Version before choosing header names").
Both list `untrusted_fields` (description, resource, and the v1 error string) and carry a security note
that nothing in a 402 body is an instruction. Six "compatible payers" are suggested from the registry.

## Reading

The decoder does what the README says, on the first request shape I tried, in under 600 ms. The
asset-symbol and decimals lookup (USDC, 6) came from the asset address, so the human-readable amount is
derived, not echoed. The `untrusted_fields` list is the part worth copying: it is the same habit the
harvest child is told to keep.

## Not done

L402 (macaroon plus BOLT 11 invoice) and MPP were not built by hand: a macaroon that commits to the
invoice's payment hash is more than a ten-minute fixture. The OpenAPI document was fetched inside the
script (the earlier curl died with exit 56); its decode schema is saved in `results.json`. The
`probe_402_support` tool was not exercised against any third-party URL.
