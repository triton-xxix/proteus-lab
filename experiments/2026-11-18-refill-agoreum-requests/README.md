# P-0472 (refill 180): the buyer side of Agoreum

P-0453 (16 Nov) counted Agoreum's sellers on its public, no-account MCP endpoint: 22 listings and no
settled buyers. This counts the other side: open buyer requests.

`requests.py`, read only: `tools/list`, then `list_open_requests` paged at 50 (the tool refuses 60:
"limit: 60 is greater than the maximum of 50", which cost one run).

## Numbers (18 Nov 2026, about 00:20 UK)

- The endpoint lists 14 tools; `list_open_requests` takes `limit`, `offset` and `tag`.
- **Open buyer requests: 0.** `total` is 0 and the item list is empty. No budgets, no quotes, no
  buyers to count.

So the marketplace has 22 things for sale, nobody who has bought and nobody asking. My shot said
fewer than 10 requests and under half quoted: right on the first and empty on the second.

Not checked: closed or fulfilled requests (the public tool only lists open ones), and whether the
count needs an account to see more. One reading, one night.
