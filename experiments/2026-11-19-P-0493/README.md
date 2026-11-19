# P-0493: do the most-starred MCP server repos ship releases?

Question: of the 50 most-starred GitHub repos tagged `mcp-server` and pushed since 1 Nov 2026, how
many shipped a release in the last 30 days, how many have never cut one, and how old is the latest?

## Method

Keyless, standard library, read only. Run 19 Nov 2026 at 12:46 UK.

- `releases.py`: one search call (`topic:mcp-server pushed:>2026-11-01`, sorted by stars, 50 a
  page), then `releases/latest` for each repo. A 404 is "no published release". It reads the
  unauthenticated quota first (59 of 60 an hour were left) and would have stopped at it.

## Numbers

- The search matches 17,457 repos. The top 50 run from 8,758 to 211,379 stars.
- **50 of 50 answered. 37 shipped a release in the last 30 days (74%), 24 of them in the last 7.**
- 8 have a release older than 30 days (30.8 to 409 days; `mrexodia/ida-pro-mcp` last cut one in
  October 2025 and was pushed a week ago). **5 have no release at all**: TrendRadar,
  mcp-for-beginners, Trail-Code, openstatus, dashboard-icons.
- **Median 6.3 days since the latest release** among the 45 that have one. 11 released in the last
  12 hours.
- The two official SDKs are among the slower ones: python-sdk 47.6 days, typescript-sdk 26.8.

## What it says

At the top of the list, this is software that ships weekly. But the topic is a loose tag: n8n,
gemini-cli, Scrapling, reactive-resume and nginx-ui are products that added an MCP server, not MCP
servers. By my read of the names, well under half of the 50 are servers first. So "74% shipped this
month" describes popular projects that carry the tag, and the tag is doing little work.

## What I did not do

- The README tools count against the code, from the source row, is not attempted.
- I did not classify the 50 into "MCP server" and "product with an MCP feature" by any rule; the
  remark above is from reading names.
- `releases/latest` skips pre-releases and drafts, and a repo that ships by tag or to a package
  registry without a GitHub release reads as "no release".
- Top 50 of 17,457: the long tail will look nothing like this.
- The run used 51 of the hour's 60 unauthenticated calls, so nothing else in this folder can use the
  GitHub API keyless until about 13:45.

Shot (works, 0.65): 28 with a release in 30 days, 15 with none, median 12 days. Measured 37, 5 and
6.3: they ship more than I thought on every count.
