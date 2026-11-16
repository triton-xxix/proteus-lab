# P-0453: Agoreum's public MCP, how many services have a settled buyer?

Called shot: under 50 listings, at most 3 with a settled buyer. Right on both counts, and generous.

`count.py` calls the public endpoint `https://agoreum.xyz/api/v1/mcp/public` over JSON-RPC, no
account: `tools/list` (14 tools, 6 of them paid per call over x402 at 0.01 to 0.03 USDC),
`chain_status`, `search_services` sorted by evidence and paged to the end, and `search_agents`.
No paid tool was called. Results in `results.json`.

- Chain: Base mainnet (8453), USDC, not a test network.
- Services listed: **22**, priced 0.01 to 35 USDC.
- Sorted by evidence, the top listing has `distinct_settled_buyers_90d` 0 and `settled_usdc_90d`
  0, so every listing has none. (The script's own counter looked for the wrong key name and also
  says 0; the sort order is what settles it.)
- Agents: **9**, every one unverified, **0 completed orders** across all of them. Two slugs
  (`i991canary5f42bc`, `i929-probe-1c7`) read like test or canary accounts.

Verdict: works. The read-only endpoint does what it says and is well built (schemas, provenance
fields, injection warnings on provider text). The marketplace itself has 22 listings and nobody
has bought anything through its escrow in 90 days.
