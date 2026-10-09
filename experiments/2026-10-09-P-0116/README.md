# P-0116: x402, does an unpaid call return a parseable 402 challenge? (9 Oct 2026)

Called shot: most listed endpoints return 402 with JSON requirements; some will be dead.

Keyless, no wallet, nothing paid. Source list: Coinbase's x402 Bazaar discovery endpoint
(`api.cdp.coinbase.com/platform/v2/x402/discovery/resources`, no key needed, 50 items returned).
One plain unpaid request to each of the first 25.

- 21 of 25 answered HTTP 402 with a JSON body that parses. 3 answered 405 (POST-only endpoints;
  my script sent GET), 1 answered 404 (api.exa.ai/search, listed but not there).
- 20 of 21 speak x402 version 2, one version 1 (cheaptokens.ai), two give no version field.
- Every one wants payment on Base (eip155:8453, one written as "base").
- Only the v1 reply carries every v1 field. The v2 replies drop `maxAmountRequired` and
  `resource` from the requirement object, which is the version change, not breakage; my field list
  was v1's. Where the Bazaar listed a price, the challenge matched it.
- Prices seen: 1,000 to 5,000 base units of USDC (0.001 to 0.005 dollars) per call on onesource.io.

Verdict: works. The handshake is real and readable without paying, and the discovery list is open.
Half the first 25 are one vendor (onesource.io), so "an ecosystem" is thinner than the count.
`probe.py`, `results.json`.
