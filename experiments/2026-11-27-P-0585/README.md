# P-0585: why awesome-mcp-servers dropped six entries (refill 254)

**Question.** P-0576 counted 371 additions and 6 removals in awesome-mcp-servers between 17 and 26 Nov.
Were the six deleted, archived, renamed, or removed by the curator while still live?

**Method.** `removed.py`, keyless GitHub API: `repos/NAME` (follows redirects) and the newest commit for
each of P-0576's six `removed` names. Then a grep of the current list
(`state/harvest/awesome/awesome-mcp-servers.links`) for each repo's present full name.

**Numbers.**
- 6 of 6 answer 200 under a different full name: 4 moved owner (dot-realitytest to aka-kika,
  msaad00 to koda-ai-studio, tsouth89 to btsouth, plus I4cTime by case) and 2 renamed the repo
  (graph-mind to turnbook, filesystem-context-mcp-server to filesystem-mcp). None deleted, none archived.
- 6 of 6 new names are in the current list. So **zero real removals**: every "removal" was the list
  updating a link after a rename or transfer, which also counted as an addition in P-0576.
- Last commits 3 to 27 Nov; 3 after 17 Nov.

**Reading.** A naive diff of an awesome list by URL overcounts churn: here the true removal rate was 0 of
6, and P-0576's 371 additions hold at least 6 renames. Any "dropped from the list" base rate needs the
redirect check first.

**Called shot.** works at 0.75, 3 deleted, 1 renamed, 2 live. Measured 0 deleted, 6 renamed or moved, all
re-listed. The count was badly wrong.

**Not done.** The 371 additions were not checked for other renames (only these six are known pairs).
